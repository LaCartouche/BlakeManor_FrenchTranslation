# Le système d'hypothèses — contraintes de conception

35 gabarits. Ils ne se traduisent pas : ils se **reconçoivent**, sous contraintes dures.

---

## Comment le jeu s'en sert

`hypothesisSentence` est une phrase à trous, stockée sur l'objet de quête :

```
We are all [v] [r]'s [r] that is [v] into [r]!
```

À l'exécution, `EHKickStarter` découpe la chaîne sur `[`, lit `[v]` ou `[r]`, et
appelle `TrySetupConnection` pour le texte fixe entre deux marqueurs, `TrySetupEvidence`
pour chaque trou. Le joueur remplit les trous :

- `[v]` — un mot pris dans la liste `verbs` de la quête (séparée par des virgules) ;
- `[r]` — le **Token Word** d'une preuve, c'est-à-dire la propriété d'inventaire n° 3,
  et non le libellé de la preuve.

Les deux listes sont des champs que le patch peut réécrire : nous contrôlons donc
la phrase **et** les deux réservoirs de mots.

---

## Les cinq règles

### 1. La séquence de marqueurs est intouchable

Les trous sont numérotés par leur position et adressés par des variables globales
(`ArwaSQ.evidence1`, `ArwaSQ.verb1`, …). Le français peut réécrire tout le texte
entre les marqueurs, **jamais** leur nombre, leur type ni leur ordre.

```
EN  We are all [v] [r]'s [r] that is [v] into [r]!     -> v r r v r
FR  Nous sommes tous en train de [v] [r] : [r] qui vient [v] dans [r] !   -> v r r v r  ✅
FR  Nous [v] tous [r] qui vient [v] dans [r] !                            -> v r v r    ❌
```

C'est la contrainte qui décide de tout le reste : la syntaxe française doit se plier
à l'ordre anglais, pas l'inverse.

### 2. L'article appartient au mot, pas au gabarit

Un `[r]` peut recevoir n'importe quel mot du réservoir de la quête, de genre et de
nombre imprévisibles. Le gabarit ne peut donc pas porter l'article :

```
❌  le [r]        -> « le séance », « le catacombes »
✅  [r]           avec les jetons « la séance », « les catacombes »
```

Chaque Token Word français est donc écrit avec son déterminant.

### 3. Jamais `de [r]` ni `à [r]`

Ce sont les deux seules prépositions françaises qui se contractent avec l'article,
et le gabarit ne peut pas savoir ce qui va tomber dans le trou :

```
❌  de [r]  -> « de le rituel »        ❌  à [r]  -> « à le manoir »
✅  par [r]   avec [r]   sur [r]   dans [r]   pour [r]   chez [r]   contre [r]
```

`de [v]` et `à [v]` restent **autorisés** : un verbe ne prend pas d'article
(« a permis de forger », « cherche à fuir »).

### 4. Aucune élision devant un trou

Le gabarit ne peut pas choisir entre `que` et `qu'`, `le` et `l'`, `de` et `d'`.
On emploie donc des mots qui ne s'élident jamais devant un trou :

```
❌  parce que [r]      ✅  car [r]
❌  l'[r]              ✅  [r]  (article dans le jeton)
```

### 5. Aucun accord avec un trou

Pas d'adjectif ni de participe passé s'accordant avec ce que le joueur dépose.
Les `[v]` sont écrits à l'**infinitif**, forme invariable.

```
❌  [r] est [v]é par …        ✅  [r] a pour but de [v] …
```

---

## Le critère de qualité

La phrase est visible **pendant** que le joueur tâtonne, donc avec des réponses
fausses dedans. Un gabarit n'est bon que s'il reste lisible avec **n'importe quelle**
combinaison tirée des réservoirs de sa quête — pas seulement avec la bonne.

C'est plus exigeant que de traduire la phrase résolue, et c'est le bon critère :
l'anglais lui-même est télégraphique et un peu bancal en cours de résolution.

## Ce qui reste à vérifier en jeu

La clé de correction n'est pas stockée dans les conditions de dialogue ni dans les
variables (toutes initialisées à `0`) : elle est calculée dans le code. Les gabarits
ci-dessous sont donc conçus pour *toutes* les combinaisons possibles, mais **chaque
mystère doit être résolu manuellement** pour confirmer que la phrase juste se lit
correctement. C'est la partie du patch la plus susceptible de demander une reprise.
