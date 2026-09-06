# Blake Manor FR

French fan translation of **The Séance of Blake Manor** (Spooky Doorway / Raw Fury).

The game ships English-only, but it was built on two middlewares that both have
working localisation paths the studio never populated. The patch finishes what
they scaffolded: it distributes **only** a mod DLL and JSON files — no game assets.

Target build: `1.1.12.360` · Unity `6000.0.66f2` · Mono · guid `9c1c65d37965437ea5f29d161938c3ed`

---

## Status

| Phase | | |
|---|---|---|
| 0 | Mod loader | **done** |
| 1 | Extract English corpus | **done** |
| 2 | Translate | **done** — 99.9%, 25 UI strings outstanding |
| 3 | Inject | **done** — four injectors verified on screen |
| 4 | QA in-game | in progress |
| 5 | Release | not started |

### Translated

| layer | units | injected via |
|---|---:|---|
| dialogue | 16,387 | `fr` field per entry |
| ui, menus, evidence, descriptions, tokens | 958 | source-string hook |
| lore | 875 | Dialogue System actor fields |
| quest, journal, mysteries, hypotheses | 363 | database `Field.value` |
| actor names and bios | 293 | `AltName fr` |
| **total** | **18,876** | **237,883 words** |

`python3 tools/status.py` prints this live. What remains is 25 UI strings worth
27 words, all of them harvested from play rather than from the static dump.

At runtime the patch reports what it actually loaded:

```
2/2 patches applied, 2357 UI strings, 1623 item fields and 16386 dialogue lines loaded.
```

The UI count exceeds the 958 corpus units because `ui.json` also carries strings
harvested from real playthroughs, which the dumper cannot enumerate statically.

### The four injectors

The game reaches its text four different ways, and each needed its own path.

| layer | how it reaches the screen |
|---|---|
| ui, evidence, descriptions, tokens | Harmony prefix on `RuntimeLanguages.GetTranslation`, keyed by source string |
| journal, mysteries, cast profiles | overwrite `Field.value` on `DialogueManager.masterDatabase`, keyed by technical name |
| conversations | a field named `fr` per entry + `Localization.language`, with English fallback |
| hypothesis sentences | `KickStarter.settingsManager.masterDatabase` + the `DialogueLua` quest-field mirror |

The fourth exists because Adventure Creator keeps a **separate** master database
from the Dialogue System's. `EHKickStarter.SetupQuests()` reads
`KickStarter.settingsManager.masterDatabase`, so writing only to
`DialogueManager.masterDatabase` translated a database the hypothesis screen
never reads. The write counter said "1623 translated" the whole time. Found by
decompiling with `ilspycmd`, not by reading logs.

### Two things that will bite again

**The language name changes after startup.** The AC↔DS bridge overwrites
`Localization.language` with the *display* name `"Français"` once the game is up,
while fields were published under the code `"fr"`. Every field is now published
under **both** names, and a watchdog re-pins the controller. Symptom if this
regresses: a clean success log and English on screen. Root cause, found later by
decompiling the bridge: it copies `Options.GetLanguageName()`, which returns the
language *code* from `SpeechManager.languages` — and the patch registers
`"Français"` as the code. Registering `fr` as code and `Français` as display name
would end the double publication.

**Entry IDs renumber between builds.** Drift is caught per line by a SHA-1 prefix
of the source English; the injector skips any line whose hash no longer matches.
After a game update, re-dump the corpus **with the FR patch removed**, or the dump
captures French and the corpus eats itself.

### Corpus (Phase 1 output)

| kind | units | words |
|---|---:|---:|
| dialogue | 16,387 | 226,006 |
| quest / journal | 363 | 5,892 |
| UI strings | 983 | 2,711 |
| character lore | 875 | 2,254 |
| actor names & bios | 293 | 1,047 |
| **total** | **18,901** | **237,910** |

4,253 conversations kept, 2 DEMO conversations excluded.

---

## Layout

```
tools/
  install-loader.sh        install BepInEx into the Steam game dir (additive)
  uninstall-loader.sh      remove it again
  CorpusDumper/            BepInEx plugin: reads both text systems from the live game
  FrenchPatch/             the patch itself
    Plugin.cs              loader, UI hook, language registration, miss log, the switch
    DialogueFields.cs      both master databases + the Lua quest mirror; remembers the English
    DialogueLines.cs       conversation lines, dual-name publication, watchdog
    LanguageOption.cs      the Language row added to Options > Interface
  build_corpus.py          raw dumps -> translation-ready corpus
  status.py                progress by layer
  export_batch.py          carve out the next slice to translate
  make_dialogue_fr.py      build + validate corpus/fr/dialogue.json
  make_fields_fr.py        build corpus/fr/fields.json
  make_ui_fr.py            build corpus/fr/ui.json from the tables
  fr_*.py                  the French tables (hypotheses, evidence, lore, quests, …)
  check_hypotheses.py      enforce the five hard rules on the templates
  hypothesis_review.py     generate the EN/FR review sheet
docs/
  STYLE.md                 translation charter — decisions settled before starting
  HYPOTHESES.md            the five hard rules for the deduction templates
  RELECTURE-HYPOTHESES.md  35 templates + 332 token words, EN/FR side by side
  relecture-hypotheses.html  the same, as a readable page
  steam-launch-options.txt
corpus/en/                 the English corpus
  units.jsonl              the work queue: one translatable unit per line
  conversations.jsonl      entries grouped and ordered by conversation
  pools.json               actors, quests, UI, hypothesis templates
  glossary_seed.tsv        1,067 proper nouns and item names to fix first
  stats.md                 scope report
corpus/fr/                 the translation
  dialogue/*.json          113 batch files, "<convId>:<entryId>": "français"
  dialogue.json            built from them, with drift hashes
  ui.json  fields.json  actors.json
vendor/                    downloaded BepInEx (gitignored)
corpus/raw/                verbatim runtime dumps (gitignored, ~51 MB)
```

## Reproducing the extract

Remove the FR patch first, or the dump captures the translation.

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

## Working on the translation

```sh
python3 tools/status.py                    # what is left
python3 tools/export_batch.py --list       # pick the largest untranslated slice
python3 tools/make_dialogue_fr.py          # build + validate; must exit clean
python3 tools/make_ui_fr.py
python3 tools/make_fields_fr.py

dotnet build -c Release tools/FrenchPatch -o build/frenchpatch
cp build/frenchpatch/BlakeManorFR.dll "$GAME/BepInEx/plugins/"
cp corpus/fr/*.json "$GAME/BepInEx/plugins/BlakeManorFR/"
```

`make_dialogue_fr.py` is the gate: it checks that every key exists, that the tag
multiset matches, that `{0}` / `[v]` / `[r]` / `$1` substitutions survive, and that
no straight apostrophe slipped in. Fix what it reports until it exits clean.

The patch writes `BepInEx/blakemanor-fr-misses.txt`: every string that passed
through untranslated. It is an **accumulating backlog**, not a session report —
it merges with what was already there and drops entries once they are translated,
so a playthrough adds to it rather than replacing it. That file is the work queue
for UI text the dumper cannot enumerate statically (hotspot names, menu labels),
so play, harvest, translate, repeat.

Set `BLAKE_FR_SHOT_AFTER=22 BLAKE_FR_SHOT_PATH=... BLAKE_FR_SHOT_QUIT=1` to grab a
screenshot and quit — that is how the glyph probe was made.

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
menus come up in French. To play in English, use the switch in the options screen
(next section); clearing the launch options also works — the patch stays installed
but inert.

## Switching language in game

The options screen gets one extra row, **Options → Interface → Langue / Language**,
cycling *Français* / *English*. It takes effect immediately: every interface label
re-translates through the game's own `OnChangeLanguage` event, the Dialogue System
moves back to its default language, and the overwritten item and actor fields are
put back to the English remembered at startup. Text already drawn by code (an open
journal page, a subtitle mid-line) catches up when it next redraws.

The choice is saved in `BepInEx/config/fr.blakemanor.frenchpatch.cfg`
(`[Language] Active = fr|en`), never in the game's own options file. The shipped
build carries an unfinished official French (`StreamingAssets/Localisations/Custom/fr`,
every line `TBT: …`) at a language index of its own; writing an index through
`Options.SetLanguage` would leave a player who later removes the patch staring at
those placeholders. Removing the patch therefore leaves nothing behind.

How the row is made: `EHOptionsMenu` builds its tabs from prefabs and picks each
row's behaviour from a closed enum, so `LanguageOption.cs` copies the "dialogue
text size" row when the menu opens, re-labels it, and points its left/right event at
`FrenchPatch.SetFrench`. The copy is not registered in the tab's entry list, so
reset-to-defaults and the menu's analytics never see it.

QA without a controller: set `[QA] SelfTestSwitch = true` (and `QuitAfterSelfTest`)
in the config. At startup the patch flips to the other language and back, logging
what the UI hook, the conversation sentinel and the hypothesis field resolve to in
each state.

## The hypothesis system

The deduction sentences are positional templates filled from word banks
(`"We are all [v] a sleeping [r]'s [r] that is [v] into [r]!"`). They cannot be
translated slot by slot: the sentence is on screen **while** the player is still
guessing, so it has to read acceptably with wrong words in the holes.

The five hard rules are in `docs/HYPOTHESES.md`: the slot sequence is untouchable,
the article belongs to the token and not to the template, never `de [r]` or `à [r]`,
no elision before a hole, no agreement with a hole. Verbs are written as
infinitives because they are invariable.

```sh
python3 tools/check_hypotheses.py      # enforce the rules
python3 tools/hypothesis_review.py     # regenerate the EN/FR review sheet
```

35 templates, 140 verbs, 332 token words. All 35 French templates preserve the
source slot sequence.

## Verified in game

- BepInEx 5.4.23.5 attaches to Unity 6 Mono, headless included.
- **Font needs no work.** Rendered on screen, not just inspected in the atlas:
  `« »`, `À É È Ê Ë Î Ï Ô Ù Û Ü Ç Œ Æ`, the lowercase set, `— – ’ “ ” … № ½ ° ×`.
  See `build/qa/glyph-probe.png`.
- Conversations, journal, cast profiles, evidence and hypothesis templates all
  display French on screen.
- **The language switch round-trips.** The startup self-test flips every layer to
  English and back: `GetTranslation("Examine")` → `Examine` → `Examiner`, the
  conversation sentinel → `Hello, Mister Ward…` → `Bonjour, monsieur Ward…`, the
  hypothesis field → `We are all [v]…` → `Nous sommes tous…`. The row itself is
  cloned into both options screens (main menu and pause variant); operating it
  by hand in game is the one check still to do.

## Still open

- **Resolved hypothesis sentences.** The answer key is computed in code and never
  stored, so the only way to check that a *solved* sentence reads correctly is to
  solve a mystery in game.
- **Text expansion.** French runs 15–25% longer into fixed comic-panel bubbles;
  evidence cards and mindmap nodes have not been checked for overflow.
- **Spirit board.** `ASHES TO ASHES` is still English, pending an in-game check
  that *CENDRE À CENDRE* fits the board's letter positions.
- **UI backlog** refills as new areas are explored. Harvest and translate.

## Known constraints

- **Fragmented markup.** articy splits runs mid-sentence
  (`<i>There are several letters,</i><i> dated late August</i>`). Tags must survive,
  but adjacent identical tags may be merged.
- **Do not translate identity fields.** Actor `Name`, `Technical Name`, `Articy Id`,
  item `Name` and the `*IDs` fields are lookup keys, not display text.

## Removing everything

```sh
tools/uninstall-loader.sh
```

Steam's "Verify integrity of game files" also restores a clean install.
