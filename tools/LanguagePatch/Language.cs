using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using BepInEx.Logging;
using Newtonsoft.Json;

namespace BlakeManor.Patch
{
    /// <summary>
    /// One language the patch can show. Each is a folder next to the plugin,
    ///
    ///     BepInEx/plugins/BlakeManorFR/&lt;code&gt;/
    ///         language.json     { "code": "fr", "name": "Français" }
    ///         ui.json           source string -> translation   (Plugin.cs)
    ///         fields.json       item/actor fields              (DialogueFields.cs)
    ///         dialogue.json     conversation lines             (DialogueLines.cs)
    ///
    /// The code is what the Dialogue System fields are named after and what the
    /// config stores; the name is what Adventure Creator registers and what the
    /// options row shows. The game's own English is the one language without a
    /// folder: <see cref="English"/>.
    /// </summary>
    internal sealed class Language
    {
        public const string Descriptor = "language.json";

        public string Code;
        public string Name;
        public string Dir;
        /// <summary>Index in SpeechManager.languages once registered; 0 is the game's English.</summary>
        public int AcIndex;

        public bool IsEnglish => Dir == null;

        /// <summary>UI layer: source string -> translation.</summary>
        public readonly Dictionary<string, string> Ui = new Dictionary<string, string>(StringComparer.Ordinal);
        public DialogueFields.Layer Fields;
        public DialogueLines.Layer Lines;
        public int FieldCount, LineCount;

        /// <summary>UI strings seen untranslated while this language was active.</summary>
        public readonly HashSet<string> Missed = new HashSet<string>(StringComparer.Ordinal);

        public static readonly Language English = new Language { Code = "en", Name = "English", AcIndex = 0 };

        public override string ToString() => Name;

        public bool Matches(string codeOrName)
            => string.Equals(codeOrName, Code, StringComparison.OrdinalIgnoreCase)
            || string.Equals(codeOrName, Name, StringComparison.Ordinal);

        /// <summary>Every folder under <paramref name="dataDir"/> holding a descriptor, in
        /// folder-name order so the choice of default is stable.</summary>
        public static List<Language> LoadAll(string dataDir, ManualLogSource log)
        {
            var found = new List<Language>();
            if (!Directory.Exists(dataDir)) return found;
            var dirs = Directory.GetDirectories(dataDir);
            Array.Sort(dirs, StringComparer.Ordinal);
            foreach (var dir in dirs)
            {
                var descriptor = Path.Combine(dir, Descriptor);
                if (!File.Exists(descriptor)) continue;
                var lang = Load(dir, descriptor, log);
                if (lang == null) continue;
                if (found.Exists(l => l.Matches(lang.Code) || l.Matches(lang.Name)))
                {
                    log.LogWarning($"Language \"{lang.Code}\" in {dir} duplicates one already loaded; skipped.");
                    continue;
                }
                found.Add(lang);
            }
            return found;
        }

        private static Language Load(string dir, string descriptor, ManualLogSource log)
        {
            Meta meta;
            try { meta = JsonConvert.DeserializeObject<Meta>(File.ReadAllText(descriptor, Encoding.UTF8)); }
            catch (Exception e)
            {
                log.LogError($"Could not read {descriptor}: {e.Message}");
                return null;
            }
            var folder = Path.GetFileName(dir);
            var code = string.IsNullOrWhiteSpace(meta?.code) ? folder : meta.code.Trim();
            if (!string.Equals(code, folder, StringComparison.Ordinal))
                log.LogWarning($"{descriptor} says code \"{code}\" but sits in folder \"{folder}\"; using \"{code}\".");
            if (English.Matches(code))
            {
                log.LogWarning($"{descriptor}: \"{code}\" is the game's own language; skipped.");
                return null;
            }
            var lang = new Language
            {
                Code = code,
                Name = string.IsNullOrWhiteSpace(meta?.name) ? code : meta.name.Trim(),
                Dir = dir,
            };
            if (English.Matches(lang.Name))
            {
                log.LogWarning($"{descriptor}: the name \"{lang.Name}\" is taken by the game's own language; skipped.");
                return null;
            }

            LoadUi(lang, Path.Combine(dir, "ui.json"), log);
            lang.FieldCount = DialogueFields.Load(lang, Path.Combine(dir, "fields.json"));
            lang.LineCount = DialogueLines.Load(lang, Path.Combine(dir, "dialogue.json"));
            if (lang.Ui.Count == 0 && lang.FieldCount == 0 && lang.LineCount == 0)
            {
                log.LogWarning($"Language \"{lang.Code}\" in {dir} has no translations at all; skipped.");
                return null;
            }
            return lang;
        }

        private static void LoadUi(Language lang, string path, ManualLogSource log)
        {
            if (!File.Exists(path)) return;
            try
            {
                var doc = JsonConvert.DeserializeObject<UiLayer>(File.ReadAllText(path, Encoding.UTF8));
                if (doc?.bySource == null) return;
                foreach (var kv in doc.bySource)
                    if (!string.IsNullOrEmpty(kv.Key)) lang.Ui[kv.Key] = kv.Value;
            }
            catch (Exception e)
            {
                log.LogError($"Could not read {path}: {e.Message}");
            }
        }

        private class Meta
        {
            public string code { get; set; }
            public string name { get; set; }
        }

        private class UiLayer
        {
            public Dictionary<string, string> bySource { get; set; }
        }
    }
}
