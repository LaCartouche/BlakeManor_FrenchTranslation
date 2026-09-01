#!/usr/bin/env python3
"""
Turn the raw runtime dumps into a translation-ready corpus.

Input   corpus/raw/{dialogue_system,adventure_creator,meta}.json
Output  corpus/en/conversations.jsonl   one record per conversation, entries in order
        corpus/en/pools.json            actors, quests/mysteries, UI strings
        corpus/en/units.jsonl           flat list of translatable units (the work queue)
        corpus/en/stats.md              scope report
        corpus/en/glossary_seed.tsv     names and recurring terms to fix up front

Every unit gets a stable key and a hash of its English source, so a later game
patch shows exactly which lines drifted instead of invalidating the whole corpus.
"""
import json
import pathlib
import re
import sys
import collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "corpus" / "raw"
OUT = ROOT / "corpus" / "en"

# ---------------------------------------------------------------- what to translate

# Dialogue entry fields. Everything not listed is structure, logic or VO metadata.
ENTRY_TRANSLATABLE = {"Dialogue Text", "Menu Text"}

# Actor fields. Lore1..15_en are the character facts shown in the lore/mindmap UI.
ACTOR_TRANSLATABLE = {"AltName", "FullName", "Title_en", "castBio", "hasNotTalkedWithBio",
                      "SocialClass", "ArrivalTime", "RoomNumber"}
ACTOR_TRANSLATABLE |= {f"Lore{i}_en" for i in range(1, 16)}

# Quest / mystery fields (the journal and deduction board).
ITEM_TRANSLATABLE = {"QuestTitle", "Conclusion_en", "Summary_en", "ShortConclusion_en",
                     "ShortQuestion_en", "ChapterTitle_en", "ChapterTime_en",
                     "ChapterLocation_en", "onSuccess", "onFail", "confrontDescription",
                     "OutcomeChanged", "SavedNPC"}

# The hypothesis builder is a positional sentence template plus its word banks.
# French needs the template restructured and the banks agreed for gender/number,
# so these are flagged for joint hand-design rather than line-by-line translation.
ITEM_HYPOTHESIS = {"hypothesisSentence", "confrontSentence", "verbs",
                   "connection1", "connection2", "connection3", "connection4", "connection5",
                   "evidence1", "evidence2", "evidence3",
                   "endOfHypothesisFullStopReplacement"}

# Conversations under these articy folders are developer scratch content.
EXCLUDE_CONV_PREFIX = ("DEMO/",)

# Inline markup that must survive translation untouched.
MARKUP = re.compile(r"(<[^>]{1,60}>|\[[a-zA-Z]\]|\{\{.*?\}\}|\$\w+)")


def fields_to_map(fields):
    return {f["title"]: (f["value"] or "") for f in fields}


def fields_hashes(fields):
    return {f["title"]: f.get("hash", "") for f in fields}


def markup_of(text):
    return MARKUP.findall(text or "")


def words(text):
    return len((text or "").split())


def main():
    if not (RAW / "dialogue_system.json").exists():
        sys.exit(f"No dump found in {RAW}. Run the dumper first.")

    OUT.mkdir(parents=True, exist_ok=True)
    ds = json.loads((RAW / "dialogue_system.json").read_text(encoding="utf-8"))
    ac = json.loads((RAW / "adventure_creator.json").read_text(encoding="utf-8"))
    meta = json.loads((RAW / "meta.json").read_text(encoding="utf-8"))

    # actor id -> display name, for speaker context on every line
    actor_name = {}
    for a in ds["actors"]:
        m = fields_to_map(a["fields"])
        name = m.get("AltName") or m.get("FullName") or m.get("Name") or f"#{a['id']}"
        # ActorOverride entries are a dialogue-routing mechanism, not characters;
        # their technical name would otherwise show up as the listener on every line.
        if name.endswith("Override"):
            name = name[: -len("Override")]
        actor_name[a["id"]] = name

    units = []
    conversations = []
    skipped_demo = 0

    for conv in ds["conversations"]:
        cm = fields_to_map(conv["fields"])
        title = cm.get("Title", "")
        if title.startswith(EXCLUDE_CONV_PREFIX):
            skipped_demo += 1
            continue

        # articy folder path doubles as scene/character context for the translator
        path = title.split("/")
        rec_entries = []
        for e in conv["entries"]:
            em = fields_to_map(e["fields"])
            eh = fields_hashes(e["fields"])
            speaker = actor_name.get(e.get("actorId", -1), "")
            listener = actor_name.get(e.get("conversantId", -1), "")

            texts = {k: v for k, v in em.items() if k in ENTRY_TRANSLATABLE and v.strip()}
            if not texts:
                continue

            rec_entries.append({
                "entryId": e["id"],
                "speaker": speaker,
                "listener": listener,
                "isRoot": e.get("isRoot", False),
                "label": em.get("Title", ""),          # articy fragment label, context only
                "text": texts.get("Dialogue Text", ""),
                "menuText": texts.get("Menu Text", ""),
                "next": [l["entryId"] for l in e.get("outgoing", [])],
            })

            for fname, value in texts.items():
                units.append({
                    "key": f"dlg:{conv['id']}:{e['id']}:{fname}",
                    "kind": "dialogue",
                    "conversation": title,
                    "speaker": speaker,
                    "listener": listener,
                    "en": value,
                    "hash": eh.get(fname, ""),
                    "words": words(value),
                    "markup": markup_of(value),
                })

        if rec_entries:
            conversations.append({
                "id": conv["id"],
                "title": title,
                "group": path[0] if path else "",
                "character": path[1] if len(path) > 1 else "",
                "articyId": cm.get("Articy Id", ""),
                "entries": rec_entries,
            })

    # ------------------------------------------------------------------ pools
    actors_out, items_out, hypotheses = [], [], []

    for a in ds["actors"]:
        m, h = fields_to_map(a["fields"]), fields_hashes(a["fields"])
        got = {k: v for k, v in m.items() if k in ACTOR_TRANSLATABLE and v.strip()}
        if not got:
            continue
        actors_out.append({"id": a["id"], "name": m.get("Name", ""), "fields": got})
        for k, v in got.items():
            units.append({
                "key": f"actor:{a['id']}:{k}", "kind": "lore" if k.startswith("Lore") else "actor",
                "conversation": m.get("Name", ""), "speaker": "", "listener": "",
                "en": v, "hash": h.get(k, ""), "words": words(v), "markup": markup_of(v),
            })

    for it in ds["items"]:
        m, h = fields_to_map(it["fields"]), fields_hashes(it["fields"])
        got = {k: v for k, v in m.items() if k in ITEM_TRANSLATABLE and v.strip()}
        hyp = {k: v for k, v in m.items() if k in ITEM_HYPOTHESIS and v.strip()}
        if got:
            items_out.append({"id": it["id"], "name": m.get("Name", ""),
                              "questTitle": m.get("QuestTitle", ""), "fields": got})
            for k, v in got.items():
                units.append({
                    "key": f"item:{it['id']}:{k}", "kind": "quest",
                    "conversation": m.get("QuestTitle") or m.get("Name", ""),
                    "speaker": "", "listener": "",
                    "en": v, "hash": h.get(k, ""), "words": words(v), "markup": markup_of(v),
                })
        if hyp:
            hypotheses.append({"id": it["id"], "name": m.get("Name", ""),
                               "questTitle": m.get("QuestTitle", ""), "template": hyp})

    ui_out = {}
    for pool, rows in (ac.get("pools") or {}).items():
        keep = []
        for r in rows:
            text = r.get("value") or r.get("label") or r.get("text") or r.get("title") or ""
            if not str(text).strip():
                continue
            ident = r.get("id", r.get("kind", len(keep)))
            keep.append({**r, "_text": text})
            units.append({
                "key": f"ui:{pool}:{ident}:{r.get('index', 0)}", "kind": "ui",
                "conversation": pool, "speaker": "", "listener": "",
                "en": str(text), "hash": "", "words": words(str(text)), "markup": markup_of(str(text)),
            })
        ui_out[pool] = keep

    # ------------------------------------------------------------------ write
    with (OUT / "conversations.jsonl").open("w", encoding="utf-8") as fh:
        for c in conversations:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    with (OUT / "units.jsonl").open("w", encoding="utf-8") as fh:
        for u in units:
            fh.write(json.dumps(u, ensure_ascii=False) + "\n")

    (OUT / "pools.json").write_text(json.dumps({
        "actors": actors_out, "quests": items_out,
        "hypotheses": hypotheses, "ui": ui_out,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    # glossary seed: proper nouns worth fixing before any line is translated
    names = set()
    for a in ds["actors"]:
        m = fields_to_map(a["fields"])
        for k in ("AltName", "FullName", "Name"):
            if m.get(k) and not m[k].endswith("Override"):
                names.add((m[k], "character"))
    for r in (ac.get("pools") or {}).get("inventoryItems", []):
        if r.get("label"):
            names.add((r["label"], "evidence/item"))
    for it in ds["items"]:
        m = fields_to_map(it["fields"])
        if m.get("QuestTitle"):
            names.add((m["QuestTitle"], "mystery"))
    with (OUT / "glossary_seed.tsv").open("w", encoding="utf-8") as fh:
        fh.write("source_en\tcategory\ttarget_fr\tnotes\n")
        for term, cat in sorted(names):
            fh.write(f"{term}\t{cat}\t\t\n")

    # ------------------------------------------------------------------ stats
    by_kind = collections.Counter()
    words_by_kind = collections.Counter()
    for u in units:
        by_kind[u["kind"]] += 1
        words_by_kind[u["kind"]] += u["words"]
    by_group = collections.Counter()
    for c in conversations:
        by_group[c["group"]] += sum(words(e["text"]) + words(e["menuText"]) for e in c["entries"])

    total_w = sum(words_by_kind.values())
    lines = [
        "# Blake Manor FR — English corpus",
        "",
        f"- Game build: `{meta.get('gameVersion')}` (guid `{meta.get('buildGuid')}`)",
        f"- Unity: `{meta.get('unityVersion')}`  ·  dumped {meta.get('dumpedAtUtc')}",
        "",
        "## Translatable units",
        "",
        "| kind | units | words |",
        "|---|---:|---:|",
    ]
    for k, n in by_kind.most_common():
        lines.append(f"| {k} | {n:,} | {words_by_kind[k]:,} |")
    lines += [f"| **total** | **{len(units):,}** | **{total_w:,}** |", ""]
    lines += [
        f"- Conversations kept: {len(conversations):,} (excluded {skipped_demo} DEMO)",
        f"- Hypothesis templates needing joint hand-design: {len(hypotheses)}",
        "",
        "## Dialogue words by articy group",
        "",
        "| group | words |",
        "|---|---:|",
    ]
    for g, w in by_group.most_common(15):
        lines.append(f"| {g or '(root)'} | {w:,} |")
    (OUT / "stats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print(f"\nwrote -> {OUT}")


if __name__ == "__main__":
    main()
