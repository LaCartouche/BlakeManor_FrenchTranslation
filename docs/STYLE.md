# Charte de traduction — Blake Manor FR

Décisions arrêtées avant traduction. Elles s'appliquent aux 238 231 mots du corpus.
Toute exception doit être justifiée ligne par ligne, pas décidée au fil de l'eau.

---

## 1. Titres et noms propres

**Abréviations françaises pour les titres, noms propres inchangés.**

| Anglais | Français |
|---|---|
| Mister Ward | M. Ward |
| Miss Deane | Mlle Deane |
| Mrs. Blake | Mme Blake |
| Father Sinnott | le père Sinnott |
| Detective Ward | le détective Ward |
| Doctor / Dr | le docteur / Dr |
| Lady / Lord | Lady / Lord *(inchangé, titre de noblesse britannique)* |

- Les patronymes, prénoms et toponymes ne sont **jamais** traduits :
  Blake Manor reste **Blake Manor**, Ó Finn reste **Ó Finn**, Fiadh reste **Fiadh**.
- Les abréviations sont choisies pour la compacité : le français déborde de 15 à 25 %
  et les bulles sont à taille fixe. `M.` gagne six caractères sur `Monsieur` à chaque
  occurrence, et Ward est nommé des milliers de fois.
- `M.` prend un point, `Mlle` et `Mme` n'en prennent pas (usage typographique français).
- Devant un nom commençant par une voyelle, pas d'élision du titre : *M. Ó Finn*.

## 2. Registre

**Français d'époque sobre.** Le ton visé est celui d'une traduction moderne et soignée
d'un roman victorien — pas un pastiche.

À faire :
- Vouvoiement par défaut, y compris entre personnages proches.
- Syntaxe soutenue, subordination assumée, pas de style haché.
- Lexique sans anachronisme : pas de *OK*, *stress*, *contacter*, *gérer*, *impacter*.
- Passé composé dans les dialogues ; le passé simple reste réservé aux textes écrits
  (lettres, documents, extraits de livres, épilogue).

À éviter :
- Imparfait du subjonctif, sauf effet comique volontaire sur un personnage guindé.
- Tournures franchement archaïsantes (*point* pour *pas*, *céans*, *derechef*).
- Le registre familier moderne, même pour le personnel de maison : leur parler se
  distingue par le lexique et la simplicité de la syntaxe, pas par l'argot contemporain.

### Tutoiement — les exceptions
Le vouvoiement est la règle. On tutoie uniquement :
- un enfant ;
- un animal ;
- une entité surnaturelle prise à partie, ou une prière ;
- deux personnages dont l'intimité est explicitement établie par le récit, et
  seulement une fois cette intimité posée à l'écran.

Toute exception se note dans `docs/VOICES.md` au moment où elle est décidée.

## 3. Typographie

- Guillemets français `« … »` avec espace insécable intérieure (` `).
  Guillemets anglais `“ ”` en second niveau, à l'intérieur d'une citation.
- Espace insécable avant `: ; ! ?` et `%`, à l'intérieur des guillemets.
- Apostrophe typographique `’` et non `'`.
- Points de suspension : le caractère `…`, jamais trois points.
- Tiret cadratin `—` pour les incises et les changements de locuteur.
- Majuscules accentuées obligatoires : **À**, **É**, **Ê**, **Ç**.
  L'atlas de police du jeu les contient toutes, c'est vérifié.

## 4. Contraintes techniques

**Le balisage doit survivre.** Les balises TMP (`<i>`, `<b>`, `<color=#…>`, `<br>`)
sont préservées. articy découpe les balises en plein milieu des phrases
(`<i>There are several letters,</i><i> dated late August</i>`) : on peut **fusionner**
des balises identiques adjacentes, jamais en supprimer ni en inventer.

**Les substitutions restent intactes.** `{0}`, `{1}`, `[v]`, `[r]`, `$000` sont
remplacés à l'exécution. Ils peuvent changer de place dans la phrase, jamais de forme.

**Les caractères de contrôle sont conservés** tels quels, y compris les `\r` et `\n`
en fin de chaîne et les espaces de début ou de fin — plusieurs chaînes d'interface
sont concaténées à l'exécution et l'espace fait partie du montage.

**Longueur.** Viser la longueur de l'anglais, tolérer +15 %. Au-delà, reformuler
plutôt que laisser TMP réduire la police. Les libellés d'interface, les boutons et
les noms de preuves sont les plus contraints.

**Ne jamais traduire les champs d'identité** : `Name`, `Technical Name`, `Articy Id`,
`verbs`, `*IDs`, ainsi que les noms de curseurs internes (`Default`, `Custom`,
`Mindmap`, `GlyphCursor`, `TransparentCursor`, `Wait`). Ce sont des clés de recherche,
pas du texte affiché.

## 5. Vocabulaire de l'enquête

Termes récurrents du système de déduction. Ils apparaissent à l'écran des dizaines de
fois et **doivent être identiques partout** — carte mentale, journal, dialogues,
notifications. Une incohérence ici rend le mystère insoluble.

| Anglais | Français | Note |
|---|---|---|
| Mystery | Mystère | |
| Lead | Piste | |
| Evidence | Preuve / Preuves | |
| Fact | Fait | |
| Clue | Indice | |
| Connection | Lien | jamais « connexion » |
| Hypothesis | Hypothèse | |
| Confront | Confronter | |
| Act | Agir | |
| Think | Réfléchir | |
| Task | Tâche | |
| Culprit | Coupable | |
| Mindmap | Carte mentale | |
| Timeline | Chronologie | |
| Séance | Séance | majuscule conservée, c'est l'événement |
| Sigil | Sceau | |
| Research Topic | Sujet de recherche | |
| Library Topic | Sujet de bibliothèque | |
| Opinion | Opinion | |

## 6. Ordre de travail

1. Glossaire et interface *(en cours)*
2. Injection et vérification en jeu sur ce petit volume
3. Dialogues, conversation par conversation — jamais ligne par ligne isolée
4. Relecture native, puis parties complètes

Le système d'hypothèses (42 gabarits) ne se traduit pas : il se **reconçoit**.
Voir `docs/HYPOTHESES.md` le moment venu.
