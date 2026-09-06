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

namespace BlakeManor.FR
{
    /// <summary>
    /// Phase 3, UI layer.
    ///
    /// Adventure Creator's translation table is empty in the shipped build, so every
    /// lineID is -1 and the usual lineID-keyed route is dead. Instead this hooks the
    /// one method all AC-side text funnels through and substitutes by source string:
    ///
    ///     RuntimeLanguages.GetTranslation(originalText, lineID, language)
    ///
    /// Many call sites skip that method entirely when the active language index is 0
    /// (see Hotspot.GetName), so a real language is registered on SpeechManager and
    /// Options.GetLanguage() is made to report it.
    ///
    /// Conversation subtitles are NOT handled here - those go through the Dialogue
    /// System's own localisation path and are a separate layer.
    ///
    /// The whole thing can be switched off and on again while the game runs: see
    /// SetFrench, and LanguageOption for the row it adds to the options screen.
    /// </summary>
    [BepInPlugin(Guid, "Blake Manor — Traduction française", "1.0.0")]
    public class FrenchPatch : BaseUnityPlugin
    {
        public const string Guid = "fr.blakemanor.frenchpatch";
        public const string LanguageName = "Français";

        internal static ManualLogSource Log;
        /// <summary>The running plugin, so the conversation layer can start coroutines
        /// after its initial pass (see DialogueLines.Watchdog).</summary>
        internal static FrenchPatch Instance;
        internal static readonly Dictionary<string, string> Map = new Dictionary<string, string>(StringComparer.Ordinal);
        /// <summary>Every French string we hand back. The game re-queries some of them,
        /// and logging our own output as "untranslated" would drown the QA signal.</summary>
        private static readonly HashSet<string> Emitted = new HashSet<string>(StringComparer.Ordinal);
        internal static int LanguageIndex = -1;
        internal static bool Ready;

        internal static long Hits, Misses;
        private static readonly HashSet<string> MissedTexts = new HashSet<string>(StringComparer.Ordinal);

        private ConfigEntry<bool> _logMisses;
        private ConfigEntry<string> _language;
        private ConfigEntry<bool> _selfTestSwitch, _quitAfterSelfTest;
        private string _dataDir;

        /// <summary>True while the French layer is on. Flipped at runtime from the
        /// options menu (LanguageOption) and persisted in the BepInEx config — never in
        /// the game's own options file, see LanguageOption for why.</summary>
        internal static bool French = true;

        private void Awake()
        {
            Instance = this;
            Log = Logger;
            _logMisses = Config.Bind("QA", "LogMisses", true,
                "Record every string that passed through untranslated, to BepInEx/blakemanor-fr-misses.txt. "
                + "This is how the remaining untranslated UI gets found.");

            _language = Config.Bind("Language", "Active", "fr",
                "Language shown in game: \"fr\" for the French patch, \"en\" for the original English. "
                + "Changed in game from Options > Interface > Language. Kept here rather than in the game's "
                + "own options file so that removing the patch leaves nothing behind.");
            French = !string.Equals(_language.Value, "en", StringComparison.OrdinalIgnoreCase);
            _selfTestSwitch = Config.Bind("QA", "SelfTestSwitch", false,
                "At startup, once every layer is applied, switch to the other language and back, logging "
                + "what each layer resolves to in each state. Leaves the language as configured.");
            _quitAfterSelfTest = Config.Bind("QA", "QuitAfterSelfTest", false,
                "Quit the game once SelfTestSwitch has finished.");

            _dataDir = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) ?? ".", "BlakeManorFR");

            int loaded = LoadLayer(Path.Combine(_dataDir, "ui.json"));
            int fields = DialogueFields.Load(Path.Combine(_dataDir, "fields.json"));
            int lines = DialogueLines.Load(Path.Combine(_dataDir, "dialogue.json"));
            // The switch's own values read the same in both languages and must never be
            // reported as untranslated.
            Emitted.Add(LanguageOption.ValueEn);
            Emitted.Add(LanguageOption.ValueFr);
            if (loaded == 0 && fields == 0 && lines == 0)
            {
                Log.LogWarning("No translations loaded — the patch will do nothing. Expected " + Path.Combine(_dataDir, "ui.json"));
                return;
            }

            var harmony = new Harmony(Guid);
            int applied = 0;
            applied += TryPatch(harmony, typeof(Patch_Options_GetLanguage));
            applied += TryPatch(harmony, typeof(Patch_RuntimeLanguages_GetTranslation));
            applied += TryPatch(harmony, typeof(LanguageOption.Patch_OptionsMenu_OnEnable));
            Log.LogInfo($"{applied}/3 patches applied, {loaded} UI strings, {fields} item fields "
                        + $"and {lines} dialogue lines loaded. Language: {(French ? "Français" : "English")}.");
            StartCoroutine(RegisterLanguage());
            if (fields > 0) StartCoroutine(DialogueFields.Apply()); else DialogueFields.Done = true;
            if (lines > 0) StartCoroutine(DialogueLines.Apply()); else DialogueLines.Done = true;
            if (_selfTestSwitch.Value) StartCoroutine(SelfTestSwitch());

            var shotAfter = Environment.GetEnvironmentVariable("BLAKE_FR_SHOT_AFTER");
            if (!string.IsNullOrEmpty(shotAfter) && float.TryParse(shotAfter, out var delay))
                StartCoroutine(CaptureScreenshot(delay));
        }

        // ------------------------------------------------------------- switching

        /// <summary>
        /// Flip every layer between French and English while the game runs. Called from
        /// the options-menu row (LanguageOption) and from the startup self-test.
        /// </summary>
        internal static void SetFrench(bool on, string reason)
        {
            French = on;
            try
            {
                if (Instance != null && Instance._language != null)
                {
                    Instance._language.Value = on ? "fr" : "en";
                    Instance.Config.Save();
                }
            }
            catch (Exception e) { Log.LogWarning("Could not save the language choice: " + e.Message); }

            int swapped = DialogueFields.SetFrench(on);
            DialogueLines.SetFrench(on);

            // Every TranslatableTMPText listens to this and re-runs GetTranslation — our
            // hook — so the whole interface re-labels itself in one pass.
            try
            {
                var em = AC.KickStarter.eventManager;
                if (em != null) em.Call_OnChangeLanguage(on ? LanguageIndex : 0);
            }
            catch (Exception e) { Log.LogWarning("Could not raise OnChangeLanguage: " + e.Message); }

            LanguageOption.AfterSwitch();
            Log.LogInfo($"Language -> {(on ? "Français" : "English")} ({reason}); {swapped} item/actor fields swapped. " + Probe());
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

            bool start = French;
            Log.LogInfo("Self-test switch [1/3] as configured: " + Probe());
            LanguageOption.ProbeMenu();
            SetFrench(!start, "self-test");
            yield return new WaitForSecondsRealtime(2f);
            Log.LogInfo("Self-test switch [2/3] flipped: " + Probe());
            SetFrench(start, "self-test");
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
                path = Path.Combine(Paths.BepInExRootPath, "blakemanor-fr-shot.png");
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

        /// <summary>Reads one translation layer. Layers merge; later files win.</summary>
        private int LoadLayer(string path)
        {
            if (!File.Exists(path)) return 0;
            try
            {
                var doc = JsonConvert.DeserializeObject<Layer>(File.ReadAllText(path, Encoding.UTF8));
                if (doc?.bySource == null) return 0;
                foreach (var kv in doc.bySource)
                {
                    if (string.IsNullOrEmpty(kv.Key)) continue;
                    Map[kv.Key] = kv.Value;
                    if (!string.IsNullOrEmpty(kv.Value)) Emitted.Add(kv.Value);
                }
                return doc.bySource.Count;
            }
            catch (Exception e)
            {
                Log.LogError($"Could not read {path}: {e.Message}");
                return 0;
            }
        }

        private class Layer
        {
            public Dictionary<string, string> bySource { get; set; }
        }

        /// <summary>
        /// Adds "Français" to the SpeechManager so language counts and name lookups stay
        /// consistent, then makes RuntimeLanguages re-copy the manager's lists.
        /// </summary>
        private IEnumerator RegisterLanguage()
        {
            float deadline = Time.realtimeSinceStartup + 120f;
            while (Time.realtimeSinceStartup < deadline)
            {
                AC.SpeechManager sm = null;
                try { sm = AC.KickStarter.speechManager; } catch { }

                if (sm != null && sm.languages != null)
                {
                    int idx = sm.languages.IndexOf(LanguageName);
                    if (idx < 0)
                    {
                        sm.languages.Add(LanguageName);
                        idx = sm.languages.Count - 1;
                        // TransferFromManager walks languageIsRightToLeft in lockstep;
                        // a short list there would desync the copy.
                        while (sm.languageIsRightToLeft != null && sm.languageIsRightToLeft.Count < sm.languages.Count)
                            sm.languageIsRightToLeft.Add(false);
                        if (sm.displayLanguages != null && sm.displayLanguages.Count > 0)
                            sm.displayLanguages.Add(LanguageName);
                        Log.LogInfo($"Registered language \"{LanguageName}\" at index {idx}.");
                    }

                    LanguageIndex = idx;
                    RefreshRuntimeLanguages();
                    Ready = true;
                    SelfTest();
                    yield break;
                }
                yield return new WaitForSecondsRealtime(0.25f);
            }
            Log.LogWarning("SpeechManager never appeared; French not registered.");
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
                Log.LogInfo($"Self-test: Options.GetLanguage()={lang} (expected {(French ? LanguageIndex : 0)}); "
                            + $"GetTranslation(\"Examine\") -> \"{probe}\" (expected \"{(French ? "Examiner" : "Examine")}\")");
            }
            catch (Exception e)
            {
                Log.LogWarning("Self-test failed: " + e.Message);
            }
        }

        internal static bool TryTranslate(string source, out string result)
        {
            result = null;
            if (string.IsNullOrEmpty(source)) return false;

            if (Map.TryGetValue(source, out result)) return true;

            // Some call sites hand over text that has already been trimmed or padded.
            var trimmed = source.Trim();
            if (trimmed.Length != source.Length && Map.TryGetValue(trimmed, out var fr))
            {
                int lead = source.Length - source.TrimStart().Length;
                result = source.Substring(0, lead) + fr + source.Substring(source.TrimEnd().Length);
                return true;
            }
            return false;
        }

        internal static void NoteMiss(string source)
        {
            if (string.IsNullOrEmpty(source)) return;
            // Already-translated text coming back round is not a miss.
            if (Emitted.Contains(source) || Emitted.Contains(source.Trim())) return;
            Misses++;
            MissedTexts.Add(source);
        }

        private void OnDestroy() => WriteMisses();
        private void OnApplicationQuit() => WriteMisses();

        private bool _missesWritten;
        internal void WriteMisses()
        {
            if (_missesWritten || _logMisses == null || !_logMisses.Value) return;
            _missesWritten = true;
            try
            {
                var path = Path.Combine(Paths.BepInExRootPath, "blakemanor-fr-misses.txt");

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
                all.UnionWith(MissedTexts);
                int added = all.Count - before;

                // Anything now covered by the patch no longer belongs in the backlog.
                int done = all.RemoveWhere(x => Map.ContainsKey(x));

                var sorted = new List<string>(all);
                sorted.Sort(StringComparer.Ordinal);
                using (var w = new StreamWriter(path, false, new UTF8Encoding(false)))
                {
                    w.WriteLine($"# untranslated UI strings still outstanding: {sorted.Count}");
                    w.WriteLine($"# this session: {MissedTexts.Count} distinct seen, {added} new; "
                                + $"{carried} carried over, {done} now translated and dropped");
                    w.WriteLine($"# lookups this session: {Hits} translated, {Misses} missed");
                    foreach (var s in sorted) w.WriteLine(JsonConvert.ToString(s));
                }
                Log.LogInfo($"Backlog: {sorted.Count} strings outstanding "
                            + $"(+{added} new this session, -{done} now translated) -> {path}");
            }
            catch (Exception e)
            {
                Log.LogWarning("Could not write miss log: " + e.Message);
            }
        }
    }

    // ------------------------------------------------------------------- patches

    /// <summary>
    /// Report French as the active language. Patched rather than set through
    /// Options.SetLanguage so the choice is never written into the player's save.
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
            if (FrenchPatch.Ready && FrenchPatch.French && FrenchPatch.LanguageIndex > 0)
                __result = FrenchPatch.LanguageIndex;
        }
    }

    /// <summary>The single funnel every AC-side string passes through.</summary>
    [HarmonyPatch(typeof(AC.RuntimeLanguages), nameof(AC.RuntimeLanguages.GetTranslation))]
    internal static class Patch_RuntimeLanguages_GetTranslation
    {
        private static bool Prefix(string originalText, ref string __result)
        {
            if (!FrenchPatch.French)
            {
                __result = originalText;   // English: hand the source back untouched
                return false;
            }
            if (FrenchPatch.TryTranslate(originalText, out var fr))
            {
                FrenchPatch.Hits++;
                __result = fr;
                return false;   // skip the original: its lineID lookup would fail anyway
            }
            FrenchPatch.NoteMiss(originalText);
            __result = originalText;
            return false;       // and skip its "translation not found" error spam
        }
    }
}
