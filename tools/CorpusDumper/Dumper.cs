using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using BepInEx;
using BepInEx.Logging;
using Newtonsoft.Json;
using UnityEngine;
using PixelCrushers.DialogueSystem;

namespace BlakeManor.Corpus
{
    /// <summary>
    /// Phase 1 of the FR translation plan: dump the game's English corpus from the
    /// live runtime, where both text systems are fully typed and carry their own IDs.
    ///
    /// Two sources, dumped independently so a failure in one still yields the other:
    ///   - PixelCrushers Dialogue System : DialogueManager.masterDatabase (conversations)
    ///   - Adventure Creator             : KickStarter.speechManager.lines (everything else)
    ///
    /// Env vars:
    ///   BLAKE_DUMP_DIR    output directory (default: ~/prj/blakemanor_translation/corpus/raw)
    ///   BLAKE_DUMP_QUIT   "1" to Application.Quit() once both dumps are written
    ///   BLAKE_DUMP_WAIT   seconds to wait for the systems to come up (default 300)
    /// </summary>
    [BepInPlugin(Guid, "Blake Manor Corpus Dumper", "0.1.0")]
    public class DumperPlugin : BaseUnityPlugin
    {
        public const string Guid = "fr.blakemanor.corpusdumper";

        private static ManualLogSource Log;
        private string _outDir;
        private bool _dsDone, _acDone;

        private void Awake()
        {
            Log = Logger;

            _outDir = Environment.GetEnvironmentVariable("BLAKE_DUMP_DIR");
            if (string.IsNullOrEmpty(_outDir))
            {
                var home = Environment.GetEnvironmentVariable("HOME") ?? ".";
                _outDir = Path.Combine(home, "prj/blakemanor_translation/corpus/raw");
            }
            Directory.CreateDirectory(_outDir);

            Log.LogInfo("Corpus dumper active. Output: " + _outDir);
            StartCoroutine(Run());
        }

        private IEnumerator Run()
        {
            float wait = 300f;
            var w = Environment.GetEnvironmentVariable("BLAKE_DUMP_WAIT");
            if (!string.IsNullOrEmpty(w)) float.TryParse(w, out wait);

            float deadline = Time.realtimeSinceStartup + wait;
            int tick = 0;

            while (Time.realtimeSinceStartup < deadline && !(_dsDone && _acDone))
            {
                if (!_dsDone && TryGetDialogueDatabase() != null)
                {
                    try { DumpDialogueSystem(); _dsDone = true; }
                    catch (Exception e) { Log.LogError("Dialogue System dump failed: " + e); _dsDone = true; }
                }

                if (!_acDone && TryGetSpeechManager() != null)
                {
                    try { DumpAdventureCreator(); _acDone = true; }
                    catch (Exception e) { Log.LogError("Adventure Creator dump failed: " + e); _acDone = true; }
                }

                if (++tick % 60 == 0)
                    Log.LogInfo(string.Format("waiting... dialogueSystem={0} adventureCreator={1}", _dsDone, _acDone));

                yield return new WaitForSecondsRealtime(0.25f);
            }

            if (!_dsDone) Log.LogWarning("Timed out waiting for DialogueManager.masterDatabase.");
            if (!_acDone) Log.LogWarning("Timed out waiting for KickStarter.speechManager.");

            WriteMeta();

            if (Environment.GetEnvironmentVariable("BLAKE_DUMP_QUIT") == "1")
            {
                Log.LogInfo("Dump complete, quitting.");
                yield return new WaitForSecondsRealtime(1f);
                Application.Quit();
            }
        }

        // ---------------------------------------------------------------- sources

        private static DialogueDatabase TryGetDialogueDatabase()
        {
            try { return DialogueManager.instance != null ? DialogueManager.masterDatabase : null; }
            catch { return null; }
        }

        private static AC.SpeechManager TryGetSpeechManager()
        {
            try
            {
                // The managers load a frame or two apart; wait for the inventory manager
                // too, otherwise the UI pools come back empty on a fast boot.
                if (AC.KickStarter.speechManager == null) return null;
                if (AC.KickStarter.inventoryManager == null) return null;
                if (AC.KickStarter.menuManager == null) return null;
                return AC.KickStarter.speechManager;
            }
            catch { return null; }
        }

        // ------------------------------------------------- Pixel Crushers dump

        private void DumpDialogueSystem()
        {
            var db = DialogueManager.masterDatabase;
            Log.LogInfo(string.Format(
                "Dumping dialogue database: {0} conversations, {1} actors, {2} items, {3} locations, {4} variables",
                db.conversations.Count, db.actors.Count, db.items.Count, db.locations.Count, db.variables.Count));

            int entryCount = 0;
            var conversations = new List<object>();

            foreach (var conv in db.conversations)
            {
                var entries = new List<object>();
                foreach (var e in conv.dialogueEntries)
                {
                    entryCount++;
                    entries.Add(new Dictionary<string, object>
                    {
                        { "id",             e.id },
                        { "conversationId", e.conversationID },
                        { "isRoot",         e.isRoot },
                        { "isGroup",        e.isGroup },
                        { "actorId",        SafeInt(() => e.ActorID) },
                        { "conversantId",   SafeInt(() => e.ConversantID) },
                        { "conditions",     e.conditionsString },
                        { "userScript",     e.userScript },
                        { "outgoing",       OutgoingLinks(e) },
                        { "fields",         FieldMap(e.fields) },
                    });
                }

                conversations.Add(new Dictionary<string, object>
                {
                    { "id",      conv.id },
                    { "fields",  FieldMap(conv.fields) },
                    { "entries", entries },
                });
            }

            var payload = new Dictionary<string, object>
            {
                { "source",  "PixelCrushers.DialogueSystem" },
                { "version", db.version },
                { "author",  db.author },
                { "counts",  new Dictionary<string, object> {
                    { "conversations", db.conversations.Count },
                    { "entries",       entryCount },
                    { "actors",        db.actors.Count },
                    { "items",         db.items.Count },
                    { "locations",     db.locations.Count },
                    { "variables",     db.variables.Count },
                }},
                { "actors",        Assets(db.actors) },
                { "items",         Assets(db.items) },
                { "locations",     Assets(db.locations) },
                { "variables",     Assets(db.variables) },
                { "conversations", conversations },
            };

            WriteJson("dialogue_system.json", payload);
            Log.LogInfo("Wrote dialogue_system.json (" + entryCount + " entries)");
        }

        private static List<object> OutgoingLinks(DialogueEntry e)
        {
            var links = new List<object>();
            if (e.outgoingLinks == null) return links;
            foreach (var l in e.outgoingLinks)
                links.Add(new Dictionary<string, object>
                {
                    { "conversationId",            l.destinationConversationID },
                    { "entryId",                   l.destinationDialogueID },
                    { "originConversationId",      l.originConversationID },
                    { "originEntryId",             l.originDialogueID },
                });
            return links;
        }

        private static List<object> Assets<T>(List<T> assets) where T : Asset
        {
            var list = new List<object>();
            if (assets == null) return list;
            foreach (var a in assets)
                list.Add(new Dictionary<string, object>
                {
                    { "id",     a.id },
                    { "fields", FieldMap(a.fields) },
                });
            return list;
        }

        /// <summary>
        /// Fields are dumped verbatim, every one of them. Deciding what is
        /// translatable is post-processing's job, not the dumper's - a field we
        /// silently drop here is a line that never gets translated.
        /// </summary>
        private static List<object> FieldMap(List<Field> fields)
        {
            var list = new List<object>();
            if (fields == null) return list;
            foreach (var f in fields)
            {
                if (f == null) continue;
                list.Add(new Dictionary<string, object>
                {
                    { "title", f.title },
                    { "value", f.value },
                    { "type",  f.type.ToString() },
                    { "hash",  Hash(f.value) },
                });
            }
            return list;
        }

        // ------------------------------------------------ Adventure Creator dump

        private void DumpAdventureCreator()
        {
            var sm = AC.KickStarter.speechManager;
            Log.LogInfo(string.Format("Dumping AC speech manager: {0} lines, {1} languages",
                sm.lines != null ? sm.lines.Count : 0,
                sm.languages != null ? sm.languages.Count : 0));

            var lines = new List<object>();
            if (sm.lines != null)
            {
                foreach (var l in sm.lines)
                {
                    if (l == null) continue;
                    lines.Add(new Dictionary<string, object>
                    {
                        { "lineID",      l.lineID },
                        { "textType",    l.textType.ToString() },
                        { "owner",       l.owner },
                        { "isPlayer",    l.isPlayer },
                        { "scene",       l.scene },
                        { "description", l.description },
                        { "text",        l.text },
                        { "hash",        Hash(l.text) },
                        { "existingTranslations", l.translationText != null ? l.translationText.Count : 0 },
                    });
                }
            }

            Log.LogInfo("Collecting UI / non-conversation pools:");
            var pools = UiDumper.Collect(m => Log.LogInfo(m));

            var payload = new Dictionary<string, object>
            {
                { "source",           "AdventureCreator" },
                { "languages",        sm.languages },
                { "displayLanguages", sm.displayLanguages },
                { "counts", new Dictionary<string, object> { { "lines", lines.Count } } },
                { "lines",            lines },
                { "pools",            pools },
            };

            WriteJson("adventure_creator.json", payload);
            Log.LogInfo("Wrote adventure_creator.json (" + lines.Count + " lines)");
        }

        // ---------------------------------------------------------------- output

        private void WriteMeta()
        {
            string buildGuid = "";
            try
            {
                var cfg = Path.Combine(Application.dataPath, "boot.config");
                if (File.Exists(cfg))
                    foreach (var line in File.ReadAllLines(cfg))
                        if (line.StartsWith("build-guid=")) buildGuid = line.Substring("build-guid=".Length);
            }
            catch (Exception e) { Log.LogWarning("boot.config unreadable: " + e.Message); }

            WriteJson("meta.json", new Dictionary<string, object>
            {
                { "dumpedAtUtc",    DateTime.UtcNow.ToString("o") },
                { "dumperVersion",  "0.1.0" },
                { "unityVersion",   Application.unityVersion },
                { "gameVersion",    Application.version },
                { "buildGuid",      buildGuid },
                { "dialogueSystemDumped",   _dsDone },
                { "adventureCreatorDumped", _acDone },
            });
        }

        private void WriteJson(string name, object payload)
        {
            var path = Path.Combine(_outDir, name);
            var json = JsonConvert.SerializeObject(payload, Formatting.Indented);
            File.WriteAllText(path, json, new UTF8Encoding(false));
            Log.LogInfo(string.Format("  -> {0} ({1:N0} bytes)", path, json.Length));
        }

        // ---------------------------------------------------------------- helpers

        private static int SafeInt(Func<int> f)
        {
            try { return f(); } catch { return -1; }
        }

        /// <summary>Short content hash, so a later game patch shows exactly which lines drifted.</summary>
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
