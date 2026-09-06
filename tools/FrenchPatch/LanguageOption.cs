using System;
using System.Collections.Generic;
using System.Reflection;
using System.Text;
using AC;
using HarmonyLib;
using SpookyDoorway.EldritchHouse.Runtime.AC;
using SpookyDoorway.EldritchHouse.Runtime.AC.UI;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace BlakeManor.FR
{
    /// <summary>
    /// The in-game switch: one extra row in the options screen, "Language",
    /// cycling Français / English.
    ///
    /// The options screen (EHOptionsMenu) is assembled from prefabs: each tab is an
    /// OptionsTabContent holding OptionEntry rows, and what a row does is chosen by
    /// a closed enum (OptionToChange) that has no notion of language. Rather than
    /// teach the menu a new option, this copies an existing two-state row — same
    /// widget, same sprites, same sounds — re-labels it and points its left/right
    /// event at FrenchPatch.SetFrench. The copy is deliberately NOT added to the
    /// tab's OptionEntries, so the menu's own code (reset to defaults, analytics,
    /// listener cleanup) never sees it.
    ///
    /// The choice is persisted in the BepInEx config, never through
    /// Options.SetLanguage. That would write a language index into the game's own
    /// options file, and the shipped build carries a placeholder French ("TBT: …"
    /// on every line) at an index of its own: remove the patch with that index
    /// saved and the player gets the placeholder.
    /// </summary>
    internal static class LanguageOption
    {
        internal const string LabelEn = "Language";
        internal const string TooltipEn = "Choose the language of the interface and dialogue. Takes effect immediately.";
        internal const string ValueFr = "Français";
        internal const string ValueEn = "English";

        private const string RowName = "BlakeManorFR_Language";

        /// <summary>One row per options screen. The game keeps two screens alive —
        /// the main menu's and the pause menu's variant — so this is a list.</summary>
        private class Entry
        {
            public EHOptionsMenu menu;
            public GameObject row;
            public TextMeshProUGUI value, name;
        }

        private static readonly List<Entry> _entries = new List<Entry>();
        private static bool _describedOnce;

        /// <summary>Runs after the menu's own OnEnable, so its tabs and entries exist.</summary>
        [HarmonyPatch]
        internal static class Patch_OptionsMenu_OnEnable
        {
            private static MethodBase TargetMethod() => AccessTools.Method(typeof(EHOptionsMenu), "OnEnable");

            private static void Postfix(EHOptionsMenu __instance)
            {
                try { Inject(__instance); }
                catch (Exception e) { FrenchPatch.Log.LogWarning("Language option could not be added: " + e); }
            }
        }

        // Two-state rows, in order of preference. The first lives in the Interface tab.
        private static readonly EHOptionsMenu.OptionToChange[] Preferred =
        {
            EHOptionsMenu.OptionToChange.DialogueTextSize,
            EHOptionsMenu.OptionToChange.MenuTextSize,
            EHOptionsMenu.OptionToChange.TextScrollSpeed,
        };

        internal static void Inject(EHOptionsMenu menu)
        {
            if (menu == null) return;
            _entries.RemoveAll(e => e.menu == null || e.row == null);   // Unity null: destroyed screens
            var existing = _entries.Find(e => ReferenceEquals(e.menu, menu));
            if (existing != null)
            {
                Refresh(existing);
                return;
            }

            var tabs = AccessTools.Field(typeof(EHOptionsMenu), "tabs")?.GetValue(menu) as OptionsTabContent[];
            if (tabs == null || tabs.Length == 0)
            {
                FrenchPatch.Log.LogWarning("Language option: the options menu has no tabs to add to.");
                return;
            }

            var template = FindTemplate(tabs, out var tab);
            if (template == null)
            {
                FrenchPatch.Log.LogWarning("Language option: no option row found to copy.");
                return;
            }

            var row = RowOf(template, tab);
            if (!_describedOnce)
            {
                _describedOnce = true;
                FrenchPatch.Log.LogInfo(Describe(row, template));
            }

            // Never two rows in one screen, even if our bookkeeping was lost.
            var previous = row.parent != null ? row.parent.Find(RowName) : null;
            if (previous != null) UnityEngine.Object.Destroy(previous.gameObject);

            var clone = UnityEngine.Object.Instantiate(row.gameObject, row.parent);
            clone.name = RowName;
            clone.transform.SetSiblingIndex(row.GetSiblingIndex() + 1);

            var option = clone.GetComponentInChildren<SDSelectableOption>(true);
            if (option == null)
            {
                UnityEngine.Object.Destroy(clone);
                FrenchPatch.Log.LogWarning("Language option: the copied row has no SDSelectableOption; removed it again.");
                return;
            }

            // The value label is whatever SetLabel writes to. The name label is any
            // other text in the row, preferring one the game re-translates itself.
            var value = AccessTools.Field(typeof(SDSelectableOption), "labelTextMesh")?.GetValue(option) as TextMeshProUGUI;
            TextMeshProUGUI name = null;
            foreach (var tmp in clone.GetComponentsInChildren<TextMeshProUGUI>(true))
            {
                if (tmp == value) continue;
                if (name == null || (tmp is TranslatableTMPText && !(name is TranslatableTMPText))) name = tmp;
            }

            foreach (var r in clone.GetComponentsInChildren<OptionRenamerPerPlatform>(true))
                UnityEngine.Object.Destroy(r);
            // The row carries an AC ConstantID; two objects with one ID is something AC
            // warns about, and the menu row has no state worth remembering.
            foreach (var c in clone.GetComponentsInChildren<ConstantID>(true))
                UnityEngine.Object.Destroy(c);
            foreach (var t in clone.GetComponentsInChildren<SDSelectableTooltip>(true))
            {
                t.lineID = -1;
                t.SetTooltip(TooltipEn);
            }

            // Replace rather than clear: RemoveAllListeners leaves the serialised ones.
            option.changeAction = new UnityEvent<bool>();
            option.changeAction.AddListener(OnMove);

            WireNavigation(template.optionSelectable, option);

            var entry = new Entry { menu = menu, row = clone, value = value, name = name };
            _entries.Add(entry);
            Refresh(entry);

            FrenchPatch.Log.LogInfo(
                $"Language option added to tab \"{tab.gameObject.name}\", copied from the {template.optionToChange} row"
                + (name == null ? " (no label found to rename)" : "")
                + (value == null ? " (no value label found)" : "") + ".");
        }

        private static EHOptionsMenu.OptionEntry FindTemplate(OptionsTabContent[] tabs, out OptionsTabContent tab)
        {
            foreach (var want in Preferred)
                foreach (var t in tabs)
                {
                    if (t == null || t.OptionEntries == null) continue;
                    foreach (var e in t.OptionEntries)
                        if (e != null && e.optionSelectable != null && e.optionToChange == want)
                        {
                            tab = t;
                            return e;
                        }
                }
            foreach (var t in tabs)
            {
                if (t == null || t.OptionEntries == null) continue;
                foreach (var e in t.OptionEntries)
                    if (e != null && e.optionSelectable != null)
                    {
                        tab = t;
                        return e;
                    }
            }
            tab = null;
            return null;
        }

        /// <summary>
        /// The object to copy: the ancestor of the entry's selectable that sits directly
        /// under the container it shares with the nearest other row of the same tab.
        /// Falls back to the first ancestor under a layout group, then to the selectable.
        /// </summary>
        private static Transform RowOf(EHOptionsMenu.OptionEntry entry, OptionsTabContent tab)
        {
            var self = entry.optionSelectable.transform;
            Transform best = null;
            int bestDepth = -1;
            foreach (var other in tab.OptionEntries)
            {
                if (other == null || other == entry || other.optionSelectable == null) continue;
                var lca = LowestCommonAncestor(self, other.optionSelectable.transform);
                if (lca == null) continue;
                int depth = Depth(lca);
                if (depth <= bestDepth) continue;
                var t = self;
                while (t.parent != null && t.parent != lca) t = t.parent;
                if (t.parent == lca)
                {
                    best = t;
                    bestDepth = depth;
                }
            }
            if (best != null) return best;

            for (var t = self; t != null && t != tab.transform; t = t.parent)
                if (t.parent != null && t.parent.GetComponent<LayoutGroup>() != null) return t;
            return self;
        }

        private static int Depth(Transform t)
        {
            int d = 0;
            while (t.parent != null) { d++; t = t.parent; }
            return d;
        }

        private static Transform LowestCommonAncestor(Transform a, Transform b)
        {
            var seen = new HashSet<Transform>();
            for (var t = a.parent; t != null; t = t.parent) seen.Add(t);
            for (var t = b.parent; t != null; t = t.parent) if (seen.Contains(t)) return t;
            return null;
        }

        /// <summary>Keyboard and pad: if the rows are linked explicitly, link ours in
        /// under the template. Automatic navigation finds it by position anyway.</summary>
        private static void WireNavigation(SDSelectableOption src, SDSelectableOption dst)
        {
            var a = src.GetComponent<Selectable>();
            if (a == null) a = src.GetComponentInChildren<Selectable>(true);
            var b = dst.GetComponent<Selectable>();
            if (b == null) b = dst.GetComponentInChildren<Selectable>(true);
            if (a == null || b == null) return;

            var na = a.navigation;
            if (na.mode != Navigation.Mode.Explicit) return;
            var after = na.selectOnDown;
            na.selectOnDown = b;
            a.navigation = na;

            var nb = b.navigation;
            nb.mode = Navigation.Mode.Explicit;
            nb.selectOnUp = a;
            nb.selectOnDown = after;
            b.navigation = nb;

            if (after != null && after != b)
            {
                var nc = after.navigation;
                nc.selectOnUp = b;
                after.navigation = nc;
            }
        }

        private static void OnMove(bool right)
        {
            FrenchPatch.SetFrench(!FrenchPatch.French, "options menu");
        }

        /// <summary>Re-label one row for the current language.</summary>
        private static void Refresh(Entry e)
        {
            if (e.name != null) SetText(e.name, LabelEn, translate: true);
            if (e.value != null) SetText(e.value, FrenchPatch.French ? ValueFr : ValueEn, translate: false);
        }

        private static void SetText(TextMeshProUGUI tmp, string source, bool translate)
        {
            if (tmp is TranslatableTMPText tr)
            {
                // Until its Awake runs, a translatable takes whatever text it finds as
                // the original; after that, SetOriginalText is the only way in.
                if (tmp.gameObject.activeInHierarchy) tr.SetOriginalText(source);
                else tmp.text = source;
                return;
            }
            tmp.text = translate && FrenchPatch.French && FrenchPatch.TryTranslate(source, out var fr) ? fr : source;
        }

        /// <summary>
        /// After a language change. The menu's own rows print their values through
        /// SetLabel, which OnChangeLanguage does not refresh, so run the menu's updater
        /// over them, then re-label our row.
        /// </summary>
        internal static void AfterSwitch()
        {
            _entries.RemoveAll(e => e.menu == null || e.row == null);
            var update = AccessTools.Method(typeof(EHOptionsMenu), "UpdateOptionEntry");
            var field = AccessTools.Field(typeof(EHOptionsMenu), "_optionEntries");
            foreach (var entry in _entries)
            {
                try
                {
                    if (entry.menu.isActiveAndEnabled && update != null && field != null
                        && field.GetValue(entry.menu) is List<EHOptionsMenu.OptionEntry> rows)
                        foreach (var r in rows)
                            if (r != null && r.optionSelectable != null)
                                update.Invoke(entry.menu, new object[] { r, false, false });
                }
                catch (Exception e)
                {
                    FrenchPatch.Log.LogWarning("Could not refresh the options menu after the switch: " + e.Message);
                }
                Refresh(entry);
            }
        }

        /// <summary>QA: add the row to any options menu already instantiated, without
        /// waiting for it to open, so the log shows the layout it was copied from.</summary>
        internal static void ProbeMenu()
        {
            int found = 0;
            foreach (var m in Resources.FindObjectsOfTypeAll<EHOptionsMenu>())
            {
                if (m == null || !m.gameObject.scene.IsValid()) continue;   // prefab assets: leave alone
                found++;
                FrenchPatch.Log.LogInfo($"Options menu instance: {Path(m.transform)} (active: {m.gameObject.activeInHierarchy})");
                try { Inject(m); }
                catch (Exception e) { FrenchPatch.Log.LogWarning("Language option (probe): " + e); }
            }
            if (found == 0)
                FrenchPatch.Log.LogInfo("No options menu instance exists yet; the language row is added when the menu first opens.");
        }

        private static string Describe(Transform row, EHOptionsMenu.OptionEntry template)
        {
            var sb = new StringBuilder("Option row copied for the language switch, at ");
            sb.Append(Path(row)).Append(":\n");
            Walk(row, 0, sb, template.optionSelectable.transform);
            return sb.ToString().TrimEnd();
        }

        private static void Walk(Transform t, int depth, StringBuilder sb, Transform mark)
        {
            sb.Append(' ', depth * 2).Append(t.name);
            if (t == mark) sb.Append("  <- the entry's SDSelectableOption");
            sb.Append("  [");
            bool first = true;
            foreach (var c in t.GetComponents<Component>())
            {
                if (c == null || c is Transform) continue;
                if (!first) sb.Append(", ");
                first = false;
                sb.Append(c.GetType().Name);
                if (c is TMP_Text tmp) sb.Append(" \"").Append(Cut(tmp.text)).Append('"');
                if (c is Selectable s) sb.Append(" nav=").Append(s.navigation.mode);
            }
            sb.Append("]\n");
            if (depth < 6)
                for (int i = 0; i < t.childCount; i++) Walk(t.GetChild(i), depth + 1, sb, mark);
        }

        private static string Path(Transform t)
        {
            var parts = new List<string>();
            for (; t != null; t = t.parent) parts.Add(t.name);
            parts.Reverse();
            return string.Join("/", parts);
        }

        private static string Cut(string s)
        {
            if (string.IsNullOrEmpty(s)) return "";
            s = s.Replace("\n", " ");
            return s.Length > 40 ? s.Substring(0, 40) + "…" : s;
        }
    }
}
