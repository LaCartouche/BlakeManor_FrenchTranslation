#!/usr/bin/env python3
"""
Build corpus/fr/fields.json — the Dialogue System layer.

Some text is not reachable through Adventure Creator's GetTranslation hook: it lives
on Dialogue System *item* fields and is read by literal field name
(`DSQuest.LookupField`). That covers the hypothesis templates, the verb banks and the
whole journal/mystery text.

These are injected by overwriting the field VALUE in the live database, keyed by the
item's technical Name (never by the displayed title, which is itself translated).

Output shape:
    {"items": {"<Technical Name>": {"<Field Title>": "<français>", ...}, ...}}
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from fr_hypotheses import TEMPLATES, VERBS            # noqa: E402
from fr_typography import normalise                  # noqa: E402
try:
    from fr_quests import QUESTS                       # noqa: E402
except ImportError:
    QUESTS = {}

RAW = ROOT.parent / "corpus" / "raw"
OUT = ROOT.parent / "corpus" / "fr" / "fields.json"

FIELD_OF = {"h": "hypothesisSentence", "c": "confrontSentence"}


def main():
    ds = json.loads((RAW / "dialogue_system.json").read_text(encoding="utf-8"))
    game = {}
    for it in ds["items"]:
        m = {f["title"]: f["value"] for f in it["fields"]}
        game[m.get("Name", "")] = m

    items, problems = {}, []

    def put(name, field, value):
        if name not in game:
            problems.append(f"[{name}] no such item")
            return
        if field not in game[name]:
            problems.append(f"[{name}] has no field {field!r}")
            return
        if not (game[name][field] or "").strip():
            problems.append(f"[{name}.{field}] English side is empty — nothing to replace")
            return
        items.setdefault(name, {})[field] = normalise(value)

    for name, parts in TEMPLATES.items():
        for key, value in parts.items():
            put(name, FIELD_OF[key], value)
    for name, value in VERBS.items():
        put(name, "verbs", value)
    for name, fields in QUESTS.items():
        for field, value in fields.items():
            put(name, field, value)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "_meta": {
            "layer": "dialogue-system-item-fields",
            "injection": "overwrite Field.value on DialogueManager.masterDatabase.items",
            "keyed_by": "item technical Name",
            "items": len(items),
            "fields": sum(len(v) for v in items.values()),
        },
        "items": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"items  : {len(items)}")
    print(f"fields : {sum(len(v) for v in items.values())}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  {p}")
    print(f"\nwrote -> {OUT}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
