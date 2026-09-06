#!/usr/bin/env bash
# Removes what install-loader.sh added, plugins included. The game's own files
# are never touched.
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/find-game.sh"
blake_find_game
rm -rf "$GAME/BepInEx" "$GAME/libdoorstop.so" "$GAME/run_bepinex.sh" \
       "$GAME/.doorstop_version" "$GAME/steam_appid.txt" "$GAME/doorstop_config.ini"
echo "Removed BepInEx from: $GAME"
echo "Clear the game's Launch Options in Steam as well."
