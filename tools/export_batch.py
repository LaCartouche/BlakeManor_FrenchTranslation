#!/usr/bin/env python3
"""
Export one slice of the dialogue for translation.

    python3 tools/export_batch.py --list
    python3 tools/export_batch.py "Cast/Jonathan Blake" > work/blake.txt

Lines come out grouped by conversation and in reply order, because a dialogue turn
translated on its own loses the thread it answers. Each line is prefixed with the
key the translation must be filed under:

    [1234:5] Miss McLeod -> Mister Ward
      Hello, Mister Ward. How are you?

Write the result as corpus/fr/dialogue/<slug>.json, mapping "1234:5" to the French,
then run make_dialogue_fr.py, which validates markup, substitutions and typography.
"""
import argparse
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONVS = ROOT / "corpus" / "en" / "conversations.jsonl"


def load():
    return [json.loads(l) for l in CONVS.open(encoding="utf-8")]


def words(conv):
    return sum(len(e["text"].split()) + len(e["menuText"].split()) for e in conv["entries"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("group", nargs="?", help='e.g. "Cast/Jonathan Blake" or "Ground floor"')
    ap.add_argument("--list", action="store_true", help="show the available slices and their size")
    ap.add_argument("--done", help="path to an existing batch json; already-translated lines are skipped")
    ap.add_argument("--max-words", type=int, default=0,
                    help="stop after roughly N words, on a conversation boundary — for slices "
                         "too large to translate in one pass")
    args = ap.parse_args()

    convs = load()

    if args.list or not args.group:
        agg = collections.Counter()
        n = collections.Counter()
        for c in convs:
            key = f"{c['group']}/{c['character']}" if c["character"] else c["group"]
            agg[key] += words(c)
            n[key] += 1
        print(f"{'words':>8} {'convs':>6}  slice")
        for key, w in agg.most_common():
            print(f"{w:8d} {n[key]:6d}  {key}")
        print(f"\n{sum(agg.values()):8d} {len(convs):6d}  TOTAL")
        return 0

    done = set()
    if args.done and pathlib.Path(args.done).exists():
        done = set(json.loads(pathlib.Path(args.done).read_text(encoding="utf-8")))

    picked = [c for c in convs
              if (f"{c['group']}/{c['character']}" if c["character"] else c["group"]).startswith(args.group)]
    if not picked:
        sys.exit(f"no conversations match {args.group!r} — try --list")

    total = 0
    stopped_early = False
    for c in sorted(picked, key=lambda x: x["title"]):
        rows = [e for e in c["entries"] if e["text"].strip() and f"{c['id']}:{e['entryId']}" not in done]
        if not rows:
            continue
        # break only between conversations: a dialogue turn split from its thread
        # loses the context that makes it translatable
        if args.max_words and total >= args.max_words:
            stopped_early = True
            break
        print(f"\n### {c['title']}")
        for e in rows:
            who = e["speaker"] or "?"
            to = f" -> {e['listener']}" if e["listener"] else ""
            print(f"[{c['id']}:{e['entryId']}] {who}{to}")
            print(f"  {e['text']}")
            if e["menuText"]:
                print(f"  MENU: {e['menuText']}")
            total += len(e["text"].split())
    print(f"\n# {total} words in this batch", file=sys.stderr)
    if stopped_early:
        print("# capped — re-run with --done to continue this slice", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
