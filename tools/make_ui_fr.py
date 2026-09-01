#!/usr/bin/env python3
"""
Build corpus/fr/ui.json — the French UI layer.

Translations are written here against STABLE IDS (the studio's TranslatableString
ids, or the English label for AC cursors and menu elements), never against the raw
source string. The exact source strings are then read back out of the dump, so
leading/trailing whitespace, \\r, \\n and {0} placeholders are reproduced byte-exact:
several of these strings are concatenated at runtime and the spacing is load-bearing.

Output is keyed BY SOURCE STRING, because that is how Phase 3 injects it —
AC funnels all of this text through RuntimeLanguages.GetTranslation(originalText, …),
and the shipped build has no usable lineIDs.
"""
import json
import pathlib
import sys

from fr_evidence import EVIDENCE
from fr_typography import normalise
from fr_hypotheses import TOKENS
from fr_descriptions import DESCRIPTIONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOLS = ROOT / "corpus" / "en" / "pools.json"
OUT = ROOT / "corpus" / "fr" / "ui.json"

# --------------------------------------------------------------- studio UI strings
# Keyed by TranslatableString.Id. Whitespace is handled automatically; write the
# French for the trimmed text only.
STUDIO = {
    # -- deduction / mindmap vocabulary (see docs/STYLE.md §5) -------------------
    "act": "Agir",
    "actNodeToDoList": "Agir",
    "actConnection": "J’ai fait ici tout ce que je pouvais.",
    "actPotentialConnection": "Il reste à faire pour conclure ce mystère.",
    "actionUnlocked": "Action débloquée",
    "conclusion": "Conclusion",
    "conclusionConnection": "J’ai résolu ce mystère !",
    "confront": "Confronter",
    "confrontNodeToDoList": "Confronter",
    "confrontConnection": "Je l’ai confronté à ses intentions.",
    "confrontDesc": "Il me faut le trouver et le confronter à mon hypothèse !",
    "confrontPotentialConnection": "J’ai formulé une hypothèse ; je devrais l’y confronter.",
    "confrontUnlocked": "Confrontation débloquée",
    "connection": "Lien",
    "inconclusiveConnection": "Lien non concluant",
    "potentialConnection": "Lien possible",
    "verifiedFalseConnection": "Lien vérifié : faux",
    "verifiedTrueConnection": "Lien vérifié : vrai",
    "hypothesisConnection": "J’ai compris ce qui se trame.",
    "hypothesisPotentialConnection": "Je devrais avoir assez de preuves pour comprendre ce qui se trame.",
    "hypothesisUnlocked": "Hypothèse débloquée",
    "mystery": "Mystère",
    "mysterySolved": "MYSTÈRE RÉSOLU",
    "mysteryUnlocked": "Mystère débloqué",
    "task": "Tâche",
    "think": "Réfléchir",
    "thinkNodeToDoList": "Réfléchir : formuler une hypothèse",
    "person": "Personne",
    "unknown": "Inconnu",
    "dialScreenUnknown": "Inconnu",
    "outcomeChanged": "DÉNOUEMENT MODIFIÉ",
    "hypothesisConfirmed": "HYPOTHÈSE CONFIRMÉE",

    # -- person status banners --------------------------------------------------
    "culpritPerson": "<color=#dc0000>LE COUPABLE, EN FIN DE COMPTE.</color>",
    "deadPerson": "<color=#dc0000>CETTE PERSONNE N’A PAS SURVÉCU À LA SÉANCE !</color>",
    "eliminatedPerson": "<color=#d3991e>VOUS PRESSENTEZ QUE CETTE PERSONNE N’EST PAS LE COUPABLE !</color>",
    "eliminationAttemptedPerson": "<color=#dc0000>RIEN À VOIR AVEC LA DISPARITION DE MLLE DEANE !</color>",
    "missingPerson": "<color=#dc0000>CETTE PERSONNE A DISPARU !</color>",
    "mysteryStillLockedPerson": "<color=#777777>VOUS N’AVEZ PAS RENCONTRÉ CETTE PERSONNE.</color>",

    # -- evidence & lore filters (short: these sit in fixed-width tabs) ----------
    "filterEverything": "Tout",
    "evidenceFilterAnalysis": "Analyse",
    "evidenceFilterConclusion": "Conclusion",
    "evidenceFilterDocuments": "Documents",
    "evidenceFilterEvidence": "Preuves",
    "evidenceFilterItems": "Objets",
    "evidenceFilterKeys": "Clés",
    "evidenceFilterLearned": "Acquis",
    "evidenceFilterObservation": "Observation",
    "evidenceFilterPeople": "Personnes",
    "evidenceFilterSigils": "Sceaux",
    "loreFilterGuests": "Invités",
    "loreFilterLocations": "Lieux",
    "loreFilterStaff": "Personnel",

    # -- dialogue actions -------------------------------------------------------
    "dialogueAnalyse": "<b>ANALYSER</b>",
    "dialogueDiscussEvidence": "<b>ÉVOQUER UNE PREUVE</b>",
    "dialogueFormHypothesis": "<b>FORMULER UNE HYPOTHÈSE</b>",

    # -- calls to action --------------------------------------------------------
    "hypothesisCTASentence": "Hypothèse « {0} ».",
    "confrontCTASentence": "Confronter {0}.",
    "actCTASentence": "Agir sur {0}.",
    "extraCTASentence": "<color=#b17e0f>{0}</color> action(s) supplémentaire(s) dans la  <color=#b17e0f>Carte mentale</color>.",

    # -- endgame ----------------------------------------------------------------
    "failStateQuestsCompleted": "Vous aviez résolu <color=#D3991E>{0}</color> des mystères du manoir.",
    "failStatePeopleSaved": "Grâce à vos actions, <color=#D3991E>{0}</color> des personnes présentes au manoir ont survécu.",
    "failStateHours": "Il restait <color=#D3991E>{0} heures</color> avant la Séance.",
    "epiloguePeopleSaved": "Le détective Ward a sauvé <color=#D3991E>{0}</color> personnes.",
    "epilogueQuestsCompleted": "<color=#D3991E>{0}</color> mystères résolus.",
    "pointOfNoReturn_stateOfThings": "<color=#D3991E>{0} personnes</color> n’assisteront pas à la Séance.<br>Il ne reste que <color=#D3991E>{1} heures</color> avant la Séance.",

    # -- notifications ----------------------------------------------------------
    "opinionUpdatedNotificationPart1": "L’opinion de {0} sur",
    "opinionUpdatedNotificationPart2": "{0} a changé",
    "notification_multi_evidenceGained": "{0} preuves obtenues",
    "notification_multi_evidenceFiled": "{0} preuves classées",
    "notification_multi_leadAdded": "{0} pistes obtenues",
    "notification_multi_factsUncovered": "{0} faits découverts",
    "notification_multi_timelineUpdated": "{0} mises à jour de la chronologie",
    "notification_multi_libraryTopicsUnlocked": "{0} sujets de bibliothèque débloqués",
    "notification_multi_researchTopicsUnlocked": "{0} sujets de recherche débloqués",
    "notification_multi_discussionsUnlocked": "{0} discussions débloquées",
    "notification_multi_opinionsUpdated": "{0} opinions modifiées entre les personnages",
    "notification_mysteriesCount": "{0} × Mystères",
    "notification_evidenceDestination": "Preuves > {0}",
    "notification_leadDestination": "Pistes > {0}",
    "notification_factsUncovered": "{0} faits découverts",

    # -- saves & options --------------------------------------------------------
    "saveTypes_auto": "Sauvegarde auto",
    "saveTypes_quick": "Sauvegarde rapide",
    "saveTypes_manual": "Sauvegarde manuelle",
    "saveMenu_import": "Importer",
    "saveMenu_save": "Sauvegarder",
    "optionsMenu_on": "Activé",
    "optionsMenu_off": "Désactivé",
    "optionsMenu_hold": "Maintenir",
    "optionsMenu_press": "Appuyer",
    "optionsMenu_toggle": "Bascule",
    "optionsMenu_dotToDot": "Point à point",
    "optionsMenu_draw": "Tracer",
    "optionsMenu_swapped": "Inversé",
    "optionsMenu_normal": "Normal",
    "optionsMenu_reduced": "Réduit",
    "optionsMenu_larger": "Plus grand",

    # -- misc -------------------------------------------------------------------
    "pickATime_day": "Jour {0}",
    "actor_no_time": "L’heure suivante est trop proche pour entreprendre cela.",
    "batteryInstructionsLabel": "Instructions",
    "dialScreenSigilCount": "{0} sceaux de la chambre trouvés",
    "nodeInfoPanel_roomNumber": "Chambre :",
    "nodeInfoPanel_arrivalDate": "Arrivée :",
    "nodeInfoPanel_socialClass": "Classe :",

    # -- puzzle content ---------------------------------------------------------
    # The well riddle names six of the eighteen ingredients below. The French keeps
    # each identification unambiguous against the distractors, and keeps a rhyme
    # scheme (venin/lin, bleus/adieux, argon/fusion) since the original rhymes.
    "mazeWellIngredients": (
        "Une goutte de venin"
        "|Un métal aux reflets bleus"
        "|L’écorce de l’if, cet arbre des adieux"
        "|Mêlez-y de l’argon"
        "|Et de la cire en fusion"
        "|Puis couronnez le tout d’une poignée de lin"
    ),
    "fiadhIngredientsDescriptions": (
        "Pétales orange de souci"
        "|Une bougie de cire d’abeille"
        "|Des runes aux motifs celtiques"
        "|Du sable à grain fin"
        "|Des rognures d’ongle de chien"
        "|Du poil de rat brun"
        "|Une branche d’if"
        "|Des graines de fleur de lin"
        "|De l’eau de source fraîche"
    ),
    "ruairiIngredientsDescriptions": (
        "De l’iode violet"
        "|Un bloc blanc de lithium"
        "|Un bras de cactus"
        "|Une fiole étiquetée « argon »"
        "|Un croc de vipère venimeux"
        "|Une météorite venue d’ailleurs"
        "|Des dents humaines"
        "|Une fiole d’un liquide épais et rougeâtre"
        "|Du gallium, un métal gris-bleu"
    ),
    "chemicalBenchIngredients": "0,Recette|1,Chlore|2,Déboucheur|3,Éthanol|4,Peroxyde|5,Soude|6,Eau|7,Vinaigre",
    "recipeTagline": "L’ingrédient suivant est…",
    "allIngredientsAdded": "TOUS LES INGRÉDIENTS AJOUTÉS",
}

# Deliberately left in English until verified in game — see REVIEW below.
STUDIO_HOLD = {"spiritWinPhrase", "spiritReadablePhrase"}

REVIEW = [
    {
        "ids": ["spiritWinPhrase", "spiritReadablePhrase"],
        "reason": (
            "Spirit-board puzzle: the player spells the phrase out letter by letter. "
            "'ASHESTOASHES' is 12 letters; 'CENDRESAUXCENDRES' would be 17. Until the "
            "board's capacity is checked in game, both stay English."
        ),
        "proposal": "CENDRES AUX CENDRES / CENDRESAUXCENDRES",
    },
    {
        "ids": ["mazeWellIngredients", "fiadhIngredientsDescriptions", "ruairiIngredientsDescriptions"],
        "reason": (
            "Riddle and ingredient lists must be translated as one unit: the riddle has "
            "to keep pointing at exactly the same six items and stay unambiguous against "
            "the twelve distractors. Verify in game that all six are still identifiable."
        ),
    },
]

# ------------------------------------------------------- AC cursors & menu labels
# Keyed by the English label. Internal cursor identifiers are never displayed and
# must not be translated - they are lookup keys.
CURSOR_AND_MENU = {
    "Use": "Utiliser",
    "Talk": "Parler",
    "Examine": "Examiner",
    "Open": "Ouvrir",
    "Listen": "Écouter",
    "Analyse": "Analyser",
    "Push": "Pousser",
    "Place Luggage": "Poser les bagages",
    "Open Object": "Ouvrir",
    "Close Object": "Fermer",
    # "Aller vers" rather than "Aller à": AC concatenates prefix + hotspot name and
    # cannot contract "à + le", so a preposition that never contracts is required.
    "Walk to": "Aller vers",
    "on": "sur",
    "Give": "Donner",
    "to": "à",
    # pause menu
    "Resume": "Reprendre",
    "Save": "Sauvegarder",
    "Save Blocked": "Sauvegarde impossible",
    "Load": "Charger",
    "How to Play": "Comment jouer",
    "Options": "Options",
    "Quit": "Quitter",
    "NOTE:": "NOTE :",
}

# ------------------------------------------------------- harvested from the game
# Strings that reach RuntimeLanguages.GetTranslation but live outside the pools the
# dumper can enumerate statically (main-menu labels, hotspot names, evidence blurbs).
# Source: BepInEx/blakemanor-fr-misses.txt, written by the patch itself. Re-run the
# game after every batch to harvest the next set.
FROM_MISSES = {
    # -- main menu, options, saves ---------------------------------------------
    "Audio": "Audio",
    "Back": "Retour",
    "Close": "Fermer",
    "Continue": "Continuer",
    "Controls": "Commandes",
    "Custom": "Personnalis\u00e9",
    "Day": "Jour",
    "Defaults": "Par d\u00e9faut",
    "Delete": "Supprimer",
    "Empty Slot": "Emplacement vide",
    "Enter": "Entr\u00e9e",
    "Exit to Main Menu": "Retour au menu principal",
    "Gameplay": "Jeu",
    "Graphics": "Graphismes",
    "Interface": "Interface",
    "Load Game": "Charger une partie",
    "Save Game": "Sauvegarder la partie",
    "Saving Blocked": "Sauvegarde impossible",
    "Paused": "En pause",
    "Master Volume": "Volume g\u00e9n\u00e9ral",
    "Music Volume": "Volume de la musique",
    "SFX Volume": "Volume des effets",
    "Voice Volume": "Volume des voix",
    "Some controls were swapped around due to your new binding":
        "Certaines commandes ont \u00e9t\u00e9 interverties du fait de votre nouvelle assignation",

    # -- interaction verbs ------------------------------------------------------
    "Look": "Regarder",
    "Place": "Poser",
    "Wait": "Attendre",

    # -- hotspot and evidence names --------------------------------------------
    # Articles are carried by the name itself: AC builds "Aller vers " + name, so
    # "le manoir" gives "Aller vers le manoir" and "Examiner le manoir".
    "manor": "le manoir",
    "local area": "les environs",
    "personal belongings": "les effets personnels",
    "photo of Miss Deane": "la photo de Mlle Deane",
    "Miss Deane": "Mlle Deane",
    "My arrival": "mon arriv\u00e9e",

    # -- evidence and lore blurbs ----------------------------------------------
    "The missing woman.": "La femme disparue.",
    "My luggage, hastily packed.": "Mes bagages, faits \u00e0 la h\u00e2te.",
    "The letter I received hiring me onto this case.":
        "La lettre par laquelle on m\u2019a engag\u00e9 sur cette affaire.",
    "A map of the area for several miles around. It's dated but fit for purpose.":
        "Une carte de la r\u00e9gion sur plusieurs milles \u00e0 la ronde. "
        "Elle date, mais elle fera l\u2019affaire.",
    "A photograph of Miss Evelyn Deane. She looks to be in her twenties.":
        "Une photographie de Mlle Evelyn Deane. Elle para\u00eet avoir une vingtaine d\u2019ann\u00e9es.",
    "Built on conquered land by Edward Blake in 1655.":
        "B\u00e2ti sur une terre conquise par Edward Blake en 1655.",
    "Miss Erickson does not have time for this.":
        "Mlle Erickson n\u2019a pas le temps de s\u2019occuper de cela.",

    # -- content warning (the \n\n paragraph breaks are load-bearing) -------------
    "Content Warning: The S\u00e9ance of Blake Manor is a gothic folk horror and, as such, "
    "touches on a lot of the human tragedies experienced throughout history.\n\nEvery effort "
    "has been taken to find a balance between authenticity and sensitivity with the language "
    "used.\n\nThe player's discretion is advised.":
        "Avertissement : The S\u00e9ance of Blake Manor est une \u0153uvre d\u2019horreur folklorique "
        "gothique et aborde \u00e0 ce titre nombre de trag\u00e9dies humaines survenues au fil de "
        "l\u2019histoire.\n\nUn soin particulier a \u00e9t\u00e9 apport\u00e9 \u00e0 l\u2019\u00e9quilibre entre authenticit\u00e9 "
        "et sensibilit\u00e9 dans le choix des mots.\n\nLa discr\u00e9tion du joueur est conseill\u00e9e.",
}

# Runtime substitution tokens, never translated.
MISS_DO_NOT_TRANSLATE = {"{InteractionX}"}


DO_NOT_TRANSLATE = {"Default", "Custom", "Mindmap", "MindmapSelected", "GlyphCursor",
                    "TransparentCursor", "Wait", "Button", "Label"}


def reaffix(source, fr):
    """Reproduce the source's leading/trailing whitespace around the translation."""
    core = source.strip()
    lead = source[: len(source) - len(source.lstrip())]
    trail = source[len(source.rstrip()):]
    if not core:
        return source
    return lead + fr + trail


def main():
    if not POOLS.exists():
        sys.exit(f"missing {POOLS} — run build_corpus.py first")
    pools = json.loads(POOLS.read_text(encoding="utf-8"))["ui"]

    by_source, untranslated, conflicts = {}, [], []

    def add(source, fr, origin):
        out = reaffix(source, normalise(fr))
        if source in by_source and by_source[source] != out:
            conflicts.append({"source": source, "a": by_source[source], "b": out, "origin": origin})
            return
        by_source[source] = out

    for row in pools["translatableStrings"]:
        src, ident = row["value"], row["id"]
        if ident in STUDIO_HOLD:
            continue
        fr = STUDIO.get(ident)
        if fr is None:
            untranslated.append({"pool": "translatableStrings", "id": ident, "en": src})
            continue
        add(src, fr, ident)

    # Evidence / clue / task labels. The displayed string is altLabel when set,
    # else label — see InvItem.GetTranslatableString(0).
    for row in pools.get("inventoryItems", []):
        src = row.get("altLabel") or row.get("label") or ""
        if not src.strip():
            continue
        fr = EVIDENCE.get(src) or EVIDENCE.get(src.strip())
        if fr is None:
            untranslated.append({"pool": "inventoryItems", "id": row.get("id"), "en": src})
            continue
        add(src, fr, "evidence")

    # Hypothesis Token Words: inventory properties 3 and 4. These fill the [r]
    # slots and carry their own determiner (docs/HYPOTHESES.md rule 2).
    for row in pools.get("inventoryItems", []):
        for prop in row.get("properties", []):
            src = prop.get("text") or ""
            if not src.strip():
                continue
            idx = prop.get("index")
            if idx in (3, 4):
                table, pool = TOKENS, "tokenWords"
            else:
                # 0 Description, 1 Updated Label, 2 Updated Description
                table, pool = DESCRIPTIONS, "descriptions"
            fr = table.get(src) or table.get(src.strip())
            if fr is None:
                untranslated.append({"pool": pool, "id": row.get("id"), "en": src})
                continue
            add(src, fr, pool)

    for pool in ("cursorIcons", "menuElements"):
        for row in pools.get(pool, []):
            src = row.get("label") or row.get("text") or ""
            if not src.strip() or src.strip() in DO_NOT_TRANSLATE:
                continue
            fr = CURSOR_AND_MENU.get(src.strip())
            if fr is None:
                untranslated.append({"pool": pool, "id": row.get("kind") or row.get("element"), "en": src})
                continue
            add(src, fr, pool)

    for src, fr in FROM_MISSES.items():
        if src in MISS_DO_NOT_TRANSLATE:
            continue
        add(src, fr, "misses")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "_meta": {
            "layer": "ui",
            "injection": "by source string, via RuntimeLanguages.GetTranslation",
            "style": "docs/STYLE.md",
            "entries": len(by_source),
        },
        "review": REVIEW,
        "bySource": by_source,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    seen_evidence = {(r.get("altLabel") or r.get("label") or "").strip()
                     for r in pools.get("inventoryItems", [])}
    seen_props = {(p.get("text") or "").strip()
                  for r in pools.get("inventoryItems", [])
                  for p in r.get("properties", []) if p.get("index") in (0, 1, 2)}
    stale_desc = sorted(k for k in DESCRIPTIONS if k.strip() not in seen_props)
    if stale_desc:
        print(f"STALE description keys ({len(stale_desc)}):")
        for k in stale_desc:
            print(f"  {k[:100]!r}")
        print()

    stale = sorted(k for k in EVIDENCE if k.strip() not in seen_evidence)
    if stale:
        print(f"STALE evidence keys ({len(stale)}) — match nothing in the game, likely typos:")
        for k in stale:
            print(f"  {k!r}")
        print()

    print(f"translated : {len(by_source)}")
    print(f"held back  : {len(STUDIO_HOLD)} (see review)")
    print(f"skipped    : identifiers not shown to the player")
    if conflicts:
        print(f"\nCONFLICTS ({len(conflicts)}): same English, two different French")
        for c in conflicts:
            print(f"  {c['source']!r}: {c['a']!r} vs {c['b']!r}  [{c['origin']}]")
    if untranslated:
        print(f"\nUNTRANSLATED ({len(untranslated)}):")
        for u in untranslated:
            print(f"  [{u['pool']}/{u['id']}] {u['en']!r}")
    print(f"\nwrote -> {OUT}")


if __name__ == "__main__":
    main()
