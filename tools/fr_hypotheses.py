#!/usr/bin/env python3
"""
The hypothesis layer: sentence templates, verb banks and evidence Token Words.

Read docs/HYPOTHESES.md first. The five rules that govern everything here:
  1. the [v]/[r] marker sequence is fixed — slots are addressed positionally
  2. the article lives in the token, never in the template
  3. never `de [r]` or `à [r]` (they contract); `de [v]` / `à [v]` are fine
  4. no elision before a slot — use `car`, not `parce que`
  5. no agreement with a slot — [v] tokens are infinitives or fixed forms

Templates and verb banks are Dialogue System item fields (injected by overwriting
the field value). Token Words are Adventure Creator inventory property 3
(injected by source string through RuntimeLanguages.GetTranslation).

Every template below is built to stay readable with ANY combination the player
can assemble, not just the correct one — the sentence is on screen while they
are still guessing. Each still needs solving in game to confirm the correct
combination reads well; that check has not been done yet.
"""

# ---------------------------------------------------------------- templates
# Keyed by the item's technical Name. "h" = hypothesisSentence, "c" = confrontSentence.
# The comment on each is the English original; the marker sequence must match it.
TEMPLATES = {
    # We are all [v] [r]'s [r] that is [v] into [r]!            v r r v r
    "main.5.0.dreams": {
        "h": "Nous sommes tous en train de [v] [r] : [r] qui vient [v] dans [r] !"},

    # The manor is haunted by [r] whose name is [r], and they want to [v] [r] through [r]!   r r v r r
    "main.4.0.entity": {
        "h": "Le manoir est hanté par [r], dont le nom est [r], et il veut [v] [r] par [r] !"},

    # Miss Deane attended because [r] [v] information about her [r]!    r v r
    "main.6.0.deaneManor": {
        "h": "Mlle Deane est venue car [r] a permis de [v] des informations sur [r] !"},

    # [r] was taken because he [v] the [r] from [r]!            r v r r
    "3.1.0.WhosWho": {
        "h": "[r] a été enlevé car il a cherché à [v] [r] chez [r] !"},

    # Something [v] has affected the [r] and they're now [v] when asked about the [r]!   v r v r
    "3.3.0.InvestigateTheStaff": {
        "h": "Quelque chose vient de [v] [r], et voilà qu’il se met à [v] dès qu’on l’interroge sur [r] !"},

    # Jonathan Blake intends to [v] his [r] to [v] his [r] but [r]!     v r v r r
    "3.4.0.BlakeResidence": {
        "h": "Jonathan Blake compte [v] [r] pour [v] [r], mais [r] !"},

    # You cannot [v] your [r]; you've been [v] by [v] so he can take over your [r]!    v r v v r
    "3.5.0.TheRitual": {
        "h": "Vous ne pouvez pas [v] [r] : on cherche à vous [v] pour [v], afin qu’il prenne [r] !",
        "c": "Vous ne pouvez pas [v] [r] : on cherche à vous [v] pour [v], afin qu’il prenne [r] !"},

    # Miss Deane was seen [v] the [r] in a [v] caused by the [r]        v r v r
    "2.1.0.DeanesRoom": {
        "h": "On a vu Mlle Deane [v] [r], plongée dans [v] — et la cause en est [r]"},

    # Miss Deane was [v] the [r] by [r] while [r] watched.              v r r r
    "2.3.0.FollowDeanesTrail": {
        "h": "Mlle Deane s’est vue [v] [r] par [r], et [r] observait la scène."},

    # Miss Deane [v] with [r] when he [v] her [r].                      v r v r
    "2.4.0.WhoFoughtWithDeane": {
        "h": "Mlle Deane a dû [v] avec [r] lorsqu’il a voulu [v] [r]."},

    # I [v] into [r] as I [v] a [r] through the ballroom's [r]!         v r v r r
    "2.6.0.TheChase": {
        "h": "J’ai dû [v] dans [r] en cherchant à [v] [r] par [r] de la salle de bal !"},

    # Corentine Quinn's goal is to perform a [r] to [v] the [r] from the [r].   r v r r
    "QuinnQuests": {
        "h": "Corentine Quinn veut accomplir [r] pour [v] [r] et libérer [r].",
        "c": "Vous voulez accomplir [r] pour [v] [r] et libérer [r] !"},

    # Vincent Varley's goal is to [v] [r] to [v] the [r] from [r].      v r v r r
    "VarleyQuests": {
        "h": "Vincent Varley veut [v] [r] pour [v] [r] et préserver [r].",
        "c": "Vous voulez [v] [r] pour [v] [r] et préserver [r] !"},

    # Olivia D'Arcy's goal is to [v] [r] as [v] for the [v] that occurred while she [r].   v r v v r
    "D'ArcyQuests": {
        "h": "Olivia D’Arcy veut [v] [r] en guise de [v] pour [v], survenu à l’époque où [r].",
        "c": "Vous voulez [v] [r] en guise de [v] pour [v], survenu à l’époque où [r] !"},

    # Lloyd Dupré's goal is to [v] the [r] of his [r] into [r].         v r r r
    "DupreQuests": {
        "h": "Lloyd Dupré veut [v] [r] — [r] — et lui offrir [r].",
        "c": "Vous voulez [v] [r] — [r] — et lui offrir [r] !"},

    # Micheal Skerritt's goal is to [v] his [r] and be [v] as the [r] to [v] from [r].   v r v r v r
    "SkerrittQuests": {
        "h": "Michael Skerritt veut [v] [r] et rester [v] comme [r], afin de [v] depuis [r].",
        "c": "Vous voulez [v] [r] et rester [v] comme [r], afin de [v] depuis [r] !"},

    # Caitlin Joyce's goal is to [v] [r] to [r] before she's able to [v] the [r].   v r r v r
    "JoyceQuests": {
        "h": "Caitlin Joyce veut [v] [r] pour [r], avant de pouvoir [v] [r].",
        "c": "Vous voulez [v] [r] pour [r], avant de pouvoir [v] [r] !"},

    # Arwa Hisham's goal is to [v] the [r] but she is [v] because it is [r].   v r v r
    "HishamQuests": {
        "h": "Arwa Hisham veut [v] [r], mais elle est [v] car tout cela est [r].",
        "c": "Vous voulez [v] [r], mais vous êtes [v] car tout cela est [r] !"},

    # Carmela Mantovani's goal is to [v] the [r] despite it [v] her as she wants to [v] for her [r].   v r v v r
    "MantovaniQuests": {
        "h": "Carmela Mantovani veut [v] [r], quitte à [v], car elle souhaite [v] pour [r].",
        "c": "Vous voulez [v] [r], quitte à [v], car vous souhaitez [v] pour [r] !"},

    # Cathal O'Meara's goal is to [v] [r] and [v] it so that he can [v] [v] his [r].   v r v v v r
    "O'MearaQuests": {
        "h": "Cathal O’Meara veut [v] [r] puis [v], afin de pouvoir [v] et [v] [r].",
        "c": "Vous voulez [v] [r] puis [v], afin de pouvoir [v] et [v] [r] !"},

    # Saoirse Murphy's goal is to [v] with [r] to [v] about her [r] now that [r].   v r v r r
    "SaoirseQuests": {
        "h": "Saoirse Murphy veut [v] avec [r] pour [v] sur [r], car [r].",
        "c": "Vous voulez [v] avec [r] pour [v] sur [r], car [r] !"},

    # Darragh Hunter's goal is to [v] [r] to [v] [r] from [r].          v r v r r
    "HunterQuests": {
        "h": "Darragh Hunter veut [v] [r] pour [v] [r] contre [r].",
        "c": "Vous voulez [v] [r] pour [v] [r] contre [r] !"},

    # Domhnall Ó Finn's goal was to [v] the [r] as it is his [v] as a [r] of the [r].   v r v r r
    "ÓFinnQuests": {
        "h": "Domhnall Ó Finn voulait [v] [r], car tel est [v] — il est [r] parmi [r]."},

    # Mister Toussaint's goal is to [v] me into [v] a [r] for [r].      v v r r
    "ToussaintQuests": {
        "h": "M. Toussaint veut me [v] pour me pousser à [v] [r] pour [r].",
        "c": "Vous voulez me [v] pour me pousser à [v] [r] pour [r] !"},

    # Father Sinnott's goal is to [v] [r] by [v] an [r] from the [r].   v r v r r
    "SinnottQuests": {
        "h": "Le père Sinnott veut [v] [r] en cherchant à [v] [r] depuis [r].",
        "c": "Vous voulez [v] [r] en cherchant à [v] [r] depuis [r] !"},

    # Fiadh Callaghan's goal is to [v] the [r] to [v] the [r] from the [r].   v r v r r
    "FiadhCallaghanQuests": {
        "h": "Fiadh Callaghan veut [v] [r] pour [v] [r] contre [r].",
        "c": "Vous voulez [v] [r] pour [v] [r] contre [r] !"},

    # Hazel Erickson's goal is to [v] the [r] of [r] to [v] her [r].    v r r v r
    "EricksonQuests": {
        "h": "Hazel Erickson veut [v] [r] — [r] — pour [v] [r].",
        "c": "Vous voulez [v] [r] — [r] — pour [v] [r] !"},

    # Ines Barbosa's goal is to [v] a [r] in her [r] now that her [r] has [r].   v r r r r
    "BarbosaQuests": {
        "h": "Ines Barbosa veut [v] [r] dans [r], car [r] a [r].",
        "c": "Vous voulez [v] [r] dans [r], car [r] a [r] !"},

    # Ivy McLeod's goal is to [v] a [r] to [v] up her [r] with [r].     v r v r r
    "DarrochQuests": {
        "h": "Ivy McLeod veut [v] [r] pour [v] [r] avec [r].",
        "c": "Vous voulez [v] [r] pour [v] [r] avec [r] !"},

    # You cannot [v] your [r]; you've been [v] by [v] so he can take over your [r]!   v r v v r
    "BlakeQuests": {
        "h": "Vous ne pouvez pas [v] [r] : on cherche à vous [v] pour [v], afin qu’il prenne [r] !",
        "c": "Vous ne pouvez pas [v] [r] : on cherche à vous [v] pour [v], afin qu’il prenne [r] !"},

    # Victoria Lau's goal is to [v] her [r] with [r] by [v] her so she can [v] [r]!   v r r v v r
    "ZhaoQuests": {
        "h": "Victoria Lau veut [v] [r] avec [r] en la faisant [v], pour pouvoir [v] [r] !",
        "c": "Vous voulez [v] [r] avec [r] en la faisant [v], pour pouvoir [v] [r] !"},

    # Ruairí Callaghan's goal is to [v] his [r] by [v] his [r] are [r].   v r v r r
    "RuairíCallaghanQuests": {
        "h": "Ruairí Callaghan veut [v] [r] en cherchant à [v] — [r] sont [r].",
        "c": "Vous voulez [v] [r] en cherchant à [v] — [r] sont [r] !"},

    # Seamus Doyle's goal was to [v] [r], but he [v] due to the [r] and now he wants to [v].   v r v r v
    "DoyleQuests": {
        "h": "Seamus Doyle voulait [v] [r], mais il a fini par [v] sous [r], et désormais il veut [v].",
        "c": "Vous vouliez [v] [r], mais vous avez fini par [v] sous [r], et désormais vous voulez [v] !"},

    # Simon Coventry's goal is to free [v] in order to assume the role of his [r], [v],
    # to inherit his [r] because his real identity is ousted heir [v].   v r v r v
    "CoventryQuests": {
        "h": "Simon Coventry veut libérer [v] pour prendre la place occupée par [r], [v], "
             "et hériter [r] — car sa véritable identité est celle de l’héritier évincé [v]."},

    # [r] [r] is [v]                                                    r r v
    "1.1.0.Arrival": {
        "h": "[r] [r] est [v]"},
}

# ------------------------------------------------------------- verb banks
# The `verbs` field, a comma-separated pool. Infinitives, except where the slot is
# nominal or predicative in its template (see the rule-5 note in docs/HYPOTHESES.md).
VERBS = {
    "main.5.0.dreams":          "vivre,rêver,jeter un sort,maudire,malveillant",
    "main.4.0.entity":          "hanter, fuir, droguer, combattre, contrefaire, parler",
    "main.6.0.deaneManor":      "assister, promettre, mentir, oublier, se battre",
    "3.1.0.WhosWho":            "enlever,reconnaître,vénérer,assassiner,aimer",
    "3.3.0.InvestigateTheStaff": "hypnotiser, parler, tromper, mentir, soudoyer",
    "3.4.0.BlakeResidence":     "sacrifier,ressusciter,abandonner,enterrer,invoquer",
    "3.5.0.TheRitual":          "assassiner,sauver,duper,enlever,invoquer",
    "2.1.0.DeanesRoom":         "cacher,repérer,errer,dormir,revenir",
    "2.3.0.FollowDeanesTrail":  "errer, guider, protéger, quitter, poursuivre, brûler",
    "2.4.0.WhoFoughtWithDeane": "embrasser, se battre, repousser, soutenir, quitter",
    "2.6.0.TheChase":           "descendre,poursuivre,halluciner,imaginer,aider",
    "QuinnQuests":              "accomplir, lever, accroître, trouver, dérober",
    "VarleyQuests":             "dissimuler, protéger, recruter, écarter, dérober",
    "D'ArcyQuests":             "commettre, vengeance, aider, équilibre, exploiter",
    "DupreQuests":              "déposer, apaiser, arracher, fuir",
    "SkerrittQuests":           "tuer, immortalisé, commettre",
    "JoyceQuests":              "souffrir, lapidation, écrire, bûcher",
    "HishamQuests":             "chercher, reprendre",
    "MantovaniQuests":          "conduire, fournir, fabriquer, lire, prédire, tuer, renforcer",
    "O'MearaQuests":            "libérer, piéger, tuer, se servir, apprendre, prendre",
    "SaoirseQuests":            "parler, apprendre, prier, absoudre, menacer",
    "HunterQuests":             "lier, protéger",
    "ÓFinnQuests":              "protéger, accomplir, détruire, oublier, condamner",
    "ToussaintQuests":          "traquer, tuer, accuser, enquêter, accuser à tort",
    "SinnottQuests":            "piéger, asservir, tuer, libérer, sauver",
    "FiadhCallaghanQuests":     "garder, protéger, partager, bénir, nuire",
    "EricksonQuests":           "accomplir, dérober, dévorer",
    "BarbosaQuests":            "voir, découvrir, trancher, exorciser, bannir",
    "DarrochQuests":            "trouver, dissimuler",
    "BlakeQuests":              "délivrer, rétablir",
    "ZhaoQuests":               "droguer, cacher",
    "RuairíCallaghanQuests":    "prouver, bâtir, détruire, dissimuler, fuir",
    "DoyleQuests":              "aider, oublier, assassiner, refuser, se repentir",
    "CoventryQuests":           "contraindre, déchoir",
    "1.1.0.Arrival":            "déchirer,contrefaire,dissimuler,remettre",
}

# --------------------------------------------------------------- token words
# Adventure Creator inventory property 3. Determiners are part of the token
# (rule 2) so the templates never have to guess gender or number.
TOKENS = {
    # -- people, gods, factions (proper nouns stay) --------------------------
    "Bríd": "Bríd", "Goibniu": "Goibniu", "Maman Brigitte": "Maman Brigitte",
    "The Cailleach": "la Cailleach", "The Morrigan": "la Morrigan",
    "Tuatha Dé Danann": "Tuatha Dé Danann", "Tír na nÓg": "Tír na nÓg",
    "fae": "les fae", "the Fae": "les Fae", "Aeon": "l’Éon",
    "Black Iron Prison": "la prison de fer noir",
    "John Dee": "John Dee", "Milesian rulers": "les souverains milésiens",
    "Detective Ward": "le détective Ward", "Evelyn Deane": "Evelyn Deane",
    "Henry Blake": "Henry Blake", "Mary Blake": "Mary Blake",
    "Walter Blake": "Walter Blake", "Master Blake": "le jeune maître Blake",
    "Marquess Blake": "le marquis Blake", "Blake Family": "la famille Blake",
    "monstrous Blake": "le Blake monstrueux",
    "Simon Coventry": "Simon Coventry", "Doctor Callaghan": "le docteur Callaghan",
    "Father Sinnott": "le père Sinnott",
    "Miss Barbosa": "Mlle Barbosa", "Miss Callaghan": "Mlle Callaghan",
    "Miss Darroch": "Mlle Darroch", "Miss Deane": "Mlle Deane",
    "Miss Hisham": "Mlle Hisham", "Miss Joyce": "Mlle Joyce",
    "Miss Mantovani": "Mlle Mantovani", "Miss McLeod": "Mlle McLeod",
    "Miss Murphy": "Mlle Murphy", "Miss Quinn": "Mlle Quinn",
    "Missus D'Arcy": "Mme D’Arcy", "Missus Erickson": "Mme Erickson",
    "Missus Lau": "Mme Lau",
    "Mister Coventry": "M. Coventry", "Mister Doyle": "M. Doyle",
    "Mister Dupré": "M. Dupré", "Mister Hunter": "M. Hunter",
    "Mister O'Meara": "M. O’Meara", "Mister Skerritt": "M. Skerritt",
    "Mister Toussaint": "M. Toussaint", "Mister Varley": "M. Varley",
    "Mister Ó Finn": "M. Ó Finn", "The manager's": "le gérant",
    "O'Connor family": "la famille O’Connor", "Quinn family": "la famille Quinn",
    "acolyte": "un acolyte", "a practitioner": "un praticien",
    "a shadowy figure": "une silhouette dans l’ombre", "a third party": "un tiers",
    "an angel": "un ange", "the entity": "l’entité", "ghost": "un fantôme",
    "ghosts": "des fantômes", "first ghost": "le premier fantôme",
    "father's ghost": "le fantôme de son père", "crows": "les corbeaux",
    "guest": "un invité", "guests": "les invités", "staff": "le personnel",
    "everyone": "tout le monde", "himself": "lui-même", "self": "soi-même",
    "son": "un fils", "child": "un enfant", "family": "la famille",
    "wife": "une épouse", "his dead wife": "son épouse défunte",
    "her husband": "son mari", "fiancé": "un fiancé", "dead friend": "un ami défunt",
    "cook": "la cuisinière", "witch": "une sorcière", "executor": "un exécuteur testamentaire",
    "kidnapper": "un ravisseur", "first millionaire": "le premier millionnaire",
    "descendant ": "un descendant ", "humanity": "l’humanité",

    # -- places -------------------------------------------------------------
    "manor": "le manoir", "ancestral home": "la demeure ancestrale",
    "the catacombs": "les catacombes", "gardens": "les jardins",
    "hedge maze": "le labyrinthe de haies", "well": "le puits",
    "local area": "les environs", "village": "le village",
    "father's homeland": "la terre de son père", "land": "la terre",
    "east corridor": "le couloir est", "east tower": "la tour est",
    "north east corridor": "le couloir nord-est", "north west corridor": "le couloir nord-ouest",
    "south east corridor": "le couloir sud-est", "south west corridor": "le couloir sud-ouest",
    "upper corridors": "les couloirs supérieurs", "changing room": "le vestiaire",
    "wardrobe": "la penderie", "jewellery shop": "la bijouterie",
    "missing doorway": "la porte disparue", "secret doorway": "le passage secret",
    "the portal": "le portail", "a place of power": "un lieu de pouvoir",
    "beyond the grave": "l’au-delà",

    # -- objects & evidence -------------------------------------------------
    "a tool": "un outil", "alcohol": "l’alcool", "an invite": "une invitation",
    "ashes": "des cendres", "anchor": "une ancre", "headdress": "une coiffe",
    "heirloom": "un bien de famille", "jewellery": "des bijoux", "jewels": "des joyaux",
    "valuables": "des objets de valeur", "stolen vase": "le vase volé",
    "letter": "une lettre", "note": "un billet", "document": "un document",
    "record": "un registre", "communications": "des communications",
    "code": "un code", "name": "un nom", "money": "de l’argent",
    "wealth": "la fortune", "luggage": "des bagages", "his luggage": "ses bagages",
    "personal belongings": "les effets personnels",
    "wife's belongings": "les affaires de son épouse",
    "photo of Miss Deane": "la photo de Mlle Deane",
    "telegraph machine": "le télégraphe", "modern techniques": "les techniques modernes",
    "skeleton key": "un passe-partout", "lock": "une serrure",
    "stone": "une pierre", "drug": "une drogue", "drugs": "des drogues",
    "substances": "des substances", "sigil under her bed": "le sceau sous son lit",
    "signed by her": "signé de sa main", "sketch": "un croquis",
    "tattoo": "un tatouage", "treasure": "un trésor", "My arrival": "mon arrivée", "request for a horse": "une demande de cheval",

    # -- abstractions -------------------------------------------------------
    "abilities": "des dons", "magical abilities": "des dons magiques",
    "magic": "la magie", "magical fabrication": "une fabrication magique",
    "ancient power": "un pouvoir ancien", "ancient duty": "un devoir ancestral",
    "pagan beliefs": "des croyances païennes", "his faith": "sa foi",
    "his society": "sa société", "research": "des recherches",
    "medical knowledge": "des connaissances médicales", "strategy": "une stratégie",
    "curse": "une malédiction", "doom": "une fatalité", "death": "la mort",
    "battle": "une bataille", "sacrifice": "un sacrifice", "ritual": "un rituel",
    "summoning ritual": "un rituel d’invocation", "séance": "la séance",
    "séance ": "la séance ", "séance's aftermath": "les suites de la séance",
    "soul": "une âme", "heart": "un cœur", "dream": "un rêve",
    "reality": "la réalité", "future": "l’avenir", "the future": "l’avenir",
    "past": "le passé", "their past": "leur passé", "old life": "l’ancienne vie",
    "new life": "une vie nouvelle", "own life": "sa propre vie",
    "life to see it.": "de vivre assez pour le voir.",
    "aunt's shadow": "l’ombre de sa tante", "affair": "une liaison",
    "relationship": "une liaison", "friendship": "une amitié", "love": "l’amour",
    "closure": "l’apaisement", "help": "de l’aide", "harm": "du mal",
    "plot": "un complot", "secret": "un secret", "meeting": "un rendez-vous",
    "plea for help": "un appel à l’aide", "fraudulence": "l’imposture",
    "health": "la santé", "addiction": "une dépendance", "terror": "la terreur",
    "daze": "un état second", "manor's effect": "l’effet du manoir",
    "speaking in unison": "de parler à l’unisson", "tongues": "des langues inconnues",
    "his society ": "sa société ", "penny-pinching": "l’avarice",
    "hard work": "un dur labeur", "work": "le travail", "horses": "les chevaux",
    "powerful Milesian ancestors": "de puissants ancêtres milésiens",
    "Miss Deane's departure": "le départ de Mlle Deane",
    "Miss Deane's disappearance": "la disparition de Mlle Deane",
    "Miss Deane can't help": "Mlle Deane ne peut rien",
    "Walter Blake isn't real": "Walter Blake n’existe pas",
    "he has no magic": "il n’a aucun pouvoir",
    "not here": "il n’est pas ici", "so": "à ce point",
    "gone up in flames": "parti en fumée", "broken": "hors d’usage",
    "fixed": "réparé", "valid": "fondé", "strange": "étrange",
    "discerning": "pénétrant", "distracting": "distrait", "exhausted": "épuisé",
    "tired": "las", "sick": "souffrant", "obsessed": "obsédée",
    "cursed": "maudit", "trapped": "prisonnier", "forgotten": "oublié",
    "reviled": "honni", "stained": "taché", "immortalised": "immortalisé",
    "blackmailed": "victime d’un chantage", "had a cold": "était souffrante",
    "miscarried": "a perdu son enfant", "played": "a joué",
    "ate": "a mangé", "fought": "s’est battu", "recognised": "l’a reconnu",
    "killed": "l’a tué", "kidnapped": "l’a enlevé", "forgot": "a oublié",
    "forged": "a contrefait", "rejected": "l’a repoussée",
    "reprimanded": "a été réprimandée", "repaired": "a réparé",
    "chased": "a donné la chasse", "descended": "est descendu",
    "wandering": "errer", "undressed in": "s’est dévêtu dans",
    "stalked through": "a rôdé dans", "brought to": "a conduit à",
    "lost in": "s’est perdu dans", "return to": "revenir vers",
    "write to": "écrire à", "join the Freemasons": "rejoindre les francs-maçons",

    # -- verb-like tokens (infinitives) -------------------------------------
    "bind": "lier", "bless": "bénir", "coerce": "contraindre", "conceal": "dissimuler",
    "condemn": "condamner", "conduct": "conduire", "consume": "consommer",
    "cover": "couvrir", "divine": "deviner", "donate": "faire don",
    "drugged": "droguer", "drugging": "droguer", "escape": "fuir",
    "expose": "démasquer", "experiencing": "vivre", "experimenting": "expérimenter",
    "exploring": "explorer", "find": "trouver", "forge": "forger",
    "free": "libérer", "freeing": "libérer", "hid": "cacher", "hide": "cacher",
    "invade": "envahir", "investigating": "enquêter", "killing": "tuer",
    "learn": "apprendre", "leave": "partir", "live": "vivre", "lose": "perdre",
    "mourn": "pleurer", "murder": "assassiner", "praying": "prier",
    "promised": "promettre", "protect": "protéger", "provide": "subvenir",
    "proving": "prouver", "reclaim": "reprendre", "reconnect": "renouer",
    "recruit": "recruter", "redeem": "racheter", "release": "délivrer",
    "remove": "écarter", "resurrect": "ressusciter", "restore": "rétablir",
    "revenge": "se venger", "risking": "risquer", "rob": "dérober",
    "save": "sauver", "scatter": "disperser", "see": "voir", "speak": "parler",
    "start": "commencer", "steal": "voler", "stitch": "coudre", "stop": "arrêter",
    "store": "entreposer", "study": "étudier", "suffer": "souffrir",
    "suffering": "souffrir", "summon": "invoquer", "take": "prendre",
    "talk": "parler", "threaten": "menacer", "transfer": "transférer",
    "transport": "transporter", "trap": "piéger", "trapping": "piéger",
    "tricked": "duper", "unlocking": "déverrouiller",
    "bleeding": "se répandre",
    "playing": "jouer",

    # -- harvested from the coverage check ----------------------------------
    "the séance": "la séance",
    "entertained": "les divertissements",
    "reading": "une consultation",              # Mantovani offers a fortune reading
    "necklace with HOGD crest": "un collier au blason H.O.G.D.",
    "packs": "des liasses",                     # REVIEW: token sits on "Burnt Symbols";
                                                # "packs" is ambiguous in the original too
}
