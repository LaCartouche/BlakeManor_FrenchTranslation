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


# ------------------------------------------ second harvest, from a real playthrough
# Source: BepInEx/blakemanor-fr-misses.txt after a session that reached the mindmap,
# the journal and the save menu. 7,078 lookups were already translated; these are
# what was left.
#
# The room and puzzle names are EHSceneCollection labels. They are safe to
# translate: collections are looked up by Path and by handle, never by label, which
# is display only — it is what appears on a save slot beside the day and time.
HARVEST_2 = {
    # -- menus, prompts and confirmations ---------------------------------------
    "New Game": "Nouvelle partie",
    "Credits": "Crédits",
    "Exit": "Quitter",
    "Go Back": "Retour",
    "Yes": "Oui",
    "No": "Non",
    "Quit game?": "Quitter le jeu ?",
    "Start a new game?": "Commencer une nouvelle partie ?",
    "Exit to Main Menu?": "Retourner au menu principal ?",
    "All unsaved progress will be lost.": "Toute progression non sauvegardée sera perdue.",
    "Mark All As Seen": "Tout marquer comme vu",
    "Map": "Plan",
    "...": "…",

    # -- skip prompts: the {token} is substituted with the player's binding ------
    "Hold {<Cancel>[#FFFFFF]} to Skip Cutscene":
        "Maintenez {<Cancel>[#FFFFFF]} pour passer la scène",
    "Press {Cancel} to Skip Animation": "Appuyez sur {Cancel} pour passer l’animation",

    # -- deduction and journal --------------------------------------------------
    "Mysteries": "Mystères",
    "Records": "Registres",
    "Investigate": "Enquêter",
    "Discuss": "Discuter",
    "Eavesdrop": "Écouter",
    "Discussion Topics": "Sujets de discussion",
    "Discussable With:": "À évoquer avec :",
    "Current Focus:": "Objectif actuel :",
    "Observations:": "Observations :",
    "All Observations Discovered": "Toutes les observations découvertes",
    "Facts About the Culprit": "Faits sur le coupable",
    "Facts Unlocked": "Faits découverts",
    "Make Hypothesis": "Formuler une hypothèse",
    "Too late to make a hypothesis": "Trop tard pour formuler une hypothèse",
    "Select Culprit": "Désigner le coupable",
    "Eliminate": "Écarter",
    "Un-eliminate": "Réintégrer",
    "Missus Joyce": "Mme Joyce",
    "Telegram": "Télégramme",
    "Phrenology Bust": "Buste de phrénologie",

    # -- save-slot metadata -----------------------------------------------------
    "Day 1": "Jour 1",
    "October 29th, 11pm": "29 octobre, 23 h",
    "Blake Manor Courtyard": "Cour de Blake Manor",
    "Courtyard": "Cour",
    "Atrium": "Atrium",
    "Lobby": "Hall",
    "Fountain": "Fontaine",
    "Statue": "Statue",

    # -- rooms tracked by sigil count -------------------------------------------
    "Carmela's Room (1 Sigil)": "Chambre de Carmela (1 sceau)",
    "Deane's Room (2 Sigils)": "Chambre de Deane (2 sceaux)",
    "Dupre's Trunk (1 Sigil)": "Malle de Dupré (1 sceau)",
    "East Tower (1 Sigil)": "Tour est (1 sceau)",
    "Empty Bedroom (1 Sigil)": "Chambre vide (1 sceau)",
    "End Chamber (3 Sigils)": "Chambre finale (3 sceaux)",
    "Hidden Room (1 Sigil)": "Pièce dissimulée (1 sceau)",
    "Ladies Bathroom (1 Sigil)": "Toilettes des dames (1 sceau)",
    "Masoleum (1 Sigil)": "Mausolée (1 sceau)",
    "O Finn's Room (1 Sigil)": "Chambre d’Ó Finn (1 sceau)",
    "Ruairi's Room (1 Sigil)": "Chambre de Ruairi (1 sceau)",
    "South East Corridor (1 Sigil)": "Couloir sud-est (1 sceau)",
    "Sun Room (1 Sigil)": "Salle du soleil (1 sceau)",
    "Sigils Master Scene": "Scène principale des sceaux",
    "Séance Secret Passage Door": "Porte du passage secret de la Séance",
    "Changing Rooms Access": "Accès aux vestiaires",
    "Basement Boxes": "Coffres du sous-sol",
    "Basement Chemicals\n": "Produits chimiques du sous-sol",

    # -- lockboxes and safes ----------------------------------------------------
    "Caitlins Lockbox": "Coffret de Caitlin",
    "Cathal's Lock Box": "Coffret de Cathal",
    "Hazel's Lock Box": "Coffret de Hazel",
    "Ines lock box in her room": "Coffret d’Ines, dans sa chambre",
    "Ivy's Lock Box": "Coffret d’Ivy",
    "Lan Fen's Lock Box": "Coffret de Lan Fen",
    "Male dorm lock box": "Coffret du dortoir des hommes",
    "Skerrit lock box": "Coffret de Skerrit",
    "Manager's Office Safe": "Coffre du bureau du gérant",
    "Safe: Projector Room": "Coffre : salle du projecteur",
    "Safe: Stables": "Coffre : écuries",

    # -- puzzles ----------------------------------------------------------------
    "Bablestone minigame": "Mini-jeu de la babelstone",
    "Ouija board minigame\n": "Mini-jeu de la planche des esprits",
    "Piano Minigame": "Mini-jeu du piano",
    "Projector Puzzle": "Énigme du projecteur",
    "Spot The Difference": "Jeu des différences",
    "Well minigame": "Mini-jeu du puits",
    "Unscramble Fiadh's torn letter": "Reconstituer la lettre déchirée de Fiadh",
    "Ogham translation": "Traduction de l’ogham",
}

# Runtime substitution tokens and Adventure Creator element placeholders.
HARVEST_2_SKIP = {"{InteractionX}", "{ScrollWheel}", "Button"}


# ------------------------------------------- third harvest: timeline, map, journal
# Source: a session that reached the timetable, the floor map and the save/load
# screen. Note the room labels: the original's spacing is irregular ("01 \nMiss
# McLeod" has a space before the newline, "05\nMiss Mantovani" does not, and
# "02 Unassigned" has no newline at all). Reproduced exactly - these are laid out
# as two lines in a grid cell.
HARVEST_3 = {
    # -- timetable hours. 12am is midnight, 12pm is noon. --------------------
    "8am": "8 h", "9am": "9 h", "10am": "10 h", "11am": "11 h",
    "12pm": "12 h", "1pm": "13 h", "2pm": "14 h", "3pm": "15 h", "4pm": "16 h",
    "5pm": "17 h", "6pm": "18 h", "7pm": "19 h", "8pm": "20 h", "9pm": "21 h",
    "10pm": "22 h", "11pm": "23 h", "12am": "0 h",

    "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche",
    "DAWN": "AUBE", "DUSK": "CRÉPUSCULE", "AWAY": "ABSENT",
    "End \nof Day": "Fin \nde journée",
    "Current Time": "Heure actuelle",
    "Timeline": "Chronologie",
    "Legend": "Légende",
    "Filter": "Filtre",
    "All": "Tout",
    "-": "-",

    # -- scheduled events ----------------------------------------------------
    "Events": "Événements",
    "Breakfast": "Petit-déjeuner",
    "Silent dinner": "Dîner silencieux",
    "Masked ball": "Bal masqué",
    "Grand Séance": "Grande Séance",
    "Flyers": "Prospectus",
    "Reminders left for": "Rappels restants pour",
    "Too late for reminders...": "Trop tard pour des rappels…",

    # -- floor map -----------------------------------------------------------
    "Basement": "Sous-sol",
    "Ground Floor": "Rez-de-chaussée",
    "First Floor": "Premier étage",
    "Courtyards": "Cours",
    "West Tower": "Tour ouest",
    "Closet": "Placard",
    "My Room": "Ma chambre",
    "WC": "WC",
    "Gents WC": "WC hommes",
    "Ladies WC": "WC dames",
    "North East Corridor Upper": "Couloir nord-est supérieur",
    "North West Corridor Upper": "Couloir nord-ouest supérieur",
    "South East Corridor Upper": "Couloir sud-est supérieur",
    "South West Corridor Upper": "Couloir sud-ouest supérieur",
    "Northern \nPass \nCorridor": "Couloir \ndu passage \nnord",

    # -- room labels on the map: number, then occupant on a second line -------
    "01 \nMiss McLeod": "01 \nMlle McLeod",
    "02 Unassigned": "02 Non attribuée",
    "03 \nMissus Lau": "03 \nMme Lau",
    "05\nMiss Mantovani": "05\nMlle Mantovani",
    "06\nMister Toussaint": "06\nM. Toussaint",
    "07 Unassigned": "07 Non attribuée",
    "08\nFather Sinnott": "08\nPère Sinnott",
    "09\nMiss Callaghan": "09\nMlle Callaghan",
    "10\nDoctor Callaghan": "10\nDocteur Callaghan",
    "11\nMister Dupré": "11\nM. Dupré",
    "12\nMiss Hisham": "12\nMlle Hisham",
    "13\nMissus D'Arcy": "13\nMme D’Arcy",
    "14\nMiss Quinn": "14\nMlle Quinn",
    "15\nUnassigned": "15\nNon attribuée",
    "16\nMister O'Meara": "16\nM. O’Meara",
    "17\nMiss Barbosa": "17\nMlle Barbosa",
    "18\nMister Skerritt": "18\nM. Skerritt",
    "19\nMissus Erickson": "19\nMme Erickson",
    "20\nMister Ó Finn": "20\nM. Ó Finn",
    "21\nUnassigned": "21\nNon attribuée",
    "22\nMister Coventry": "22\nM. Coventry",

    # -- room list -----------------------------------------------------------
    "Room 01": "Chambre 01", "Room 03": "Chambre 03", "Room 05": "Chambre 05",
    "Room 06": "Chambre 06", "Room 08": "Chambre 08", "Room 09": "Chambre 09",
    "Room 10": "Chambre 10", "Room 11": "Chambre 11", "Room 12": "Chambre 12",
    "Room 13": "Chambre 13", "Room 14": "Chambre 14", "Room 16": "Chambre 16",
    "Room 17": "Chambre 17", "Room 18": "Chambre 18", "Room 19": "Chambre 19",
    "Room 20": "Chambre 20", "Room 22": "Chambre 22",

    # -- evidence and save/load ----------------------------------------------
    "Evidence Pieces Found": "Preuves trouvées",
    "This evidence is included in the following cases:":
        "Cette preuve figure dans les affaires suivantes :",
    "Load this save?": "Charger cette sauvegarde ?",
    "You can also load to an earlier point on this save's timeline.":
        "Vous pouvez aussi revenir à un moment antérieur de cette sauvegarde.",
}


DO_NOT_TRANSLATE = {"Default", "Custom", "Mindmap", "MindmapSelected", "GlyphCursor",
                    "TransparentCursor", "Wait", "Button", "Label"}


# Source: the first real playthrough on build 1.1.12.360, harvested from the
# accumulating miss log. Options-screen labels and mindmap/deduction vocabulary
# are not in Adventure Creator's tables at all — the studio never ran "Gather
# Text" — so observing them at runtime is the only way they can be found.
HARVEST_4 = {
    # -- options screen ------------------------------------------------------
    "Fullscreen": "Plein écran",
    "Resolution": "Résolution",
    "Quality": "Qualité",
    "VSync": "Synchro verticale",
    "Brightness": "Luminosité",
    "Contrast": "Contraste",
    "Vignette": "Vignettage",
    "Motion Blur": "Flou de mouvement",
    "Screenshake": "Tremblement de l’écran",
    "Run Mode": "Mode course",
    "Skip Mode": "Mode accéléré",
    "Tutorial Mode": "Mode tutoriel",
    "Sigil Mode": "Mode sceau",
    "Sigil Drawing Speed": "Vitesse de tracé des sceaux",
    "Reset": "Réinitialiser",
    "Select": "Sélectionner",
    "Cancel": "Annuler",
    "Clear": "Effacer",
    "Privacy Policy": "Politique de confidentialité",
    "Privacy Policy\nhttps://rawfury.com/privacy-policy/":
        "Politique de confidentialité\nhttps://rawfury.com/privacy-policy/",

    # -- prompts. {InteractionA} is a runtime token and must survive verbatim. -
    "<color=#D3991E>Hold <color=#FFFFFF>{InteractionA}</color> to proceed.</color>":
        "<color=#D3991E>Maintenez <color=#FFFFFF>{InteractionA}</color> pour continuer.</color>",
    "<color=#D3991E>Press <color=#FFFFFF>{InteractionA}</color> to proceed.</color>":
        "<color=#D3991E>Appuyez sur <color=#FFFFFF>{InteractionA}</color> pour continuer.</color>",

    # -- actions / navigation -----------------------------------------------
    "Analyse Dupre": "Analyser Dupré",
    "Talk To Ghosts": "Parler aux fantômes",
    "Consider!": "Réfléchir !",
    "Investigate Mister Dupre's Bedroom": "Enquêter sur la chambre de M. Dupré",
    "Previewing items you can discuss with:": "Objets dont vous pouvez parler avec :",
    "Document": "Document",
    "Item": "Objet",
    "Ghost": "Fantôme",

    # -- sigils --------------------------------------------------------------
    "Memory Sigil": "Sceau de mémoire",
    "Missing Door Sigil": "Sceau de la porte manquante",
    "Unlock Sigil": "Sceau d’ouverture",
    "Wake Up Sigil ": "Sceau d’éveil ",
    "Eye Of Goibniu Sigil": "Sceau de l’Œil de Goibniu",
    "Dissolve Sigil": "Sceau de dissolution",

    # -- evidence and documents ---------------------------------------------
    "Cathal's Journal": "Journal de Cathal",
    "Skerritt's Diary": "Journal de Skerritt",
    "Journal Of Mister Dupre": "Journal de M. Dupré",
    "Correspondence With Mister Dupre": "Correspondance avec M. Dupré",
    "Mister Dupre's Letter To A Deceased Friend": "Lettre de M. Dupré à une amie défunte",
    "Letters From Fiadh's Sister": "Lettres de la belle-sœur de Fiadh",
    "Notes On Hazel Erickson": "Notes sur Hazel Erickson",
    "Death Certificate": "Certificat de décès",
    "Family Photograph": "Photographie de famille",
    "Gnostic Bible": "Bible gnostique",
    "Magical Grimoire": "Grimoire magique",
    "Strange Paper": "Papier étrange",
    "Keys Note": "Note sur les clés",
    "Postal Orders": "Mandats postaux",
    "Preserved White Heather Hairpin": "Épingle de bruyère blanche séchée",
    "Spiritual Jewellery": "Bijoux spirites",
    "Cross Around Neck": "Croix au cou",
    "Vestments": "Habits sacerdotaux",
    "Ghost Photography Machine": "Appareil de photographie spirite",
    "Gauging Device": "Appareil de mesure",
    "Firepit": "Foyer",
    "Sun Door": "Porte du Soleil",
    "Hazel's Room Key": "Clé de la chambre de Hazel",
    "Saloon Key ": "Clé de l’atrium ",
    "H.O.G.D": "H.O.G.D",
    "Mama Brigitte": "Maman Brigitte",
    "The Goddess, Bridget": "La déesse Brigitte",
    "Tobar Síofra": "Tobar Síofra",

    # -- mindmap connection labels; names are never translated ---------------
    "Fighting: Cathal O'Meara": "Dispute : Cathal O’Meara",
    "Fighting: Darragh Hunter": "Dispute : Darragh Hunter",
    "Fighting: Domhnall Ó Finn": "Dispute : Domhnall Ó Finn",
    "Fighting: Ettiene Toussaint": "Dispute : Ettiene Toussaint",
    "Fighting: Father Lorcan Sinnott": "Dispute : le père Lorcan Sinnott",
    "Fighting: Jonathan Blake": "Dispute : Jonathan Blake",
    "Fighting: Lloyd Dupré": "Dispute : Lloyd Dupré",
    "Fighting: Michael Skerritt": "Dispute : Michael Skerritt",
    "Fighting: Ruairi Callaghan": "Dispute : Ruairi Callaghan",
    "Fighting: Seamus Doyle": "Dispute : Seamus Doyle",
    "Fighting: Simon Coventry": "Dispute : Simon Coventry",
    "Fighting: Vincent Varley": "Dispute : Vincent Varley",
    "Fighting: Walter Blake": "Dispute : Walter Blake",
    "Doyle: Father Lorcan Sinnott": "Doyle : le père Lorcan Sinnott",
    "Joyce: Mantovani": "Joyce : Mantovani",
    "Trail: East Corridors": "Piste : corridors est",
    "Trail: East Tower": "Piste : tour est",
    "Trail: Gardens": "Piste : jardins",
    "Trail: South East Corridor": "Piste : corridor sud-est",

    # -- observed traits -----------------------------------------------------
    "Confident, Elegant Bearing": "Port assuré et élégant",
    "Proud Bearing": "Port altier",
    "Relaxed Regard": "Regard détendu",
    "Tense Body Language": "Attitude crispée",
    "Thoughtful, Troubled Expression": "Expression pensive et troublée",
    "Tightly-Held Purse": "Sac serré contre soi",
    "Dusty, Scuffed Clothes": "Vêtements poussiéreux et éraflés",
    "Dressed Well, But Not Ostentatiously": "Bien mis, sans ostentation",
    "Well And Practically Dressed": "Vêtu avec soin et sens pratique",
    "Scent Of Antiseptic": "Odeur d’antiseptique",
    "Scent Of Tobacco On Breath": "Haleine chargée de tabac",
    "Signs Of Childs Play": "Traces de jeux d’enfant",

    # -- motives and states --------------------------------------------------
    "Dead Wife": "Épouse défunte",
    "Her Health": "Sa santé",
    "Ghostly Desire": "Désir spectral",
    "Missing Lovers": "Amants disparus",
    "No Friends": "Aucun ami",
    "She's A Goner": "Elle est perdue",
    "MOTIVE: Wants to place his friend's soul into Miss Deane's body.":
        "MOBILE : veut placer l’âme de son amie dans le corps de Mlle Deane.",

    # -- deduction chips. "They" is the unknown culprit: kept genderless. -----
    "He had never met Miss Deane before this event.":
        "Il n’avait jamais rencontré Mlle Deane avant cet événement.",
    "He has never been to this side of the world before. ":
        "Il n’était jamais venu dans cette partie du monde. ",
    "He has various life-like drawings in his room.":
        "Il a dans sa chambre plusieurs dessins d’un grand réalisme.",
    "He is a Vodouists Oungan.": "C’est un oungan vaudou.",
    "He is mourning the recent loss of a friend.":
        "Il porte le deuil d’une amie récemment perdue.",
    "He wears a medium shoe.": "Il chausse une pointure moyenne.",
    "In his late 40s.": "Il approche de la cinquantaine.",
    "I found a letter written by him in the lobby.":
        "J’ai trouvé à la réception une lettre de sa main.",
    "I found writings in English in her room.":
        "J’ai trouvé des écrits en anglais dans sa chambre.",
    "I found writings of his in his room. ":
        "J’ai trouvé de ses écrits dans sa chambre. ",
    "I watched him perform magical rites.":
        "Je l’ai vu accomplir des rites magiques.",
    "Her room contains art supplies.":
        "Sa chambre contient du matériel de dessin.",
    "She has been drawing maps of the grounds.":
        "Elle dresse des plans du domaine.",
    "She has medium sized shoes in her room.":
        "Elle a dans sa chambre des souliers de pointure moyenne.",
    "She is a Sunni Muslim.": "Elle est musulmane sunnite.",
    "She is in her early 30s.": "Elle a un peu plus de trente ans.",
    "She was invited to the manor by Miss Deane.":
        "Elle a été invitée au manoir par Mlle Deane.",
    "They are a Christian.": "Cette personne est chrétienne.",
    "They are a skilled artist.": "Cette personne a un vrai talent d’artiste.",
    "They are able to write.": "Cette personne sait écrire.",
    "They are not in mourning.": "Cette personne n’est pas en deuil.",
    "They are not staff.": "Cette personne ne fait pas partie du personnel.",
    "They have no pre-Manor history with Miss Deane.":
        "Cette personne n’avait aucun lien avec Mlle Deane avant le manoir.",
    "They know the grounds, or have maps.":
        "Cette personne connaît le domaine, ou possède des plans.",
    "They used magic in the kidnapping.":
        "Cette personne a usé de magie lors de l’enlèvement.",
    "They wear medium shoes.": "Cette personne chausse une pointure moyenne.",
}


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

    for src, fr in HARVEST_2.items():
        if src in HARVEST_2_SKIP:
            continue
        add(src, fr, "harvest2")

    for src, fr in HARVEST_3.items():
        if src in HARVEST_2_SKIP:
            continue
        add(src, fr, "harvest3")

    for src, fr in HARVEST_4.items():
        if src in HARVEST_2_SKIP:
            continue
        add(src, fr, "harvest4")

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
