using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;
using UnityEngine;
using PixelCrushers.DialogueSystem;

namespace BlakeManor.Patch
{
    /// <summary>
    /// The conversation layer — the one that uses the Dialogue System's own
    /// localisation path rather than a hook.
    ///
    ///     DialogueEntry.GetCurrentDialogueTextField()
    ///         -> Field.AssignedField(fields, Localization.language)
    ///            ?? Field.Lookup(fields, "Dialogue Text")
    ///
    /// So: add a field named after the language's code ("fr") to each entry, set
    /// Localization.language to that code, and the game reads the translation with
    /// English as an automatic fallback for anything not yet translated. Menu text
    /// uses the "Menu Text fr" convention (Field.LocalizedTitle), and speaker labels
    /// use "AltName fr" — see below. Every shipped language gets its fields; only
    /// Localization.language decides which one shows.
    ///
    /// Each line carries a hash of the English it was translated from. If a game
    /// patch edits that line, the hash stops matching and the line is left in
    /// English and reported, instead of silently showing a translation of text the
    /// player is no longer being shown.
    ///
    /// Switching language at runtime is cheap here: the fields stay where they are
    /// and only Localization.language moves — a code for a shipped language, empty
    /// for the game's default English (see SetLanguage).
    /// </summary>
    internal static class DialogueLines
    {
        internal class Line
        {
            public string t { get; set; }   // Dialogue Text
            public string m { get; set; }   // Menu Text, when the entry has one
            public string h { get; set; }   // hash of the English source
        }

        internal class Layer
        {
            public Dictionary<string, Line> entries { get; set; }
            public Dictionary<string, string> actors { get; set; }
        }

        private static DialogueEntry _sentinel;   // one entry we translated, to detect a database reset
        private static Language _sentinelLang;    // the language whose field the sentinel is checked under
        private static bool _warnedLanguage, _warnedEnglish, _warnedWiped;
        private static string _lastLang;

        /// <summary>Set once Apply has finished (or found nothing to do).</summary>
        internal static bool Done;

        public static int Load(Language lang, string path)
        {
            if (!File.Exists(path)) return 0;
            try
            {
                lang.Lines = JsonConvert.DeserializeObject<Layer>(File.ReadAllText(path, Encoding.UTF8));
                return lang.Lines?.entries?.Count ?? 0;
            }
            catch (Exception e)
            {
                LanguagePatch.Log.LogError($"Could not read {path}: {e.Message}");
                return 0;
            }
        }

        private static bool HasLines(Language lang) => lang.Lines?.entries != null && lang.Lines.entries.Count > 0;

        public static IEnumerator Apply()
        {
            if (!LanguagePatch.Languages.Exists(HasLines))
            {
                Done = true;
                yield break;
            }

            float deadline = Time.realtimeSinceStartup + 120f;
            DialogueDatabase db = null;
            while (Time.realtimeSinceStartup < deadline)
            {
                try { db = DialogueManager.instance != null ? DialogueManager.masterDatabase : null; }
                catch { db = null; }
                if (db != null) break;
                yield return new WaitForSecondsRealtime(0.25f);
            }
            if (db == null)
            {
                LanguagePatch.Log.LogWarning("Dialogue database never appeared; conversations not translated.");
                Done = true;
                yield break;
            }

            foreach (var lang in LanguagePatch.Languages)
            {
                if (!HasLines(lang)) continue;
                ApplyLanguage(db, lang);
            }

            if (LanguagePatch.Translating)
            {
                Localization.language = LanguagePatch.Active.Code;
                PinControllerLanguage(LanguagePatch.Active.Code);
            }

            // Prove the game's own lookup now resolves as wanted, rather than trusting
            // that the field was written. subtitleText is what the subtitle panel
            // actually reads.
            if (_sentinel != null)
            {
                var en = Field.LookupValue(_sentinel.fields, "Dialogue Text");
                LanguagePatch.Log.LogInfo(
                    $"Self-test [{_sentinelLang.Code}] EN {Trim(en)} -> resolved {Trim(_sentinel.subtitleText)}");
            }

            Done = true;
            LanguagePatch.Instance.StartCoroutine(Watchdog());
        }

        private static void ApplyLanguage(DialogueDatabase db, Language lang)
        {
            var layer = lang.Lines;
            int applied = 0, drifted = 0, missing = 0;
            var seen = new HashSet<string>(StringComparer.Ordinal);

            foreach (var conv in db.conversations)
            {
                foreach (var entry in conv.dialogueEntries)
                {
                    var key = conv.id + ":" + entry.id;
                    if (!layer.entries.TryGetValue(key, out var line)) continue;
                    seen.Add(key);

                    var english = Field.LookupValue(entry.fields, "Dialogue Text");
                    if (!string.IsNullOrEmpty(line.h) && Hash(english) != line.h)
                    {
                        // the developers changed this line since it was translated
                        drifted++;
                        continue;
                    }

                    if (!string.IsNullOrEmpty(line.t))
                    {
                        SetField(entry.fields, lang.Code, line.t);
                        SetField(entry.fields, lang.Name, line.t);
                        if (_sentinel == null)
                        {
                            _sentinel = entry;
                            _sentinelLang = lang;
                        }
                        applied++;
                    }
                    if (!string.IsNullOrEmpty(line.m))
                    {
                        SetField(entry.fields, "Menu Text " + lang.Code, line.m);
                        SetField(entry.fields, "Menu Text " + lang.Name, line.m);
                    }
                }
            }

            foreach (var key in layer.entries.Keys)
                if (!seen.Contains(key)) missing++;

            // Speaker labels. EHUnityDialogueUI.ShowSubtitle reads
            //     actor.LookupLocalizedValue("AltName")
            // which resolves to the field "AltName <code>" once the language is set —
            // NOT "Display Name", and not the Lua table.
            //
            // Careful: that same method branches on speakerInfo.Name.Contains("Ward")
            // to choose the player subtitle panel over the NPC one, so Ward's
            // translated name has to keep the substring "Ward". "M. Ward" does.
            int actors = 0;
            if (layer.actors != null)
            {
                foreach (var actor in db.actors)
                {
                    var name = Field.LookupValue(actor.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!layer.actors.TryGetValue(name, out var alt)) continue;
                    if (string.IsNullOrEmpty(alt)) continue;
                    SetField(actor.fields, "AltName " + lang.Code, alt);
                    SetField(actor.fields, "AltName " + lang.Name, alt);
                    actors++;
                }
            }

            LanguagePatch.Log.LogInfo(
                $"Conversations [{lang.Code}]: {applied} lines translated, {actors} actor names"
                + (drifted > 0 ? $", {drifted} SKIPPED (English changed since translation)" : "")
                + (missing > 0 ? $", {missing} keys not found in the database" : ""));
            if (drifted > 0)
                LanguagePatch.Log.LogWarning(
                    $"[{lang.Code}] {drifted} lines were left in English because the game's text no longer "
                    + "matches what was translated. Re-run the dumper and re-translate those lines.");
        }

        /// <summary>
        /// Move the Dialogue System to a language or back to its default. Goes through
        /// DialogueManager.SetLanguage so the controller's own setting moves with it,
        /// which is also what the Adventure Creator bridge calls.
        /// </summary>
        internal static void SetLanguage(Language lang)
        {
            var target = lang.IsEnglish ? string.Empty : lang.Code;
            try
            {
                if (DialogueManager.instance != null) DialogueManager.SetLanguage(target);
                else Localization.language = target;
                PinControllerLanguage(target);
                _lastLang = null;   // so the watchdog reports what the next lookup resolves to
            }
            catch (Exception e)
            {
                LanguagePatch.Log.LogWarning("Could not set the Dialogue System language: " + e.Message);
            }
        }

        /// <summary>For the log: the current language and what the sentinel line resolves to.</summary>
        internal static string Describe()
        {
            string s;
            try { s = _sentinel != null ? Trim(_sentinel.subtitleText) : "(no sentinel)"; }
            catch (Exception e) { s = "(lookup failed: " + e.Message + ")"; }
            return "DS language " + Trim(Localization.language) + ", sentinel -> " + s;
        }

        /// <summary>
        /// The one-shot assignment in Apply() is not enough: DialogueSystemController
        /// re-applies its own localisation settings when it initialises or a scene
        /// loads, which puts Localization.language back to the default and drops every
        /// conversation to the English fallback. Pinning the controller's own setting
        /// makes the wanted language what it restores TO, rather than something it
        /// overwrites.
        /// </summary>
        private static void PinControllerLanguage(string lang)
        {
            try
            {
                var c = DialogueManager.instance;
                if (c == null) return;
                var ls = c.displaySettings?.localizationSettings;
                if (ls == null) return;
                ls.useSystemLanguage = false;
                ls.language = lang;
                LanguagePatch.Log.LogInfo("Pinned DialogueSystemController localisation language to \"" + lang + "\".");
            }
            catch (Exception e)
            {
                LanguagePatch.Log.LogWarning("Could not pin controller language: " + e.Message);
            }
        }

        /// <summary>A language we publish fields under, by code or by name.</summary>
        private static bool IsOurs(string lang)
            => !string.IsNullOrEmpty(lang) && LanguagePatch.Languages.Exists(l => l.Matches(lang));

        /// <summary>
        /// Diagnose and repair the ways conversations can silently end up in the wrong
        /// language after startup: the language being reset by something else, or the
        /// database being reloaded (which discards the runtime fields entirely).
        /// Each cause is reported once, so the log says which actually happened.
        /// </summary>
        private static IEnumerator Watchdog()
        {
            var wait = new WaitForSecondsRealtime(2f);
            while (true)
            {
                // Cheap, every tick: is the language the one the player chose?
                var lang = Localization.language;
                var want = LanguagePatch.Active;

                if (!want.IsEnglish && !want.Matches(lang))
                {
                    // Neither name we publish this language's fields under - restore the code.
                    if (!_warnedLanguage)
                    {
                        _warnedLanguage = true;
                        LanguagePatch.Log.LogWarning(
                            "Localization.language became \"" + lang + "\" while " + want.Name
                            + " is selected; restoring \"" + want.Code + "\".");
                    }
                    Localization.language = want.Code;
                    PinControllerLanguage(want.Code);
                }
                else if (want.IsEnglish && IsOurs(lang))
                {
                    if (!_warnedEnglish)
                    {
                        _warnedEnglish = true;
                        LanguagePatch.Log.LogWarning(
                            "Localization.language became \"" + lang + "\" while English is selected; "
                            + "restoring the default.");
                    }
                    SetLanguage(Language.English);
                }
                else if (!string.Equals(lang, _lastLang, StringComparison.Ordinal))
                {
                    // The bridge switched which name it uses. Prove the lookup still
                    // resolves as wanted under the new one rather than assuming it.
                    _lastLang = lang;
                    if (_sentinel != null)
                        LanguagePatch.Log.LogInfo(
                            "Localization.language is now \"" + lang + "\"; sentinel resolves to "
                            + Trim(_sentinel.subtitleText));
                }

                // Has the database been reloaded, discarding our fields?
                if (_sentinel != null && string.IsNullOrEmpty(Field.LookupValue(_sentinel.fields, _sentinelLang.Code)))
                {
                    if (!_warnedWiped)
                    {
                        _warnedWiped = true;
                        LanguagePatch.Log.LogWarning(
                            "CAUSE FOUND: the dialogue database was reloaded and the runtime \"" + _sentinelLang.Code
                            + "\" fields were discarded — re-applying all conversation lines.");
                    }
                    _sentinel = null;
                    _sentinelLang = null;
                    LanguagePatch.Instance.StartCoroutine(Apply());
                    yield break;   // Apply() restarts this watchdog
                }

                yield return wait;
            }
        }

        private static string Trim(string s)
        {
            if (string.IsNullOrEmpty(s)) return "(empty)";
            s = s.Replace("\n", " ");
            return "\"" + (s.Length > 70 ? s.Substring(0, 70) + "…" : s) + "\"";
        }

        private static void SetField(List<Field> fields, string title, string value)
        {
            var f = Field.Lookup(fields, title);
            if (f != null) f.value = value;
            else fields.Add(new Field(title, value, FieldType.Text));
        }

        private static string Hash(string s)
        {
            if (string.IsNullOrEmpty(s)) return "";
            using (var sha = SHA1.Create())
            {
                var b = sha.ComputeHash(Encoding.UTF8.GetBytes(s));
                var sb = new StringBuilder(16);
                for (int i = 0; i < 8; i++) sb.Append(b[i].ToString("x2"));
                return sb.ToString();
            }
        }
    }
}
