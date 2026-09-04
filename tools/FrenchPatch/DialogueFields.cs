using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
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
                yield break;

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
                yield break;
            }

            int applied = 0, missingItems = 0, missingFields = 0, skipped = 0, luaErrors = 0;

            if (_wanted != null)
            {
                foreach (var item in db.items)
                {
                    var name = Field.LookupValue(item.fields, "Name");
                    if (string.IsNullOrEmpty(name)) continue;
                    if (!_wanted.TryGetValue(name, out var fields)) continue;

                    foreach (var kv in fields)
                    {
                        if (Protected.Contains(kv.Key)) { skipped++; continue; }
                        var f = Field.Lookup(item.fields, kv.Key);
                        if (f == null) { missingFields++; continue; }
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
                        f.value = kv.Value;
                        var loc = Field.Lookup(actor.fields, kv.Key + " fr");
                        if (loc != null) loc.value = kv.Value;
                        else actor.fields.Add(new Field(kv.Key + " fr", kv.Value, FieldType.Text));
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
            foreach (var item in db.items)
            {
                var nm = Field.LookupValue(item.fields, "Name");
                if (string.IsNullOrEmpty(nm) || !_wanted.ContainsKey(nm)) continue;
                if (!_wanted[nm].ContainsKey("hypothesisSentence")) continue;

                var inDb = Field.LookupValue(item.fields, "hypothesisSentence");
                string inLua;
                try { inLua = DialogueLua.GetQuestField(nm, "hypothesisSentence").asString; }
                catch (Exception e) { inLua = "(lookup failed: " + e.Message + ")"; }

                FrenchPatch.Log.LogInfo($"Hypothesis probe [{nm}]");
                FrenchPatch.Log.LogInfo($"   db.items  -> {Cut(inDb)}");
                FrenchPatch.Log.LogInfo($"   Lua quest -> {Cut(inLua)}");
                break;
            }

            FrenchPatch.Log.LogInfo(
                $"Dialogue System fields: {applied} translated"
                + (missingItems > 0 ? $", {missingItems} items not found" : "")
                + (missingFields > 0 ? $", {missingFields} fields not found" : "")
                + (skipped > 0 ? $", {skipped} protected fields skipped" : "")
                + (luaErrors > 0 ? $", {luaErrors} Lua writes failed" : ""));
        }

        private static string Cut(string s)
        {
            if (string.IsNullOrEmpty(s)) return "(empty)";
            s = s.Replace("\n", " ");
            return "\"" + (s.Length > 90 ? s.Substring(0, 90) + "…" : s) + "\"";
        }
    }
}
