using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Text;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using Newtonsoft.Json;
using UnityEngine;

namespace BlakeManor.Patch
{
    /// <summary>
    /// The plugin, and the UI layer.
    ///
    /// Every language the patch ships is a folder next to this assembly (see
    /// Language.cs). All of them are loaded at startup, one is active, and the player
    /// moves between them — and the game's own English — from the options screen
    /// (LanguageOption) without restarting.
    ///
    /// UI layer: Adventure Creator's translation table is empty in the shipped build,
    /// so every lineID is -1 and the usual lineID-keyed route is dead. Instead this
    /// hooks the one method all AC-side text funnels through and substitutes by
    /// source string:
    ///
    ///     RuntimeLanguages.GetTranslation(originalText, lineID, language)
    ///
    /// Many call sites skip that method entirely when the active language index is 0
    /// (see Hotspot.GetName), so each language is registered on SpeechManager and
    /// Options.GetLanguage() is made to report the active one.
    ///
    /// Conversation subtitles and item fields are NOT handled here — see
    /// DialogueLines and DialogueFields.
    /// </summary>
    [BepInPlugin(Guid, "Blake Manor — Traduction française", "1.1.0")]
    public class LanguagePatch : BaseUnityPlugin
    {
        public const string Guid = "fr.blakemanor.frenchpatch";
        /// <summary>Folder next to the assembly holding one sub-folder per language.</summary>
        public const string DataFolder = "BlakeManorFR";

        internal static ManualLogSource Log;
        /// <summary>The running plugin, so the layers can start coroutines after their
        /// initial pass (see DialogueLines.Watchdog).</summary>
        internal static LanguagePatch Instance;

        /// <summary>Every language shipped, in load order. English is not in it.</summary>
        internal static readonly List<Language> Languages = new List<Language>();
        /// <summary>What the player sees right now. Flipped at runtime from the options
        /// menu and persisted in the BepInEx config — never in the game's own options
        /// file, see LanguageOption for why.</summary>
        internal static Language Active = Language.English;
        /// <summary>True while a shipped language is on; false for the game's English.</summary>
        internal static bool Translating => !Active.IsEnglish;

        /// <summary>Every string we hand back, in any language. The game re-queries
        /// some of them, and logging our own output as "untranslated" would drown the
        /// QA signal.</summary>
        private static readonly HashSet<string> Emitted = new HashSet<string>(StringComparer.Ordinal);
        internal static bool Ready;
        internal static long Hits, Misses;

        private ConfigEntry<bool> _logMisses;
        private ConfigEntry<string> _language;
        private ConfigEntry<bool> _selfTestSwitch, _quitAfterSelfTest;
        private string _dataDir;

        private void Awake()
        {
            Instance = this;
            Log = Logger;
            _logMisses = Config.Bind("QA", "LogMisses", true,
                "Record every string that passed through untranslated, to BepInEx/blakemanor-<code>-misses.txt "
                + "for the language that was active. This is how the remaining untranslated UI gets found.");
            _language = Config.Bind("Language", "Active", "",
                "Code of the language shown in game (the folder name under BepInEx/plugins/" + DataFolder + "), "
                + "or \"en\" for the original English. Empty: the first language shipped. Changed in game from "
                + "Options > Interface > Language. Kept here rather than in the game's own options file so that "
                + "removing the patch leaves nothing behind.");
            _selfTestSwitch = Config.Bind("QA", "SelfTestSwitch", false,
                "At startup, once every layer is applied, switch to another language and back, logging "
                + "what each layer resolves to in each state. Leaves the language as configured.");
            _quitAfterSelfTest = Config.Bind("QA", "QuitAfterSelfTest", false,
                "Quit the game once SelfTestSwitch has finished.");

            _dataDir = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) ?? ".", DataFolder);
            Languages.AddRange(Language.LoadAll(_dataDir, Log));
            if (Languages.Count == 0)
            {
                Log.LogWarning("No language found — the patch will do nothing. Expected e.g. "
                               + Path.Combine(_dataDir, "fr", Language.Descriptor));
                return;
            }
            Emitted.Add(Language.English.Name);
            foreach (var lang in Languages)
            {
                Emitted.Add(lang.Name);
                foreach (var v in lang.Ui.Values)
                    if (!string.IsNullOrEmpty(v)) Emitted.Add(v);
            }
            Active = Resolve(_language.Value);

            var harmony = new Harmony(Guid);
            int applied = 0;
            applied += TryPatch(harmony, typeof(Patch_Options_GetLanguage));
            applied += TryPatch(harmony, typeof(Patch_RuntimeLanguages_GetTranslation));
            applied += TryPatch(harmony, typeof(LanguageOption.Patch_OptionsMenu_OnEnable));

            var summary = new StringBuilder();
            foreach (var lang in Languages)
                summary.Append(summary.Length > 0 ? "; " : "")
                       .Append($"{lang.Name} [{lang.Code}]: {lang.Ui.Count} UI strings, {lang.FieldCount} item fields, {lang.LineCount} dialogue lines");
            Log.LogInfo($"{applied}/3 patches applied. Languages: {summary}. Active: {Active.Name}.");

            StartCoroutine(RegisterLanguages());
            StartCoroutine(DialogueFields.Apply());
            StartCoroutine(DialogueLines.Apply());
            if (_selfTestSwitch.Value) StartCoroutine(SelfTestSwitch());

            var shotAfter = Environment.GetEnvironmentVariable("BLAKE_FR_SHOT_AFTER");
            if (!string.IsNullOrEmpty(shotAfter) && float.TryParse(shotAfter, out var delay))
                StartCoroutine(CaptureScreenshot(delay));
        }

        /// <summary>The language a config value names; the first shipped one when it
        /// names nothing we have.</summary>
        private static Language Resolve(string code)
        {
            if (string.IsNullOrWhiteSpace(code)) return Languages[0];
            if (Language.English.Matches(code)) return Language.English;
            var lang = Languages.Find(l => l.Matches(code));
            if (lang != null) return lang;
            Log.LogWarning($"Configured language \"{code}\" is not shipped; using {Languages[0].Name}.");
            return Languages[0];
        }

        /// <summary>The language <paramref name="step"/> places after the active one, in
        /// the order English, then the shipped languages, wrapping round.</summary>
        internal static Language Neighbour(int step)
        {
            var all = new List<Language> { Language.English };
            all.AddRange(Languages);
            int i = all.IndexOf(Active);
            if (i < 0) i = 0;
            int n = all.Count;
            return all[((i + step) % n + n) % n];
        }

        // ------------------------------------------------------------- switching

        /// <summary>
        /// Move every layer to another language while the game runs. Called from the
        /// options-menu row (LanguageOption) and from the startup self-test.
        /// </summary>
        internal static void SetLanguage(Language lang, string reason)
        {
            if (lang == null) return;
            Active = lang;
            try
            {
                if (Instance != null && Instance._language != null)
                {
                    Instance._language.Value = lang.Code;
                    Instance.Config.Save();
                }
            }
            catch (Exception e) { Log.LogWarning("Could not save the language choice: " + e.Message); }

            int swapped = DialogueFields.SetLanguage(lang);
            DialogueLines.SetLanguage(lang);

            // Every TranslatableTMPText listens to this and re-runs GetTranslation — our
            // hook — so the whole interface re-labels itself in one pass.
            try
            {
                var em = AC.KickStarter.eventManager;
                if (em != null) em.Call_OnChangeLanguage(lang.AcIndex);
            }
            catch (Exception e) { Log.LogWarning("Could not raise OnChangeLanguage: " + e.Message); }

            LanguageOption.AfterSwitch();
            Log.LogInfo($"Language -> {lang.Name} ({reason}); {swapped} item/actor fields swapped. " + Probe());
        }

        /// <summary>One line saying what each layer resolves to right now.</summary>
        internal static string Probe()
        {
            string ui;
            try
            {
                int lang = AC.KickStarter.options != null ? AC.KickStarter.options.GetLanguage() : -1;
                string probe = AC.KickStarter.runtimeLanguages != null
                    ? AC.KickStarter.runtimeLanguages.GetTranslation("Examine", -1, lang)
                    : "(no runtimeLanguages)";
                ui = $"GetLanguage={lang}, UI \"Examine\" -> \"{probe}\"";
            }
            catch (Exception e) { ui = "UI probe failed: " + e.Message; }
            return ui + " | " + DialogueLines.Describe() + " | hypothesis -> " + DialogueFields.ProbeHypothesis();
        }

        /// <summary>QA: prove the switch works without a hand on the controller.</summary>
        private IEnumerator SelfTestSwitch()
        {
            float deadline = Time.realtimeSinceStartup + 180f;
            while (Time.realtimeSinceStartup < deadline && !(Ready && DialogueFields.Done && DialogueLines.Done))
                yield return new WaitForSecondsRealtime(0.5f);
            if (!(Ready && DialogueFields.Done && DialogueLines.Done))
            {
                Log.LogWarning("Self-test switch: the layers never finished applying; nothing tested.");
                yield break;
            }
            yield return new WaitForSecondsRealtime(3f);   // let the AC↔DS bridge settle first

            var start = Active;
            var other = Neighbour(1);
            Log.LogInfo("Self-test switch [1/3] as configured: " + Probe());
            LanguageOption.ProbeMenu();
            SetLanguage(other, "self-test");
            yield return new WaitForSecondsRealtime(2f);
            Log.LogInfo("Self-test switch [2/3] flipped: " + Probe());
            SetLanguage(start, "self-test");
            yield return new WaitForSecondsRealtime(2f);
            Log.LogInfo("Self-test switch [3/3] restored: " + Probe());

            if (_quitAfterSelfTest.Value)
            {
                WriteMisses();
                Application.Quit();
            }
        }

        /// <summary>QA aid: capture the screen after a delay, then quit. Used to check
        /// rendering and text overflow without sitting through the game by hand.</summary>
        private IEnumerator CaptureScreenshot(float delay)
        {
            yield return new WaitForSecondsRealtime(delay);
            var path = Environment.GetEnvironmentVariable("BLAKE_FR_SHOT_PATH");
            if (string.IsNullOrEmpty(path))
                path = Path.Combine(Paths.BepInExRootPath, "blakemanor-shot.png");
            try { ScreenCapture.CaptureScreenshot(path); Log.LogInfo("Screenshot -> " + path); }
            catch (Exception e) { Log.LogWarning("Screenshot failed: " + e.Message); }
            yield return new WaitForSecondsRealtime(3f);
            if (Environment.GetEnvironmentVariable("BLAKE_FR_SHOT_QUIT") == "1")
            {
                WriteMisses();
                Application.Quit();
            }
        }

        /// <summary>Patch one class at a time: a target that moved should disable one
        /// hook, not silently abort the rest of them.</summary>
        private static int TryPatch(Harmony harmony, Type patchClass)
        {
            try
            {
                harmony.CreateClassProcessor(patchClass).Patch();
                return 1;
            }
            catch (Exception e)
            {
                Log.LogError($"Patch {patchClass.Name} failed: {e.Message}");
                return 0;
            }
        }

        /// <summary>
        /// Adds each shipped language to the SpeechManager so language counts and name
        /// lookups stay consistent, then makes RuntimeLanguages re-copy the manager's lists.
        /// </summary>
        private IEnumerator RegisterLanguages()
        {
            float deadline = Time.realtimeSinceStartup + 120f;
            while (Time.realtimeSinceStartup < deadline)
            {
                AC.SpeechManager sm = null;
                try { sm = AC.KickStarter.speechManager; } catch { }

                if (sm != null && sm.languages != null)
                {
                    foreach (var lang in Languages)
                    {
                        int idx = sm.languages.IndexOf(lang.Name);
                        if (idx < 0)
                        {
                            sm.languages.Add(lang.Name);
                            idx = sm.languages.Count - 1;
                            // TransferFromManager walks languageIsRightToLeft in lockstep;
                            // a short list there would desync the copy.
                            while (sm.languageIsRightToLeft != null && sm.languageIsRightToLeft.Count < sm.languages.Count)
                                sm.languageIsRightToLeft.Add(false);
                            if (sm.displayLanguages != null && sm.displayLanguages.Count > 0)
                                sm.displayLanguages.Add(lang.Name);
                            Log.LogInfo($"Registered language \"{lang.Name}\" at index {idx}.");
                        }
                        lang.AcIndex = idx;
                    }
                    RefreshRuntimeLanguages();
                    Ready = true;
                    SelfTest();
                    yield break;
                }
                yield return new WaitForSecondsRealtime(0.25f);
            }
            Log.LogWarning("SpeechManager never appeared; no language registered.");
        }

        /// <summary>RuntimeLanguages caches the manager's lists on Awake; make it re-read them.</summary>
        private static void RefreshRuntimeLanguages()
        {
            try
            {
                var rl = AC.KickStarter.runtimeLanguages;
                if (rl == null) return;
                var m = typeof(AC.RuntimeLanguages).GetMethod("TransferFromManager",
                    BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
                if (m != null) m.Invoke(rl, null);
            }
            catch (Exception e)
            {
                Log.LogWarning("Could not refresh RuntimeLanguages: " + e.Message);
            }
        }

        /// <summary>Proves the two hooks are live without needing a playthrough.</summary>
        private static void SelfTest()
        {
            try
            {
                int lang = AC.KickStarter.options != null ? AC.KickStarter.options.GetLanguage() : -1;
                string probe = AC.KickStarter.runtimeLanguages != null
                    ? AC.KickStarter.runtimeLanguages.GetTranslation("Examine", -1, lang)
                    : "(no runtimeLanguages)";
                string expected = Active.Ui.TryGetValue("Examine", out var ex) ? ex : "Examine";
                Log.LogInfo($"Self-test: Options.GetLanguage()={lang} (expected {Active.AcIndex}); "
                            + $"GetTranslation(\"Examine\") -> \"{probe}\" (expected \"{expected}\")");
            }
            catch (Exception e)
            {
                Log.LogWarning("Self-test failed: " + e.Message);
            }
        }

        /// <summary>The active language's UI translation of a source string, if any.</summary>
        internal static bool TryTranslate(string source, out string result)
        {
            result = null;
            if (string.IsNullOrEmpty(source) || !Translating) return false;
            var map = Active.Ui;
            if (map.TryGetValue(source, out result)) return true;

            // Some call sites hand over text that has already been trimmed or padded.
            var trimmed = source.Trim();
            if (trimmed.Length != source.Length && map.TryGetValue(trimmed, out var t))
            {
                int lead = source.Length - source.TrimStart().Length;
                result = source.Substring(0, lead) + t + source.Substring(source.TrimEnd().Length);
                return true;
            }
            return false;
        }

        internal static void NoteMiss(string source)
        {
            if (string.IsNullOrEmpty(source) || !Translating) return;
            // Already-translated text coming back round is not a miss.
            if (Emitted.Contains(source) || Emitted.Contains(source.Trim())) return;
            Misses++;
            Active.Missed.Add(source);
        }

        private void OnDestroy() => WriteMisses();
        private void OnApplicationQuit() => WriteMisses();

        private bool _missesWritten;
        internal void WriteMisses()
        {
            if (_missesWritten || _logMisses == null || !_logMisses.Value) return;
            _missesWritten = true;
            foreach (var lang in Languages)
            {
                var path = Path.Combine(Paths.BepInExRootPath, $"blakemanor-{lang.Code}-misses.txt");
                if (lang.Missed.Count == 0 && !File.Exists(path)) continue;
                try { WriteMisses(lang, path); }
                catch (Exception e) { Log.LogWarning($"Could not write miss log for {lang.Name}: {e.Message}"); }
            }
        }

        private static void WriteMisses(Language lang, string path)
        {
            // The file is a backlog, not a session report. One playthrough only
            // reaches a fraction of the game's UI, so overwriting it threw away
            // every string the previous sessions had found. Accumulate instead,
            // and drop anything that has since been translated so the list only
            // ever shrinks as the work lands.
            var all = new HashSet<string>(StringComparer.Ordinal);
            int carried = 0;
            if (File.Exists(path))
            {
                foreach (var line in File.ReadAllLines(path, Encoding.UTF8))
                {
                    var t = line.Trim();
                    if (t.Length == 0 || t[0] == '#') continue;
                    try
                    {
                        var prev = JsonConvert.DeserializeObject<string>(t);
                        if (!string.IsNullOrEmpty(prev) && all.Add(prev)) carried++;
                    }
                    catch { /* a hand-edited line: skip it rather than lose the file */ }
                }
            }
            int before = all.Count;
            all.UnionWith(lang.Missed);
            int added = all.Count - before;

            // Anything now covered by the patch no longer belongs in the backlog.
            int done = all.RemoveWhere(x => lang.Ui.ContainsKey(x));

            var sorted = new List<string>(all);
            sorted.Sort(StringComparer.Ordinal);
            using (var w = new StreamWriter(path, false, new UTF8Encoding(false)))
            {
                w.WriteLine($"# {lang.Name} [{lang.Code}]: untranslated UI strings still outstanding: {sorted.Count}");
                w.WriteLine($"# this session: {lang.Missed.Count} distinct seen, {added} new; "
                            + $"{carried} carried over, {done} now translated and dropped");
                w.WriteLine($"# lookups this session, all languages: {Hits} translated, {Misses} missed");
                foreach (var s in sorted) w.WriteLine(JsonConvert.ToString(s));
            }
            Log.LogInfo($"Backlog [{lang.Code}]: {sorted.Count} strings outstanding "
                        + $"(+{added} new this session, -{done} now translated) -> {path}");
        }
    }

    // ------------------------------------------------------------------- patches

    /// <summary>
    /// Report the active language as Adventure Creator's. Patched rather than set
    /// through Options.SetLanguage so the choice is never written into the player's
    /// save.
    /// </summary>
    [HarmonyPatch]
    internal static class Patch_Options_GetLanguage
    {
        // Declared on AC.AbstractOptions<OptionsData>, not on AC.Options, so the
        // attribute form of the patch cannot find it. AccessTools walks base types.
        private static MethodBase TargetMethod()
        {
            return AccessTools.Method(typeof(AC.Options), "GetLanguage")
                ?? AccessTools.Method(typeof(AC.AbstractOptions<AC.OptionsData>), "GetLanguage");
        }

        private static void Postfix(ref int __result)
        {
            if (LanguagePatch.Ready && LanguagePatch.Active.AcIndex > 0)
                __result = LanguagePatch.Active.AcIndex;
        }
    }

    /// <summary>The single funnel every AC-side string passes through.</summary>
    [HarmonyPatch(typeof(AC.RuntimeLanguages), nameof(AC.RuntimeLanguages.GetTranslation))]
    internal static class Patch_RuntimeLanguages_GetTranslation
    {
        private static bool Prefix(string originalText, ref string __result)
        {
            if (!LanguagePatch.Translating)
            {
                __result = originalText;   // English: hand the source back untouched
                return false;
            }
            if (LanguagePatch.TryTranslate(originalText, out var t))
            {
                LanguagePatch.Hits++;
                __result = t;
                return false;   // skip the original: its lineID lookup would fail anyway
            }
            LanguagePatch.NoteMiss(originalText);
            __result = originalText;
            return false;       // and skip its "translation not found" error spam
        }
    }
}
