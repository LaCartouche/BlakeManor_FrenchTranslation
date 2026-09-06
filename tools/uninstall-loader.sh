#!/usr/bin/env bash
# Removes the patch and BepInEx from the game. Same as ./install.sh --uninstall.
exec "$(cd "$(dirname "$0")/.." && pwd)/install.sh" --uninstall "$@"
