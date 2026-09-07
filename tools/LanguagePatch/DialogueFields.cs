using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using Newtonsoft.Json;
using UnityEngine;
using PixelCrushers.DialogueSystem;

namespace BlakeManor.Patch
{
    /// <summary>
    /// The Dialogue System layer.
    ///
    /// Hypothesis templates, verb banks and the journal/mystery text live on DS *item*
    /// fields and are read by literal field name (DSQuest.LookupField), so they never
    /// pass through Adventure Creator's GetTranslation hook. They are injected by
    /// overwriting the field value in the live database instead.
    ///
    /// Items are matched on their technical Name, never on the displayed title —
    /// the title is itself translated, and several quests share one.
    ///
    /// Identity fields (Name, Technical Name, Articy Id, *IDs) are never touched:
    /// they are lookup keys, and EHDialogueUtilities.FindActorByArticyId resolves
    /// actors by comparing them.
    ///
    /// Because the overwrite is destructive, every field's English is remembered the
    /// first time it is seen, and every shipped language's value for it is kept
    /// alongside; that is what lets SetLanguage move between them when the player
    /// switches in the options screen.
    /// </summary>
    internal static class DialogueFields
    {
        internal class Layer
        {
            public Dictionary<string, Dictionary<string, string>> items { get; set; }
            public Dictionary<string, Dictionary<string, string>> actors { get; set; }
        }

        /// <summary>Field titles that must never be overwritten — they are keys, not text.</summary>
        private static readonly HashSet<string> Protected = new HashSet<string>(StringComparer.Ordinal)
        {
            "Name", "Technical Name", "Articy Id", "Is Item", "IsQuest", "State",
            "evidenceIDs", "essentialEvidenceIDs", "variablesPrefixOverride",
            "LinkedActor", "QuestType", "IsNPCQuest", "IsTopLevelMystery",
        };

        /// <summary>One overwritten field: the object, what the game shipped, and what
        /// each language puts there.</summary>
        private class Swap
        {
            public Field field;
            public string en;
            public readonly Dictionary<Language, string> values = new Dictionary<Language, string>();
            public string item, key;
            public bool lua;   // quest fields are mirrored into the Lua environment too
        }

        private static readonly List<Swap> _swaps = new List<Swap>();
        private static readonly Dictionary<Field, Swap> _byField = new Dictionary<Field, Swap>(new RefEq());

        // The English as first seen, per field object, so a second Apply (after a
        // database reload) does not mistake our own translation for the original.
        private static readonly Dictionary<Field, string> _original = new Dictionary<Field, string>(new RefEq());

        private class RefEq : IEqualityComparer<Field>
        {
            public bool Equals(Field a, Field b) => ReferenceEquals(a, b);
            public int GetHashCode(Field f) => RuntimeHelpers.GetHashCode(f);
        }

        /// <summary>Set once Apply has finished (or found nothing to do).</summary>
        internal static bool Done;

        public static int Load(Language lang, string path)
        {
            if (!File.Exists(path)) return 0;
            try
            {
                var doc = JsonConvert.DeserializeObject<Layer>(File.ReadAllText(path, Encoding.UTF8));
                lang.Fields = doc;
                int n = 0;
                if (doc?.items != null) foreach (var kv in doc.items) n += kv.Value.Count;
                if (doc?.actors != null) foreach (var kv in doc.actors) n += kv.Value.Count;
                return n;
            }
            catch (Exception e)
            {
                LanguagePatch.Log.LogError($"Could not read {path}: {e.Message}");
                return 0;
            }
        }

        private static bool HasFields(Language lang)
            => (lang.Fields?.items != null && lang.Fields.items.Count > 0)
            || (lang.Fields?.actors != null && lang.Fields.actors.Count > 0);

        public static IEnumerator Apply()
        {
            if (!LanguagePatch.Languages.Exists(HasFields))
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
                LanguagePatch.Log.LogWarning("Dialogue database never appeared; item fields not translated.");
                Done = true;
                yield break;
            }

            // The hypothesis screen does NOT read DialogueManager.masterDatabase.
            // EHKickStarter.SetupQuests iterates KickStarter.settingsManager.masterDatabase
            // and wraps those Item objects in DSQuest, so the panel reads whatever is in
            // Adventure Creator's copy. Writing only the Dialogue System's database left
            // every template English while reporting complete success.
            var databases = new List<DialogueDatabase> { db };
            try
            {
                var acDb = AC.KickStarter.settingsManager != null
                    ? AC.KickStarter.settingsManager.masterDatabase : null;
                if (acDb != null && !ReferenceEquals(acDb, db))
                {
                    databases.Add(acDb);
                    LanguagePatch.Log.LogInfo(
                        "Adventure Creator uses a separate master database; translating that too.");
                }
            }
            catch (Exception e)
            {
                LanguagePatch.Log.LogWarning("Could not reach AC's master database: " + e.Message);
            }

            _swaps.Clear();
            _byField.Clear();
            foreach (var lang in LanguagePatch.Languages)
            {
                if (!HasFields(lang)) continue;
                ApplyLanguage(databases, db, lang);
            }

            // The database is not necessarily what the screen reads. The Dialogue
            // System mirrors quest/item fields into its Lua environment at startup,
            // and code that calls DialogueLua.GetQuestField sees that copy, not
            // db.items. Read both back for one hypothesis template and log them, so
            // the log says which path the hypothesis screen is actually using
            // instead of us assuming the write was enough.
            var probe = FirstTemplate(db);
            if (probe != null)
            {
                var nm = Field.LookupValue(probe.fields, "Name");
                string inLua;
                try { inLua = DialogueLua.GetQuestField(nm, "hypothesisSentence").asString; }
                catch (Exception e) { inLua = "(lookup failed: " + e.Message + ")"; }

                LanguagePatch.Log.LogInfo($"Hypothesis probe [{nm}]");
                LanguagePatch.Log.LogInfo($"   db.items  -> {Cut(Field.LookupValue(probe.fields, "hypothesisSentence"))}");
                LanguagePatch.Log.LogInfo($"   Lua quest -> {Cut(inLua)}");
                LanguagePatch.Log.LogInfo($"   AC db (what the panel reads) -> {ProbeHypothesis()}");
            }
            Done = true;
        }

        private static void ApplyLanguage(List<DialogueDatabase> databases, DialogueDatabase db, Language lang)
        {
            var layer = lang.Fields;
            bool active = ReferenceEquals(lang, LanguagePatch.Active);
            int applied = 0, missingItems = 0, missingFields = 0, skipped = 0, luaErrors = 0, placeholders = 0;

            if (layer.items != null)
            {
              foreach (var database in databases)
                foreach (var item in database.items)
                {
                    var name = Field.LookupValue(item.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!layer.items.TryGetValue(name, out var fields)) continue;

                    foreach (var kv in fields)
                    {
                        if (Protected.Contains(kv.Key)) { skipped++; continue; }
                        var f = Field.Lookup(item.fields, kv.Key);
                        if (f == null) { missingFields++; continue; }

                        SwapFor(f, name, kv.Key, lua: true).values[lang] = kv.Value;
                        if (active)
                        {
                            f.value = kv.Value;

                            // The database is only half of it. The Dialogue System mirrors
                            // item/quest fields into its Lua environment at startup, and the
                            // hypothesis screen reads that copy — proven by the probe in
                            // Apply, which found the translation in db.items and English in
                            // Lua. Writing only the database left every template in English.
                            try { DialogueLua.SetQuestField(name, kv.Key, kv.Value); }
                            catch (Exception e)
                            {
                                if (luaErrors++ == 0)
                                    LanguagePatch.Log.LogWarning(
                                        $"Could not write Lua quest field '{kv.Key}' on '{name}': {e.Message}");
                            }
                        }

                        // Also publish the localised variants the game's own loader
                        // would create. The shipped build carries an unfinished French
                        // ("TBT: ...") under exactly these names; ours must win.
                        placeholders += SetVariant(item.fields, kv.Key + " " + lang.Code, kv.Value);
                        SetVariant(item.fields, kv.Key + " " + lang.Name, kv.Value);
                        applied++;
                    }
                }
            }

            // Actor cast/lore fields. These are read two different ways depending on
            // the screen — LookupValue for the lore panel, LookupLocalizedValue for
            // the dialogue UI — so write both the base field and its localised variant.
            if (layer.actors != null)
            {
                foreach (var actor in db.actors)
                {
                    var name = Field.LookupValue(actor.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!layer.actors.TryGetValue(name, out var fields)) continue;

                    foreach (var kv in fields)
                    {
                        if (Protected.Contains(kv.Key)) { skipped++; continue; }
                        var f = Field.Lookup(actor.fields, kv.Key);
                        if (f == null) { missingFields++; continue; }

                        SwapFor(f, name, kv.Key, lua: false).values[lang] = kv.Value;
                        if (active) f.value = kv.Value;
                        placeholders += SetVariant(actor.fields, kv.Key + " " + lang.Code, kv.Value);
                        SetVariant(actor.fields, kv.Key + " " + lang.Name, kv.Value);
                        applied++;
                    }
                }
            }

            // report anything the database did not have, so a game patch that renames
            // an item shows up as a warning rather than as silently English text
            if (layer.items != null)
            {
                var present = new HashSet<string>(StringComparer.Ordinal);
                foreach (var item in db.items)
                {
                    var n = Field.LookupValue(item.fields, "Name");
                    if (!string.IsNullOrEmpty(n)) present.Add(n);
                }
                foreach (var kv in layer.items)
                    if (!present.Contains(kv.Key)) missingItems++;
            }

            LanguagePatch.Log.LogInfo(
                $"Dialogue System fields [{lang.Code}]: {applied} " + (active ? "translated" : "prepared (not the active language)")
                + (missingItems > 0 ? $", {missingItems} items not found" : "")
                + (missingFields > 0 ? $", {missingFields} fields not found" : "")
                + (skipped > 0 ? $", {skipped} protected fields skipped" : "")
                + (luaErrors > 0 ? $", {luaErrors} Lua writes failed" : "")
                + (placeholders > 0
                    ? $", {placeholders} placeholder fields from the game's own unfinished localisation overwritten"
                    : ""));
        }

        private static Swap SwapFor(Field f, string item, string key, bool lua)
        {
            if (_byField.TryGetValue(f, out var s)) return s;
            s = new Swap { field = f, en = Original(f), item = item, key = key, lua = lua };
            _byField[f] = s;
            _swaps.Add(s);
            return s;
        }

        /// <summary>
        /// Put every overwritten field to the given language's value, or back to
        /// English — also for a language that has no value for a field. The Lua mirror
        /// follows for quest fields, once per field rather than once per database copy.
        /// </summary>
        internal static int SetLanguage(Language lang)
        {
            int n = 0, luaErrors = 0;
            var luaDone = new HashSet<string>(StringComparer.Ordinal);
            foreach (var s in _swaps)
            {
                if (s.field == null) continue;
                if (lang.IsEnglish || !s.values.TryGetValue(lang, out var v)) v = s.en;
                s.field.value = v;
                n++;
                if (!s.lua || !luaDone.Add(s.item + "|" + s.key)) continue;
                try { DialogueLua.SetQuestField(s.item, s.key, v); }
                catch (Exception e)
                {
                    if (luaErrors++ == 0)
                        LanguagePatch.Log.LogWarning($"Could not write Lua quest field '{s.key}' on '{s.item}': {e.Message}");
                }
            }
            if (luaErrors > 0) LanguagePatch.Log.LogWarning($"{luaErrors} Lua quest fields could not be rewritten.");
            return n;
        }

        /// <summary>What the hypothesis panel reads for the first template — exactly
        /// DSQuest.HypothesisSentence: a localised lookup on Adventure Creator's copy.</summary>
        internal static string ProbeHypothesis()
        {
            try
            {
                DialogueDatabase acDb = null;
                try { acDb = AC.KickStarter.settingsManager != null ? AC.KickStarter.settingsManager.masterDatabase : null; }
                catch { }
                var item = FirstTemplate(acDb) ?? FirstTemplate(DialogueManager.masterDatabase);
                if (item == null) return "(no template found)";
                return Cut(Field.LookupLocalizedValue(item.fields, "hypothesisSentence"));
            }
            catch (Exception e)
            {
                return "(lookup failed: " + e.Message + ")";
            }
        }

        /// <summary>The first item any shipped language gives a hypothesis sentence for,
        /// preferring the active language's set.</summary>
        private static Item FirstTemplate(DialogueDatabase db)
        {
            if (db == null) return null;
            var order = new List<Language>();
            if (LanguagePatch.Translating) order.Add(LanguagePatch.Active);
            order.AddRange(LanguagePatch.Languages);
            foreach (var lang in order)
            {
                var items = lang.Fields?.items;
                if (items == null) continue;
                foreach (var item in db.items)
                {
                    var nm = Field.LookupValue(item.fields, "Name");
                    if (string.IsNullOrEmpty(nm) || !items.TryGetValue(nm, out var fields)) continue;
                    if (fields.ContainsKey("hypothesisSentence")) return item;
                }
            }
            return null;
        }

        private static string Original(Field f)
        {
            if (!_original.TryGetValue(f, out var en))
            {
                en = f.value;
                _original[f] = en;
            }
            return en;
        }

        /// <summary>Write a localised variant field, adding it if absent. Returns 1 when
        /// it replaced one of the game's own "TBT:" placeholders, for the log.</summary>
        private static int SetVariant(List<Field> fields, string title, string value)
        {
            var f = Field.Lookup(fields, title);
            if (f == null)
            {
                fields.Add(new Field(title, value, FieldType.Text));
                return 0;
            }
            int placeholder = f.value != null && f.value.StartsWith("TBT:", StringComparison.Ordinal) ? 1 : 0;
            f.value = value;
            return placeholder;
        }

        private static string Cut(string s)
        {
            if (string.IsNullOrEmpty(s)) return "(empty)";
            s = s.Replace("\n", " ");
            return "\"" + (s.Length > 90 ? s.Substring(0, 90) + "…" : s) + "\"";
        }
    }
}
