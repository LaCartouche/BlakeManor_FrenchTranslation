# Blake Manor FR

French fan translation of **The Séance of Blake Manor** (Spooky Doorway / Raw Fury).

The game ships English-only, but it was built on two middlewares that both have
working localisation paths the studio never populated. The patch finishes what
they scaffolded: it distributes **only** a mod DLL and a JSON file — no game assets.

Target build: `1.0.801.75` · Unity `6000.0.66f2` · Mono · guid `109118c4b13244e78e186c1cd5335be8`

---

## Status

| Phase | | |
|---|---|---|
| 0 | Mod loader | **done** |
| 1 | Extract English corpus | **done** |
| 2 | Translate | **everything except dialogue done** · 226k words of dialogue remain |
| 3 | Inject | **both injectors working in game** (UI hook + DS fields) |
| 4 | QA in-game | miss-harvesting + screenshot capture in place |
| 5 | Release | not started |

### Translated so far

| layer | count | injected via |
|---|---:|---|
| UI, cursors, menus, notifications | ~180 | source-string hook |
| evidence / clue / task labels | 781 | source-string hook |
| evidence descriptions | 862 | source-string hook |
| hypothesis token words | 331 | source-string hook |
| journal, mysteries, hypothesis templates | 451 | Dialogue System fields |
| **total** | **2,505** | ~22,000 French words |

Remaining: the 226,328 words of dialogue.

### Verified in game

- BepInEx 5.4.23.5 attaches to Unity 6 Mono, headless included.
- The only untranslated string left at boot is `{InteractionX}`, a runtime
  substitution token that must stay.
- **Font needs no work.** Rendered on screen, not just inspected in the atlas:
  `« »`, `À É È Ê Ë Î Ï Ô Ù Û Ü Ç Œ Æ`, the lowercase set, `— – ’ “ ” … № ½ ° ×`.
  See `build/qa/glyph-probe.png`.

### Corpus (Phase 1 output)

| kind | units | words |
|---|---:|---:|
| dialogue | 16,411 | 226,328 |
| quest / journal | 359 | 5,783 |
| UI strings | 983 | 2,790 |
| character lore | 879 | 2,283 |
| actor names & bios | 293 | 1,047 |
| **total** | **18,925** | **238,231** |

4,261 conversations. 16,530 distinct strings (2,395 units are exact duplicates).
Plus 42 hypothesis templates that need hand-design rather than translation — see below.

---

## Layout

```
tools/
  install-loader.sh        install BepInEx into the Steam game dir (additive)
  uninstall-loader.sh      remove it again
  CorpusDumper/            BepInEx plugin: reads both text systems from the live game
  build_corpus.py          raw dumps -> translation-ready corpus
vendor/                    downloaded BepInEx (gitignored)
corpus/raw/                verbatim runtime dumps (gitignored, ~51 MB)
corpus/en/                 the corpus
  units.jsonl              the work queue: one translatable unit per line
  conversations.jsonl      entries grouped and ordered by conversation
  pools.json               actors, quests, UI, hypothesis templates
  glossary_seed.tsv        1,067 proper nouns and item names to fix first
  stats.md                 scope report
```

## Reproducing the extract

```sh
tools/install-loader.sh
dotnet build -c Release tools/CorpusDumper -o build/dumper
cp build/dumper/BlakeManorCorpusDumper.dll "$GAME/BepInEx/plugins/"

cd "$GAME"
BLAKE_DUMP_QUIT=1 BLAKE_DUMP_DIR=.../corpus/raw \
  ./run_bepinex.sh "$GAME/The Seance of Blake Manor.x86_64" -batchmode -nographics

python3 tools/build_corpus.py
```

Runs headless in about 40 seconds. No window, no playthrough needed.

---

## How the injection will work (Phase 3)

Two different mechanisms, because the two text systems differ:

**Conversations** — the Dialogue System picks subtitle text with
`Field.AssignedField(fields, Localization.language) ?? Field.Lookup(fields, "Dialogue Text")`.
Adding a field named `fr` to each entry and setting `Localization.language = "fr"`
translates the game through its own supported path, with English as automatic fallback.

**Everything else** — Adventure Creator's `SpeechManager.lines` is **empty** in the
shipped build (the studio never ran "Gather Text"), so every `lineID` is `-1` and the
lineID-keyed table is unusable. But all UI text still funnels through one method:

```csharp
KickStarter.runtimeLanguages.GetTranslation(originalText, lineID, language)
```

A Harmony postfix there, keyed on `originalText`, covers hotspot labels, menus,
inventory, notifications and the studio's own `RuntimeTranslatables.Get(id)` strings.

Quest and lore fields (`Conclusion_en`, `Lore1_en`, …) are read by literal field name
via `LookupField`, which tries the bare name *first* — so a field named `Conclusion`
wins over `Conclusion_en` without touching the original.

## Launching through Steam

Steam runs the game executable directly, so Doorstop is never injected and the game
comes up in English. Set this in **Properties → General → Launch Options**
(quotes included — the path contains spaces):

```
"/home/jguillaume/.local/share/Steam/steamapps/common/The Seance of Blake Manor/run_bepinex.sh" %command%
```

`run_bepinex.sh` detects Steam's `SteamLaunch` argument and re-runs itself through
Steam's bootstrapper, so this works with the Steam Linux Runtime. It is also what
makes Steam overlay, achievements and playtime keep working.

To confirm it took: `BepInEx/LogOutput.log` gets rewritten on every launch, and the
menus come up in French. To play in English again, clear the launch options — the
patch stays installed but inert.

## Working on the translation

```sh
python3 tools/make_ui_fr.py          # rebuild corpus/fr/ui.json from the tables
dotnet build -c Release tools/FrenchPatch -o build/frenchpatch
cp build/frenchpatch/BlakeManorFR.dll "$GAME/BepInEx/plugins/"
cp corpus/fr/ui.json "$GAME/BepInEx/plugins/BlakeManorFR/ui.json"
```

The patch writes `BepInEx/blakemanor-fr-misses.txt` on exit: every string that passed
through untranslated. That file is the work queue for UI text the dumper cannot
enumerate statically (hotspot names, menu labels), so run the game, harvest, translate,
repeat. Set `BLAKE_FR_SHOT_AFTER=22 BLAKE_FR_SHOT_PATH=... BLAKE_FR_SHOT_QUIT=1`
to grab a screenshot and quit — that is how the glyph probe above was made.

## Known hard spots

- **Hypothesis builder (42 templates).** The deduction sentences are positional
  templates (`"We are all [v] a sleeping [r]'s [r] that is [v] into [r]!"`) filled from
  word banks. French needs the template restructured and the banks agreed for gender
  and number; these cannot be translated slot-by-slot. Flagged in `pools.json`.
- **Text expansion.** French runs 15–25% longer into fixed comic-panel bubbles.
- **Fragmented markup.** articy splits runs mid-sentence
  (`<i>There are several letters,</i><i> dated late August</i>`). Tags must survive,
  but may be merged — 4,411 units contain markup.
- **Do not translate identity fields.** Actor `Name`, `Technical Name`, `Articy Id`,
  item `Name` and the `*IDs` fields are lookup keys, not display text.

## Removing everything

```sh
tools/uninstall-loader.sh
```

Steam's "Verify integrity of game files" also restores a clean install.
