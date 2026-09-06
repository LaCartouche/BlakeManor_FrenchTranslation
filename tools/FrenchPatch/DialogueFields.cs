using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text;
using Newtonsoft.Json;
using UnityEngine;
using PixelCrushers.DialogueSystem;

namespace BlakeManor.FR
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
    /// first time it is seen, which is what lets SetFrench put it back when the
    /// player switches language in the options screen.
    /// </summary>
    internal static class DialogueFields
    {
        private class Layer
        {
            public Dictionary<string, Dictionary<string, string>> items { get; set; }
            public Dictionary<string, Dictionary<string, string>> actors { get; set; }
        }

        private static Dictionary<string, Dictionary<string, string>> _wanted;
        private static Dictionary<string, Dictionary<string, string>> _actors;

        /// <summary>Field titles that must never be overwritten — they are keys, not text.</summary>
        private static readonly HashSet<string> Protected = new HashSet<string>(StringComparer.Ordinal)
        {
            "Name", "Technical Name", "Articy Id", "Is Item", "IsQuest", "State",
            "evidenceIDs", "essentialEvidenceIDs", "variablesPrefixOverride",
            "LinkedActor", "QuestType", "IsNPCQuest", "IsTopLevelMystery",
        };

        /// <summary>One overwritten field: the object, what the game shipped, what we put there.</summary>
        private class Swap
        {
            public Field field;
            public string en, fr;
            public string item, key;
            public bool lua;   // quest fields are mirrored into the Lua environment too
        }

        private static readonly List<Swap> _swaps = new List<Swap>();

        // The English as first seen, per field object, so a second Apply (after a
        // database reload) does not mistake our own French for the original.
        private static readonly Dictionary<Field, string> _original = new Dictionary<Field, string>(new RefEq());

        private class RefEq : IEqualityComparer<Field>
        {
            public bool Equals(Field a, Field b) => ReferenceEquals(a, b);
            public int GetHashCode(Field f) => RuntimeHelpers.GetHashCode(f);
        }

        /// <summary>Set once Apply has finished (or found nothing to do).</summary>
        internal static bool Done;

        public static int Load(string path)
        {
            if (!File.Exists(path)) return 0;
            try
            {
                var doc = JsonConvert.DeserializeObject<Layer>(File.ReadAllText(path, Encoding.UTF8));
                _wanted = doc?.items;
                _actors = doc?.actors;
                int n = 0;
                if (_wanted != null) foreach (var kv in _wanted) n += kv.Value.Count;
                if (_actors != null) foreach (var kv in _actors) n += kv.Value.Count;
                return n;
            }
            catch (Exception e)
            {
                FrenchPatch.Log.LogError($"Could not read {path}: {e.Message}");
                return 0;
            }
        }

        public static IEnumerator Apply()
        {
            if ((_wanted == null || _wanted.Count == 0) && (_actors == null || _actors.Count == 0))
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
                FrenchPatch.Log.LogWarning("Dialogue database never appeared; item fields not translated.");
                Done = true;
                yield break;
            }

            int applied = 0, missingItems = 0, missingFields = 0, skipped = 0, luaErrors = 0, placeholders = 0;

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
                    FrenchPatch.Log.LogInfo(
                        "Adventure Creator uses a separate master database; translating that too.");
                }
            }
            catch (Exception e)
            {
                FrenchPatch.Log.LogWarning("Could not reach AC's master database: " + e.Message);
            }

            _swaps.Clear();
            bool french = FrenchPatch.French;

            if (_wanted != null)
            {
              foreach (var database in databases)
                foreach (var item in database.items)
                {
                    var name = Field.LookupValue(item.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!_wanted.TryGetValue(name, out var fields)) continue;

                    foreach (var kv in fields)
                    {
                        if (Protected.Contains(kv.Key)) { skipped++; continue; }
                        var f = Field.Lookup(item.fields, kv.Key);
                        if (f == null) { missingFields++; continue; }

                        _swaps.Add(new Swap
                        {
                            field = f, en = Original(f), fr = kv.Value, item = name, key = kv.Key, lua = true,
                        });
                        if (french)
                        {
                            f.value = kv.Value;

                            // The database is only half of it. The Dialogue System mirrors
                            // item/quest fields into its Lua environment at startup, and the
                            // hypothesis screen reads that copy — proven by the probe below,
                            // which found French in db.items and English in Lua. Writing only
                            // the database left every template in English.
                            try { DialogueLua.SetQuestField(name, kv.Key, kv.Value); }
                            catch (Exception e)
                            {
                                if (luaErrors++ == 0)
                                    FrenchPatch.Log.LogWarning(
                                        $"Could not write Lua quest field '{kv.Key}' on '{name}': {e.Message}");
                            }
                        }

                        // Also publish the localised variants the game's own loader
                        // would create. The shipped build carries an unfinished French
                        // ("TBT: ...") under exactly these names; ours must win.
                        placeholders += SetVariant(item.fields, kv.Key + " fr", kv.Value);
                        SetVariant(item.fields, kv.Key + " " + FrenchPatch.LanguageName, kv.Value);
                        applied++;
                    }
                }
            }

            // Actor cast/lore fields. These are read two different ways depending on
            // the screen — LookupValue for the lore panel, LookupLocalizedValue for
            // the dialogue UI — so write both the base field and its " fr" variant.
            if (_actors != null)
            {
                foreach (var actor in db.actors)
                {
                    var name = Field.LookupValue(actor.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!_actors.TryGetValue(name, out var fields)) continue;

                    foreach (var kv in fields)
                    {
                        if (Protected.Contains(kv.Key)) { skipped++; continue; }
                        var f = Field.Lookup(actor.fields, kv.Key);
                        if (f == null) { missingFields++; continue; }

                        _swaps.Add(new Swap
                        {
                            field = f, en = Original(f), fr = kv.Value, item = name, key = kv.Key, lua = false,
                        });
                        if (french) f.value = kv.Value;
                        placeholders += SetVariant(actor.fields, kv.Key + " fr", kv.Value);
                        SetVariant(actor.fields, kv.Key + " " + FrenchPatch.LanguageName, kv.Value);
                        applied++;
                    }
                }
            }

            // report anything the database did not have, so a game patch that renames
            // an item shows up as a warning rather than as silently English text
            var present = new HashSet<string>(StringComparer.Ordinal);
            foreach (var item in db.items)
            {
                var n = Field.LookupValue(item.fields, "Name");
                if (!string.IsNullOrEmpty(n)) present.Add(n);
            }
            if (_wanted != null)
                foreach (var kv in _wanted)
                    if (!present.Contains(kv.Key)) missingItems++;

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

                FrenchPatch.Log.LogInfo($"Hypothesis probe [{nm}]");
                FrenchPatch.Log.LogInfo($"   db.items  -> {Cut(Field.LookupValue(probe.fields, "hypothesisSentence"))}");
                FrenchPatch.Log.LogInfo($"   Lua quest -> {Cut(inLua)}");
                FrenchPatch.Log.LogInfo($"   AC db (what the panel reads) -> {ProbeHypothesis()}");
            }

            FrenchPatch.Log.LogInfo(
                $"Dialogue System fields: {applied} " + (french ? "translated" : "prepared (English selected)")
                + (missingItems > 0 ? $", {missingItems} items not found" : "")
                + (missingFields > 0 ? $", {missingFields} fields not found" : "")
                + (skipped > 0 ? $", {skipped} protected fields skipped" : "")
                + (luaErrors > 0 ? $", {luaErrors} Lua writes failed" : "")
                + (placeholders > 0
                    ? $", {placeholders} placeholder fields from the game's own unfinished French overwritten"
                    : ""));
            Done = true;
        }

        /// <summary>
        /// Put every overwritten field back to English, or to French again. The Lua
        /// mirror follows for quest fields, once per field rather than once per
        /// database copy.
        /// </summary>
        internal static int SetFrench(bool on)
        {
            int n = 0, luaErrors = 0;
            var luaDone = new HashSet<string>(StringComparer.Ordinal);
            foreach (var s in _swaps)
            {
                var v = on ? s.fr : s.en;
                if (s.field == null) continue;
                s.field.value = v;
                n++;
                if (!s.lua || !luaDone.Add(s.item + "|" + s.key)) continue;
                try { DialogueLua.SetQuestField(s.item, s.key, v); }
                catch (Exception e)
                {
                    if (luaErrors++ == 0)
                        FrenchPatch.Log.LogWarning($"Could not write Lua quest field '{s.key}' on '{s.item}': {e.Message}");
                }
            }
            if (luaErrors > 0) FrenchPatch.Log.LogWarning($"{luaErrors} Lua quest fields could not be rewritten.");
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

        private static Item FirstTemplate(DialogueDatabase db)
        {
            if (db == null || _wanted == null) return null;
            foreach (var item in db.items)
            {
                var nm = Field.LookupValue(item.fields, "Name");
                if (string.IsNullOrEmpty(nm) || !_wanted.TryGetValue(nm, out var fields)) continue;
                if (fields.ContainsKey("hypothesisSentence")) return item;
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
