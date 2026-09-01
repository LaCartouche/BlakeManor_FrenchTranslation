#!/usr/bin/env bash
set -euo pipefail
GAME="${GAME:-$HOME/.local/share/Steam/steamapps/common/The Seance of Blake Manor}"
rm -rf "$GAME/BepInEx" "$GAME/libdoorstop.so" "$GAME/run_bepinex.sh" \
       "$GAME/.doorstop_version" "$GAME/steam_appid.txt" "$GAME/doorstop_config.ini"
echo "Removed BepInEx from: $GAME"
