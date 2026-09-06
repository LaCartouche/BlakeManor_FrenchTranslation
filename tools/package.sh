#!/usr/bin/env bash
# Builds the patch and packs a release: one zip that drops into any BepInEx 5
# install of the game — Linux, Steam Deck or Windows — as
#
#   build/BlakeManorFR-<version>.zip
#     INSTALL.txt  install.sh  install.ps1  install.bat
#     BepInEx/plugins/BlakeManorFR.dll
#     BepInEx/plugins/BlakeManorFR/{ui,fields,dialogue,actors}.json + LICENSE
#
# Needs the dotnet SDK, BepInEx unpacked in vendor/be5 (tools/install-loader.sh
# does that) and the game's Managed folder for the references; the game is found
# the way install.sh finds it, or pass GAME=/path.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERSION="$(sed -n 's/.*BepInPlugin(Guid, "[^"]*", "\([^"]*\)").*/\1/p' tools/FrenchPatch/Plugin.cs)"
[ -n "$VERSION" ] || { echo "Could not read the plugin version from tools/FrenchPatch/Plugin.cs" >&2; exit 1; }
[ -f vendor/be5/BepInEx/core/BepInEx.dll ] || { echo "BepInEx not unpacked in vendor/be5 — run tools/install-loader.sh first." >&2; exit 1; }
GAME="$(./install.sh --print-game)"
MANAGED="$GAME/The Seance of Blake Manor_Data/Managed"

dotnet build -c Release tools/FrenchPatch -o build/frenchpatch -p:GameManaged="$MANAGED" --nologo -v quiet

STAGE="build/package"
ZIP="build/BlakeManorFR-$VERSION.zip"
rm -rf "$STAGE" "$ZIP"
mkdir -p "$STAGE/BepInEx/plugins/BlakeManorFR"
cp build/frenchpatch/BlakeManorFR.dll "$STAGE/BepInEx/plugins/"
cp corpus/fr/ui.json corpus/fr/fields.json corpus/fr/dialogue.json corpus/fr/actors.json \
   "$STAGE/BepInEx/plugins/BlakeManorFR/"
cp LICENSE "$STAGE/BepInEx/plugins/BlakeManorFR/LICENSE"
sed "s/@VERSION@/$VERSION/g" docs/INSTALL.txt > "$STAGE/INSTALL.txt"
cp install.sh install.ps1 install.bat "$STAGE/"
chmod +x "$STAGE/install.sh"

# zip via Python so the only tool needed is one the repo already requires
python3 - "$STAGE" "$ZIP" <<'PY'
import os, sys, zipfile
stage, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _, files in os.walk(stage):
        for f in sorted(files):
            p = os.path.join(base, f)
            z.write(p, os.path.relpath(p, stage))
PY
echo "Packed $ZIP ($(du -h "$ZIP" | cut -f1)):"
python3 -c "import zipfile,sys; [print('  ' + n) for n in zipfile.ZipFile(sys.argv[1]).namelist()]" "$ZIP"
