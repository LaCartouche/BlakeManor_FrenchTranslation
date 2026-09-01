#!/usr/bin/env python3
"""
Enforce the rules in docs/HYPOTHESES.md mechanically.

  1. marker sequence identical to the English (slots are positional)
  2. no article immediately before a slot   -> it lives in the token
  3. no `de [r]` / `à [r]` and no contracted form -> they would produce "de le rituel"
  4. no elidable word immediately before a slot -> the template cannot choose qu'/que
  5. verb bank has the same number of entries as the English

Also reports Token Word coverage.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from fr_hypotheses import TEMPLATES, VERBS, TOKENS  # noqa: E402

RAW = ROOT.parent / "corpus" / "raw"
MARK = re.compile(r"\[[vr]\]")

# Anything that must not sit directly in front of a slot.
BAD_BEFORE_SLOT = [
    (re.compile(r"\bde\s+\[r\]"),        "`de [r]` contracts with le/les"),
    (re.compile(r"\bà\s+\[r\]"),         "`à [r]` contracts with le/les"),
    (re.compile(r"\b(du|des|au|aux)\s+\[r\]"), "already-contracted article before a slot"),
    (re.compile(r"\b(le|la|les|un|une|ce|cette|ces|son|sa|ses)\s+\[r\]"),
                                          "article/determiner before a slot — put it in the token"),
    (re.compile(r"\b(que|qui|ne|je|me|te|se|ce|si)\s+\[r\]"),
                                          "elidable word before a slot"),
    (re.compile(r"[’']\s*\[r\]"),        "elision before a slot"),
]


def seq(s):
    return "".join("v" if m == "[v]" else "r" for m in MARK.findall(s or ""))


def main():
    ds = json.loads((RAW / "dialogue_system.json").read_text(encoding="utf-8"))
    items = {}
    for it in ds["items"]:
        m = {f["title"]: f["value"] for f in it["fields"]}
        items[m.get("Name", "")] = m

    problems, checked = [], 0

    for name, fr in TEMPLATES.items():
        en = items.get(name)
        if en is None:
            problems.append(f"[{name}] no such item in the game")
            continue
        for key, field in (("h", "hypothesisSentence"), ("c", "confrontSentence")):
            if key not in fr:
                continue
            en_s, fr_s = (en.get(field) or "").strip(), fr[key]
            if not en_s:
                problems.append(f"[{name}.{field}] translated but the English field is empty")
                continue
            checked += 1
            if seq(en_s) != seq(fr_s):
                problems.append(
                    f"[{name}.{field}] marker sequence changed: EN {seq(en_s)} -> FR {seq(fr_s)}")
            for rx, why in BAD_BEFORE_SLOT:
                for hit in rx.finditer(fr_s):
                    problems.append(f"[{name}.{field}] {why}: ...{hit.group(0)!r}...")

    # every template with an English sentence needs a French one
    for name, m in items.items():
        if (m.get("hypothesisSentence") or "").strip() and name not in TEMPLATES:
            problems.append(f"[{name}] has an English hypothesis but no French template")
        if (m.get("confrontSentence") or "").strip() and "c" not in TEMPLATES.get(name, {}):
            problems.append(f"[{name}] has an English confrontSentence but no French one")

    for name, fr_v in VERBS.items():
        en_v = (items.get(name, {}).get("verbs") or "")
        n_en = len([x for x in en_v.split(",") if x.strip()])
        n_fr = len([x for x in fr_v.split(",") if x.strip()])
        if n_en != n_fr:
            problems.append(f"[{name}.verbs] {n_en} entries in English, {n_fr} in French")

    # Token Word coverage
    ac = json.loads((RAW / "adventure_creator.json").read_text(encoding="utf-8"))
    game_tokens = {p["text"] for r in ac["pools"]["inventoryItems"]
                   for p in r.get("properties", []) if p["index"] in (3, 4)}
    missing = sorted(t for t in game_tokens if t not in TOKENS and t.strip() not in TOKENS)
    stale = sorted(t for t in TOKENS if t not in game_tokens and t.strip() not in
                   {g.strip() for g in game_tokens})

    print(f"templates checked : {checked}")
    print(f"token words       : {len(game_tokens)} in game, "
          f"{len(game_tokens) - len(missing)} translated, {len(missing)} missing")
    if stale:
        print(f"\nSTALE tokens ({len(stale)}) — match nothing in the game:")
        for t in stale:
            print(f"  {t!r}")
    if missing:
        print(f"\nMISSING tokens ({len(missing)}):")
        for t in missing:
            print(f"  {t!r}")
    if problems:
        print(f"\nRULE VIOLATIONS ({len(problems)}):")
        for p in problems:
            print(f"  {p}")
    if not problems and not missing:
        print("\nall rules satisfied")
    return 1 if (problems or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
