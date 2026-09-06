#!/usr/bin/env bash
# Installs BepInEx 5 into the game's Steam install. Purely additive: adds
# BepInEx/, libdoorstop.so, run_bepinex.sh, .doorstop_version, steam_appid.txt.
# Remove with tools/uninstall-loader.sh; Steam "Verify integrity" also clears it.
#
# Finds the game in any Steam library (or takes GAME=/path), downloads BepInEx
# once into vendor/ and checks its SHA-256, then prints the exact launch option
# to paste into Steam. Linux and Steam Deck; Windows installs by hand (README).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/find-game.sh"

BEPINEX_VERSION="5.4.23.5"
ZIP_NAME="BepInEx_linux_x64_${BEPINEX_VERSION}.zip"
ZIP_URL="https://github.com/BepInEx/BepInEx/releases/download/v${BEPINEX_VERSION}/${ZIP_NAME}"
ZIP_SHA256="e538560be65739f562519ab518a75f9c65b3f57f87457403ae7cde683c12dab7"
VENDOR="$HERE/../vendor"
SRC="$VENDOR/be5"

case "$(uname -s)" in
    Linux) ;;
    *)  echo "This installer is for the native Linux build (and Steam Deck)." >&2
        echo "On Windows, unzip BepInEx_win_x64_${BEPINEX_VERSION}.zip into the game folder instead — see README." >&2
        exit 1 ;;
esac

blake_find_game

if [ ! -f "$SRC/run_bepinex.sh" ]; then
    mkdir -p "$VENDOR"
    if [ ! -f "$VENDOR/$ZIP_NAME" ]; then
        echo "Downloading BepInEx $BEPINEX_VERSION ..."
        curl -fL --progress-bar -o "$VENDOR/$ZIP_NAME.part" "$ZIP_URL"
        mv "$VENDOR/$ZIP_NAME.part" "$VENDOR/$ZIP_NAME"
    fi
    echo "$ZIP_SHA256  $VENDOR/$ZIP_NAME" | sha256sum -c - >/dev/null \
        || { echo "Checksum mismatch on $ZIP_NAME — not installing it." >&2; exit 1; }
    rm -rf "$SRC"
    mkdir -p "$SRC"
    unzip -q "$VENDOR/$ZIP_NAME" -d "$SRC"
fi

cp -r "$SRC/BepInEx" "$SRC/libdoorstop.so" "$SRC/run_bepinex.sh" "$SRC/.doorstop_version" "$GAME/"
chmod +x "$GAME/run_bepinex.sh"
# Lets the game init Steamworks directly instead of relaunching through Steam
# (a relaunch would drop the Doorstop injection) — needed for headless runs.
echo 1395520 > "$GAME/steam_appid.txt"
mkdir -p "$GAME/BepInEx/plugins"

echo "Installed BepInEx $BEPINEX_VERSION into:"
echo "  $GAME"
echo
echo "Now set this as the game's Launch Options in Steam (Properties > General),"
echo "quotes included:"
echo
echo "  \"$(blake_launch_path)\" %command%"
