using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;
using UnityEngine;
using PixelCrushers.DialogueSystem;

namespace BlakeManor.FR
{
    /// <summary>
    /// The conversation layer — the one that uses the Dialogue System's own
    /// localisation path rather than a hook.
    ///
    ///     DialogueEntry.GetCurrentDialogueTextField()
    ///         -> Field.AssignedField(fields, Localization.language)
    ///            ?? Field.Lookup(fields, "Dialogue Text")
    ///
    /// So: add a field literally named "fr" to each entry, set Localization.language
    /// to "fr", and the game reads French with English as an automatic fallback for
    /// anything not yet translated. Menu text uses the "Menu Text fr" convention
    /// (Field.LocalizedTitle), and speaker labels use "AltName fr" — see below.
    ///
    /// Each line carries a hash of the English it was translated from. If a game
    /// patch edits that line, the hash stops matching and the line is left in
    /// English and reported, instead of silently showing a translation of text the
    /// player is no longer being shown.
    /// </summary>
    internal static class DialogueLines
    {
        private const string Lang = "fr";

        private class Line
        {
            public string t { get; set; }   // Dialogue Text
            public string m { get; set; }   // Menu Text, when the entry has one
            public string h { get; set; }   // hash of the English source
        }

        private class Layer
        {
            public Dictionary<string, Line> entries { get; set; }
            public Dictionary<string, string> actors { get; set; }
        }

        private static Layer _layer;

        public static int Load(string path)
        {
            if (!File.Exists(path)) return 0;
            try
            {
                _layer = JsonConvert.DeserializeObject<Layer>(File.ReadAllText(path, Encoding.UTF8));
                return _layer?.entries?.Count ?? 0;
            }
            catch (Exception e)
            {
                FrenchPatch.Log.LogError($"Could not read {path}: {e.Message}");
                return 0;
            }
        }

        public static IEnumerator Apply()
        {
            if (_layer?.entries == null || _layer.entries.Count == 0) yield break;

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
                FrenchPatch.Log.LogWarning("Dialogue database never appeared; conversations not translated.");
                yield break;
            }

            int applied = 0, drifted = 0, missing = 0;
            var seen = new HashSet<string>(StringComparer.Ordinal);

            foreach (var conv in db.conversations)
            {
                foreach (var entry in conv.dialogueEntries)
                {
                    var key = conv.id + ":" + entry.id;
                    if (!_layer.entries.TryGetValue(key, out var line)) continue;
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
                        SetField(entry.fields, Lang, line.t);
                        applied++;
                    }
                    if (!string.IsNullOrEmpty(line.m))
                        SetField(entry.fields, "Menu Text " + Lang, line.m);
                }
            }

            foreach (var key in _layer.entries.Keys)
                if (!seen.Contains(key)) missing++;

            // Speaker labels. EHUnityDialogueUI.ShowSubtitle reads
            //     actor.LookupLocalizedValue("AltName")
            // which resolves to the field "AltName fr" once the language is set —
            // NOT "Display Name", and not the Lua table.
            //
            // Careful: that same method branches on speakerInfo.Name.Contains("Ward")
            // to choose the player subtitle panel over the NPC one, so Ward's French
            // name has to keep the substring "Ward". "M. Ward" does.
            int actors = 0;
            if (_layer.actors != null)
            {
                foreach (var actor in db.actors)
                {
                    var name = Field.LookupValue(actor.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!_layer.actors.TryGetValue(name, out var fr)) continue;
                    if (string.IsNullOrEmpty(fr)) continue;
                    SetField(actor.fields, "AltName " + Lang, fr);
                    actors++;
                }
            }

            Localization.language = Lang;

            // Prove the game's own lookup now resolves to French, rather than
            // trusting that the field was written. subtitleText is what the
            // subtitle panel actually reads.
            foreach (var conv in db.conversations)
            {
                bool done = false;
                foreach (var entry in conv.dialogueEntries)
                {
                    if (!_layer.entries.ContainsKey(conv.id + ":" + entry.id)) continue;
                    if (string.IsNullOrEmpty(Field.LookupValue(entry.fields, Lang))) continue;
                    var resolved = entry.subtitleText;
                    var en = Field.LookupValue(entry.fields, "Dialogue Text");
                    FrenchPatch.Log.LogInfo(
                        $"Self-test [{conv.id}:{entry.id}] EN {Trim(en)} -> resolved {Trim(resolved)}");
                    done = true;
                    break;
                }
                if (done) break;
            }

            FrenchPatch.Log.LogInfo(
                $"Conversations: {applied} lines translated, {actors} actor names"
                + (drifted > 0 ? $", {drifted} SKIPPED (English changed since translation)" : "")
                + (missing > 0 ? $", {missing} keys not found in the database" : ""));
            if (drifted > 0)
                FrenchPatch.Log.LogWarning(
                    $"{drifted} lines were left in English because the game's text no longer "
                    + "matches what was translated. Re-run the dumper and re-translate those lines.");
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
