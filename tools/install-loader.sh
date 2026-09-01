#!/usr/bin/env bash
# Installs BepInEx 5 into the Blake Manor Steam install. Purely additive:
# adds BepInEx/, libdoorstop.so, run_bepinex.sh, .doorstop_version, steam_appid.txt.
# Remove with tools/uninstall-loader.sh. Steam "Verify integrity" also clears it.
set -euo pipefail
GAME="${GAME:-$HOME/.local/share/Steam/steamapps/common/The Seance of Blake Manor}"
SRC="$(cd "$(dirname "$0")/.." && pwd)/vendor/be5"
[ -d "$GAME" ] || { echo "Game not found: $GAME" >&2; exit 1; }
[ -d "$SRC" ]  || { echo "BepInEx not unpacked: $SRC" >&2; exit 1; }
cp -r "$SRC/BepInEx" "$SRC/libdoorstop.so" "$SRC/run_bepinex.sh" "$SRC/.doorstop_version" "$GAME/"
chmod +x "$GAME/run_bepinex.sh"
# Lets the game init Steamworks directly instead of relaunching through Steam
# (a relaunch would drop the Doorstop injection).
echo 1395520 > "$GAME/steam_appid.txt"
mkdir -p "$GAME/BepInEx/plugins"
echo "Installed BepInEx into: $GAME"
