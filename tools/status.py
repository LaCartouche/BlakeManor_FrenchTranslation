#!/usr/bin/env python3
"""
What is translated, and what is left. Run it to get an honest number.

Compares corpus/en/units.jsonl against every French layer, matching each unit the
same way the patch does: dialogue by conversation:entry key, quest text by item
field, everything else by source string.
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FR = ROOT / "corpus" / "fr"


def load(name, default):
    p = FR / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def main():
    units = [json.loads(l) for l in (ROOT / "corpus/en/units.jsonl").open(encoding="utf-8")]
    ui = set(load("ui.json", {"bySource": {}})["bySource"])
    fj = load("fields.json", {"items": {}, "actors": {}})
    fields, fr_actors = fj.get("items", {}), fj.get("actors", {})
    dialogue = load("dialogue.json", {"entries": {}})["entries"]

    # actor units are keyed by database id; the French layer is keyed by technical Name
    raw = json.loads((ROOT / "corpus/raw/dialogue_system.json").read_text(encoding="utf-8"))
    actor_name = {}
    for a in raw["actors"]:
        m = {f["title"]: f["value"] for f in a["fields"]}
        actor_name[str(a["id"])] = m.get("Name", "")

    done, todo = collections.Counter(), collections.Counter()
    dwords, twords = collections.Counter(), collections.Counter()

    for u in units:
        kind = u["kind"]
        if kind == "dialogue":
            _, conv, entry, _ = u["key"].split(":", 3)
            ok = f"{conv}:{entry}" in dialogue
        elif kind == "quest":
            _, _, field = u["key"].split(":", 2)
            ok = any(field in v for v in fields.values())
        elif kind in ("lore", "actor"):
            _, aid, field = u["key"].split(":", 2)
            ok = field in fr_actors.get(actor_name.get(aid, ""), {})
        else:
            ok = u["en"] in ui
        (done if ok else todo)[kind] += 1
        (dwords if ok else twords)[kind] += u["words"]

    print(f"{'layer':22} {'done':>7} {'left':>7} {'words left':>12}")
    print("-" * 51)
    for kind in sorted(set(done) | set(todo)):
        print(f"{kind:22} {done[kind]:7,} {todo[kind]:7,} {twords[kind]:12,}")
    print("-" * 51)
    total_d, total_t = sum(done.values()), sum(todo.values())
    pct = 100 * total_d / max(total_d + total_t, 1)
    print(f"{'TOTAL':22} {total_d:7,} {total_t:7,} {sum(twords.values()):12,}")
    print(f"\n{pct:.1f}% of units translated; "
          f"{sum(dwords.values()):,} of {sum(dwords.values()) + sum(twords.values()):,} words.")


if __name__ == "__main__":
    main()
