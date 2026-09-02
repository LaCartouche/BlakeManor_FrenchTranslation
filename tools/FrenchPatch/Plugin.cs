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
    /// </summary>
    [BepInPlugin(Guid, "Blake Manor — Traduction française", "0.1.0")]
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
        private string _dataDir;

        private void Awake()
        {
            Instance = this;
            Log = Logger;
            _logMisses = Config.Bind("QA", "LogMisses", true,
                "Record every string that passed through untranslated, to BepInEx/blakemanor-fr-misses.txt. "
                + "This is how the remaining untranslated UI gets found.");

            _dataDir = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) ?? ".", "BlakeManorFR");

            int loaded = LoadLayer(Path.Combine(_dataDir, "ui.json"));
            int fields = DialogueFields.Load(Path.Combine(_dataDir, "fields.json"));
            int lines = DialogueLines.Load(Path.Combine(_dataDir, "dialogue.json"));
            if (loaded == 0 && fields == 0 && lines == 0)
            {
                Log.LogWarning("No translations loaded — the patch will do nothing. Expected " + Path.Combine(_dataDir, "ui.json"));
                return;
            }

            var harmony = new Harmony(Guid);
            int applied = 0;
            applied += TryPatch(harmony, typeof(Patch_Options_GetLanguage));
            applied += TryPatch(harmony, typeof(Patch_RuntimeLanguages_GetTranslation));
            Log.LogInfo($"{applied}/2 patches applied, {loaded} UI strings, {fields} item fields "
                        + $"and {lines} dialogue lines loaded.");
            StartCoroutine(RegisterLanguage());
            if (fields > 0) StartCoroutine(DialogueFields.Apply());
            if (lines > 0) StartCoroutine(DialogueLines.Apply());

            var shotAfter = Environment.GetEnvironmentVariable("BLAKE_FR_SHOT_AFTER");
            if (!string.IsNullOrEmpty(shotAfter) && float.TryParse(shotAfter, out var delay))
                StartCoroutine(CaptureScreenshot(delay));
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
                Log.LogInfo($"Self-test: Options.GetLanguage()={lang} (expected {LanguageIndex}); "
                            + $"GetTranslation(\"Examine\") -> \"{probe}\" (expected \"Examiner\")");
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
                var sorted = new List<string>(MissedTexts);
                sorted.Sort(StringComparer.Ordinal);
                using (var w = new StreamWriter(path, false, new UTF8Encoding(false)))
                {
                    w.WriteLine($"# untranslated strings seen this session: {sorted.Count}");
                    w.WriteLine($"# translated lookups: {Hits}, untranslated lookups: {Misses}");
                    foreach (var s in sorted) w.WriteLine(JsonConvert.ToString(s));
                }
                Log.LogInfo($"Translated {Hits} lookups, {Misses} missed ({sorted.Count} distinct) -> {path}");
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
            if (FrenchPatch.Ready && FrenchPatch.LanguageIndex > 0)
                __result = FrenchPatch.LanguageIndex;
        }
    }

    /// <summary>The single funnel every AC-side string passes through.</summary>
    [HarmonyPatch(typeof(AC.RuntimeLanguages), nameof(AC.RuntimeLanguages.GetTranslation))]
    internal static class Patch_RuntimeLanguages_GetTranslation
    {
        private static bool Prefix(string originalText, ref string __result)
        {
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
