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
| 2 | Translate | not started |
| 3 | Inject | not started |
| 4 | QA in-game | not started |
| 5 | Release | not started |

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
