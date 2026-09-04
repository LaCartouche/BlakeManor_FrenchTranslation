# Relecture — système d’hypothèses

Anglais et français côte à côte. Régénérer avec `python3 tools/hypothesis_review.py`.

## Ce qu’il faut vérifier

La phrase s’affiche **pendant** que le joueur cherche : elle doit rester lisible
avec n’importe quelle combinaison, y compris fausse. Les règles dures
(`docs/HYPOTHESES.md`) : séquence de trous intouchable, l’article appartient au
jeton et non au gabarit, jamais `de [r]` ni `à [r]`, aucune élision devant un
trou, aucun accord avec un trou.

---

## Gabarits

### Miss Deane's Departure
`1.1.0.Arrival` — trous `rrv` ✅

| | |
|---|---|
| **EN** | [r] [r] is [v] |
| **FR** | [r] [r] est [v] |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| torn | déchirer |
| forged | contrefaire |
| covered | dissimuler |
| gave | remettre |

### Miss Deane's Bedroom
`2.1.0.DeanesRoom` — trous `vrvr` ✅

| | |
|---|---|
| **EN** | Miss Deane was seen [v] the [r] in a [v] caused by the [r] |
| **FR** | On a vu Mlle Deane [v] [r], plongée dans [v] — et la cause en est [r] |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| hidden | cacher |
| spotted | repérer |
| wandering | errer |
| sleeping | dormir |
| returning | revenir |

### The Trail
`2.3.0.FollowDeanesTrail` — trous `vrrr` ✅

| | |
|---|---|
| **EN** | Miss Deane was [v] the [r] by [r] while [r] watched. |
| **FR** | Mlle Deane s’est vue [v] [r] par [r], et [r] observait la scène. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| wandered | errer |
| led | guider |
| protected | protéger |
| left | quitter |
| chased | poursuivre |
| burnt | brûler |

### The Fight
`2.4.0.WhoFoughtWithDeane` — trous `vrvr` ✅

| | |
|---|---|
| **EN** | Miss Deane [v] with [r] when he [v] her [r]. |
| **FR** | Mlle Deane a dû [v] avec [r] lorsqu’il a voulu [v] [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| kissed | embrasser |
| fought | se battre |
| rejected | repousser |
| supported | soutenir |
| left | quitter |

### The Chase
`2.6.0.TheChase` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | I [v] into [r] as I [v] a [r] through the ballroom's [r]! |
| **FR** | J’ai dû [v] dans [r] en cherchant à [v] [r] par [r] de la salle de bal ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| descended | descendre |
| chased | poursuivre |
| hallucinated | halluciner |
| imagined | imaginer |
| aided | aider |

### The Missing Person
`3.1.0.WhosWho` — trous `rvrr` ✅

| | |
|---|---|
| **EN** | [r] was taken because he [v] the [r] from [r]! |
| **FR** | [r] a été enlevé car il a cherché à [v] [r] chez [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| kidnapped | enlever |
| recognised | reconnaître |
| worshipped | vénérer |
| murdered | assassiner |
| loved | aimer |

### The Basement
`3.3.0.InvestigateTheStaff` — trous `vrvr` ✅

| | |
|---|---|
| **EN** | Something [v] has affected the [r] and they're now [v] when asked about the [r]! |
| **FR** | Quelque chose vient de [v] [r], et voilà qu’il se met à [v] dès qu’on l’interroge sur [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| mesmerised | hypnotiser |
| speaking | parler |
| tricked | tromper |
| lying | mentir |
| bribed | soudoyer |

### Blake Residence
`3.4.0.BlakeResidence` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Jonathan Blake intends to [v] his [r] to [v] his [r] but [r]! |
| **FR** | Jonathan Blake compte [v] [r] pour [v] [r], mais [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| sacrifice | sacrifier |
| resurrect | ressusciter |
| abandon | abandonner |
| bury | enterrer |
| summon | invoquer |

### The Ritual
`3.5.0.TheRitual` — trous `vrvvr` ✅

| | |
|---|---|
| **EN** | You cannot [v] your [r]; you've been [v] by [v] so he can take over your [r]!
 |
| **FR** | Vous ne pouvez pas [v] [r] : on cherche à vous [v] pour [v], afin qu’il prenne [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| murder | assassiner |
| save | sauver |
| fooled | duper |
| kidnapped | enlever |
| summoned | invoquer |

### Ines Barbosa
`BarbosaQuests` — trous `vrrrr` ✅

| | |
|---|---|
| **EN** | Ines Barbosa's goal is to [v] a [r] in her [r] now that her [r] has [r]. |
| **FR** | Ines Barbosa veut [v] [r] dans [r], car [r] a [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| see | voir |
| discover | découvrir |
| sever | trancher |
| exorcise | exorciser |
| banish | bannir |

### Jonathan Blake
`BlakeQuests` — trous `vrvvr` ✅

| | |
|---|---|
| **EN** | You cannot [v] your [r]; you've been [v] by [v] so he can take over your [r]!
 |
| **FR** | Vous ne pouvez pas [v] [r] : on cherche à vous [v] pour [v], afin qu’il prenne [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| release | délivrer |
| restore | rétablir |

### Simon Coventry
`CoventryQuests` — trous `vrvrv` ✅

| | |
|---|---|
| **EN** | Simon Coventry's goal is to free [v] in order to assume the role of his [r], [v], to inherit his [r] because his real identity is ousted heir [v]. |
| **FR** | Simon Coventry veut libérer [v] pour prendre la place occupée par [r], [v], et hériter [r] — car sa véritable identité est celle de l’héritier évincé [v]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| coerce | contraindre |
| falling | déchoir |

### Olivia D'Arcy
`D'ArcyQuests` — trous `vrvvr` ✅

| | |
|---|---|
| **EN** | Olivia D'Arcy's goal is to [v] [r] as [v] for the [v] that occurred while she [r]. |
| **FR** | Olivia D’Arcy veut [v] [r] en guise de [v] pour [v], survenu à l’époque où [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| commit | commettre |
| revenge | vengeance |
| help | aider |
| balance | équilibre |
| exploit | exploiter |

### Ivy McLeod
`DarrochQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Ivy McLeod's goal is to [v] a [r] to [v] up her [r] with [r]. |
| **FR** | Ivy McLeod veut [v] [r] pour [v] [r] avec [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| find | trouver |
| cover | dissimuler |

### Seamus Doyle
`DoyleQuests` — trous `vrvrv` ✅

| | |
|---|---|
| **EN** | Seamus Doyle's goal was to [v] [r], but he [v] due to the [r] and now he wants to [v]. |
| **FR** | Seamus Doyle voulait [v] [r], mais il a fini par [v] sous [r], et désormais il veut [v]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| help | aider |
| forgot | oublier |
| murder | assassiner |
| declined | refuser |
| repented | se repentir |

### Lloyd Dupré
`DupreQuests` — trous `vrrr` ✅

| | |
|---|---|
| **EN** | Lloyd Dupré's goal is to [v] the [r] of his [r] into [r]. |
| **FR** | Lloyd Dupré veut [v] [r] — [r] — et lui offrir [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| lay | déposer |
| rest | apaiser |
| remove | arracher |
| run | fuir |

### Hazel Erickson
`EricksonQuests` — trous `vrrvr` ✅

| | |
|---|---|
| **EN** | Hazel Erickson's goal is to [v] the [r] of [r] to [v] her [r]. |
| **FR** | Hazel Erickson veut [v] [r] — [r] — pour [v] [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| perform | accomplir |
| steal | dérober |
| eating | dévorer |

### Fiadh Callaghan
`FiadhCallaghanQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Fiadh Callaghan's goal is to [v] the [r] to [v] the [r] from the [r]. |
| **FR** | Fiadh Callaghan veut [v] [r] pour [v] [r] contre [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| keep | garder |
| protect | protéger |
| share | partager |
| bless | bénir |
| harm | nuire |

### Arwa Hisham
`HishamQuests` — trous `vrvr` ✅

| | |
|---|---|
| **EN** | Arwa Hisham's goal is to [v] the [r] but she is [v] because it is [r].
 |
| **FR** | Arwa Hisham veut [v] [r], mais elle est [v] car tout cela est [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| search | chercher |
| reclaim | reprendre |

### Darragh Hunter
`HunterQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Darragh Hunter's goal is to [v] [r] to [v] [r] from [r]. |
| **FR** | Darragh Hunter veut [v] [r] pour [v] [r] contre [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| bind | lier |
| protect | protéger |

### Caitlin Joyce
`JoyceQuests` — trous `vrrvr` ✅

| | |
|---|---|
| **EN** | Caitlin Joyce's goal is to [v] [r] to [r] before she's able to [v] the [r]. |
| **FR** | Caitlin Joyce veut [v] [r] pour [r], avant de pouvoir [v] [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| suffer | souffrir |
| stoning | lapidation |
| write | écrire |
| burning | bûcher |

### Carmela Mantovani
`MantovaniQuests` — trous `vrvvr` ✅

| | |
|---|---|
| **EN** | Carmela Mantovani's goal is to [v] the [r] despite it [v] her as she wants to [v] for her [r]. |
| **FR** | Carmela Mantovani veut [v] [r], quitte à [v], car elle souhaite [v] pour [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| conduct | conduire |
| provide | fournir |
| manufacture | fabriquer |
| read | lire |
| predict | prédire |
| kill | tuer |
| strengthen | renforcer |

### Cathal O'Meara
`O'MearaQuests` — trous `vrvvvr` ✅

| | |
|---|---|
| **EN** | Cathal O'Meara's goal is to [v] [r] and [v] it so that he can [v] [v] his [r]. |
| **FR** | Cathal O’Meara veut [v] [r] puis [v], afin de pouvoir [v] et [v] [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| free | libérer |
| trap | piéger |
| kill | tuer |
| using | se servir |
| learning | apprendre |
| taking | prendre |

### Corentine Quinn
`QuinnQuests` — trous `rvrr` ✅

| | |
|---|---|
| **EN** | Corentine Quinn's goal is to perform a [r] to [v] the [r] from the [r]. |
| **FR** | Corentine Quinn veut accomplir [r] pour [v] [r] et libérer [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| perform | accomplir |
| remove | lever |
| increase | accroître |
| find | trouver |
| steal | dérober |

### Ruairí Callaghan
`RuairíCallaghanQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Ruairí Callaghan's goal is to [v] his [r] by [v] his [r] are [r]. |
| **FR** | Ruairí Callaghan veut [v] [r] en cherchant à [v] — [r] sont [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| proving | prouver |
| build | bâtir |
| destroy | détruire |
| conceal | dissimuler |
| escape | fuir |

### Saoirse Murphy
`SaoirseQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Saoirse Murphy's goal is to [v] with [r] to [v] about her [r] now that [r]. |
| **FR** | Saoirse Murphy veut [v] avec [r] pour [v] sur [r], car [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| speak | parler |
| learn | apprendre |
| pray | prier |
| absolve | absoudre |
| threaten | menacer |

### Lorcan Sinnott
`SinnottQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Father Sinnott's goal is to [v] [r] by [v] an [r] from the [r]. |
| **FR** | Le père Sinnott veut [v] [r] en cherchant à [v] [r] depuis [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| trap | piéger |
| enslave | asservir |
| kill | tuer |
| freeing | libérer |
| save | sauver |

### Michael Skerritt
`SkerrittQuests` — trous `vrvrvr` ✅

| | |
|---|---|
| **EN** | Micheal Skerritt's goal is to [v] his [r] and be [v] as the [r] to [v] from [r]. |
| **FR** | Michael Skerritt veut [v] [r] et rester [v] comme [r], afin de [v] depuis [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| kill | tuer |
| immortalised | immortalisé |
| commit | commettre |

### Etienne Toussaint
`ToussaintQuests` — trous `vvrr` ✅

| | |
|---|---|
| **EN** | Mister Toussaint's goal is to [v] me into [v] a [r] for [r]. |
| **FR** | M. Toussaint veut me [v] pour me pousser à [v] [r] pour [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| root | traquer |
| kill | tuer |
| frame | accuser |
| investigating | enquêter |
| framing | accuser à tort |

### Vincent Varley
`VarleyQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Vincent Varley's goal is to [v] [r] to [v] the [r] from [r]. |
| **FR** | Vincent Varley veut [v] [r] pour [v] [r] et préserver [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| conceal | dissimuler |
| protect | protéger |
| recruit | recruter |
| remove | écarter |
| steal | dérober |

### Victoria Lau
`ZhaoQuests` — trous `vrrvvr` ✅

| | |
|---|---|
| **EN** | Victoria Lau's goal is to [v] her [r] with [r] by [v] her so she can [v] [r]! |
| **FR** | Victoria Lau veut [v] [r] avec [r] en la faisant [v], pour pouvoir [v] [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| drugged | droguer |
| hide | cacher |

### The Haunting
`main.4.0.entity` — trous `rrvrr` ✅

| | |
|---|---|
| **EN** | The manor is haunted by [r] whose name is [r], and they want to [v] [r] through [r]! |
| **FR** | Le manoir est hanté par [r], dont le nom est [r], et il veut [v] [r] par [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| haunted | hanter |
| escape | fuir |
| drugged | droguer |
| fight | combattre |
| forged | contrefaire |
| speak | parler |

### The Dream
`main.5.0.dreams` — trous `vrrvr` ✅

| | |
|---|---|
| **EN** | We are all [v] [r]'s [r] that is [v] into [r]! |
| **FR** | Nous sommes tous en train de [v] [r] : [r] qui vient [v] dans [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| experiencing | vivre |
| dreams | rêver |
| spells | jeter un sort |
| cursed | maudire |
| malevolent | malveillant |

### Miss Deane's Attendance 
`main.6.0.deaneManor` — trous `rvr` ✅

| | |
|---|---|
| **EN** | Miss Deane attended because [r] [v] information about her [r]! |
| **FR** | Mlle Deane est venue car [r] a permis de [v] des informations sur [r] ! |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| attended | assister |
| promised | promettre |
| lied | mentir |
| forgot | oublier |
| fought | se battre |

### Domhnall Ó Finn
`ÓFinnQuests` — trous `vrvrr` ✅

| | |
|---|---|
| **EN** | Domhnall Ó Finn's goal was to [v] the [r] as it is his [v] as a [r] of the [r]. |
| **FR** | Domhnall Ó Finn voulait [v] [r], car tel est [v] — il est [r] parmi [r]. |

**Banque de verbes** — remplissent les trous `[v]`, à l’infinitif (invariables)

| EN | FR |
|---|---|
| protect | protéger |
| perform | accomplir |
| destroy | détruire |
| forget | oublier |
| condemn | condamner |

---

## Mots-jetons (332)

Ils remplissent les trous `[r]`. Chacun **porte son déterminant**, puisque le
gabarit ne peut pas savoir quel genre ni quel nombre va tomber dans le trou.

| EN | FR |
|---|---|
| a place of power | un lieu de pouvoir |
| a practitioner | un praticien |
| a shadowy figure | une silhouette dans l’ombre |
| a third party | un tiers |
| a tool | un outil |
| abilities | des dons |
| acolyte | un acolyte |
| addiction | une dépendance |
| Aeon | l’Éon |
| affair | une liaison |
| alcohol | l’alcool |
| an angel | un ange |
| an invite | une invitation |
| ancestral home | la demeure ancestrale |
| anchor | une ancre |
| ancient duty | un devoir ancestral |
| ancient power | un pouvoir ancien |
| ashes | des cendres |
| ate | a mangé |
| aunt's shadow | l’ombre de sa tante |
| battle | une bataille |
| beyond the grave | l’au-delà |
| bind | lier |
| Black Iron Prison | la prison de fer noir |
| blackmailed | victime d’un chantage |
| Blake Family | la famille Blake |
| bleeding | se répandre |
| bless | bénir |
| broken | hors d’usage |
| brought to | a conduit à |
| Bríd | Bríd |
| changing room | le vestiaire |
| chased | a donné la chasse |
| child | un enfant |
| closure | l’apaisement |
| code | un code |
| coerce | contraindre |
| communications | des communications |
| conceal | dissimuler |
| condemn | condamner |
| conduct | conduire |
| consume | consommer |
| cook | la cuisinière |
| cover | couvrir |
| crows | les corbeaux |
| curse | une malédiction |
| cursed | maudit |
| daze | un état second |
| dead friend | un ami défunt |
| death | la mort |
| descendant  | un descendant  |
| descended | est descendu |
| Detective Ward | le détective Ward |
| discerning | pénétrant |
| distracting | distrait |
| divine | deviner |
| Doctor Callaghan | le docteur Callaghan |
| document | un document |
| donate | faire don |
| doom | une fatalité |
| dream | un rêve |
| drug | une drogue |
| drugged | droguer |
| drugging | droguer |
| drugs | des drogues |
| east corridor | le couloir est |
| east tower | la tour est |
| entertained | les divertissements |
| escape | fuir |
| Evelyn Deane | Evelyn Deane |
| everyone | tout le monde |
| executor | un exécuteur testamentaire |
| exhausted | épuisé |
| experiencing | vivre |
| experimenting | expérimenter |
| exploring | explorer |
| expose | démasquer |
| fae | les fae |
| family | la famille |
| Father Sinnott | le père Sinnott |
| father's ghost | le fantôme de son père |
| father's homeland | la terre de son père |
| fiancé | un fiancé |
| find | trouver |
| first ghost | le premier fantôme |
| first millionaire | le premier millionnaire |
| fixed | réparé |
| forge | forger |
| forged | a contrefait |
| forgot | a oublié |
| forgotten | oublié |
| fought | s’est battu |
| fraudulence | l’imposture |
| free | libérer |
| freeing | libérer |
| friendship | une amitié |
| future | l’avenir |
| gardens | les jardins |
| ghost | un fantôme |
| ghosts | des fantômes |
| Goibniu | Goibniu |
| gone up in flames | parti en fumée |
| guest | un invité |
| guests | les invités |
| had a cold | était souffrante |
| hard work | un dur labeur |
| harm | du mal |
| he has no magic | il n’a aucun pouvoir |
| headdress | une coiffe |
| health | la santé |
| heart | un cœur |
| hedge maze | le labyrinthe de haies |
| heirloom | un bien de famille |
| help | de l’aide |
| Henry Blake | Henry Blake |
| her husband | son mari |
| hid | cacher |
| hide | cacher |
| himself | lui-même |
| his dead wife | son épouse défunte |
| his faith | sa foi |
| his luggage | ses bagages |
| his society | sa société |
| his society  | sa société  |
| horses | les chevaux |
| humanity | l’humanité |
| immortalised | immortalisé |
| invade | envahir |
| investigating | enquêter |
| jewellery | des bijoux |
| jewellery shop | la bijouterie |
| jewels | des joyaux |
| John Dee | John Dee |
| join the Freemasons | rejoindre les francs-maçons |
| kidnapped | l’a enlevé |
| kidnapper | un ravisseur |
| killed | l’a tué |
| killing | tuer |
| land | la terre |
| learn | apprendre |
| leave | partir |
| letter | une lettre |
| life to see it. | de vivre assez pour le voir. |
| live | vivre |
| local area | les environs |
| lock | une serrure |
| lose | perdre |
| lost in | s’est perdu dans |
| love | l’amour |
| luggage | des bagages |
| magic | la magie |
| magical abilities | des dons magiques |
| magical fabrication | une fabrication magique |
| Maman Brigitte | Maman Brigitte |
| manor | le manoir |
| manor's effect | l’effet du manoir |
| Marquess Blake | le marquis Blake |
| Mary Blake | Mary Blake |
| Master Blake | le jeune maître Blake |
| medical knowledge | des connaissances médicales |
| meeting | un rendez-vous |
| Milesian rulers | les souverains milésiens |
| miscarried | a perdu son enfant |
| Miss Barbosa | Mlle Barbosa |
| Miss Callaghan | Mlle Callaghan |
| Miss Darroch | Mlle Darroch |
| Miss Deane | Mlle Deane |
| Miss Deane can't help | Mlle Deane ne peut rien |
| Miss Deane's departure | le départ de Mlle Deane |
| Miss Deane's disappearance | la disparition de Mlle Deane |
| Miss Hisham | Mlle Hisham |
| Miss Joyce | Mme Joyce |
| Miss Mantovani | Mlle Mantovani |
| Miss McLeod | Mlle McLeod |
| Miss Murphy | Mlle Murphy |
| Miss Quinn | Mlle Quinn |
| missing doorway | la porte disparue |
| Missus D'Arcy | Mme D’Arcy |
| Missus Erickson | Mme Erickson |
| Missus Lau | Mme Lau |
| Mister Coventry | M. Coventry |
| Mister Doyle | M. Doyle |
| Mister Dupré | M. Dupré |
| Mister Hunter | M. Hunter |
| Mister O'Meara | M. O’Meara |
| Mister Skerritt | M. Skerritt |
| Mister Toussaint | M. Toussaint |
| Mister Varley | M. Varley |
| Mister Ó Finn | M. Ó Finn |
| modern techniques | les techniques modernes |
| money | de l’argent |
| monstrous Blake | le Blake monstrueux |
| mourn | pleurer |
| murder | assassiner |
| My arrival | mon arrivée |
| name | un nom |
| necklace with HOGD crest | un collier au blason H.O.G.D. |
| new life | une vie nouvelle |
| north east corridor | le couloir nord-est |
| north west corridor | le couloir nord-ouest |
| not here | il n’est pas ici |
| note | un billet |
| O'Connor family | la famille O’Connor |
| obsessed | obsédée |
| old life | l’ancienne vie |
| own life | sa propre vie |
| packs | des liasses |
| pagan beliefs | des croyances païennes |
| past | le passé |
| penny-pinching | l’avarice |
| personal belongings | les effets personnels |
| photo of Miss Deane | la photo de Mlle Deane |
| played | a joué |
| playing | jouer |
| plea for help | un appel à l’aide |
| plot | un complot |
| powerful Milesian ancestors | de puissants ancêtres milésiens |
| praying | prier |
| promised | promettre |
| protect | protéger |
| provide | subvenir |
| proving | prouver |
| Quinn family | la famille Quinn |
| reading | une consultation |
| reality | la réalité |
| reclaim | reprendre |
| recognised | l’a reconnu |
| reconnect | renouer |
| record | un registre |
| recruit | recruter |
| redeem | racheter |
| rejected | l’a repoussée |
| relationship | une liaison |
| release | délivrer |
| remove | écarter |
| repaired | a réparé |
| reprimanded | a été réprimandée |
| request for a horse | une demande de cheval |
| research | des recherches |
| restore | rétablir |
| resurrect | ressusciter |
| return to | revenir vers |
| revenge | se venger |
| reviled | honni |
| risking | risquer |
| ritual | un rituel |
| rob | dérober |
| sacrifice | un sacrifice |
| save | sauver |
| scatter | disperser |
| secret | un secret |
| secret doorway | le passage secret |
| see | voir |
| self | soi-même |
| sick | souffrant |
| sigil under her bed | le sceau sous son lit |
| signed by her | signé de sa main |
| Simon Coventry | Simon Coventry |
| skeleton key | un passe-partout |
| sketch | un croquis |
| so | à ce point |
| son | un fils |
| soul | une âme |
| south east corridor | le couloir sud-est |
| south west corridor | le couloir sud-ouest |
| speak | parler |
| speaking in unison | de parler à l’unisson |
| staff | le personnel |
| stained | taché |
| stalked through | a rôdé dans |
| start | commencer |
| steal | voler |
| stitch | coudre |
| stolen vase | le vase volé |
| stone | une pierre |
| stop | arrêter |
| store | entreposer |
| strange | étrange |
| strategy | une stratégie |
| study | étudier |
| substances | des substances |
| suffer | souffrir |
| suffering | souffrir |
| summon | invoquer |
| summoning ritual | un rituel d’invocation |
| séance | la séance |
| séance  | la séance  |
| séance's aftermath | les suites de la séance |
| take | prendre |
| talk | parler |
| tattoo | un tatouage |
| telegraph machine | le télégraphe |
| terror | la terreur |
| The Cailleach | la Cailleach |
| the catacombs | les catacombes |
| the entity | l’entité |
| the Fae | les Fae |
| the future | l’avenir |
| The manager's | le gérant |
| The Morrigan | la Morrigan |
| the portal | le portail |
| the séance | la séance |
| their past | leur passé |
| threaten | menacer |
| tired | las |
| tongues | des langues inconnues |
| transfer | transférer |
| transport | transporter |
| trap | piéger |
| trapped | prisonnier |
| trapping | piéger |
| treasure | un trésor |
| tricked | duper |
| Tuatha Dé Danann | Tuatha Dé Danann |
| Tír na nÓg | Tír na nÓg |
| undressed in | s’est dévêtu dans |
| unlocking | déverrouiller |
| upper corridors | les couloirs supérieurs |
| valid | fondé |
| valuables | des objets de valeur |
| village | le village |
| Walter Blake | Walter Blake |
| Walter Blake isn't real | Walter Blake n’existe pas |
| wandering | errer |
| wardrobe | la penderie |
| wealth | la fortune |
| well | le puits |
| wife | une épouse |
| wife's belongings | les affaires de son épouse |
| witch | une sorcière |
| work | le travail |
| write to | écrire à |
