#!/usr/bin/env python3
"""
Evidence descriptions — Adventure Creator inventory properties 0, 1 and 2
(Description, Updated Label, Updated Description). 862 strings, ~12k words.

These are what fills the evidence card on the mindmap and in the journal, and they
are the largest single pool outside the dialogue. They reach the screen through
EHInvItem.Description -> GetProperty(n).GetDisplayValue(language) -> GetTranslation,
so they are injected by source string like the rest of the UI layer.

Register: Ward's own case notes — first person, sober period French, passé composé.
Leading and trailing whitespace is reapplied automatically from the source, so the
French here is written trimmed.
"""


# ------------------------------------------------------------------ helpers
# Whole families of descriptions are formulaic. Generating them keeps the
# gender agreement consistent and makes a missing character impossible to hide.

def _fight(who, fem=False):
    return f"Serait-ce {who} qui s’est disputé{'e' if fem else ''} avec Mlle Deane ?"


def _profile(who, fem=False):
    p = "elle" if fem else "lui"
    return (f"Je puis dresser le profil {who} en l’analysant, en m’entretenant avec {p} ou "
            f"avec d’autres invités à son sujet, et en fouillant le manoir.")


def _guest(what):
    return f"Un invité de l’hôtel. {what}"


def _guest_f(what):
    return f"Une invitée de l’hôtel. {what}"


def _search_quarters(who, fem=False):
    d = "de" if not fem else "de"
    return (f"Je devrais fouiller les quartiers {d} {who} pour voir s’ils recèlent quoi que ce soit "
            f"d’utile. Je suppose qu’{'elle' if fem else 'il'} loge au sous-sol du manoir.")


def _room_of(who):
    return f"Je pourrais trouver des renseignements utiles en fouillant la chambre {who}."


def _quarters_of(who, fem=False):
    return (f"Je devrais fouiller les quartiers {who} pour voir s’ils recèlent quoi que ce soit "
            f"d’utile.")


DESCRIPTIONS = {
    # ------------------------------------------------------------- A
    "A sequence of numbers.": "Une suite de chiffres.",
    "Someone fought with Miss Deane on Tuesday night. If I can determine where the guests were "
    "then, I can narrow down who it was she was arguing with.":
        "Quelqu’un s’est querellé avec Mlle Deane mardi soir. Si je parviens à établir où se "
        "trouvaient les invités à cette heure-là, je pourrai resserrer le cercle.",
    "8pm Tuesday 26th October": "Mardi 26 octobre, 20 h",
    "An elaborate crest, worn with pride. I don't recognise the symbol itself, however.":
        "Un blason ouvragé, porté avec fierté. Le symbole lui-même ne me dit pourtant rien.",
    "Holy Order Of The Golden Dawn Necklace": "Collier de l’Ordre de l’Aube dorée",
    "Missus Erickson is a member of an occult organisation.":
        "Mme Erickson appartient à une organisation occulte.",
    "I'm told Master Blake enjoys spending time in the library, I should investigate the books he "
    "has had read to him.":
        "On me dit que le jeune maître Blake aime passer du temps à la bibliothèque ; je devrais "
        "m’intéresser aux livres qu’on lui a lus.",
    "Can I find proof of somebody building a legacy through charitable deeds?":
        "Puis-je trouver la preuve qu’un homme s’est bâti une postérité par des œuvres charitables ?",
    "A note on key locations I made based on a conversation I overheard.":
        "Une note sur l’emplacement des clés, rédigée d’après une conversation surprise.",
    "A gateway to another world...": "Une porte vers un autre monde…",
    "There is a third ancient bloodline mentioned, but who is it?":
        "Une troisième lignée ancienne est mentionnée — mais laquelle ?",
    "An old legend of a dwarf magician known for mind control and drinking the blood of its "
    "subjects. Susceptible to the wood of yew.":
        "Une vieille légende de magicien nain, réputé pour asservir les esprits et boire le sang de "
        "ses victimes. Le bois d’if lui est fatal.",
    "The staff seem quite fond of the young Master.":
        "Le personnel paraît fort attaché au jeune maître.",
    "A sigil that reveals doors hidden behind illusionary walls.":
        "Un sceau qui révèle les portes dissimulées derrière des murs d’illusion.",
    "An empty glass with the scent of strong alcohol about it.":
        "Un verre vide qui sent l’alcool fort.",
    "These people have already been cleared.": "Ces personnes sont déjà mises hors de cause.",
    "How I, and presumably the others, experience the hotel seems to be altered by repeated "
    "exposure to that dream.":
        "Ma perception de l’hôtel — et sans doute celle des autres — semble altérée par la "
        "répétition de ce rêve.",
    "An old safe. It's locked.": "Un vieux coffre-fort. Il est fermé.",
    "An ancient machine comprising of ominous stones with holes in them. Dark brown stains ring "
    "the holes. They seem connected to the vats...":
        "Une machine ancienne faite de pierres inquiétantes, percées de trous. Des taches d’un brun "
        "sombre en cernent les bords. Elles semblent reliées aux cuves…",
    "Sketches of something labelled 'my angel'.":
        "Des croquis de quelque chose, légendés « mon ange ».",
    "Servants of God.": "Les serviteurs de Dieu.",
    "The hedge maze is a ruin. Everyone's life hangs in the balance. I must catch the culprit "
    "before further harm is caused.":
        "Le labyrinthe est en ruine. Toutes les vies sont en jeu. Il me faut prendre le coupable "
        "avant qu’il ne fasse d’autres victimes.",
    "Doctor Ruairí Callaghan is her nephew and apprentice.":
        "Le docteur Ruairí Callaghan est son neveu et son apprenti.",
    "A chef's apron I found in the kitchen.": "Un tablier de cuisine trouvé aux cuisines.",
    "A hotel guest. An archaeologist from Egypt.": _guest_f("Une archéologue venue d’Égypte."),
    "Doctor Callaghan's equipment looks like a camera but also more. I should ask him about his.":
        "L’appareil du docteur Callaghan ressemble à une chambre photographique, mais pas "
        "seulement. Je devrais l’interroger à son sujet.",
    "I should enquire as to Miss Deane's whereabouts with the manager Mister Varley.":
        "Je devrais m’enquérir auprès du gérant, M. Varley, de ce qu’il est advenu de Mlle Deane.",
    "Who or what is the shadowy figure I caught a glimpse of? A man, a figment of my imagination, "
    "or something more?":
        "Qui, ou quoi, était cette silhouette entrevue dans l’ombre ? Un homme, une chimère de mon "
        "esprit, ou quelque chose de plus ?",
    "I should ask around about Tír na nÓg.": "Je devrais me renseigner sur Tír na nÓg.",
    "I want to find out if there is anything strange to the dreams here - I need three other "
    "points of information to spot a pattern.":
        "Je veux savoir si ces rêves ont quelque chose d’étrange — il me faut trois autres "
        "témoignages pour déceler une régularité.",
    "There are only two possible suspects who could have worn the skull mask, I should find out "
    "which one did.":
        "Deux suspects seulement ont pu porter le masque de crâne ; il me faut établir lequel.",
    "A sigil is inscribed inside the locket.": "Un sceau est gravé à l’intérieur du médaillon.",
    "Help find a way for Missus Joyce to repent for her actions.":
        "Aider Mme Joyce à trouver le moyen d’expier ses actes.",
    "A portrait of the Blake Family.": "Un portrait de la famille Blake.",
    "A master key for all bedrooms in the atrium, for use by the staff.":
        "Un passe-partout ouvrant toutes les chambres de l’atrium, à l’usage du personnel.",
    "I should attend the Silent Dinner.": "Je devrais assister au Dîner silencieux.",
    "Doctor Callaghan seeks to burst from his Aunt's formidable shadow.":
        "Le docteur Callaghan cherche à s’arracher à la formidable ombre de sa tante.",
    "I suspect she'd rather not be talking at all.":
        "Je soupçonne qu’elle préférerait ne pas parler du tout.",
    "A babelstone, used for translating ancient texts. This one helps with the Enochian language, "
    "reputed to be the language of angels and similar celestial beings.":
        "Une babelstone, servant à traduire les textes anciens. Celle-ci porte sur l’énochien, "
        "réputé être la langue des anges et autres créatures célestes.",
    "What could be the cause of the strife between Missus Joyce and Miss Mantovani?":
        "Quelle peut être la cause de la discorde entre Mme Joyce et Mlle Mantovani ?",
    "A mostly unintelligible note apparently addressed to Father Sinnott.":
        "Un billet presque illisible, apparemment adressé au père Sinnott.",
    "A box of baking soda. Half of it has been used, but there's still plenty left.":
        "Une boîte de bicarbonate de soude. À moitié entamée, mais il en reste largement.",
    "A key that opens every door in the basement.":
        "Une clé qui ouvre toutes les portes du sous-sol.",
    "A collection of keys opening the men's dormitory, the South West corridor, and most rooms in "
    "the basement.":
        "Un trousseau ouvrant le dortoir des hommes, le couloir sud-ouest et la plupart des pièces "
        "du sous-sol.",
    "It would be prudent to try alternative routes into the basement to bypass the staff, or to "
    "try again when they are busy.":
        "Il serait prudent de chercher d’autres accès au sous-sol pour éviter le personnel, ou de "
        "revenir quand il sera occupé.",
    "Miss Callaghan is a local wise woman, a witch of sorts .":
        "Mlle Callaghan est une femme savante du pays, une manière de sorcière.",
    "The magical duties that Miss Callaghan undertakes as a bean draoí.":
        "Les devoirs magiques dont Mlle Callaghan s’acquitte en tant que bean draoí.",
    "An envelope containing all the material Miss Evelyn Deane gathered on Miss Ivy McLeod. I "
    "shan't be opening it.":
        "Une enveloppe contenant tout ce que Mlle Evelyn Deane avait réuni sur Mlle Ivy McLeod. Je "
        "ne l’ouvrirai pas.",
    "A letter from our missing woman, Evelyn Deane, attempting to blackmail Miss McLeod regarding "
    "her relationship with Missus Lau.":
        "Une lettre de notre disparue, Evelyn Deane, tentant de faire chanter Mlle McLeod au sujet "
        "de sa liaison avec Mme Lau.",
    "The Blake family are descended from the sorcerer rulers of the Milesians.":
        "Les Blake descendent des souverains sorciers milésiens.",
    "A complete and uncensored examination of the Blake History - there is no horror spared. The "
    "letter \"P\" has been scrawled with red ink in the margins.":
        "Un examen complet et sans fard de l’histoire des Blake — aucune horreur n’y est épargnée. "
        "La lettre « P » a été griffonnée à l’encre rouge dans la marge.",
    "Built on conquered land by Edward Blake in 1655.":
        "Bâti sur une terre conquise par Edward Blake en 1655.",
    "The portrait of the Blake Family, found within the residence.":
        "Le portrait de la famille Blake, trouvé dans la résidence.",
    "A key to the Blake family's private wing of the manor, which is accessed through the basement "
    "or the manor's ground floor.":
        "Une clé de l’aile privée des Blake, à laquelle on accède par le sous-sol ou par le "
        "rez-de-chaussée du manoir.",
    "The hotel seems to be getting supplies in for the remainder of the event.":
        "L’hôtel semble se réapprovisionner pour le reste de la réception.",
    "Miss Mantovani is not well.": "Mlle Mantovani n’est pas en bonne santé.",
    "A book containing information on some of the old Irish Gods.":
        "Un ouvrage traitant de quelques-uns des anciens dieux d’Irlande.",
    "Titled \"A Guide to Common Housekeeping and Similar Concerns\", this book holds a wealth of "
    "domestic information.":
        "Intitulé « Guide de la tenue de maison et sujets connexes », ce livre est une mine de "
        "renseignements domestiques.",
    "Medium sized boot prints found out in the hedge maze.":
        "Des empreintes de bottes de taille moyenne, relevées dans le labyrinthe de haies.",
    "A bottle of good alcohol acquired in the hotel.":
        "Une bouteille de bon alcool obtenue à l’hôtel.",
    "A normal bottle of water.": "Une bouteille d’eau ordinaire.",
    "The holy ribbon.": "Le ruban sacré.",
    "A bridge game held in the library on Tuesday evening.":
        "Une partie de bridge tenue à la bibliothèque le mardi soir.",
    "These people were playing bridge at the time Miss Deane was having her fight in the hedge "
    "maze.":
        "Ces personnes jouaient au bridge à l’heure où Mlle Deane se querellait dans le labyrinthe.",
    "A striking brooch worn around the collar.":
        "Une broche saisissante, portée au col.",
    "A tin bucket, probably used for cleaning.":
        "Un seau de fer-blanc, sans doute destiné au nettoyage.",
    "A burial record for a Miss Alessandra Barbosa Mariano. It lists only one surviving relative - "
    "Ines Barbosa.":
        "Un acte d’inhumation au nom de Mlle Alessandra Barbosa Mariano. Une seule parente "
        "survivante y figure : Ines Barbosa.",
    "That dream contains buried messages of my home used to invoke feelings of longing that are "
    "being manipulated into making me - and others - want to attend the séance.":
        "Ce rêve recèle des messages enfouis, tirés de mon pays, qui éveillent une nostalgie dont "
        "on se sert pour nous pousser — moi et les autres — à assister à la séance.",
    "A burnt letter from an unknown contact, informing Hazel Erickson that she is void of magic "
    "and cannot learn how to wield the unholy powers.":
        "Une lettre brûlée, d’un correspondant inconnu, informant Hazel Erickson qu’elle est "
        "dépourvue de tout pouvoir et ne saurait apprendre à manier les puissances impies.",
    "Symbols on burnt paper. Some of them are charred beyond visibility.":
        "Des symboles sur du papier brûlé. Certains sont calcinés au point d’être illisibles.",
    "Missus Lau has a collection of Miss Deane's documents, presumably stolen.":
        "Mme Lau détient une collection de documents appartenant à Mlle Deane, sans doute dérobés.",
    "The hotel's housekeeper.": "La gouvernante de l’hôtel.",
    "A hotel guest. The medium of honour at the Grand Séance.":
        _guest_f("Le médium d’honneur de la Grande Séance."),
    "A tragic carriage accident involving the Blake family left the Marquess a widower.":
        "Un tragique accident de voiture impliquant la famille Blake a laissé le marquis veuf.",
    "A carriage accident killed Mary Blake and left the young Master Blake crippled.":
        "Un accident de voiture a tué Mary Blake et laissé le jeune maître Blake infirme.",
    "A key to the catacombs under the manor.":
        "Une clé des catacombes situées sous le manoir.",
    "Ancient tunnels beneath the house, filled with long-forgotten tombs. Are there more?":
        "D’anciens souterrains sous la maison, emplis de tombeaux oubliés depuis longtemps. Y en "
        "a-t-il d’autres ?",
    "A hotel guest. A carefree rake from south Dublin.":
        _guest("Un libertin insouciant du sud de Dublin."),
    "A lockbox that requires a 4 digit code to open.":
        "Un coffret qui s’ouvre à l’aide d’un code à quatre chiffres.",
    "A Celtic Cross, similar to many worn by Catholics in the country.":
        "Une croix celtique, semblable à beaucoup de celles que portent les catholiques du pays.",
    "A cross in the Celtic style. A sign of his faith mingled with one of his heritage.":
        "Une croix de style celtique. Un signe de sa foi mêlé à un signe de ses origines.",
    "I found a ceremonial dagger inside Mister Skerritt's lockbox.":
        "J’ai trouvé une dague cérémonielle dans le coffret de M. Skerritt.",
    "A hidden chamber under the church.": "Une chambre dissimulée sous l’église.",
    "Miss McLeod came to the event with her chaperone, Missus Lau.":
        "Mlle McLeod est venue à la réception avec son chaperon, Mme Lau.",
    "Miss Ivy McLeod has a live in chaperone, Missus Victoria Lau.":
        "Mlle Ivy McLeod a un chaperon à demeure, Mme Victoria Lau.",
    "There are dark smudges on her hands, perhaps she has been drawing?":
        "Ses mains portent des traces sombres ; aurait-elle dessiné ?",
    "I should check into the hotel.": "Je devrais m’enregistrer à l’hôtel.",
    "I should search the luggage room for clues.":
        "Je devrais fouiller la consigne à bagages en quête d’indices.",
    "The cook's office, used to separate the logistics of the kitchen with the actual workings of "
    "it.":
        "Le bureau de la cuisinière, qui sépare l’intendance des cuisines de leur travail même.",
    "A bench for mixing chemicals that's located in the Laundry.":
        "Une paillasse à mélanger les produits, installée dans la buanderie.",
    "Miss Mantovani taught me her 'sigil key' to open the magical lock and find her payment.":
        "Mlle Mantovani m’a enseigné sa « clé de sceau » pour ouvrir la serrure magique et trouver "
        "ses gages.",
    "I found what can only be described as a primitive charm stuffed up the chimney in the room of "
    "Miss Deane. Was this placed before or after her disappearance?":
        "J’ai trouvé ce qu’il faut bien appeler un charme grossier, enfoncé dans la cheminée de la "
        "chambre de Mlle Deane. A-t-il été placé avant ou après sa disparition ?",
    "Burns on the armchair from a dropped cigar.":
        "Des brûlures sur le fauteuil, laissées par un cigare tombé.",
    "There's a strong smell of cigars on the man's breath and his moustache is stained with them.":
        "L’haleine de cet homme sent fortement le cigare, et sa moustache en est jaunie.",
    "A set of circled numbers I found inside a strange book. 74, 53, 26, in that order.":
        "Une série de nombres entourés, trouvée dans un livre étrange. 74, 53, 26, dans cet ordre.",
    "I found Mister O'Meara and Miss McLeod meeting without the girl's chaperone. They met to "
    "discuss the business of marriage.":
        "J’ai surpris M. O’Meara et Mlle McLeod en tête-à-tête, sans le chaperon de la jeune fille. "
        "Ils s’entretenaient d’un projet de mariage.",
    "A cleaning solution I made.": "Une solution nettoyante de ma composition.",
    "A note to Miss Deane requesting to meet found in a jacket pocket in the cloakroom.":
        "Un billet adressé à Mlle Deane, demandant un rendez-vous, trouvé dans la poche d’une veste "
        "au vestiaire.",
    "Mister Ó Finn follows a code that considers all people, places, and creatures as equal.":
        "M. Ó Finn suit un code qui tient pour égaux tous les êtres, tous les lieux et toutes les "
        "créatures.",
    "Sheets of paper with mysterious dots on them - and little else.":
        "Des feuillets couverts de points mystérieux — et de guère plus.",
    "Chilling, whilst attending the Silent Dinner I observed the Shade of Missus Mary Blake "
    "turning her back on her husband. What does this bode for us?":
        "Glaçant : lors du Dîner silencieux, j’ai vu l’ombre de Mme Mary Blake tourner le dos à son "
        "époux. Que faut-il en augurer ?",
    "I should find some way to commune with the ghost I found at the firepit in the hedge maze.":
        "Je devrais trouver le moyen de communier avec le fantôme du foyer, dans le labyrinthe.",
    "Miss Mantovani will be the conductor of the séance that's taking place on Sunday evening.":
        "Mlle Mantovani officiera à la séance qui se tiendra dimanche soir.",
    "Missus Erickson confessed to me she is a magical void, lacking any abilities. However, she "
    "remains undeterred in carrying out her ritual. Mister Toussaint may know how to sway her from "
    "her chosen course.":
        "Mme Erickson m’a avoué n’avoir aucun pouvoir, être un vide magique. Elle n’en démord pas "
        "moins de son rituel. M. Toussaint saura peut-être l’en détourner.",
    "There appears to be some kind of connection between Father Sinnott and Mister Doyle, I should "
    "dig deeper into their history.":
        "Il semble exister un lien entre le père Sinnott et M. Doyle ; je devrais creuser leur passé.",
    "The door to the cook's office in the kitchen.":
        "La porte du bureau de la cuisinière, dans les cuisines.",
    "Discs made of old copper.": "Des disques de vieux cuivre.",
    "A hotel guest. An English noblewoman and head of her household.":
        _guest_f("Une aristocrate anglaise, chef de sa maison."),
    "Letters to Mister Doyle from Father Sinnott. It sounds like the two were plotting something "
    "related to... well, I am unsure what. A ritual, perhaps?":
        "Des lettres du père Sinnott à M. Doyle. Les deux hommes semblaient tramer quelque chose "
        "en rapport avec… eh bien, je ne sais trop quoi. Un rituel, peut-être ?",
    "An exchange between Miss Mantovani and Mister Dupré, arranging a meeting for this weekend to "
    "discuss funeral rites. 6pm, Saturday, in the drawing room.":
        "Un échange entre Mlle Mantovani et M. Dupré, fixant un rendez-vous ce week-end pour parler "
        "de rites funéraires. Samedi, 18 h, au petit salon.",
    "An array of jewellery, the sort worn by spiritualists and show-women.":
        "Un assortiment de bijoux, du genre que portent les spirites et les femmes de spectacle.",
    "Simon Coventry has been tapping into the entity's dream and reshaping reality throughout the "
    "estate.":
        "Simon Coventry puise dans le rêve de l’entité et refaçonne la réalité dans tout le domaine.",
    "They must be difficult to see through... The damage must be recent, or surely he'd have had "
    "them fixed.":
        "On doit y voir bien mal… La fêlure doit être récente, sans quoi il les aurait fait "
        "réparer.",
    "Walter Blake is chair-bound.": "Walter Blake est cloué dans un fauteuil.",
    "A cross of Saint Brigid, one of the Irish patron Saints.":
        "Une croix de sainte Brigide, l’une des patronnes de l’Irlande.",
    "A roughly made crown of wood and leather.":
        "Une couronne grossière, de bois et de cuir.",
    "Pagan Circlet": "Diadème païen",
    "A roughly made circlet of wood and leather.":
        "Un diadème grossier, de bois et de cuir.",
    "There is an unusual number of crows about these grounds...":
        "Il y a sur ces terres un nombre inhabituel de corbeaux…",
    "A sigil that appeared on the wall in Mister Ó Finns room once the magical phrase was spoke.":
        "Un sceau apparu sur le mur de la chambre de M. Ó Finn dès que la formule magique fut "
        "prononcée.",
    "A finely-crafted tattoo in a design I don't recognise.":
        "Un tatouage finement exécuté, d’un motif qui m’est inconnu.",
    "Tattoo Of Maman Brigitte": "Tatouage de Maman Brigitte",
    "He bears the mark of a Haitian Loa. She seems to be some incarnation of the Irish Goddess "
    "Bríd.":
        "Il porte la marque d’un loa haïtien. Elle paraît être une incarnation de la déesse "
        "irlandaise Bríd.",
    "The Quinn family is rumoured to be cursed, such that many of the members die young.":
        "La famille Quinn passe pour maudite : nombre des siens meurent jeunes.",
    "A key to room 13.": "Une clé de la chambre 13.",
    "The hotel's stablemaster and groundsman.":
        "Le maître d’écurie et jardinier de l’hôtel.",
    "I lost the trail in the hedge maze. It came to an abrupt end. Where could they have possibly "
    "gone from here?":
        "J’ai perdu la piste dans le labyrinthe. Elle s’interrompt net. Où ont-ils bien pu aller "
        "depuis là ?",
    "The Reverend has been recently murdered.":
        "Le révérend a été assassiné récemment.",
    "He does not look well.": "Il n’a pas bonne mine.",
    "The room's a wreck, someone was drinking while they were writing - a dangerous combination.":
        "La pièce est sens dessus dessous ; quelqu’un buvait en écrivant — dangereux mélange.",
    "Mary Blake, the Marquess' wife, had recently passed.":
        "Mary Blake, l’épouse du marquis, était morte depuis peu.",
    "The notes are sealed by some powerful and complex magic. I may need to look elsewhere if I'm "
    "to find a way to decipher it.":
        "Ces notes sont scellées par une magie puissante et complexe. Il me faudra chercher "
        "ailleurs le moyen de les déchiffrer.",
    "A series of notes and drawings obsessively concerning a particular vase.":
        "Une série de notes et de dessins portant obstinément sur un vase en particulier.",
    "Miss Mantovani is suffering from some kind of ailment. I wonder if she's has been seeing a "
    "Doctor whilst staying at the Manor?":
        "Mlle Mantovani souffre de quelque mal. A-t-elle consulté un médecin durant son séjour au "
        "manoir ?",
    "A discarded note found in the cleaning closet. Whoever wrote this lost their bible, but then "
    "remembered they \"left it handy for mass on Sunday\".":
        "Un billet jeté, trouvé dans le placard à balais. Son auteur avait égaré sa bible, avant de "
        "se rappeler l’avoir « mise de côté pour la messe de dimanche ».",
    "He has a careful eye on the goings on, as if taking in every detail.":
        "Il observe attentivement ce qui se passe, comme s’il en relevait chaque détail.",
    "What does that code refer to? I wonder if there is somebody or someplace I can learn that "
    "from?":
        "À quoi renvoie ce code ? Existe-t-il quelqu’un, ou quelque endroit, où je pourrais "
        "l’apprendre ?",
    "I should follow the path laid out for me by the ghost and uncover what really happened here.":
        "Je devrais suivre le chemin que le fantôme m’a tracé et découvrir ce qui s’est réellement "
        "passé ici.",
    "A pile of discs in various materials.": "Un tas de disques de diverses matières.",
    "She does not seem impressed with something - the event, the attendees, or me perhaps?":
        "Quelque chose ne l’impressionne guère — la réception, les invités, ou moi-même ?",
    "Percival Blake's portrait is painted next to a distinctive archway.":
        "Le portrait de Percival Blake est peint auprès d’une arche remarquable.",
    "Something about his eyes gives me the impression he's only half in the room.":
        "Quelque chose dans son regard me donne l’impression qu’il n’est qu’à demi présent.",
    "Doctor Callaghan's owns a strange camera, can it capture images of the dead?":
        "Le docteur Callaghan possède un étrange appareil photographique ; peut-il saisir l’image "
        "des morts ?",
    "Doctor Callaghan's studies in magic have led him to own a spirit camera. According to him, it "
    "can capture images of spirits long dead.":
        "Ses études de magie ont conduit le docteur Callaghan à se procurer un appareil à spectres. "
        "À l’en croire, il saisit l’image d’esprits morts depuis longtemps.",
    "Doctor Callaghan has asked me to prove to his aunt that his methods, though new, are as valid "
    "as her own.":
        "Le docteur Callaghan m’a demandé de prouver à sa tante que ses méthodes, quoique "
        "nouvelles, valent bien les siennes.",
    "A hotel guest. A traveller and protector of the lands.":
        _guest("Un voyageur, protecteur des terres."),
    "Things do not look good for Miss Mantovani - she'll be dead sooner rather than later.":
        "L’avenir de Mlle Mantovani est sombre — elle mourra plus tôt que tard.",
    "Doyle has taken to self medicating.": "Doyle s’est mis à se soigner lui-même.",
    "Doyle has appeared to have sketched maps of what looks like the area encompassing Blake "
    "Manor.":
        "Doyle semble avoir tracé des plans de ce qui paraît être les environs de Blake Manor.",
    "Drawings of a young woman - is this Evelyn Deane?":
        "Des dessins d’une jeune femme — serait-ce Evelyn Deane ?",
    "Drawings of a young woman - Mister Dupré's recently departed friend, Laura.":
        "Des dessins d’une jeune femme — Laura, l’amie récemment disparue de M. Dupré.",
    "I should try to enter that dream in a lucid state so I can decipher its message.":
        "Je devrais tenter d’entrer dans ce rêve en pleine conscience, afin d’en déchiffrer le "
        "message.",
    "A strange symbol I saw carved into a standing stone in my dream.":
        "Un symbole étrange, vu gravé sur un menhir dans mon rêve.",
    "A jug of water in which the water is ever-so-slightly cloudy - as if it may have been "
    "contaminated.":
        "Une carafe dont l’eau est très légèrement trouble — comme si on l’avait souillée.",
    "Mister Ó Finn is a druid.": "M. Ó Finn est un druide.",
    "Either he's recently been moving around in old spaces or he has not cleaned this suit in a "
    "while.":
        "Ou bien il a récemment fréquenté de vieux lieux, ou bien il n’a pas fait nettoyer ce "
        "costume depuis longtemps.",
    "According to the ledger the Estate is in a drastic position.":
        "À en croire le registre, le domaine est dans une situation critique.",
    "A sigil that unlocks doors that have been magically sealed.":
        "Un sceau qui déverrouille les portes scellées par magie.",
    "A strange sigil I saw in my dream that woke me on using it.":
        "Un sceau étrange, vu en rêve, qui m’a réveillé dès que je m’en suis servi.",
    "This sigil fills me with a deep sense of sadness and the fear of being trapped. Are these "
    "emotions my own, or do they belong to someone else?":
        "Ce sceau m’emplit d’une profonde tristesse et de la crainte d’être pris au piège. Ces "
        "émotions sont-elles miennes, ou appartiennent-elles à un autre ?",
    "Dún (Close)": "Dún (Fermer)",
    "She seems a welcoming and conversational sort.":
        "Elle paraît d’un abord avenant et volontiers causante.",
    "There are signs of a trail in the East Corridors on the ground floor.":
        "On relève des traces de passage dans les couloirs est du rez-de-chaussée.",
    "One of several entrances to the basement.":
        "L’une des nombreuses entrées du sous-sol.",
    "There are signs of a trail in the East Tower.":
        "On relève des traces de passage dans la tour est.",
    "I witnessed Missus Lau and Miss Ivy McLeod discussing the need to find a husband. They appear "
    "to be a lot closer than simply chaperone and ward.":
        "J’ai surpris Mme Lau et Mlle Ivy McLeod parlant de la nécessité de lui trouver un mari. "
        "Elles semblent bien plus proches que ne le sont un chaperon et sa pupille.",
    "I witnessed Mister Hunter and Miss McLeod discussing something to be added later.":
        "J’ai surpris M. Hunter et Mlle McLeod s’entretenant de quelque chose.",
    "I overheard Missus Erickson and it seems she will not be in her room until after breakfast.":
        "J’ai surpris Mme Erickson : il semble qu’elle ne regagnera sa chambre qu’après le "
        "déjeuner du matin.",
    "It had the initials E.D. on it - could that be Evelyn Deane?":
        "Il portait les initiales E. D. — serait-ce Evelyn Deane ?",
    "A mostly-empty room in the Blake residence.":
        "Une chambre presque vide, dans la résidence Blake.",
    "An empty bottle of pills.": "Un flacon de pilules vide.",
    "The Marquess and Master Walter are the last remaining Blakes.":
        "Le marquis et le jeune Walter sont les derniers des Blake.",
    "Pages on Enochian magic, including a script I cannot decipher.":
        "Des pages sur la magie énochienne, dont une écriture que je ne sais déchiffrer.",
    "A printed schedule of events planned throughout the week, up 'til and including the Grand "
    "Séance itself.":
        "Un programme imprimé des événements prévus au long de la semaine, jusqu’à la Grande Séance "
        "elle-même incluse.",
    "I found evidence that suggests that the Marquess and Walter are not the last of their line "
    "after all...":
        "J’ai trouvé de quoi croire que le marquis et Walter ne sont pas, après tout, les derniers "
        "de leur lignée…",
    "A hotel guest. A French academic and debunker of false mystics.":
        _guest("Un universitaire français, pourfendeur de faux mystiques."),
    "The missing woman.": "La femme disparue.",
    "How am I meant to learn how to exorcise a ghost?":
        "Comment diable suis-je censé apprendre à exorciser un fantôme ?",
    "I should search the manager's office for information.":
        "Je devrais fouiller le bureau du gérant en quête de renseignements.",
    "I must find the compromising material Miss Deane collected on Missus Lau and Miss McLeod.":
        "Il me faut trouver les pièces compromettantes que Mlle Deane a réunies sur Mme Lau et "
        "Mlle McLeod.",
    "I should retrace my steps down to the catacombs and look for clues.":
        "Je devrais redescendre dans les catacombes sur mes pas et y chercher des indices.",
    "Unearthly creatures of the woods, rivers, and hills.":
        "Des créatures surnaturelles des bois, des rivières et des collines.",
    "The letter Miss Deane supposedly wrote is faked, but who wrote it?":
        "La lettre que Mlle Deane aurait écrite est un faux — mais de quelle main ?",
    "Marquess Blake has seen the family fortunes diminishing in recent times.":
        "Le marquis Blake a vu la fortune familiale décliner ces derniers temps.",
    "Marquess Blake was strapping himself into one of the vats.":
        "Le marquis Blake était en train de s’attacher dans l’une des cuves.",
    "A tear-stained letter to Miss Mantovani, postmarked from Italy.":
        "Une lettre à Mlle Mantovani, tachée de larmes, oblitérée d’Italie.",
    "A photograph of Miss Mantovani and her family.":
        "Une photographie de Mlle Mantovani et de sa famille.",
    "Miss Mantovani provides for her family in rural Italy, buying them a better life, but at what "
    "cost?":
        "Mlle Mantovani fait vivre sa famille dans la campagne italienne et lui achète une vie "
        "meilleure — mais à quel prix ?",
    "Miss Hisham is fixating on a specific vase; I wonder whether I can learn more of this.":
        "Mlle Hisham est obnubilée par un vase précis ; peut-être puis-je en apprendre davantage.",
    "A hotel guest. A Catholic priest with a cold demeanour.":
        _guest("Un prêtre catholique au maintien glacial."),
    "An elderly priest.": "Un prêtre âgé.",
    "A Gnostic bible. Father Sinnott seems to have circled passages about a Black Iron Prison, but "
    "I cannot make out what that means.":
        "Une bible gnostique. Le père Sinnott semble avoir entouré des passages sur une prison de "
        "fer noir, mais le sens m’en échappe.",
    "A series of strange symbols which I found in Father Sinnott's room.":
        "Une série de symboles étranges, trouvée dans la chambre du père Sinnott.",
    "Is there a way for her to see her dead father's face?":
        "Existe-t-il un moyen pour elle de voir le visage de son père défunt ?",
    "Seamus O'Connor's Likeness": "Le portrait de Seamus O’Connor",
    "Miss Ines Barbosa wishes to know what her father, Seamus O'Connor, looked like":
        "Mlle Ines Barbosa souhaite savoir à quoi ressemblait son père, Seamus O’Connor",
    "Mister Dupré sent me to his room to get a spirit board.":
        "M. Dupré m’a envoyé chercher une planche des esprits dans sa chambre.",
    "I'm told that ghosts can be bound to the world of the living by objects and old emotional "
    "ties - the chains are called 'fetters'.":
        "On me dit que les fantômes peuvent être retenus au monde des vivants par des objets et de "
        "vieux liens affectifs — on nomme ces chaînes des « entraves ».",
    "A hotel guest. A local wise-woman.": _guest_f("Une femme savante du pays."),
    "Doctor Callaghan feels underappreciated by his aunt Miss Callaghan. I must find a way for her "
    "to realise his worth.":
        "Le docteur Callaghan s’estime mal apprécié de sa tante, Mlle Callaghan. Il me faut trouver "
        "le moyen de lui en faire reconnaître la valeur.",
    "Can I re-enter the dream to decipher the message, I wonder? What do I need to do this?":
        "Puis-je entrer de nouveau dans le rêve pour en déchiffrer le message ? Que me faut-il pour "
        "cela ?",
    "Miss Murphy has asked me to find a means for her to see her child. If she cannot see them "
    "physically perhaps there is a magical means?":
        "Mlle Murphy m’a demandé de trouver un moyen de voir son enfant. À défaut de la voir en "
        "chair et en os, peut-être existe-t-il une voie magique.",
    "If Miss Deane was blackmailing both Miss McLeod and Missus Lau, might I find something of use "
    "by investigating the chaperone?":
        "Si Mlle Deane faisait chanter à la fois Mlle McLeod et Mme Lau, peut-être trouverai-je "
        "quelque chose d’utile du côté du chaperon.",
    "Perhaps Mister Hunter has been leaving charms around chimneys.":
        "Peut-être M. Hunter dépose-t-il des charmes dans les cheminées.",
    "Doctor Callaghan was in direct communication with Miss Deane, regarding a mentorship in the "
    "mystic arts. I should search the manor for any further correspondence that might have been "
    "hidden away.":
        "Le docteur Callaghan correspondait directement avec Mlle Deane au sujet d’un enseignement "
        "des arts mystiques. Je devrais fouiller le manoir en quête d’autres lettres qu’on aurait "
        "cachées.",
    "I'm told Miss Deane left the Manor, leaving behind a letter to explain her absence. I need to "
    "find that letter.":
        "On me dit que Mlle Deane a quitté le manoir en laissant une lettre pour expliquer son "
        "absence. Il me faut trouver cette lettre.",
    "Miss Quinn is looking for a book on local records - I should find it bring it to them.":
        "Mlle Quinn cherche un ouvrage de registres locaux — je devrais le trouver et le lui "
        "porter.",
}


DESCRIPTIONS.update({
    "I must find some hypnotic music to aid my attempt to lucid dream. Surely I can find something "
    "suitable within the manor.":
        "Il me faut une musique hypnotique pour favoriser mon rêve lucide. Je trouverai sûrement "
        "mon bonheur dans le manoir.",
    "I should find Miss Deane's departure letter in case she left any clues as to her whereabouts.":
        "Je devrais trouver la lettre de départ de Mlle Deane, au cas où elle y aurait laissé "
        "quelque indice.",
    "I found some evidence, likely stashed by Miss Deane, that indicate her reason for being here. "
    "She must not have wanted others to find them. I should search Blake Manor for whatever else "
    "she may have hidden away in secret.":
        "J’ai trouvé des pièces, sans doute cachées par Mlle Deane, qui révèlent la raison de sa "
        "venue. Elle tenait à ce que nul ne les découvre. Je devrais fouiller Blake Manor pour "
        "trouver ce qu’elle a pu dissimuler d’autre.",
    "If I want to know where Miss Deane went, it would be good to know where she started. Which "
    "room was she assigned?":
        "Pour savoir où Mlle Deane est allée, mieux vaut savoir d’où elle est partie. Quelle "
        "chambre lui avait-on attribuée ?",
    "I suspect I need more components to bless the well - but where can I find some?":
        "Je soupçonne qu’il me faut d’autres composants pour bénir le puits — mais où en trouver ?",
    "Mister Dupré says that he needs something of considerable emotional value to Mister D'Arcy to "
    "exorcise his ghost.\n\nIf he was cheating on his wife I suspect I won't find anything there. "
    "With his mistress, though?":
        "M. Dupré dit qu’il lui faut un objet d’une grande valeur affective pour M. D’Arcy afin "
        "d’exorciser son fantôme.\n\nS’il trompait sa femme, je doute de trouver quoi que ce soit "
        "de ce côté-là. Du côté de sa maîtresse, en revanche ?",
    "Mister Varley has given me a key that reputedly will open the door to the hidden treasure. I "
    "should explore to find the lock.":
        "M. Varley m’a remis une clé qui ouvrirait, dit-on, la porte du trésor caché. Il me reste à "
        "trouver la serrure.",
    "I found a scrap of paper at Miss Quinn's research station in the library. I should "
    "investigate the location referred to.":
        "J’ai trouvé un bout de papier au poste de travail de Mlle Quinn, à la bibliothèque. Je "
        "devrais me rendre au lieu qu’il désigne.",
    "I found a door in the catacombs that was locked - but looked as though it had been recently "
    "used. Who would have the key?":
        "J’ai trouvé dans les catacombes une porte verrouillée — mais qui semblait avoir servi "
        "récemment. Qui en détiendrait la clé ?",
    "There must be clues nearby which will help me decipher to the code to open this safe.":
        "Il doit se trouver dans les parages des indices propres à me livrer la combinaison de ce "
        "coffre.",
    "I should find something suitable to play the tune from Miss Hisham.":
        "Je devrais trouver de quoi jouer convenablement l’air de Mlle Hisham.",
    "He's well dressed - and it is evident he can afford some luxury.":
        "Il est bien mis — et l’on voit qu’il peut s’offrir quelque luxe.",
    "A scorched piece of paper I found in the firepit. It suggests that someone was planning to "
    "transfer a spirit into Evelyn Deane's body.":
        "Un papier roussi trouvé dans le foyer. Il donne à penser que quelqu’un projetait de "
        "transférer un esprit dans le corps d’Evelyn Deane.",
    "Perhaps fixing the telegraph machine will distract the manager and enable me to search his "
    "office.":
        "Réparer le télégraphe occupera peut-être le gérant assez longtemps pour que je fouille son "
        "bureau.",
    "She has a tan on her skin, as if she's spent time working outside.":
        "Sa peau est hâlée, comme si elle avait longtemps travaillé au dehors.",
    "Deane's dazed trail has led me to the gardens.":
        "La piste laissée par Mlle Deane, hébétée, m’a mené aux jardins.",
    "I should follow the trail of knocked over furnishings through the Manor and see where they "
    "lead me.":
        "Je devrais suivre la traînée de meubles renversés à travers le manoir et voir où elle me "
        "mène.",
    "I followed a trail into the hedge maze.":
        "J’ai suivi une piste jusque dans le labyrinthe de haies.",
    "I found a treasure map of some sort laying underneath the floorboards of Miss Deane's room. "
    "Where will it lead me?":
        "J’ai trouvé une manière de carte au trésor sous le plancher de la chambre de Mlle Deane. "
        "Où me conduira-t-elle ?",
    "Footprints found in the hedge maze.":
        "Des empreintes de pas relevées dans le labyrinthe de haies.",
    "Miss Deane's footprints found in the hedge maze.":
        "Les empreintes de Mlle Deane, relevées dans le labyrinthe de haies.",
    "Either in an attempt to blend in or, or out of practicality, she is wearing local fashion "
    "along with what I assume are her usual clothes.":
        "Soit pour se fondre dans le décor, soit par commodité, elle porte des vêtements du pays "
        "mêlés à ce que je suppose être sa mise habituelle.",
    "It's a perfect forgery and easy to miss, but Walter Blake has only recently been painted into "
    "the Blake family portraits.":
        "La contrefaçon est parfaite et facile à manquer : Walter Blake n’a été ajouté aux "
        "portraits de famille que tout récemment.",
    "Mister Toussaint has suggested that there may be frauds at the event, con artists hoping to "
    "take advantage of the more vulnerable attendees.":
        "M. Toussaint donne à entendre qu’il y aurait des imposteurs à cette réception, des "
        "escrocs comptant profiter des invités les plus fragiles.",
    "A series of letters sent to Mister Skerritt from fellow Freemasons - all with a similarly "
    "short tone.":
        "Une série de lettres adressées à M. Skerritt par des frères francs-maçons — toutes d’un "
        "ton également sec.",
    "A secret society of fraternities interested in ritual.":
        "Une société secrète de confréries vouées au rituel.",
    "My deductions lead me to the basement, now to find a way in there...":
        "Mes déductions me mènent au sous-sol ; reste à trouver comment y entrer…",
    "The letter from Miss Deane could be in the manager's office, but Mister Varley is working in "
    "there. I need to get him out.":
        "La lettre de Mlle Deane est peut-être dans le bureau du gérant, mais M. Varley y travaille. "
        "Il me faut l’en faire sortir.",
    "There are signs of a trail in the Gardens.":
        "On relève des traces de passage dans les jardins.",
    "I encountered a ghost at the firepit who seems to want to communicate something.":
        "J’ai rencontré au foyer un fantôme qui semble vouloir communiquer quelque chose.",
    "I've communicated to the ghost with the Spirit Board.":
        "J’ai communiqué avec le fantôme au moyen de la planche des esprits.",
    "I have learned that an Aeon is a form of Gnostic angel and the Black Iron Prison is their "
    "interpretation of hell, which is this material plane we are all in now.":
        "J’ai appris qu’un Éon est une sorte d’ange gnostique, et que la prison de fer noir est "
        "leur idée de l’enfer — à savoir ce plan matériel où nous sommes tous.",
    "I should attend the silent dinner.": "Je devrais assister au dîner silencieux.",
    "I must see what the guests were doing on Tuesday night.":
        "Il me faut établir ce que faisaient les invités le mardi soir.",
    "A record of who arrived and departed - and when. I notice Miss Deane did not sign out.":
        "Un relevé des arrivées et des départs — avec les heures. Je note que Mlle Deane n’a pas "
        "signé son départ.",
    "A book Hermetic Order of the Golden Dawn.":
        "Un ouvrage sur l’Ordre hermétique de l’Aube dorée.",
    "I saw a large figuring hammering at an anvil in the hedge maze.":
        "J’ai vu une grande silhouette battre le fer sur une enclume, dans le labyrinthe.",
    "He keeps checking his pocket watch. He's either pressed for time, ruled by routine, or both.":
        "Il consulte sans cesse sa montre. Ou il est pressé, ou il est esclave de ses habitudes — "
        "ou les deux.",
    "A child's toy, lovingly carved.": "Un jouet d’enfant, taillé avec amour.",
    "An old brooch in an Irish style. The image on it is of an old oak tree.":
        "Une vieille broche de style irlandais. Elle représente un vieux chêne.",
    "O'Connor Family Brooch": "Broche de la famille O’Connor",
    "An old brooch in an Irish style. Looks to have the crest of the O'Connor family":
        "Une vieille broche de style irlandais. Elle semble porter le blason de la famille O’Connor",
    "A hatch in the East Courtyard that leads to the basement.":
        "Une trappe, dans la cour est, qui mène au sous-sol.",
    "There's a troubled look in his eyes.": "Son regard est troublé.",
    "I'm told many have witnessed strange apparitions in and around the manor. Certainly, I have "
    "had improbable experiences here myself.":
        "On me dit que beaucoup ont vu d’étranges apparitions dans le manoir et alentour. J’ai "
        "moi-même connu ici des expériences peu croyables.",
    "Hauntings": "Hantises",
    "I have seen some... inexplicable things here. Others, too, have witnessed strange apparitions "
    "in and around the manor.":
        "J’ai vu ici des choses… inexplicables. D’autres aussi ont vu d’étranges apparitions dans "
        "le manoir et alentour.",
    "A hotel guest. An enthusiastic American medium.":
        _guest_f("Un médium américain plein d’enthousiasme."),
    "A headdress of some sort.": "Une manière de coiffe.",
    "A hedge maze found on the manor grounds, out behind the walled garden.":
        "Un labyrinthe de haies, sur les terres du manoir, derrière le jardin clos.",
    "There are signs of a trail in the Hedge Maze.":
        "On relève des traces de passage dans le labyrinthe de haies.",
    "A maze at the back of the manor grounds.":
        "Un labyrinthe au fond des terres du manoir.",
    "I had a vision of Miss Deane's last moments before her disappearance.":
        "J’ai eu une vision des derniers instants de Mlle Deane avant sa disparition.",
    "I attended a ball last night in which I was drugged and saw some strange events - but how "
    "much of it was real?":
        "J’ai assisté hier soir à un bal où l’on m’a drogué et où j’ai vu d’étranges choses — mais "
        "qu’y avait-il de réel ?",
    "The missing Blake heir.": "L’héritier Blake disparu.",
    "Photos of Henry Coventry as a child.": "Des photographies de Henry Coventry enfant.",
    "Miss Mantovani appears incredibly close to her family.":
        "Mlle Mantovani paraît extrêmement proche des siens.",
    "The Hermetic Order of the Golden Dawn, or The Golden Order, is a semi-secret magic society "
    "established in England.":
        "L’Ordre hermétique de l’Aube dorée, ou Ordre doré, est une société magique semi-secrète "
        "fondée en Angleterre.",
    "A hidden doorway in the Blake residence lab.":
        "Une porte dérobée dans le laboratoire de la résidence Blake.",
    "The letter I received hiring me onto this case.":
        "La lettre par laquelle on m’a engagé sur cette affaire.",
    "The vase has a long storied history before being 'acquired' by the Blake family.":
        "Le vase a une longue histoire avant d’avoir été « acquis » par la famille Blake.",
    "According to these records, the hotel is on its last legs - in part from the amount being "
    "spent to host this gathering.":
        "À en croire ces registres, l’hôtel est aux abois — en partie à cause des sommes englouties "
        "dans cette réception.",
    "Miss Barbosa suspects Miss Deane of knowing about her more than she should. Perhaps I can "
    "find how Miss Deane came upon knowledge of her fellow séance attendee.":
        "Mlle Barbosa soupçonne Mlle Deane d’en savoir sur elle plus qu’il ne faudrait. Peut-être "
        "puis-je découvrir comment Mlle Deane s’est renseignée sur sa compagne de séance.",
    "Mister Toussaint seems to know who I am...":
        "M. Toussaint semble savoir qui je suis…",
    "Marquess Blake appears to have loved his wife greatly, even in death she influences his life. "
    "Such control sends a shiver down my spine.":
        "Le marquis Blake semble avoir aimé sa femme à la folie ; même morte, elle gouverne sa vie. "
        "Un tel empire me donne le frisson.",
    "A hotel guest. A Brazilian woman seeking information.":
        _guest_f("Une Brésilienne en quête de renseignements."),
    "Symbols on ink-blotted scrap paper. I can't make them all out.":
        "Des symboles sur un papier maculé d’encre. Je ne parviens pas à tous les lire.",
    "She presents herself more like a child than an adult.":
        "Elle se présente davantage en enfant qu’en adulte.",
    "A scratched out note suggesting Missus Lau's problem would go away if Evelyn Deane was to "
    "die.":
        "Un billet raturé donnant à entendre que l’ennui de Mme Lau s’évanouirait si Evelyn Deane "
        "venait à mourir.",
    "I have eliminated all other suspects, it must have been Mister Cathal O'Meara who fought with "
    "Deane.<br>I must find out why he lied and what they were arguing about.":
        "J’ai écarté tous les autres suspects : c’est M. Cathal O’Meara qui s’est querellé avec "
        "Mlle Deane.<br>Il me faut savoir pourquoi il a menti et sur quoi portait la dispute.",
    "I should investigate Mister Varley's office to see if it contains anything useful.":
        "Je devrais fouiller le bureau de M. Varley pour voir s’il recèle quoi que ce soit d’utile.",
    "I should learn more about Percival Blake. Perhaps the library or the staff will know more.":
        "Je devrais en apprendre davantage sur Percival Blake. La bibliothèque ou le personnel en "
        "sauront peut-être plus.",
    "I gave Miss Quinn the book she is looking for, I should check the table Miss Quinn was doing "
    "her research on to see if there are any clues to where she went.":
        "J’ai remis à Mlle Quinn le livre qu’elle cherchait ; je devrais examiner la table où elle "
        "travaillait, au cas où elle y aurait laissé trace de sa destination.",
    "Investigate their room to see what they could be hiding.":
        "Fouiller leur chambre pour voir ce qu’ils pourraient cacher.",
    "Investigate their room and see what they could be hiding.":
        "Fouiller leur chambre et voir ce qu’ils pourraient cacher.",
    "I should search room 19 for proof that she is a fraud.":
        "Je devrais fouiller la chambre 19 pour prouver son imposture.",
    "Investigate Missus Erickson's bedroom for proof she is a fraud.":
        "Fouiller la chambre de Mme Erickson pour prouver son imposture.",
    "Investigate Mister Toussaint's room to see what they could be hiding.":
        "Fouiller la chambre de M. Toussaint pour voir ce qu’il pourrait cacher.",
    "I should find out what's happening in the basement - there may be important information for "
    "me there.":
        "Je devrais découvrir ce qui se passe au sous-sol — il pourrait s’y trouver des "
        "renseignements de poids.",
    "Miss Murphy works in the staff quarters under the house. I should investigate this area "
    "fully.":
        "Mlle Murphy travaille dans les quartiers du personnel, sous la maison. Je devrais explorer "
        "ces lieux de fond en comble.",
    "There's something sinister going on here. I should see what I can find out about it.":
        "Il se trame ici quelque chose de sinistre. Je devrais voir ce que je puis en découvrir.",
    "If I want to learn more about the boy, I would need to search his bedroom and general "
    "residence.":
        "Pour en apprendre davantage sur le garçon, il me faudrait fouiller sa chambre et la "
        "résidence en général.",
    "I must get into the Blake residence and look for clues.":
        "Il me faut pénétrer dans la résidence Blake et y chercher des indices.",
    "I found a piece of paper with burnt symbols in the men's dormitory, what could it mean? I "
    "should continue searching the basement for further clues.":
        "J’ai trouvé au dortoir des hommes un papier couvert de symboles brûlés ; que peut-il "
        "signifier ? Je devrais poursuivre la fouille du sous-sol.",
    "Mister Dupré's letter mentioned a presence near a firepit outside.":
        "La lettre de M. Dupré mentionnait une présence près d’un foyer, au dehors.",
    "I should find out what is going on here. There might be something of use to me.":
        "Je devrais découvrir ce qui se passe ici. Il pourrait s’y trouver quelque chose d’utile.",
    "I should investigate the mausoleum for clues.":
        "Je devrais fouiller le mausolée en quête d’indices.",
    "I may find some useful information searching where Mister Hunter works.":
        "Je pourrais trouver des renseignements utiles en fouillant le lieu où travaille M. Hunter.",
    "I should investigate the well.": "Je devrais examiner le puits.",
    "Is this land, or has this land ever been, home to a portal to the Otherworld? I gather I "
    "should look under the cover of darkness...":
        "Cette terre abrite-t-elle, ou a-t-elle jamais abrité, un portail vers l’Autre Monde ? Je "
        "crois comprendre qu’il faut chercher à la faveur de la nuit…",
    "A hotel guest. A young Scottish noblewoman with the Second Sight.":
        _guest_f("Une jeune aristocrate écossaise douée de double vue."),
    "Miss McLeod fears the loss of her Second Sight. Casting the blame on Miss Deane, it appears "
    "she has asked Mister Hunter for help.":
        "Mlle McLeod redoute de perdre sa double vue. En rejetant la faute sur Mlle Deane, elle "
        "semble avoir demandé l’aide de M. Hunter.",
    "Mister Coventry is a jeweller by trade.": "M. Coventry est joaillier de son état.",
    "The Marquess of Doon. Owns the hotel.": "Le marquis de Doon. Propriétaire de l’hôtel.",
    "Mister Dupré's journal, found in his room.":
        "Le journal de M. Dupré, trouvé dans sa chambre.",
    "Mister Dupré's journal, found in his room. It contains writings on Evelyn Deane.":
        "Le journal de M. Dupré, trouvé dans sa chambre. Il contient des pages sur Evelyn Deane.",
    "I lost the kidnapper near that otherworldly portal.":
        "J’ai perdu le ravisseur près de ce portail d’un autre monde.",
    "One of the guests was kidnapped during the masked ball.":
        "L’un des invités a été enlevé pendant le bal masqué.",
    "I have the impression she knows more about those around her than they would like.":
        "J’ai l’impression qu’elle en sait sur son entourage plus qu’il ne le souhaiterait.",
    "Lady Wilhelmina Blake was the last owner of the Vase, what ever became of her?":
        "Lady Wilhelmina Blake fut la dernière propriétaire du vase ; qu’est-elle devenue ?",
    "A book on local historical land records from the turn of the century. The spine is broken.":
        "Un ouvrage de registres fonciers locaux du tournant du siècle. Le dos en est brisé.",
    "An intricate brooch, perhaps representing something... and less dainty than one would expect "
    "such a lady to wear.":
        "Une broche ouvragée, figurant peut-être quelque chose… et moins délicate que ce qu’on "
        "attendrait d’une telle dame.",
    "Holy Order Of The Golden Dawn Brooch": "Broche de l’Ordre de l’Aube dorée",
    "A brooch bearing the symbol of a large occult organisation. It seems entwined with a personal "
    "coat of arms.":
        "Une broche portant le symbole d’une grande organisation occulte, entrelacé, semble-t-il, "
        "avec des armes personnelles.",
    "A large bottle of laudanum, a strong painkiller - it is nearly empty.":
        "Un grand flacon de laudanum, puissant analgésique — presque vide.",
    "It seems as though an awful lot of Quinn family members have died young. Is there any "
    "connection between the deaths? I should learn more about the family history.":
        "Il semble qu’un nombre effrayant de Quinn soient morts jeunes. Ces morts ont-elles un "
        "lien ? Je devrais me renseigner sur l’histoire de la famille.",
    "I must learn the name of Miss Barbosa's father.":
        "Il me faut apprendre le nom du père de Mlle Barbosa.",
    "Mister O'Meara wants me to use the Babelstone with the notes on Enochian magic in his trunk, "
    "in order to learn the angel's name.":
        "M. O’Meara veut que je me serve de la babelstone avec les notes de magie énochienne "
        "rangées dans sa malle, afin d’apprendre le nom de l’ange.",
    "Miss Murphy appears to have been receiving tutelage in the magical arts from Miss Deane.":
        "Mlle Murphy semble avoir reçu de Mlle Deane un enseignement des arts magiques.",
    "Mister Skerritt seeks to secure his legacy.":
        "M. Skerritt cherche à assurer sa postérité.",
    "A letter from Doctor Callaghan to Miss Deane. It seems he'd offered to teach her Irish magic, "
    "disregarding his aunt's apprehensions in the process.":
        "Une lettre du docteur Callaghan à Mlle Deane. Il lui aurait proposé de lui enseigner la "
        "magie irlandaise, au mépris des réserves de sa tante.",
    "A letter from Miss Mantovani to Missus Joyce seeking to calm the waters. Smells faintly of "
    "tea.":
        "Une lettre de Mlle Mantovani à Mme Joyce, cherchant à apaiser les esprits. Elle sent "
        "faiblement le thé.",
    "A letter from Miss Deane, thanking Doctor Callaghan for his offer but stating that she wants "
    "to learn from a \"true master\" - his aunt Fiadh. The letter was found in a bin.":
        "Une lettre de Mlle Deane remerciant le docteur Callaghan de son offre, mais déclarant "
        "vouloir apprendre d’un « véritable maître » — sa tante Fiadh. Trouvée dans une corbeille.",
    "A menacing letter to Miss Deane.": "Une lettre de menaces adressée à Mlle Deane.",
    "A letter addressed to Mister Varley, soundly rebuking a request for information on behalf of "
    "a young mother. It is signed by the bishop of this diocese.":
        "Une lettre adressée à M. Varley, rabrouant vertement une demande de renseignements faite "
        "au nom d’une jeune mère. Elle est signée de l’évêque du diocèse.",
    "Doctor Callaghan's mother feels her son's potential, abilities, and future are being held "
    "back by his apprenticeship under Fiadh.":
        "La mère du docteur Callaghan estime que son apprentissage auprès de Fiadh bride ses "
        "capacités, ses dons et son avenir.",
    "<i>\"A man also or woman that hath a familiar spirit, or that is a wizard, shall surely be "
    "put to death: they shall stone them with stones: their blood shall be upon them.\" </i>":
        "<i>« L’homme ou la femme qui évoque les esprits ou qui s’adonne à la divination sera puni "
        "de mort ; on les lapidera : leur sang retombera sur eux. » </i>",
    "The Quinn family is cursed! That is not a fate I would wish on anybody, I must see if I can "
    "lift the curse. Miss Quinn said she needed to find something belonging to the spirit.":
        "La famille Quinn est maudite ! Je ne souhaiterais ce sort à personne ; il me faut voir si "
        "je puis lever la malédiction. Mlle Quinn a dit qu’il lui fallait un objet ayant appartenu "
        "à l’esprit.",
    "A list of séance attendees who could be magic practitioners, found in Missus Erickson's room, "
    "with Evelyn Deane's name circled.":
        "Une liste des participants à la séance susceptibles de pratiquer la magie, trouvée dans la "
        "chambre de Mme Erickson, le nom d’Evelyn Deane entouré.",
    "A hotel guest. A funeral director from New Orleans.":
        _guest("Un ordonnateur de pompes funèbres de La Nouvelle-Orléans."),
    "A key for a locker. The number 11 is stamped onto the back of the tag.":
        "Une clé de casier. Le numéro 11 est frappé au dos de l’étiquette.",
    "I found a locket in the hallway outside Mister Coventry's room.":
        "J’ai trouvé un médaillon dans le couloir, devant la chambre de M. Coventry.",
    "The locket is initialled 'E, D'.": "Le médaillon porte les initiales « E. D. ».",
    "A long red hair attached to the skull mask I found lying in the catacombs.":
        "Un long cheveu roux resté accroché au masque de crâne trouvé dans les catacombes.",
    "The entity longs to return home.": "L’entité aspire à rentrer chez elle.",
    "A large shrouded figure I have seen and felt around the manor.":
        "Une grande silhouette voilée, que j’ai vue et sentie dans le manoir.",
    "A technique for experiencing dreams in a waking state.":
        "Une technique permettant de vivre ses rêves en état de veille.",
    "My luggage, hastily packed.": "Mes bagages, faits à la hâte.",
    "This appears to be a ticket for luggage left in bay 12 of the luggage room.":
        "Ceci paraît être un bulletin pour des bagages déposés dans la case 12 de la consigne.",
    "This appears to be a ticket for luggage left in bay 46 of the luggage room. I found it in "
    "Mister Dupré's room.":
        "Ceci paraît être un bulletin pour des bagages déposés dans la case 46 de la consigne. Je "
        "l’ai trouvé dans la chambre de M. Dupré.",
    "An invite to lunch with Marquess Blake. The Dining Hall, 1pm.":
        "Une invitation à déjeuner avec le marquis Blake. Salle à manger, 13 h.",
    "A sigil that reveals events from the past.":
        "Un sceau qui révèle les événements du passé.",
    "Many here claim to have true magical abilities.":
        "Beaucoup, ici, se disent véritablement doués de pouvoirs.",
    "I found a hidden doorway that asks for a name. Perhaps the suspect's?":
        "J’ai trouvé une porte dérobée qui réclame un nom. Celui du suspect, peut-être ?",
    "I found a hidden doorway that asked for a name. It opened to the name Simon Coventry.":
        "J’ai trouvé une porte dérobée qui réclamait un nom. Elle s’est ouverte au nom de Simon "
        "Coventry.",
    "Carved into the staff I found this phrase 'Díghlasáil an Draíocht dom', which means something "
    "akin to 'Unlock the magic to me'.":
        "Gravée dans le bâton, j’ai trouvé cette formule, « Díghlasáil an Draíocht dom », qui "
        "signifie à peu près « Déverrouille pour moi la magie ».",
    "A Loa of life and death who protects those who have passed, and much like her celtic "
    "counterpart, is associated with healing.":
        "Une loa de la vie et de la mort, qui protège les défunts et que l’on associe, comme sa "
        "contrepartie celtique, à la guérison.",
    "Mister Varley's private quarters. He has a room to himself.":
        "Les quartiers privés de M. Varley. Il dispose d’une chambre à lui seul.",
    "The hotel manager's office.": "Le bureau du gérant de l’hôtel.",
    "A key to the manager's quarters.": "Une clé des quartiers du gérant.",
    "Handwritten notes and a few compiled snippets of paper on Miss Deane - and where she might "
    "have gone.":
        "Des notes manuscrites et quelques coupures rassemblées sur Mlle Deane — et sur l’endroit "
        "où elle aurait pu se rendre.",
    "Maps of the manor I found in Miss Hisham's room. Some areas are circled.":
        "Des plans du manoir trouvés dans la chambre de Mlle Hisham. Certaines zones sont entourées.",
    "Miss Mantovani has entrusted me with her fortune, I shall wire it on to her family when I've "
    "left this forsaken place.":
        "Mlle Mantovani m’a confié sa fortune ; je la ferai parvenir aux siens dès que j’aurai "
        "quitté ce lieu maudit.",
    "A map of the catacombs beneath Blake Manor.":
        "Un plan des catacombes sous Blake Manor.",
    "A map of the area for several miles around. It's dated but fit for purpose.":
        "Une carte de la région sur plusieurs milles à la ronde. Elle date, mais elle fera "
        "l’affaire.",
    "Miss McLeod is looking to find herself a suitable marriage candidate at this event.":
        "Mlle McLeod cherche à se trouver un parti convenable à cette réception.",
    "Details of marriage plans found in Victoria's Journal":
        "Des détails sur des projets de mariage, trouvés dans le journal de Victoria",
    "Details of marriage plans found in Cathal's Journal":
        "Des détails sur des projets de mariage, trouvés dans le journal de Cathal",
    "Whatever Father Sinnott's plans to \"save humanity\" are, he intends to carry on with or "
    "without Mister Doyle.":
        "Quels que soient les desseins du père Sinnott pour « sauver l’humanité », il entend les "
        "poursuivre avec ou sans M. Doyle.",
    "The late wife of our host, Jonathan Blake.":
        "La défunte épouse de notre hôte, Jonathan Blake.",
    "The Late Wife Of Our Host, Jonathan Blake. She Died A Few Years Ago In A Carriage Accident "
    "That Also Crippled Their Son, Walter.":
        "La défunte épouse de notre hôte, Jonathan Blake. Elle est morte il y a quelques années "
        "dans un accident de voiture qui a laissé leur fils Walter infirme.",
    "I found a secret room full of things belonging to Simon Coventry.":
        "J’ai trouvé une pièce secrète emplie d’effets appartenant à Simon Coventry.",
    "A medical certificate belonging to Missus D'Arcy's with an unknown code, U0.33, written on "
    "it.":
        "Un certificat médical au nom de Mme D’Arcy, portant un code inconnu : U0.33.",
    "Medical code U0.33 means 'spontaneous abortion'. A miscarriage.":
        "Le code médical U0.33 signifie « avortement spontané ». Une fausse couche.",
    "Found whilst exploring Doctor Callaghan's room, his assessment of Miss Mantovani. Things do "
    "not look good for her.":
        "Trouvé en fouillant la chambre du docteur Callaghan : son diagnostic sur Mlle Mantovani. "
        "L’avenir est sombre pour elle.",
    "I have been invited to luncheon with Marquess Blake, what must he want to discuss with me?":
        "Je suis convié à déjeuner avec le marquis Blake ; que peut-il bien vouloir me dire ?",
    "A relic in memory of a Quinn family member, recently passed. Miss Quinn has quite a few items "
    "in memory of deceased relatives stored in her room.":
        "Une relique à la mémoire d’un Quinn récemment disparu. Mlle Quinn conserve dans sa chambre "
        "bon nombre d’objets en mémoire de parents défunts.",
    "A key to open the Men's Dormitory.": "Une clé ouvrant le dortoir des hommes.",
    "A lockbox I found near Mister Doyle's bed in the men's dormitory with strange symbols in "
    "place of buttons.":
        "Un coffret trouvé près du lit de M. Doyle, au dortoir des hommes, avec d’étranges symboles "
        "en guise de boutons.",
    "Miss Fiadh Callaghan is his aunt and mentor.":
        "Mlle Fiadh Callaghan est sa tante et son mentor.",
    "A hotel guest. An old money gentleman in the winter of his years.":
        _guest("Un gentleman de vieille fortune, à l’hiver de sa vie."),
    "The final race to settle in Ireland, and the ancestry to its current inhabitants.":
        "Le dernier peuple à s’être établi en Irlande, et l’ascendance de ses habitants actuels.",
    "The person who was kidnapped has red hair. I should check to see if Miss Callaghan is still "
    "about.":
        "La personne enlevée avait les cheveux roux. Je devrais vérifier que Mlle Callaghan est "
        "toujours là.",
    "Fiadh has asked me to see if I can help protect her well, as she is struggling to do so "
    "alone.":
        "Fiadh m’a demandé de voir si je puis l’aider à protéger son puits, n’y parvenant pas "
        "seule.",
    "Miss Deane was overheard fighting with someone. This may be important.":
        "On a entendu Mlle Deane se quereller avec quelqu’un. Cela pourrait avoir son importance.",
    "Miss Deane is still alive. I have a chance to save her!":
        "Mlle Deane est encore en vie. J’ai une chance de la sauver !",
    "I'm too late to save Miss Deane...":
        "J’arrive trop tard pour sauver Mlle Deane…",
    "Miss Deane is descended from the sorcerer rulers of the Milesians.":
        "Mlle Deane descend des souverains sorciers milésiens.",
    "An invitation for Miss Deane, promising her revelations about her 'magical abilities'.":
        "Une invitation adressée à Mlle Deane, lui promettant des révélations sur ses « dons "
        "magiques ».",
    "Deane’s journal, delivered to me by Missus Joyce. The sender is unknown.":
        "Le journal de Mlle Deane, remis par Mme Joyce. L’expéditeur est inconnu.",
    "Miss Deane’s journal, delivered to me by Missus Joyce. The sender is unknown.":
        "Le journal de Mlle Deane, remis par Mme Joyce. L’expéditeur demeure inconnu.",
    "A letter apparently written and signed by Miss Deane, excusing her from the event in favour "
    "of urgent business back home.":
        "Une lettre apparemment écrite et signée de Mlle Deane, l’excusant de la réception pour "
        "affaires urgentes chez elle.",
    "Forged Leaving Letter": "Lettre de départ contrefaite",
    "A letter excusing Miss Deane from the event. It is a fake, the signature forged.":
        "Une lettre excusant Mlle Deane de la réception. C’est un faux : la signature est "
        "contrefaite.",
    "Miss Deane checked in only a few days ago, so someone should recall which room she stayed in.":
        "Mlle Deane s’est enregistrée il y a quelques jours à peine ; quelqu’un doit se rappeler sa "
        "chambre.",
    "Miss Deane signed the registration book a few days ago.":
        "Mlle Deane a signé le registre il y a quelques jours.",
    "By process of elimination, it seems Mister O'Meara is the man who Miss Deane fought with "
    "before she went missing.":
        "Par élimination, c’est M. O’Meara qui s’est querellé avec Mlle Deane avant sa disparition.",
    "Miss Deane was seen wandering the halls in a daze the night she went missing.":
        "On a vu Mlle Deane errer dans les couloirs, hébétée, la nuit de sa disparition.",
    "I found a drawing that Miss Hisham has done of a vase.":
        "J’ai trouvé un dessin de vase exécuté par Mlle Hisham.",
    "Miss Hisham supplied me with a piece of music, reputed to be the key to the lock that hides "
    "the vase.":
        "Mlle Hisham m’a remis un morceau de musique, réputé être la clé de la serrure qui protège "
        "le vase.",
    "Miss Mantovani appears to be alive.. at least for now.":
        "Mlle Mantovani paraît en vie… du moins pour l’instant.",
    "Miss Mantovani... She is dead... Evaporated by the ritual...":
        "Mlle Mantovani… Elle est morte… Volatilisée par le rituel…",
    "Signs suggest Miss Mantovani is unwell.":
        "Tout indique que Mlle Mantovani est souffrante.",
    "Diary belonging to Miss Ivy McLeod, found in her room.":
        "Journal intime appartenant à Mlle Ivy McLeod, trouvé dans sa chambre.",
    "A lockbox belonging to Miss McLeod, located within her room.":
        "Un coffret appartenant à Mlle McLeod, trouvé dans sa chambre.",
    "A note from Miss McLeod to Mister Hunter. Miss McLeod believes Miss Deane is psychically "
    "attacking her, and asking Mister Hunter for help. Could he have acted on this?":
        "Un billet de Mlle McLeod à M. Hunter. Elle y dit que Mlle Deane l’attaque par voie "
        "psychique et lui demande son aide. Aurait-il agi en conséquence ?",
})


DESCRIPTIONS.update({
    "One of the hotel doors is missing. Somehow... closed over?":
        "Une des portes de l’hôtel a disparu. Comme… murée ?",
    "The door to Miss Deane's room is missing. Somehow... closed over?":
        "La porte de la chambre de Mlle Deane a disparu. Comme… murée ?",
    "A journal entry detailing a recent altercation between Miss Deane and Miss Quinn.":
        "Une page de journal relatant une altercation récente entre Mlle Deane et Mlle Quinn.",
    "Some of the Séance spaces are empty now...":
        "Certaines places de la Séance sont désormais vides…",
    "The library research books on Tír na nÓg are missing.":
        "Les ouvrages de la bibliothèque sur Tír na nÓg ont disparu.",
    "A collection of notes I found in Missus Erickson's lockbox.":
        "Un ensemble de notes trouvées dans le coffret de Mme Erickson.",
    "Missus Erickson intends to murder and then eat someone's heart. I must find a way to stop "
    "her.":
        "Mme Erickson entend assassiner quelqu’un puis lui dévorer le cœur. Il me faut trouver le "
        "moyen de l’arrêter.",
    "This well thumbed bible. It is clear Leviticus was a favorite as the pages are more marked "
    "and worn.":
        "Cette bible très feuilletée. Le Lévitique en était manifestement le passage favori : les "
        "pages y sont plus marquées et plus usées.",
    "A scarlet locked box found in the room of Missus Lau.":
        "Un coffret écarlate, fermé à clé, trouvé dans la chambre de Mme Lau.",
    "I found a dagger in Missus Lau's lockbox. It is a thin blade with a decorative handle. There "
    "is no blood on the blade.":
        "J’ai trouvé une dague dans le coffret de Mme Lau. Une lame fine, au manche ouvragé. Aucune "
        "trace de sang.",
    "Diary belonging to Missus Victoria Lau, found in her room.":
        "Journal intime appartenant à Mme Victoria Lau, trouvé dans sa chambre.",
    "I noticed the numbered sequence '34525' written in the journal of Missus Lau.":
        "J’ai relevé la suite de chiffres « 34525 » dans le journal de Mme Lau.",
    "A key I found under the pillow of Missus Victoria Lau.":
        "Une clé trouvée sous l’oreiller de Mme Victoria Lau.",
    "Romantic correspondence between Mister D'Arcy and his mistress wherein they arrange to meet "
    "here, at this event.":
        "Une correspondance amoureuse entre M. D’Arcy et sa maîtresse, où ils conviennent de se "
        "retrouver ici, à cette réception.",
    "A Gnostic bible. I found this in the Men's Dormitory, under Mister Doyle's bed. It doesn't "
    "seem to have been opened in a while.":
        "Une bible gnostique, trouvée au dortoir des hommes, sous le lit de M. Doyle. Elle ne "
        "semble pas avoir été ouverte depuis longtemps.",
    "Mister Doyle has asked me to tell Father Sinnott that he is abandoning their Gnostic quest.":
        "M. Doyle m’a demandé d’annoncer au père Sinnott qu’il renonce à leur quête gnostique.",
    "Mister Dupré has suffered a recent loss. It has affected him greatly.":
        "M. Dupré a subi une perte récente. Elle l’a profondément affecté.",
    "I found a letter from Mister Dupré, saying he feels the company of his deceased friend when "
    "he has been to the firepit.":
        "J’ai trouvé une lettre de M. Dupré disant qu’il sent la présence de son amie défunte "
        "lorsqu’il se rend au foyer.",
    "One of the guests.": "L’un des invités.",
    "A record of Mister O'Meara's time at the hotel.":
        "Un relevé du séjour de M. O’Meara à l’hôtel.",
    "Three tarot cards - one marked 'The Hanged Man', another called 'Death', and a third called "
    "'Ten of Pentacles'.":
        "Trois cartes de tarot : l’une marquée « Le Pendu », une autre « La Mort », et une "
        "troisième « Dix de deniers ».",
    "A number I noticed imprinted onto a letter I found.":
        "Un nombre que j’ai relevé, imprimé en creux sur une lettre trouvée.",
    "Mister Skerritt is a failed businessman - though he still has a fortune in wealth.":
        "M. Skerritt est un homme d’affaires en faillite — quoiqu’il demeure fort riche.",
    "He seems very interested in who the summoned ghost might be at the séance, and what it would "
    "do for that ghost's reputation.":
        "Il paraît fort intéressé de savoir quel fantôme sera invoqué à la séance, et ce que cela "
        "ferait pour la renommée dudit fantôme.",
    "Learn the meaning of Mister Skerritt's tarot cards.":
        "Découvrir le sens des cartes de tarot de M. Skerritt.",
    "Mister Skerritt has no idea what to do with his fortune once he dies as he has no family to "
    "pass it to.":
        "M. Skerritt ignore que faire de sa fortune après sa mort, n’ayant aucune famille à qui la "
        "léguer.",
    "The hotel manager.": "Le gérant de l’hôtel.",
    "A code found in the quarters of Mister Varley - 37, 22, 34":
        "Un code trouvé dans les quartiers de M. Varley — 37, 22, 34",
    "The person who was kidnapped has red hair. I should check to see if Mister Ó Finn is still "
    "about.":
        "La personne enlevée avait les cheveux roux. Je devrais vérifier que M. Ó Finn est toujours "
        "là.",
    "Mister Ó Finn is still alive. I have a chance to save him!":
        "M. Ó Finn est encore en vie. J’ai une chance de le sauver !",
    "I'm too late to save Mister Ó Finn...": "J’arrive trop tard pour sauver M. Ó Finn…",
    "A bag of ritual components, full of natural objects inscribed with the Ogham language.":
        "Un sac de composants rituels, empli d’objets naturels gravés d’ogham.",
    "Mister Ó Finn is descended from the sorcerer rulers of the Milesians.":
        "M. Ó Finn descend des souverains sorciers milésiens.",
    "Mister D'Arcy's letters are to his mistress, who was Miss Deane.":
        "Les lettres de M. D’Arcy s’adressent à sa maîtresse, qui n’était autre que Mlle Deane.",
    "I should learn the reason behind the Marquess' motivation for the séance.":
        "Je devrais découvrir ce qui pousse le marquis à tenir cette séance.",
    "A jet and ivory cameo depicting a man's silhouette.":
        "Un camée de jais et d’ivoire figurant la silhouette d’un homme.",
    "A crib with the name \"Murphy\" carved into the headboard.":
        "Un berceau dont la tête porte le nom « Murphy » gravé.",
    "He's wearing a crest pinned to his necktie, but I don't recognise it.":
        "Il porte un blason épinglé à sa cravate, mais je ne le reconnais pas.",
    "Masonic Crest On Necktie": "Blason maçonnique sur une cravate",
    "He's wearing a crest pinned to his necktie, and it seems to be of the Freemasons. I can only "
    "assume he is a member.":
        "Il porte un blason épinglé à sa cravate, et il semble être celui des francs-maçons. Je ne "
        "puis que le supposer membre.",
    "Coming back to the house, I saw someone watching me from a window in the Blake private "
    "residence. It left me with a terrible sense of unease.":
        "En revenant vers la maison, j’ai vu quelqu’un m’observer d’une fenêtre de la résidence "
        "privée des Blake. Cela m’a laissé un affreux malaise.",
    "There appears to something hidden behind the vent in the luggage room.":
        "Quelque chose semble dissimulé derrière la bouche d’aération de la consigne.",
    "A symbol I do not recognise which I found on a door in the catacombs.":
        "Un symbole inconnu, trouvé sur une porte des catacombes.",
    "I saw this symbol on a door in the catacombs.":
        "J’ai vu ce symbole sur une porte des catacombes.",
    "Mister Coventry has given me two names for his deceased wife - Lillian Smith and Elaine "
    "Dabny.":
        "M. Coventry m’a donné deux noms pour sa défunte épouse : Lillian Smith et Elaine Dabny.",
    "Mister O'Meara's recent brush with death seems to be a common thing for him - one he wants to "
    "put a stop to.":
        "M. O’Meara a récemment frôlé la mort, ce qui paraît lui être coutumier — et il souhaite y "
        "mettre un terme.",
    "A near-empty bottle, its remaining contents most definitely a hard liquor of some kind.":
        "Une bouteille presque vide, dont le fond est à coup sûr quelque alcool fort.",
    "The design on her necklace is reminiscent of cracked porcelain.":
        "Le motif de son collier évoque de la porcelaine fêlée.",
    "She hides it well, but seems uncomfortable... for what reason?":
        "Elle le cache bien, mais paraît mal à l’aise… pour quelle raison ?",
    "A series of newspaper clippings... with my picture or name circled in each of them.":
        "Une série de coupures de presse… avec, dans chacune, mon portrait ou mon nom entouré.",
    "A series of newspaper clippings... with my name circled.":
        "Une série de coupures de presse… avec mon nom entouré.",
    "Mister Skerritt has no family, either close or otherwise.":
        "M. Skerritt n’a aucune famille, proche ou éloignée.",
    "Despite his efforts, Mister Skerritt has failed to build himself any form of close network.":
        "Malgré ses efforts, M. Skerritt n’est parvenu à se constituer aucun cercle proche.",
    "Mister Coventry's room has no mementos of his recently deceased wife.":
        "La chambre de M. Coventry ne contient aucun souvenir de sa femme récemment disparue.",
    "A master key for all bedrooms in the North East Corridor, for use by the staff.":
        "Un passe-partout ouvrant toutes les chambres du couloir nord-est, à l’usage du personnel.",
    "Mister Hunter's master key.": "Le passe-partout de M. Hunter.",
    "A note from Mister Varley instructing Miss Murphy to come pick up a letter from his office.":
        "Un billet de M. Varley enjoignant à Mlle Murphy de venir prendre une lettre à son bureau.",
    "A notebook, worn around the edges, kept close to hand.":
        "Un carnet aux bords usés, gardé à portée de main.",
    "Miss Deane has been investigating her own bloodline - one of three ancient Milesian lines. "
    "She seeks to tap into that power. Can this be real?":
        "Mlle Deane enquêtait sur sa propre lignée — l’une des trois anciennes lignées milésiennes. "
        "Elle cherche à en puiser le pouvoir. Cela peut-il être vrai ?",
    "Mister Toussaint has compiled a veritable archive on Missus Erickson, now with the crucial "
    "proof that she is a fraud.":
        "M. Toussaint a constitué un véritable dossier sur Mme Erickson, désormais assorti de la "
        "preuve décisive de son imposture.",
    "A collection of notes and reminders kept in the servants' hall.":
        "Un ensemble de notes et de pense-bêtes tenus dans la salle des domestiques.",
    "An apparently abandoned nursery.": "Une chambre d’enfant, apparemment abandonnée.",
    "Extensive research on the O'Connor family from the 1700s to almost the present day.":
        "Des recherches approfondies sur la famille O’Connor, du XVIIIe siècle à presque nos jours.",
    "I found this in the safe in the Blake Residence. It feels oddly warm in my hand. What could "
    "its purpose be?":
        "J’ai trouvé ceci dans le coffre de la résidence Blake. Elle est étrangement tiède dans ma "
        "main. À quoi peut-elle bien servir ?",
    "Hagstone": "Pierre-à-trou",
    "Somehow, this stone saved me at the séance...":
        "D’une manière ou d’une autre, cette pierre m’a sauvé à la séance…",
    "An ancient alphabet of Irish origin, primarily written with straight lines.":
        "Un alphabet ancien d’origine irlandaise, tracé pour l’essentiel en traits droits.",
    "An old anvil, untouched by everything but the weather.":
        "Une vieille enclume, que rien n’a touchée hormis les intempéries.",
    "I found a tome of old Irish magic in the walled garden after following the clues in Miss "
    "Deane's room. It surely belonged to her.":
        "J’ai trouvé dans le jardin clos un tome de vieille magie irlandaise, en suivant les "
        "indices de la chambre de Mlle Deane. Il lui appartenait à coup sûr.",
    "A photograph of a much younger Miss McLeod and Mister Hunter, standing in front of a "
    "different estate.":
        "Une photographie de Mlle McLeod et de M. Hunter, bien plus jeunes, devant un autre domaine.",
    "A key with a strange symbol on it. Mister Varley believes it may lead to a stash of gold "
    "hidden somewhere on the manor grounds.":
        "Une clé portant un symbole étrange. M. Varley croit qu’elle mène à un dépôt d’or caché "
        "quelque part sur les terres du manoir.",
    "The old well in the hedge maze.": "Le vieux puits, dans le labyrinthe de haies.",
    "A hotel guest. An English socialite with a sharp personality.":
        _guest_f("Une mondaine anglaise au caractère acéré."),
    "I should find a means to open this box.":
        "Je devrais trouver le moyen d’ouvrir ce coffret.",
    "He's not leaning on it - it's just for show.":
        "Il ne s’y appuie pas — elle n’est là que pour la parade.",
    "His belt is quite eye-catching.": "Sa ceinture attire l’œil.",
    "This sigil fills me with dread, but then it's overpowered by a sense of ambition. Are these "
    "emotions my own, or do they belong to someone else?":
        "Ce sceau m’emplit d’effroi, aussitôt supplanté par un sentiment d’ambition. Ces émotions "
        "sont-elles miennes, ou appartiennent-elles à un autre ?",
    "Oscail (Open)": "Oscail (Ouvrir)",
    "Sturdy working clothes, and well worn-in. He must spend a lot of time outside.":
        "Des vêtements de travail solides et bien usés. Il doit passer beaucoup de temps dehors.",
    "I found an unfinished portrait of Miss Deane.":
        "J’ai trouvé un portrait inachevé de Mlle Deane.",
    "Discs of finely cut paper.": "Des disques de papier finement découpés.",
    "An envelope of money I found in a purse marked E.D.. There is a note included with it that "
    "reads, \"£100. £50 taken.\"":
        "Une enveloppe d’argent trouvée dans une bourse marquée E. D. Un billet l’accompagne : "
        "« 100 £. 50 £ prélevées. »",
    "I should so as Mister Doyle has asked.":
        "Je devrais faire ce que M. Doyle m’a demandé.",
    "I have been told that it is possible to cross over to Tír na nÓg via special passageways.":
        "On m’a dit qu’il est possible de passer à Tír na nÓg par certains passages.",
    "Her clothes have seen many repairs.": "Ses vêtements ont été maintes fois raccommodés.",
    "Its varnish is worn around the grip - she uses it often, and probably for long periods of "
    "time.":
        "Le vernis est usé là où on la tient — elle s’en sert souvent, et sans doute longuement.",
    "The portrait of Percy Blake.": "Le portrait de Percy Blake.",
    "A recently-created ordering system for the elements that make up the world.":
        "Un système de classement récent des éléments qui composent le monde.",
    "Mary Blake was remembered for her charitable work.":
        "On gardait de Mary Blake le souvenir de ses œuvres charitables.",
    "A photograph of me with my brother. Taken here, now. How is this possible? However it is, I "
    "am grateful for it.":
        "Une photographie de moi et de mon frère. Prise ici, maintenant. Comment est-ce possible ? "
        "Quoi qu’il en soit, j’en suis reconnaissant.",
    "A photograph of Miss Evelyn Deane. She looks to be in her twenties.":
        "Une photographie de Mlle Evelyn Deane. Elle paraît avoir une vingtaine d’années.",
    "A photograph of Miss Murphy's infant daughter.":
        "Une photographie de la petite fille de Mlle Murphy.",
    "A book I found in the Blake Residence.":
        "Un livre trouvé dans la résidence Blake.",
    "A small bust with letters inscribed in the skull. Is this modern science?":
        "Un petit buste dont le crâne porte des lettres inscrites. Est-ce là la science moderne ?",
    "It is believed by some that Blake Manor, or rather the land is now sits on, is a place of "
    "ancient power.":
        "Certains tiennent Blake Manor, ou plutôt la terre où il s’élève, pour un lieu de pouvoir "
        "ancien.",
    "Though he might hide it, he is keeping a close eye on the time.":
        "Il a beau le dissimuler, il surveille l’heure de près.",
    "A bottle of drinking alcohol - with a high ethanol content.":
        "Une bouteille d’alcool de bouche — à forte teneur en éthanol.",
    "An otherworldly portal I saw in the hedge maze while hallucinating.":
        "Un portail d’un autre monde, vu dans le labyrinthe alors que j’hallucinais.",
    "Mister D'Arcy's ring and final resting place.":
        "La bague de M. D’Arcy, et sa dernière demeure.",
    "Miss Mantovani has prepared some money for sending to Italy.":
        "Mlle Mantovani a préparé une somme à envoyer en Italie.",
    "Miss Deane's journal, found in my room after I had that strange dream.":
        "Le journal de Mlle Deane, trouvé dans ma chambre après cet étrange rêve.",
    "There are traces of a white substance around his pocket.":
        "Des traces d’une substance blanche entourent sa poche.",
    "Proof is needed to declare somebody to be a fraud.":
        "Il faut des preuves pour déclarer quelqu’un imposteur.",
    "The waters that spring forth from this well protect the area. I should examine the well to "
    "find a way to bless it, and in doing so, protect the innocents nearby.":
        "Les eaux qui jaillissent de ce puits protègent la contrée. Je devrais l’examiner pour "
        "trouver le moyen de le bénir et, ce faisant, protéger les innocents des environs.",
    "Miss Callaghan is a protector of the land.":
        "Mlle Callaghan est une protectrice de la terre.",
    "An open, straight stance, as is so common with the gentry.":
        "Un maintien droit et ouvert, si commun chez les gens de qualité.",
    "Mister D'Arcy is tormenting Missus D'Arcy in the afterlife, I should find a means to ease him "
    "from visiting this mortal coil.":
        "M. D’Arcy tourmente Mme D’Arcy depuis l’au-delà ; je devrais trouver le moyen de le "
        "détourner de ce bas monde.",
    "A bottle of quinine powder found in the locked box of Missus Lau.":
        "Un flacon de poudre de quinine trouvé dans le coffret fermé de Mme Lau.",
    "His hands are red raw, with a subtle but unmistakable smell of a modern doctor's office.":
        "Ses mains sont à vif, avec l’odeur discrète mais reconnaissable d’un cabinet médical "
        "moderne.",
    "My Old Testament is rusty, I should find a bible and look up 'Leviticus 20:27'.":
        "Mon Ancien Testament est rouillé ; je devrais trouver une bible et chercher « Lévitique "
        "20, 27 ».",
    "Mister Skerritt is ready for his end.": "M. Skerritt est prêt pour sa fin.",
    "Miss Deane fought with Mister O'Meara as she asked for his help and he rejected her.":
        "Mlle Deane s’est querellée avec M. O’Meara après qu’il eut refusé l’aide qu’elle lui "
        "demandait.",
    "Her dress has been taken in somewhat, like it was made for someone else.":
        "Sa robe a été quelque peu reprise, comme si elle avait été taillée pour une autre.",
    "A recipe for an cleaning solution especially good for sticky substances. 2 parts chlorine to "
    "1 part soap, mixed with a dash of ethanol in a bucket of water. Substitutes can be used.":
        "Une recette de solution nettoyante, excellente contre les substances collantes. Deux parts "
        "de chlore pour une de savon, avec un trait d’éthanol dans un seau d’eau. On peut y "
        "substituer d’autres produits.",
    "Mister Ó Finn and his kidnapper recognised one another, which may be why he was kidnapped.":
        "M. Ó Finn et son ravisseur se sont reconnus, ce qui explique peut-être son enlèvement.",
    "A record of hypnotic music that is ideal for keeping the listener in a certain type of sleep "
    "state.":
        "Un disque de musique hypnotique, idéal pour maintenir l’auditeur dans un certain état de "
        "sommeil.",
    "With his issues laid to rest, what is next for him?":
        "Ses tourments apaisés, que lui réserve la suite ?",
    "With her issues laid to rest, what is next for her?":
        "Ses tourments apaisés, que lui réserve la suite ?",
    "Despite being a most eligible bachelor, Marquess Blake has refused remarrying, dedicating "
    "himself to his wife's memory and his son.":
        "Quoique fort bon parti, le marquis Blake a refusé de se remarier, se consacrant à la "
        "mémoire de sa femme et à son fils.",
    "Some extensive research into the history of the region.":
        "Des recherches approfondies sur l’histoire de la région.",
    "A request from Miss Deane to be tutored in Irish magic by Miss Callaghan. Rejected and ripped "
    "to pieces.":
        "Une demande de Mlle Deane sollicitant de Mlle Callaghan un enseignement de la magie "
        "irlandaise. Refusée et déchirée en morceaux.",
    "Remains I found inside a hidden room.":
        "Des restes trouvés dans une pièce dissimulée.",
    "One of the stable doors has been replaced. Judging by the weathering, I would say it was done "
    "recently.":
        "L’une des portes d’écurie a été remplacée. À en juger par la patine, c’est récent.",
    "Where can I find out more about this faith?":
        "Où puis-je en apprendre davantage sur cette foi ?",
    "There must be more information in the library to assist me.":
        "La bibliothèque doit contenir de quoi m’éclairer davantage.",
    "I should learn more about lucid dreaming to see if it can help me revisit the dream I had.":
        "Je devrais me documenter sur le rêve lucide, pour voir s’il peut m’aider à revivre mon "
        "rêve.",
    "Learning about the ancient Milesian rulers may help me discover why Miss Deane and Mister Ó "
    "Finn were targeted by the culprit.":
        "M’instruire des anciens souverains milésiens m’aidera peut-être à comprendre pourquoi le "
        "coupable a choisi Mlle Deane et M. Ó Finn.",
    "Could the apparition I saw near the Old Anvil be connected to the entity? I should revisit "
    "the book in the library and see if there are any connections to smithing.":
        "L’apparition vue près de la vieille enclume aurait-elle un lien avec l’entité ? Je devrais "
        "revenir au livre de la bibliothèque et chercher un rapport avec la forge.",
    "I should learn what happened the Tuatha Dé Danann.":
        "Je devrais apprendre ce qu’il est advenu des Tuatha Dé Danann.",
    "I should learn more about the Tuatha Dé Danann.":
        "Je devrais en apprendre davantage sur les Tuatha Dé Danann.",
    "Something strange is happening with Mister Ó Finn's staff. I found it and his crown floating. "
    "There are strange runes carved into it.":
        "Il se passe quelque chose d’étrange avec le bâton de M. Ó Finn. Je l’ai trouvé en "
        "lévitation, avec sa couronne. D’étranges runes y sont gravées.",
    "I should delve deeper into the history of the vase.":
        "Je devrais creuser l’histoire du vase.",
    "Perhaps there's something in the Library that could help me translate the Ogham language.":
        "La bibliothèque recèle peut-être de quoi m’aider à traduire l’ogham.",
    "Any books on Tír na nÓg have been taken from the library, I might be better to ask around "
    "about it instead.":
        "Tous les livres sur Tír na nÓg ont disparu de la bibliothèque ; mieux vaudrait sans doute "
        "me renseigner de vive voix.",
    "I must see what the Marquess, the Manager, and the stablemaster were doing on Tuesday night.":
        "Il me faut établir ce que faisaient le marquis, le gérant et le maître d’écurie le mardi "
        "soir.",
    "Miss Mantovani has a bad feeling about the Séance, and has instructed me to hold her money to "
    "send to her next of kin at the first available opportunity.":
        "Mlle Mantovani a un mauvais pressentiment au sujet de la Séance ; elle m’a chargé de "
        "garder son argent pour l’envoyer aux siens à la première occasion.",
    "There looks to be something stuffed behind this vent. If I had a tool of some kind perhaps I "
    "could reach it.":
        "Quelque chose semble coincé derrière cette bouche d’aération. Avec un outil quelconque, je "
        "pourrais peut-être l’atteindre.",
    "Miss Barbosa is urgently waiting for a telegram. What information might it have that has her "
    "so testy.":
        "Mlle Barbosa attend un télégramme avec impatience. Quel renseignement peut-il contenir "
        "pour la rendre si irritable ?",
    "I should return to the ladies bathroom to investigate once some time has passed and the room "
    "is free.":
        "Je devrais retourner examiner les toilettes des dames une fois quelque temps écoulé et la "
        "pièce libre.",
    "The blackmail has caused a rift between the two women...":
        "Le chantage a creusé une faille entre les deux femmes…",
    "The intent of this ritual was to lure a victim to something... I wonder what impact this had "
    "on Miss Deane and if the other guests saw anything suspicious.":
        "Ce rituel visait à attirer une victime vers quelque chose… Je me demande quel effet il a "
        "eu sur Mlle Deane, et si les autres invités ont remarqué quoi que ce soit de suspect.",
    "A series of markings painted onto the floor. Somehow I understand its intent - to lure the "
    "victim into a sleep state and draw their attention to... something?":
        "Une série de marques peintes sur le plancher. J’en saisis d’instinct le dessein : plonger "
        "la victime dans le sommeil et attirer son attention vers… quelque chose ?",
    "I found ritual markings painted onto the floor under Mister Ó Finn's bed.":
        "J’ai trouvé des marques rituelles peintes sur le plancher, sous le lit de M. Ó Finn.",
    "Notes describing an arcane ritual to consume a magic user's heart in order to gain their "
    "powers and vigour.":
        "Des notes décrivant un rituel obscur : dévorer le cœur d’un praticien pour s’emparer de "
        "ses pouvoirs et de sa vigueur.",
    "Mister Dupré gave me the key to his room":
        "M. Dupré m’a remis la clé de sa chambre",
    "A key to room 19, where Missus Hazel Erickson is staying.":
        "Une clé de la chambre 19, où loge Mme Hazel Erickson.",
    "Rooms 2, 7, 15, and 21 are unoccupied for this event. Miss Deane must have been staying in "
    "one of those rooms.":
        "Les chambres 2, 7, 15 et 21 sont inoccupées durant cette réception. Mlle Deane devait "
        "loger dans l’une d’elles.",
    "A hotel guest. A local Doctor and apprentice in magic.":
        _guest("Un médecin du pays, apprenti en magie."),
    "Marquess Blake intends to sacrifice his son as the third bloodline for his ritual.":
        "Le marquis Blake entend sacrifier son fils comme troisième lignée pour son rituel.",
    "A Saint Brigid's cross, presumably put out by one of the staff.":
        "Une croix de sainte Brigide, sans doute disposée par quelqu’un du personnel.",
    "A block of salt from the cloakroom.": "Un bloc de sel pris au vestiaire.",
    "The hotel's cook.": "La cuisinière de l’hôtel.",
    "A sigil Father Sinnott had carved into his chest. He claims that it has the ability to kill a "
    "powerful otherworldly entity's body, thus freeing its soul.":
        "Un sceau que le père Sinnott s’est fait graver dans la poitrine. Il affirme qu’il peut "
        "tuer le corps d’une puissante entité d’un autre monde, et libérer ainsi son âme.",
    "Scaoil (Release)": "Scaoil (Libérer)",
    "A sigil Father Sinnott claims has the ability to kill a powerful otherworldly entity's body, "
    "thus freeing its soul. Miss Deane's note in her Grimoire translated this name as 'release'.":
        "Un sceau qui, selon le père Sinnott, peut tuer le corps d’une puissante entité d’un autre "
        "monde et libérer ainsi son âme. Une note de Mlle Deane, dans son grimoire, en traduit le "
        "nom par « libérer ».",
    "His scarring looks as if he's seen some sort of combat.":
        "Ses cicatrices donnent à penser qu’il a connu quelque combat.",
    "Multiple scars, as if she's suffered several different accidents and injuries.":
        "De multiples cicatrices, comme si elle avait subi plusieurs accidents et blessures.",
    "The mad scrawlings on these papers are largely indecipherable. There are notes about "
    "'séances', 'life energy' and 'channelling' among them. The letter \"S\" has been scratched on "
    "the topmost page in red ink.":
        "Les gribouillages fous de ces feuillets sont pour l’essentiel indéchiffrables. On y "
        "distingue des notes sur les « séances », l’« énergie vitale » et le « canal ». La lettre "
        "« S » a été tracée à l’encre rouge sur la page du dessus.",
    "I suspect he's got treats for the horses in his pockets.":
        "Je le soupçonne d’avoir des friandises pour les chevaux dans ses poches.",
    "A scrap of paper left in the library by Miss Quinn - it seems to suggest an intention to "
    "undertake something strange.":
        "Un bout de papier laissé à la bibliothèque par Mlle Quinn — il semble annoncer le projet "
        "de quelque chose d’étrange.",
    "Symbols on scrap paper. Some of them have been scratched out.":
        "Des symboles sur un bout de papier. Certains ont été rayés.",
    "An old rusted screwdriver I found in the stables.":
        "Un vieux tournevis rouillé trouvé aux écuries.",
    "A sigil that dissolved whatever it has been linked to.":
        "Un sceau qui dissout ce à quoi on le lie.",
    "The lineage of the Blakes going back hundreds of years.":
        "La lignée des Blake, remontant sur des siècles.",
    "In the place where Room 20's door should be, I can only see a sigil on the wall. How can that "
    "be?":
        "Là où devrait se trouver la porte de la chambre 20, je ne vois qu’un sceau sur le mur. "
        "Comment est-ce possible ?",
    "The hotel's porter.": "Le portier de l’hôtel.",
    "Miss Barbosa finally knows her late father's real name.":
        "Mlle Barbosa connaît enfin le véritable nom de son défunt père.",
    "Something feels different since the lucid dream. I should thoroughly search my room.":
        "Quelque chose a changé depuis le rêve lucide. Je devrais fouiller ma chambre de fond en "
        "comble.",
    "There could be some insights I can glean if I search around. There must be a cleaning closet "
    "Missus Joyce works from. However Missus Joyce being the housekeeper could have left something "
    "in any of the main manor rooms.":
        "Je pourrais glaner quelque chose en fouillant. Mme Joyce doit avoir un placard à balais "
        "d’où elle opère. Mais, en tant que gouvernante, elle a pu laisser quelque chose dans "
        "n’importe quelle pièce du manoir.",
    "All sightings of the Entity are linked to the hedge maze, can I learn more about it somewhere "
    "there?":
        "Toutes les apparitions de l’Entité se rattachent au labyrinthe ; puis-je y apprendre "
        "quelque chose de plus ?",
    "Where meals are prepared.": "Là où l’on prépare les repas.",
    "Where clothes are washed and mended, and other housekeeping tasks take place.":
        "Là où l’on lave et raccommode le linge, et où se font les autres travaux de maison.",
    "A collection of newspaper clippings and notes on Miss Evelyn Deane.":
        "Un ensemble de coupures de presse et de notes sur Mlle Evelyn Deane.",
    "Mister Varley mentioned in a note that he has a letter for Miss Murphy, I should search his "
    "room to find what is written.":
        "M. Varley mentionnait dans un billet qu’il détient une lettre pour Mlle Murphy ; je "
        "devrais fouiller sa chambre pour en connaître la teneur.",
    "Mister Varley's private quarters.": "Les quartiers privés de M. Varley.",
    "Where the men among the staff sleep (not including the manager).":
        "Là où dorment les hommes du personnel (le gérant excepté).",
    "I should thoroughly search the room, exhausting all avenues in the search for clues.":
        "Je devrais fouiller la pièce de fond en comble, sans négliger la moindre piste.",
    "The staff's recreational area.": "La salle de détente du personnel.",
    "I should investigate the sleeping quarters of the staff.":
        "Je devrais fouiller les dortoirs du personnel.",
    "A storehouse for deliveries and household valuables not on display.":
        "Une réserve pour les livraisons et les objets de valeur qu’on ne laisse pas en vue.",
    "Where wine and other alcoholic drinks are stored.":
        "Là où l’on entrepose le vin et les autres boissons alcoolisées.",
    "Where the women among the staff sleep.":
        "Là où dorment les femmes du personnel.",
    "An ability in foreknowledge and foresight in Scottish tradition, one which Miss McLeod claims "
    "to possess.":
        "Un don de prescience et de seconde vue, dans la tradition écossaise, dont Mlle McLeod se "
        "réclame.",
    "A hidden door leading from the ballroom to underground catacombs.":
        "Une porte dérobée menant de la salle de bal aux catacombes souterraines.",
    "It appears to be a home laboratory. I suppose the Blakes are known to be eccentric...":
        "Ceci paraît être un laboratoire domestique. Les Blake ont, il est vrai, une réputation "
        "d’excentricité…",
    "Miss Barbosa wishes to see her dead father's image.":
        "Mlle Barbosa souhaite voir le portrait de son père défunt.",
    "A large shrouded figure I have felt around the manor.":
        "Une grande silhouette voilée, dont j’ai senti la présence dans le manoir.",
    "Miss Mantovani's jewellery is quietly jangling - it's as if her entire body is shaking "
    "despite the mild temperature.":
        "Les bijoux de Mlle Mantovani tintent doucement — comme si tout son corps tremblait, malgré "
        "la douceur de l’air.",
    "He seems to be suffering from some kind of tremor.":
        "Il semble atteint d’une sorte de tremblement.",
    "Symbols on some grubby paper. Some of them are too shaky to make out.":
        "Des symboles sur un papier crasseux. Certains sont trop tremblés pour être lus.",
    "It's not just myself and Miss Deane sharing dreams - many guests are experiencing their own "
    "versions of this dream.":
        "Nous ne sommes pas seuls, Mlle Deane et moi, à partager ces songes — bien des invités "
        "vivent leur propre version de ce rêve.",
    "The staff all spoke in unison when pressed about the Blake family.":
        "Le personnel a parlé à l’unisson lorsqu’on l’a pressé au sujet des Blake.",
    "The staff all spoke in a glassy-eyed unison when pressed about the Blake family as if in a "
    "trance.":
        "Le personnel a parlé à l’unisson, le regard vitreux, lorsqu’on l’a pressé au sujet des "
        "Blake — comme en transe.",
    "I must show Missus Erickson the notes to prevent her from going forward with her hideous "
    "plan.":
        "Il me faut montrer ces notes à Mme Erickson pour l’empêcher de mener à bien son "
        "abominable dessein.",
    "A collection of notes Mister Toussaint has collated, gathering together Missus Ericksons "
    "various fraudulent activities. I used this to convince Missus Erickson that murder will not "
    "aid her.":
        "Un dossier rassemblé par M. Toussaint, recensant les diverses impostures de Mme Erickson. "
        "Je m’en suis servi pour la convaincre que le meurtre ne lui servirait de rien.",
    "I should present the picture of Miss Murphy's child to Father Sinnott and see if he is "
    "willing to help her.":
        "Je devrais présenter au père Sinnott le portrait de l’enfant de Mlle Murphy et voir s’il "
        "consent à l’aider.",
    "Mary Blake's bedroom in the Blake residence.":
        "La chambre de Mary Blake, dans la résidence Blake.",
    "A sigil I found in with other papers related to Henry Blake.":
        "Un sceau trouvé parmi d’autres papiers concernant Henry Blake.",
    "The hotel's sign-in book.": "Le registre des arrivées de l’hôtel.",
    "There are signs that a trail was left through Blake Manor.":
        "Tout indique qu’une piste a été laissée à travers Blake Manor.",
    "I found children's toys under the bed in room 2. I wonder if they are from the young master "
    "or a previous guest?":
        "J’ai trouvé des jouets d’enfant sous le lit de la chambre 2. Sont-ils au jeune maître ou à "
        "un précédent occupant ?",
    "His fine blue scarf seems at odds with the rest of his attire.":
        "Sa belle écharpe bleue jure avec le reste de sa mise.",
    "A hotel guest. An aging jeweller from London, unfamiliar with events of this sort.":
        _guest("Un joaillier vieillissant venu de Londres, peu familier de ce genre de réception."),
    "Seamus Doyle, porter of the Blake Manor.":
        "Seamus Doyle, portier de Blake Manor.",
    "Mister Skerritt's reading suggests he should make a sacrifice to gain a new perspective on "
    "the world.":
        "La lecture de M. Skerritt lui conseille un sacrifice pour porter sur le monde un regard "
        "neuf.",
    "Charcoal and papyrus which appear to have been used for drawing.":
        "Du fusain et du papyrus qui semblent avoir servi à dessiner.",
    "A skull-shaped mask I found in the catacombs. It has a long red hair stuck inside of it.":
        "Un masque en forme de crâne trouvé dans les catacombes. Un long cheveu roux y est resté "
        "pris.",
    "Sleeping aids found in the room of Mister Coventry.":
        "Des somnifères trouvés dans la chambre de M. Coventry.",
    "A set of projector slides.": "Un jeu de plaques de projection.",
    "A slipper I found in the hedge maze.":
        "Un chausson trouvé dans le labyrinthe de haies.",
    "Scars from years of cooking.": "Des cicatrices dues à des années de cuisine.",
    "A crest which reads, Society of Psychical Research.":
        "Un blason portant l’inscription « Society for Psychical Research ».",
    "Jars used to capture souls, or soul-like entities.":
        "Des jarres servant à capturer les âmes, ou les entités qui leur ressemblent.",
    "There are signs of a trail in the South East Corridor on the first floor.":
        "On relève des traces de passage dans le couloir sud-est du premier étage.",
    "A master key for the bedrooms in the south east corridor, meant for use by the staff.":
        "Un passe-partout ouvrant les chambres du couloir sud-est, à l’usage du personnel.",
    "A key that unlocks all the bedrooms in the upper southwest corridor, meant for use by the "
    "staff.":
        "Une clé ouvrant toutes les chambres du couloir sud-ouest supérieur, à l’usage du personnel.",
    "A disc that can be rotated to form a number of different sigils.":
        "Un disque que l’on fait tourner pour composer différents sceaux.",
    "A board used to communicate, of a fashion, with the dead.":
        "Une planche servant à communiquer, en quelque manière, avec les morts.",
    "A photography set-up supposedly capable of capturing the image of spirits.":
        "Un dispositif photographique censé saisir l’image des esprits.",
    "A yew branch with the simplest of ornamentation but he carries it proudly.":
        "Une branche d’if, de l’ornementation la plus simple, qu’il porte pourtant avec fierté.",
    "The staff's rota for the weekend -  I have recorded their movements in my timetable.":
        "Le tableau de service du personnel pour le week-end — j’en ai consigné les allées et "
        "venues dans mon emploi du temps.",
    "His hands are stained with something but I cannot tell what.":
        "Ses mains sont tachées de quelque chose, mais je ne saurais dire de quoi.",
    "\"It was 8pm they fought. I know because the bar was quiet with all the blue bloods playing "
    "bridge.\"":
        "« Ils se sont querellés à 20 heures. Je le sais parce que le bar était calme, tous les "
        "gens de qualité étant au bridge. »",
    "\"The lovely Miss Mantovani offered me a reading. How could I refuse?\"":
        "« La charmante Mlle Mantovani m’a proposé une consultation. Comment refuser ? »",
    "Mister Hunter claims he was working on the stall door on the night of the bridge game.":
        "M. Hunter affirme qu’il réparait la porte d’une stalle le soir de la partie de bridge.",
    "Mister Toussaint claims that Miss Murphy can attest to his whereabouts while Miss Deane was "
    "engaged in her fight.":
        "M. Toussaint affirme que Mlle Murphy peut témoigner de l’endroit où il se trouvait pendant "
        "la querelle de Mlle Deane.",
    "\"I took the opportunity to meet with the housekeeper and coordinate rotas for the following "
    "day.\"":
        "« J’en ai profité pour voir la gouvernante et régler les services du lendemain. »",
    "Searching the supply closet I found a stone cross. There are rusty red stains across it...":
        "En fouillant la réserve, j’ai trouvé une croix de pierre. Elle est striée de taches d’un "
        "rouge de rouille…",
    "This madness has gone on too long! I need to stop Coventry's ritual from proceeding. Only I "
    "can stop it now.":
        "Cette folie n’a que trop duré ! Il me faut empêcher le rituel de Coventry d’aboutir. Moi "
        "seul le puis désormais.",
    "I must get to the Grand Séance ritual and stop it from proceeding.":
        "Il me faut gagner le rituel de la Grande Séance et l’empêcher d’aboutir.",
    "Something terrible is going to happen. I must stop it.":
        "Quelque chose d’épouvantable va se produire. Il me faut l’empêcher.",
    "A cage inside the store room, for securing things the staff want to keep especially safe.":
        "Une cage, dans la réserve, où le personnel met à l’abri ce qu’il tient pour précieux.",
    "A bible but not one that I recognise.":
        "Une bible, mais qui ne m’est pas familière.",
    "A strange contraption in the atrium. It has a gauge on the front of it.":
        "Un étrange appareil dans l’atrium. Un cadran en orne la face.",
    "A strange contraption in the atrium. It has a gauge on the front of it that seems to move as "
    "people's plans for the séance change.":
        "Un étrange appareil dans l’atrium. Le cadran qui en orne la face paraît bouger à mesure "
        "que changent les intentions de chacun quant à la séance.",
    "I had a strange dream on my first night here and Miss Deane's journal suggests she might have "
    "experienced the same - are we alone in that?":
        "J’ai fait un rêve étrange ma première nuit ici, et le journal de Mlle Deane donne à penser "
        "qu’elle a connu le même — sommes-nous seuls dans ce cas ?",
    "It seems the guests are having strange dreams - something beyond the occasional nightmare "
    "here and there.":
        "Il semble que les invités fassent d’étranges rêves — bien au-delà du cauchemar "
        "occasionnel.",
    "I saw a strange light coming from the door of the ladies bathroom.":
        "J’ai vu une lueur étrange filtrer sous la porte des toilettes des dames.",
    "A bundle of horse hair and twigs found in the stable's safe. They are covered in chimney "
    "soot.":
        "Un paquet de crin et de brindilles trouvé dans le coffre des écuries. Le tout est couvert "
        "de suie de cheminée.",
    "It may be the atmosphere and the occult talk getting to me, but I am starting to think I am "
    "seeing some unsettling sights in these old halls...\"":
        "C’est peut-être l’atmosphère et tous ces propos d’occultisme qui me montent à la tête, "
        "mais je commence à croire que j’aperçois des choses troublantes dans ces vieux couloirs…",
    "A man's ring with a crucifix and rose in its centre.":
        "Une bague d’homme, ornée en son centre d’un crucifix et d’une rose.",
    "Man's Stylised Ring": "Bague d’homme stylisée",
    "A man's ring with a crucifix and rose in its centre, the same symbol on Missus D'arcy's "
    "brooch.":
        "Une bague d’homme, ornée en son centre d’un crucifix et d’une rose — le même symbole que "
        "sur la broche de Mme D’Arcy.",
    "The translation of Mister O'Meara's Enochian text, revealed to be the name of a supposed "
    "angel.":
        "La traduction du texte énochien de M. O’Meara, qui se révèle être le nom d’un prétendu "
        "ange.",
    "Mister Skerritt is willing to make the ultimate sacrifice to achieve his goals.":
        "M. Skerritt est prêt au sacrifice suprême pour parvenir à ses fins.",
    "Mister Dupré is having trouble laying his friend to rest, and seeks to bring out the 3 "
    "aspects of Saint Brigid. Dupré represents Maman Brigitte, and the ghost has chosen myself to "
    "represent the Goddess Bríd. I must find another to represent Saint Brigid.":
        "M. Dupré peine à donner le repos à son amie et cherche à faire paraître les trois aspects "
        "de sainte Brigide. Dupré représente Maman Brigitte, et le fantôme m’a choisi pour "
        "représenter la déesse Bríd. Il me faut trouver quelqu’un pour représenter sainte Brigide.",
    "Somebody undertook a ritual to summon a ghost.":
        "Quelqu’un a accompli un rituel pour invoquer un fantôme.",
    "Miss Quinn undertook a ritual to summon a ghost.":
        "Mlle Quinn a accompli un rituel pour invoquer un fantôme.",
    "A distinct archway in the basement of the east tower.":
        "Une arche remarquable, au sous-sol de la tour est.",
    "There's to be a delivery on Sunday around noon.":
        "Une livraison est prévue dimanche, vers midi.",
    "Miss Mantovani looks very tired.": "Mlle Mantovani paraît fort lasse.",
    "His eyes are red, as if something is irritating them.":
        "Ses yeux sont rouges, comme irrités par quelque chose.",
    "A suspiciously large locked box that I should open for proof of fraudulence. A correct series "
    "of letters is needed to open the lock. I wonder what would be close to Missus Erickson's "
    "heart?":
        "Un coffret fermé, d’une taille suspecte, que je devrais ouvrir pour prouver l’imposture. "
        "Il faut une suite de lettres exacte. Qu’est-ce qui peut bien tenir au cœur de Mme "
        "Erickson ?",
    "A sequence of symbols.": "Une suite de symboles.",
    "A syringe containing a potent narcotic - possibly enough to knock a grown man unconscious for "
    "several hours.":
        "Une seringue contenant un narcotique puissant — de quoi, sans doute, assommer un homme "
        "fait pour plusieurs heures.",
    "A ritual intended to allow the participants to speak with the dead.":
        "Un rituel censé permettre aux participants de s’entretenir avec les morts.",
    "Fiadh is worried about the spiritual aftermath of the séance.":
        "Fiadh s’inquiète des suites spirituelles de la séance.",
    "Miss Mantovani's contract to host the séance. It seems she's being paid a substantial sum.":
        "Le contrat par lequel Mlle Mantovani s’engage à tenir la séance. La somme paraît "
        "considérable.",
    "The séance ended in chaos and disaster. The real ritual, then, has begun.":
        "La séance s’est achevée dans le chaos et le désastre. Le véritable rituel a donc commencé.",
    "The ghost that will speak at the séance - whichever ghost they can lure in and make speak.":
        "Le fantôme qui parlera à la séance — quel qu’il soit, pourvu qu’on parvienne à l’attirer "
        "et à le faire parler.",
    "Surviving Séance participants.": "Les participants survivants de la Séance.",
    "The people who attended the séance.": "Les personnes qui ont assisté à la séance.",
    "Mister Coventry's gift to the young master piques my interest. I should talk to the boy to "
    "understand their connection.":
        "Le présent de M. Coventry au jeune maître pique ma curiosité. Je devrais parler au garçon "
        "pour comprendre ce qui les lie.",
    "Talk!": "Parler !",
    "A schedule containing the titles, topics, and speakers of every talk planned for the week.":
        "Un programme donnant les titres, les sujets et les orateurs de toutes les conférences "
        "prévues cette semaine.",
    "Evidence of a ring, worn for a long time, and since removed.":
        "La marque d’une bague longtemps portée, puis retirée.",
    "I have been warned to watch Missus Erickson, she is not all she claims to be.":
        "On m’a mis en garde contre Mme Erickson : elle n’est pas ce qu’elle prétend.",
    "Miss Barbosa's search for information on her father has hit a dead end.":
        "Les recherches de Mlle Barbosa sur son père sont dans l’impasse.",
    "The manor's method for sending and receiving telegrams.":
        "Le moyen dont dispose le manoir pour envoyer et recevoir des télégrammes.",
    "Telegraph Machine, Fixed": "Télégraphe, réparé",
    "The manor's method for sending and receiving telegrams. Now fixed.":
        "Le moyen dont dispose le manoir pour envoyer et recevoir des télégrammes. Réparé.",
    "Missus Erickson confessed to being a fraud intending to murder and canabalise Miss Deane. I "
    "should inform Mister Toussaint.":
        "Mme Erickson a avoué son imposture et son intention d’assassiner Mlle Deane pour la "
        "dévorer. Je devrais en informer M. Toussaint.",
    "Her body language is tense. Is it due to the event or something else?":
        "Son maintien est crispé. Est-ce la réception, ou autre chose ?",
    "From what I gather, this is some form of Gnostic entity. Supposedly, one is trapped here at "
    "Blake Manor.":
        "D’après ce que je comprends, il s’agit d’une entité gnostique. L’une d’elles serait "
        "prisonnière ici, à Blake Manor.",
    "The final battle between the Milesians and the Tuatha Dé Danann that saw the gods leave this "
    "realm.":
        "L’ultime bataille entre les Milésiens et les Tuatha Dé Danann, au terme de laquelle les "
        "dieux quittèrent ce monde.",
    "I'm unsure what this is but the Gnostics think we need to be freed from it.":
        "J’ignore ce que c’est, mais les gnostiques estiment qu’il nous en faut être délivrés.",
    "The remaining members of the Blake family.":
        "Les derniers membres de la famille Blake.",
    "There was once a door here... I must find a way to make it reappear.":
        "Il y avait une porte ici, autrefois… Il me faut trouver le moyen de la faire reparaître.",
    "An enraged Jonathan Blake killed Simon Coventry, really Henry Blake, and accidentally himself "
    "- ending the Blake bloodline.":
        "Jonathan Blake, hors de lui, a tué Simon Coventry — en réalité Henry Blake — et, par "
        "accident, lui-même : la lignée des Blake s’éteint.",
    "The entity haunting Blake Manor.": "L’entité qui hante Blake Manor.",
    "Goibniu": "Goibniu",
    "The entity haunting Blake Manor - the ancient Irish god of smithing, Goibniu.":
        "L’entité qui hante Blake Manor — Goibniu, l’ancien dieu irlandais de la forge.",
    "The Fae are said to be a mythical race that live alongside humanity... and sometimes cause "
    "them all manner of grief.":
        "Les Fae seraient un peuple mythique vivant aux côtés des hommes… et leur causant parfois "
        "toutes sortes de tourments.",
    "The ancient Irish god of smithing and hospitality.":
        "L’ancien dieu irlandais de la forge et de l’hospitalité.",
    "A goddess, a hag, and diviner, whose domains are cold, winds, and winter.":
        "Une déesse, une vieille et une devineresse, dont les domaines sont le froid, les vents et "
        "l’hiver.",
    "The war witch of the Tuatha Dé Danann was the goddess of war, wealth, and death. Crows are "
    "her symbol.":
        "La sorcière guerrière des Tuatha Dé Danann était la déesse de la guerre, de la richesse et "
        "de la mort. Les corbeaux sont son emblème.",
    "The old Irish goddess of healing, poetry, the hearth, smithing, and much else besides.":
        "L’ancienne déesse irlandaise de la guérison, de la poésie, du foyer, de la forge et de "
        "bien d’autres choses encore.",
    "The manor is hosting 'The Grand Séance', which claims it will be the most advanced gathering "
    "of its kind, allowing the audience to speak directly with a spirit instead of through a "
    "medium.":
        "Le manoir accueille « la Grande Séance », qui se veut la plus avancée du genre : "
        "l’assistance y parlerait directement à un esprit, sans passer par un médium.",
    "The séance attendees staying at the manor.":
        "Les participants à la séance qui logent au manoir.",
    "The letter 'P' found scrawled across some Blake family histories.":
        "La lettre « P », griffonnée en travers de certaines histoires de la famille Blake.",
    "The letter 'S' was found highlighted in some scattered notes within the Blake residence.":
        "La lettre « S », relevée dans des notes éparses de la résidence Blake.",
    "The letter 'Y' was circled in a book of Celtic Legends.":
        "La lettre « Y », entourée dans un recueil de légendes celtiques.",
    "Walter Blake does not like the company of strangers.":
        "Walter Blake n’aime pas la compagnie des étrangers.",
    "When I arrived at the manor I found Miss Mantovani's shawl in the fountain, where I saw the "
    "washer woman. What could the connection be?":
        "À mon arrivée au manoir, j’ai trouvé le châle de Mlle Mantovani dans la fontaine, là où "
        "j’ai vu la blanchisseuse. Quel peut être le lien ?",
    "The stewards of the manor.": "Les gens de maison du manoir.",
    "Percival Blake was drowned in retaliation for supposedly walling up some locals, though no "
    "signs of the walling have been found. A portrait of him hangs in the east tower.":
        "Percival Blake fut noyé en représailles pour avoir prétendument emmuré des gens du pays, "
        "quoiqu’on n’ait jamais trouvé trace de cet emmurement. Son portrait est accroché dans la "
        "tour est.",
    "The Vase of Nectanebo was found in the piano of its last known owner, Wilhelmina Blake.":
        "Le vase de Nectanébo fut trouvé dans le piano de sa dernière propriétaire connue, "
        "Wilhelmina Blake.",
    "Mister Hunter and Miss McLeod seem to have had a close bond from before this event.":
        "M. Hunter et Mlle McLeod semblent liés d’avant cette réception.",
    "I must find someone to represent Saint Brigid to help lay Mister Dupré's friend to rest.":
        "Il me faut trouver quelqu’un pour représenter sainte Brigide et aider l’amie de M. Dupré à "
        "trouver le repos.",
    "The Milesians were led by three brothers - Éber Finn,  Amergin, and Eremon.":
        "Les Milésiens étaient menés par trois frères : Éber Finn, Amergin et Érémon.",
    "Ominous stones with holes in them. Dark brown stains ring the holes.":
        "Des pierres inquiétantes, percées de trous. Des taches d’un brun sombre en cernent les "
        "bords.",
    "Mister O'Meara has a reputation as somewhat of a thrill seeker.":
        "M. O’Meara passe pour être quelque peu amateur de sensations fortes.",
    "A drawing that I found scrawled on the underside of a ticket for luggage bay 46. It depicts a "
    "sigil.":
        "Un dessin griffonné au dos d’un bulletin de la case 46. Il figure un sceau.",
    "My record of the other attendee's movements across the weekend.":
        "Mon relevé des allées et venues des autres invités durant le week-end.",
    "She looks tired, as if she hasn't slept well in a long time.":
        "Elle paraît lasse, comme si elle n’avait pas bien dormi depuis longtemps.",
    "He looks exhausted - and like he has been exhausted for a very long time, at that.":
        "Il paraît épuisé — et épuisé depuis fort longtemps, qui plus est.",
    "A torn up letter found in the room of Miss Callaghan. I can piece this together.":
        "Une lettre déchirée trouvée dans la chambre de Mlle Callaghan. Je puis la reconstituer.",
    "Mister Doyle seems to be planning to leave Blake Manor to go travelling.":
        "M. Doyle semble projeter de quitter Blake Manor pour courir le monde.",
    "A lost cache of gold, stashed away for safe keeping and long since forgotten.":
        "Un dépôt d’or perdu, mis à l’abri puis oublié de longue date.",
    "<i>“Start in the garden in autumn. Walk east to the junction, then north for three. Turn west "
    "and walk for two junctions, then south for one. It is kept behind the cornerstone which is "
    "seen when you face the stairs.” </i>":
        "<i>« Partez du jardin en automne. Allez à l’est jusqu’au croisement, puis au nord sur "
        "trois. Tournez à l’ouest et marchez deux croisements, puis un vers le sud. Il est gardé "
        "derrière la pierre d’angle que l’on voit en faisant face à l’escalier. » </i>",
    "A trunk I found in bay 46 of the luggage room. There's something odd about the pattern on its "
    "lid.":
        "Une malle trouvée dans la case 46 de la consigne. Le motif de son couvercle a quelque "
        "chose d’étrange.",
    "Miss Murphy seems to be trying to speak with Father Sinnott on some matter.":
        "Mlle Murphy semble chercher à s’entretenir avec le père Sinnott de quelque affaire.",
    "The old Irish gods, said once to live alongside humanity.":
        "Les anciens dieux d’Irlande, qui vécurent jadis, dit-on, aux côtés des hommes.",
    "A bottle of turpentine that I found under Miss Deane's bed, along with a set of strange "
    "markings.":
        "Un flacon de térébenthine trouvé sous le lit de Mlle Deane, avec un ensemble de marques "
        "étranges.",
    "A fallen typewriter. I can see drafts of invites to a 'Deane', an 'Ó Finn' and a 'Mantovani' "
    "for the séance.":
        "Une machine à écrire renversée. J’y distingue des brouillons d’invitations à la séance "
        "pour une « Deane », un « Ó Finn » et une « Mantovani ».",
    "The Irish Otherworld and afterlife. Home of the Tuatha Dé Danann and the Fae.":
        "L’Autre Monde irlandais, et l’au-delà. Demeure des Tuatha Dé Danann et des Fae.",
    "Why is Miss McLeod suddenly chasing a husband? I should look into her motive for this.":
        "Pourquoi Mlle McLeod se met-elle soudain en quête d’un mari ? Je devrais en chercher le "
        "motif.",
    "He looks profoundly displeased. Is it with me, or something else?":
        "Il paraît profondément mécontent. Est-ce de moi, ou d’autre chose ?",
    "A Celtic cross - though it seems somehow different to many I've seen.":
        "Une croix celtique — quoiqu’elle diffère, je ne sais trop comment, de beaucoup de celles "
        "que j’ai vues.",
    "His resurrectix looks different to any I've seen.":
        "Son crucifix ne ressemble à aucun de ceux que j’ai vus.",
    "A stark streak of white runs through her otherwise red hair.":
        "Une mèche d’un blanc net traverse sa chevelure par ailleurs rousse.",
    "An urn, full of ashes.": "Une urne, pleine de cendres.",
    "Mister Hunter has given me a key to a door. Of which, he's unsure of. What will it unlock?":
        "M. Hunter m’a remis la clé d’une porte. Laquelle, il l’ignore. Qu’ouvrira-t-elle ?",
    "A flyer for the Séance nailed to Miss Mantovani's door. <i>Leviticus 20:27</i> is scrawled "
    "across it.":
        "Un prospectus de la Séance cloué à la porte de Mlle Mantovani. <i>Lévitique 20, 27</i> y "
        "est griffonné en travers.",
    "Modern vats sit in the room. They seem to have figures inside them.":
        "Des cuves modernes occupent la pièce. Des formes semblent s’y trouver.",
    "Inside the locket I've found a small vial of what can only be blood.":
        "Dans le médaillon, j’ai trouvé une petite fiole de ce qui ne peut être que du sang.",
    "A half empty bottle of thallium. What's left is enough to kill someone - as is what has been "
    "used...":
        "Un flacon de thallium à moitié vide. Ce qui reste suffirait à tuer quelqu’un — tout comme "
        "ce qui en a été prélevé…",
    "A hotel guest. Miss McLeod's chaperone.": _guest_f("Le chaperon de Mlle McLeod."),
    "A vision sparked by the sigil in Miss Deane's room. In it, I saw someone attempt to remove "
    "the sigil under the bed. When they couldn't, they magically sealed the room to cover their "
    "tracks.":
        "Une vision déclenchée par le sceau de la chambre de Mlle Deane. J’y ai vu quelqu’un tenter "
        "d’effacer le sceau sous le lit. N’y parvenant pas, il a scellé la pièce par magie pour "
        "couvrir ses traces.",
    "Cells from the makeshift battery I found.":
        "Les éléments de la pile de fortune que j’ai trouvée.",
    "He's leaning on that cane for support. The way he's standing leaves no doubt.":
        "Il s’appuie vraiment sur cette canne. Son maintien ne laisse aucun doute.",
    "A young couple walled up to punish their love.":
        "Un jeune couple emmuré en châtiment de son amour.",
    "Marquess Blake's young son.": "Le jeune fils du marquis Blake.",
    "The young Master of Blake Manor.": "Le jeune maître de Blake Manor.",
    "Discarded attempts to add Walter Blake into the family portraits.":
        "Des essais abandonnés visant à ajouter Walter Blake aux portraits de famille.",
    "A wanted poster for Miss Barbosa - she is wanted for arson and manslaughter.":
        "Un avis de recherche visant Mlle Barbosa — pour incendie volontaire et homicide.",
    "Mister Hunter created wards of protection for Miss McLeod, Missus Lau, and himself.":
        "M. Hunter a créé des sceaux de protection pour Mlle McLeod, Mme Lau et lui-même.",
    "I thought I saw a woman washing clothes in the fountain out front of the manor...":
        "J’ai cru voir une femme laver du linge dans la fontaine, devant le manoir…",
    "She has an acute gaze, no doubt watching events quite carefully.":
        "Son regard est perçant ; nul doute qu’elle observe les choses de fort près.",
    "Mister Skerritt is wealthy through vast inheritance.":
        "M. Skerritt doit sa fortune à un vaste héritage.",
    "Expensive attire, but nothing flashy. He's wealthy, but doesn't care if people know it or "
    "not.":
        "Une mise coûteuse, mais sans ostentation. Il est riche et se moque qu’on le sache.",
    "The magical process of asking a well for visions or insights.":
        "Le procédé magique consistant à demander à un puits visions ou révélations.",
    "The magical process of asking a well for visions or insights. Miss Callaghan is performing a "
    "few on Sunday. I have marked the information in my timetable.":
        "Le procédé magique consistant à demander à un puits visions ou révélations. Mlle Callaghan "
        "en pratiquera quelques-unes dimanche. Je l’ai consigné dans mon emploi du temps.",
    "Celtic symbols painted around the well. These markings appear to be a recent addition.":
        "Des symboles celtiques peints autour du puits. Ces marques semblent récentes.",
    "A tarot deck, worn by years of use.":
        "Un jeu de tarot, usé par des années d’usage.",
    "What was Missus Lau using the quinine powder for, and why was it locked away?":
        "À quoi Mme Lau destinait-elle cette poudre de quinine, et pourquoi la tenait-elle sous "
        "clé ?",
    "I must discover the connection and meaning of these symbols.<br>Are they an attempt to "
    "perform magic?":
        "Il me faut découvrir le lien et le sens de ces symboles.<br>Sont-ils une tentative de "
        "magie ?",
    "I found a three digit number but what is its relevance?":
        "J’ai trouvé un nombre à trois chiffres — mais quelle en est la portée ?",
    "Perhaps clues relating to the disappearance of Miss Deane are hidden in this safe.":
        "Peut-être ce coffre recèle-t-il des indices sur la disparition de Mlle Deane.",
    "There is a safe in the stabes. Might there be something useful to my investigation contained "
    "within?":
        "Il y a un coffre aux écuries. Contiendrait-il quelque chose d’utile à mon enquête ?",
    "I should find some substancial evidence regarding Mister Hunter and Miss McLeod's past.":
        "Je devrais trouver des preuves sérieuses touchant le passé de M. Hunter et de Mlle McLeod.",
    "A collection of small, dried, white flowers in her hair.":
        "Un bouquet de petites fleurs blanches séchées dans ses cheveux.",
    "All records point to three Milesian bloodlines - if this is related to the disappearing "
    "guests, then who is the third line?":
        "Tous les documents désignent trois lignées milésiennes — si cela touche aux disparitions, "
        "quelle est donc la troisième ?",
    "Mister Coventry is here on the hope of speaking one last time with his recently deceased "
    "wife.":
        "M. Coventry est ici dans l’espoir de s’entretenir une dernière fois avec sa femme "
        "récemment disparue.",
    "He looks to be living a hermit's lifestyle.":
        "Il paraît mener une vie d’ermite.",
    "A will I found in Mister Coventry's room requesting all his ownings go to Walter Blake on his "
    "death.":
        "Un testament trouvé dans la chambre de M. Coventry, léguant tous ses biens à Walter Blake "
        "à sa mort.",
    "Her skin shows signs of much time spent outdoors.":
        "Sa peau porte les marques de longues heures passées au dehors.",
    "I found a lock in the wine cellar. I can see a key hanging on the wall inside.":
        "J’ai trouvé une serrure dans la cave à vin. J’aperçois une clé pendue au mur, à "
        "l’intérieur.",
    "A list of wines and their vintages.": "Une liste de vins et de leurs millésimes.",
    "A key to the women's dormitory.": "Une clé du dortoir des femmes.",
    "A lockbox I found near Missus Joyce's bed in the women's dormitory with strange symbols in "
    "place of buttons.":
        "Un coffret trouvé près du lit de Mme Joyce, au dortoir des femmes, avec d’étranges "
        "symboles en guise de boutons.",
    "A note to the manager complaining about Missus Joyce's prying conduct. It is signed by "
    "'Missus Olivia D'Arcy'.":
        "Un billet au gérant se plaignant de l’indiscrétion de Mme Joyce. Il est signé « Mme "
        "Olivia D’Arcy ».",
    "Discs made of zinc. Heavy for their size.":
        "Des disques de zinc. Lourds pour leur taille.",
})


# --------------------------------------------------- generated families
# "Could it have been X fighting with Miss Deane?" — one per suspect. Generated so
# the past participle always agrees with the right gender.
_SUSPECTS = [
    ("Doctor Callaghan", "le docteur Callaghan", False),
    ("Father Sinnott", "le père Sinnott", False),
    ("Marquess Blake", "le marquis Blake", False),
    ("Master Blake", "le jeune maître Blake", False),
    ("Miss Barbosa", "Mlle Barbosa", True),
    ("Miss Callaghan", "Mlle Callaghan", True),
    ("Missus Joyce", "Mme Joyce", True),
    ("Miss Mantovani", "Mlle Mantovani", True),
    ("Miss McLeod", "Mlle McLeod", True),
    ("Miss Murphy", "Mlle Murphy", True),
    ("Miss Quinn", "Mlle Quinn", True),
    ("Missus D'Arcy", "Mme D’Arcy", True),
    ("Missus Lau", "Mme Lau", True),
    ("Mister Coventry", "M. Coventry", False),
    ("Mister Doyle", "M. Doyle", False),
    ("Mister Dupré", "M. Dupré", False),
    ("Mister Hunter", "M. Hunter", False),
    ("Mister O'Meara", "M. O’Meara", False),
    ("Mister Skerritt", "M. Skerritt", False),
    ("Mister Touissaint", "M. Toussaint", False),   # the original misspells it
    ("Mister Varley", "M. Varley", False),
    ("Mister Ó Finn", "M. Ó Finn", False),
]
for _en, _fr, _fem in _SUSPECTS:
    DESCRIPTIONS[f"Could it have been {_en} fighting with Miss Deane?"] = _fight(_fr, _fem)

# "I can build a profile on X by analysing him/her, ..." — one per character.
_PROFILES = [
    ("Doctor Callaghan", "du docteur Callaghan", False),
    ("Father Sinnott", "du père Sinnott", False),
    ("Master Blake", "du jeune maître Blake", False),
    ("Miss Barbosa", "de Mlle Barbosa", True),
    ("Miss Callaghan", "de Mlle Callaghan", True),
    ("Miss Hisham", "de Mlle Hisham", True),
    ("Miss Mantovani", "de Mlle Mantovani", True),
    ("Miss McLeod", "de Mlle McLeod", True),
    ("Miss Murphy", "de Mlle Murphy", True),
    # Miss Quinn's profile line uses "them" in the original, not "her" — it is
    # added explicitly below rather than generated here.
    ("Missus D'Arcy", "de Mme D’Arcy", True),
    ("Missus Erickson", "de Mme Erickson", True),
    ("Missus Joyce", "de Mme Joyce", True),
    ("Missus Lau", "de Mme Lau", True),
    ("Mister Coventry", "de M. Coventry", False),
    ("Mister Doyle", "de M. Doyle", False),
    ("Mister Hunter", "de M. Hunter", False),
    ("Mister O'Meara", "de M. O’Meara", False),
    ("Mister Skerritt", "de M. Skerritt", False),
    ("Mister Toussaint", "de M. Toussaint", False),
    ("Mister Varley", "de M. Varley", False),
    ("Mister Ó Finn", "de M. Ó Finn", False),
]
for _en, _fr, _fem in _PROFILES:
    _pron = "her" if _fem else "him"
    DESCRIPTIONS[
        f"I can build a profile on {_en} by analysing {_pron}, speaking to {_pron} or other "
        f"guests about {_pron} and searching the manor."] = _profile(_fr, _fem)
# three that break the pattern in the original: doubled space, "them", "Marquess Blake"
DESCRIPTIONS["I can build a profile on Mister Dupré  by analysing him, speaking to him or other "
             "guests about him and searching the manor."] = _profile("de M. Dupré")
DESCRIPTIONS["I can build a profile on Miss Quinn by analysing them, speaking to them or other "
             "guests about them and searching the manor."] = _profile("de Mlle Quinn", True)
DESCRIPTIONS["I can build a profile on Marquess Blake by analysing him, speaking to him or other "
             "guests about him and searching the manor."] = _profile("du marquis Blake")

# staff quarters, one phrasing per character
for _en, _fr, _fem in [
    ("Miss Murphy's", "de Mlle Murphy", True),
    ("Missus Joyce's", "de Mme Joyce", True),
    ("Mister Doyle's", "de M. Doyle", False),
    ("Mister Hunter's", "de M. Hunter", False),
    ("Mister Varley's", "de M. Varley", False),
]:
    pass  # handled individually below, the English wording differs per character

DESCRIPTIONS.update({
    "I should investigate Miss Murphy's quarters to see if it contains anything useful. I assume "
    "she is housed in the manor's basement.":
        "Je devrais fouiller les quartiers de Mlle Murphy pour voir s’ils recèlent quoi que ce soit "
        "d’utile. Je suppose qu’elle loge au sous-sol du manoir.",
    "I must search where Missus Joyce sleeps. I assume she is housed in the manor's basement.":
        "Il me faut fouiller l’endroit où dort Mme Joyce. Je suppose qu’elle loge au sous-sol du "
        "manoir.",
    "I may find some useful information searching Mister Doyle's room. I assume he is housed in "
    "the manor's basement.":
        "Je pourrais trouver des renseignements utiles en fouillant la chambre de M. Doyle. Je "
        "suppose qu’il loge au sous-sol du manoir.",
    "Investigate his room to see what he could be hiding. I assume he is housed in the manor's "
    "basement.":
        "Fouiller sa chambre pour voir ce qu’il pourrait cacher. Je suppose qu’il loge au sous-sol "
        "du manoir.",
    "I should investigate Mister Varley's quarters to see if it contains anything useful. I assume "
    "he is housed in the manor's basement.":
        "Je devrais fouiller les quartiers de M. Varley pour voir s’ils recèlent quoi que ce soit "
        "d’utile. Je suppose qu’il loge au sous-sol du manoir.",
    "I may find some useful information searching Doctor Callaghan's room.":
        _room_of("du docteur Callaghan"),
    "I may find some useful information searching Mister O'Meara's room.":
        _room_of("de M. O’Meara"),
    "I may find some useful information searching Mister Ó Finn's room.":
        _room_of("de M. Ó Finn"),
    "I may find some useful information searching Mister Coventry's room.":
        _room_of("de M. Coventry"),
    "I may find some useful information searching Father Sinnott's room.":
        _room_of("du père Sinnott"),
    "I may find some useful information searching Miss Callaghan's room.":
        _room_of("de Mlle Callaghan"),
    "I should investigate Missus D'Arcy's quarters to see if it contains anything useful.":
        _quarters_of("de Mme D’Arcy", True),
    "I should investigate Miss Quinn's quarters to see if it contains anything useful.":
        _quarters_of("de Mlle Quinn", True),
    "I should investigate Miss Barbosa's quarters to see if it contains anything useful.":
        _quarters_of("de Mlle Barbosa", True),
    "I should investigate Mister Skerritt's room to see if it contains anything useful.":
        "Je devrais fouiller la chambre de M. Skerritt pour voir si elle recèle quoi que ce soit "
        "d’utile.",
})

# hotel rooms, by corridor
for _n, _corridor in [(15, "sud-est"), (2, "nord-ouest"), (21, "sud-ouest"), (7, "nord-est")]:
    _en_corridor = {"sud-est": "south east", "nord-ouest": "north west",
                    "sud-ouest": "south west", "nord-est": "north east"}[_corridor]
    DESCRIPTIONS[f"A room in the hotel's {_en_corridor} corridor."] = \
        f"Une chambre du couloir {_corridor} de l’hôtel."
