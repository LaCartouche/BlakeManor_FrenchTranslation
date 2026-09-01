using System;
using System.Collections.Generic;
using UnityEngine;
using AC;

namespace BlakeManor.Corpus
{
    /// <summary>
    /// The non-conversation half of the corpus.
    ///
    /// Adventure Creator's own translation table (SpeechManager.lines) is EMPTY in the
    /// shipped build - the studio never ran "Gather Text" - so every lineID is -1 and
    /// the lineID-keyed door is unusable. Everything here is therefore collected and
    /// later re-injected by SOURCE STRING, through the one method all of this text
    /// funnels into: RuntimeLanguages.GetTranslation(originalText, lineID, language).
    /// </summary>
    internal static class UiDumper
    {
        private const int MaxTranslatableSlots = 16;

        public static Dictionary<string, object> Collect(Action<string> log)
        {
            var pools = new Dictionary<string, object>();

            Pool(pools, "translatableStrings", log, TranslatableStrings);
            Pool(pools, "inventoryItems",      log, InventoryItems);
            Pool(pools, "documents",           log, Documents);
            Pool(pools, "cursorIcons",         log, CursorIcons);
            Pool(pools, "menuElements",        log, MenuElements);
            Pool(pools, "variables",           log, Variables);

            return pools;
        }

        private static void Pool(Dictionary<string, object> into, string name,
                                 Action<string> log, Func<List<object>> collect)
        {
            try
            {
                var rows = collect();
                into[name] = rows;
                log(string.Format("  {0,-20} {1,5} entries", name, rows.Count));
            }
            catch (Exception e)
            {
                into[name] = new List<object>();
                log(string.Format("  {0,-20} FAILED: {1}", name, e.Message));
            }
        }

        /// <summary>The studio's own keyed UI string bag (notifications, button labels, prompts).</summary>
        private static List<object> TranslatableStrings()
        {
            var rows = new List<object>();
            var mgr = SpookyDoorway.EldritchHouse.Runtime.AC.EHKickStarter.TranslatablesManager;
            if (mgr == null || mgr.TranslatableStrings == null) return rows;
            foreach (var ts in mgr.TranslatableStrings)
            {
                if (ts == null) continue;
                rows.Add(new Dictionary<string, object>
                {
                    { "id",     ts.Id },
                    { "value",  ts.Value },
                    { "lineID", ts.LineID },
                });
            }
            return rows;
        }

        private static List<object> InventoryItems()
        {
            var rows = new List<object>();
            var im = KickStarter.inventoryManager;
            if (im == null || im.items == null) return rows;
            foreach (var it in im.items)
            {
                if (it == null) continue;
                // Item PROPERTIES carry the evidence descriptions shown on the
                // mindmap and in the journal: EHInvItem.Description reads
                // GetProperty(0) normally and GetProperty(2) once the evidence is
                // updated. Both go through GetDisplayValue -> GetTranslation.
                var props = new List<object>();
                if (it.vars != null)
                {
                    for (int i = 0; i < it.vars.Count; i++)
                    {
                        var v = it.vars[i];
                        if (v == null || string.IsNullOrEmpty(v.textVal)) continue;
                        props.Add(new Dictionary<string, object>
                        {
                            { "index",   i },
                            { "propId",  v.id },
                            { "name",    v.label },
                            { "text",    v.textVal },
                            { "lineID",  v.textValLineID },
                        });
                    }
                }

                rows.Add(new Dictionary<string, object>
                {
                    { "id",         it.id },
                    { "label",      it.label },
                    { "altLabel",   it.altLabel },
                    { "lineID",     it.lineID },
                    { "properties", props },
                });
            }
            return rows;
        }

        private static List<object> Documents()
        {
            var rows = new List<object>();
            var im = KickStarter.inventoryManager;
            if (im == null || im.documents == null) return rows;
            foreach (var d in im.documents)
            {
                if (d == null) continue;
                var pages = new List<object>();
                if (d.pages != null)
                    foreach (var p in d.pages)
                        if (p != null) pages.Add(new Dictionary<string, object> { { "text", p.text }, { "lineID", p.lineID } });
                rows.Add(new Dictionary<string, object>
                {
                    { "id",          d.ID },
                    { "title",       d.title },
                    { "titleLineID", d.titleLineID },
                    { "pages",       pages },
                });
            }
            return rows;
        }

        private static List<object> CursorIcons()
        {
            var rows = new List<object>();
            var cm = KickStarter.cursorManager;
            if (cm == null) return rows;
            if (cm.cursorIcons != null)
                foreach (var ic in cm.cursorIcons)
                    if (ic != null)
                        rows.Add(new Dictionary<string, object>
                        { { "kind", "cursorIcon" }, { "id", ic.id }, { "label", ic.label }, { "lineID", ic.lineID } });

            AddPrefix(rows, "walkPrefix",     cm.walkPrefix);
            AddPrefix(rows, "hotspotPrefix1", cm.hotspotPrefix1);
            AddPrefix(rows, "hotspotPrefix2", cm.hotspotPrefix2);
            AddPrefix(rows, "hotspotPrefix3", cm.hotspotPrefix3);
            AddPrefix(rows, "hotspotPrefix4", cm.hotspotPrefix4);
            return rows;
        }

        private static void AddPrefix(List<object> rows, string kind, HotspotPrefix p)
        {
            if (p == null || string.IsNullOrEmpty(p.label)) return;
            rows.Add(new Dictionary<string, object> { { "kind", kind }, { "label", p.label }, { "lineID", p.lineID } });
        }

        private static List<object> MenuElements()
        {
            var rows = new List<object>();
            var mm = KickStarter.menuManager;
            if (mm == null || mm.menus == null) return rows;
            foreach (var menu in mm.menus)
            {
                if (menu == null || menu.elements == null) continue;
                foreach (var el in menu.elements)
                {
                    if (el == null) continue;
                    // Every MenuElement exposes its translatable slots through ISpookyTranslatable,
                    // which avoids hand-listing MenuLabel/MenuButton/MenuToggle/... variants.
                    // AC's editor-side GetNumTranslatables() is stripped from the shipped build,
                    // so probe indices until the element stops yielding text.
                    var t = el as SpookyDoorway.Localisation.ISpookyTranslatable;
                    if (t == null) continue;
                    for (int i = 0; i < MaxTranslatableSlots; i++)
                    {
                        string text = null;
                        int lineID = -1;
                        try { text = t.GetTranslatableString(i); lineID = t.GetTranslationID(i); }
                        catch { break; }
                        if (string.IsNullOrEmpty(text)) continue;
                        rows.Add(new Dictionary<string, object>
                        {
                            { "menu",    menu.title },
                            { "element", el.title },
                            { "index",   i },
                            { "text",    text },
                            { "lineID",  lineID },
                        });
                    }
                }
            }
            return rows;
        }

        private static List<object> Variables()
        {
            var rows = new List<object>();
            var vm = KickStarter.variablesManager;
            if (vm == null || vm.vars == null) return rows;
            foreach (var v in vm.vars)
            {
                if (v == null) continue;
                // Only PopUp variables carry player-visible text.
                string popups = null;
                try { popups = v.GetPopUpsString(); } catch { }
                if (string.IsNullOrEmpty(popups)) continue;
                rows.Add(new Dictionary<string, object>
                {
                    { "id",     v.id },
                    { "label",  v.label },
                    { "popups", popups },
                    { "lineID", v.popUpsLineID },
                });
            }
            return rows;
        }
    }
}
