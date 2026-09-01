#!/usr/bin/env python3
"""
Merge the per-batch dialogue translations into corpus/fr/dialogue.json.

Input   corpus/fr/dialogue/*.json   {"<convId>:<entryId>": "français", ...}
Output  corpus/fr/dialogue.json     what the patch loads

Every line is written with a hash of the English it was translated from. At runtime
the injector re-hashes the game's current English and skips any line that no longer
matches, so a game patch leaves those lines in English and reports them instead of
showing a translation of text the player is not being given.

Validation, run on every build:
  - the key exists in the corpus
  - inline markup survives: no tag invented, none dropped. Adjacent identical tags
    may be merged (articy splits them mid-sentence), so tags are compared as a
    multiset of tag NAMES, not as an exact string
  - runtime substitutions ({0}, [v], [r], $000) are preserved exactly
  - no straight apostrophes, per docs/STYLE.md
  - length is flagged past +40%, but only for lines long enough to overflow
"""
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus" / "en" / "units.jsonl"
INDIR = ROOT / "corpus" / "fr" / "dialogue"
OUT = ROOT / "corpus" / "fr" / "dialogue.json"
ACTORS = ROOT / "corpus" / "fr" / "actors.json"

TAG = re.compile(r"<(/?)([a-zA-Z]+)(?:=[^>]*)?>")
SUBST = re.compile(r"\{\d+\}|\[[vr]\]|\$\d+")
LENGTH_LIMIT = 1.40


def tag_names(s):
    """The SET of tag names used. articy splits a run of italics into several
    <i>..</i> pairs mid-sentence; merging them back into one is allowed and reads
    better, so counts are deliberately not compared — only which tags appear."""
    return {f"{m.group(1)}{m.group(2)}".lower() for m in TAG.finditer(s or "")}


# Void tags have no closing form, so they are never "unbalanced".
VOID_TAGS = {"br", "sprite", "space", "nbsp", "page", "align", "pos"}


def unbalanced(s):
    """Tag names opened but never closed, or closed but never opened."""
    opened = collections.Counter()
    for m in TAG.finditer(s or ""):
        name = m.group(2).lower()
        if name in VOID_TAGS:
            continue
        opened[name] += -1 if m.group(1) else 1
    return {n for n, v in opened.items() if v != 0}


def main():
    if not CORPUS.exists():
        sys.exit(f"missing {CORPUS} — run build_corpus.py first")

    english, hashes = {}, {}
    for raw in CORPUS.open(encoding="utf-8"):
        u = json.loads(raw)
        if u["kind"] != "dialogue":
            continue
        # key is dlg:<conv>:<entry>:<field>
        _, conv, entry, field = u["key"].split(":", 3)
        if field != "Dialogue Text":
            continue
        english[f"{conv}:{entry}"] = u["en"]
        hashes[f"{conv}:{entry}"] = u["hash"]

    merged, problems, warnings = {}, [], []
    files = sorted(INDIR.glob("*.json")) if INDIR.exists() else []

    for path in files:
        try:
            batch = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            problems.append(f"{path.name}: unreadable ({e})")
            continue
        for key, fr in batch.items():
            if not isinstance(fr, str) or not fr.strip():
                continue
            en = english.get(key)
            if en is None:
                problems.append(f"{path.name} [{key}] no such line in the corpus")
                continue
            if key in merged:
                problems.append(f"{path.name} [{key}] already translated in another batch")
                continue

            en_tags, fr_tags = tag_names(en), tag_names(fr)
            if en_tags != fr_tags:
                bits = []
                if en_tags - fr_tags:
                    bits.append("dropped " + ", ".join(sorted(en_tags - fr_tags)))
                if fr_tags - en_tags:
                    bits.append("invented " + ", ".join(sorted(fr_tags - en_tags)))
                problems.append(f"{path.name} [{key}] markup: {'; '.join(bits)}")
                continue
            bad = unbalanced(fr)
            if bad:
                problems.append(f"{path.name} [{key}] unbalanced markup: {', '.join(sorted(bad))}")
                continue

            en_sub, fr_sub = sorted(SUBST.findall(en)), sorted(SUBST.findall(fr))
            if en_sub != fr_sub:
                problems.append(f"{path.name} [{key}] substitutions changed: {en_sub} -> {fr_sub}")
                continue

            if "'" in fr:
                problems.append(f"{path.name} [{key}] straight apostrophe — use ’")
                continue

            # Only long lines can actually overflow a bubble; a short line at 150%
            # of a 24-character original is not a risk and only adds noise.
            if len(fr) > 80 and len(fr) / len(en) > LENGTH_LIMIT:
                warnings.append(f"[{key}] {len(fr)/len(en):.0%} of English, {len(fr)} chars")

            merged[key] = {"t": fr, "h": hashes[key]}

    actors = {}
    if ACTORS.exists():
        actors = json.loads(ACTORS.read_text(encoding="utf-8"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "_meta": {
            "layer": "dialogue",
            "injection": "Field named 'fr' on each DialogueEntry + Localization.language",
            "lines": len(merged),
            "of_total": len(english),
            "batches": [p.name for p in files],
        },
        "entries": merged,
        "actors": actors,
    }, ensure_ascii=False, indent=0), encoding="utf-8")

    done_words = sum(len(v["t"].split()) for v in merged.values())
    all_words = sum(len(v.split()) for v in english.values())
    pct = 100 * len(merged) / max(len(english), 1)

    print(f"batches   : {len(files)}")
    print(f"lines     : {len(merged):,} / {len(english):,}  ({pct:.1f}%)")
    print(f"words     : ~{done_words:,} / {all_words:,}")
    print(f"actors    : {len(actors)}")
    if warnings:
        print(f"\nLENGTH WARNINGS ({len(warnings)}) — may overflow a bubble:")
        for w in warnings[:15]:
            print("  " + w)
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems[:40]:
            print("  " + p)
    print(f"\nwrote -> {OUT}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
