#!/usr/bin/env bash
# Blake Manor FR — installer for Linux and Steam Deck.
#
#   ./install.sh                 install BepInEx and the patch, print the Steam launch option
#   ./install.sh --uninstall     remove the patch and BepInEx (saves are never touched)
#   ./install.sh --loader-only   BepInEx alone, which is what a build needs
#   ./install.sh --print-game    only print where the game is
#   GAME=/path ./install.sh      when the game is somewhere Steam does not list
#
# The patch comes from next to this script when it sits in the release zip, or
# from the build when it sits in a clone; otherwise the latest release is
# fetched from GitHub. Windows: install.bat / install.ps1.
set -euo pipefail

APP_DIR="The Seance of Blake Manor"
APP_ID=1395520
BEPINEX_VERSION="5.4.23.5"
BEPINEX_ZIP="BepInEx_linux_x64_${BEPINEX_VERSION}.zip"
BEPINEX_URL="https://github.com/BepInEx/BepInEx/releases/download/v${BEPINEX_VERSION}/${BEPINEX_ZIP}"
BEPINEX_SHA256="e538560be65739f562519ab518a75f9c65b3f57f87457403ae7cde683c12dab7"
RELEASES_API="https://api.github.com/repos/LaCartouche/BlakeManor_FrenchTranslation/releases/latest"

HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=install
for a in "$@"; do
    case "$a" in
        --uninstall)   MODE=uninstall ;;
        --loader-only) MODE=loader ;;
        --print-game)  MODE=print ;;
        -h|--help)     sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "Unknown option: $a (try --help)" >&2; exit 2 ;;
    esac
done

say() { printf '%s\n' "$*"; }
die() { printf 'Error: %s\n' "$*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "'$1' is required but not installed."; }

# ------------------------------------------------------------------ the game
steam_roots() {
    local r
    for r in "$HOME/.local/share/Steam" "$HOME/.steam/steam" "$HOME/.steam/root" \
             "$HOME/.var/app/com.valvesoftware.Steam/.local/share/Steam" \
             "$HOME/snap/steam/common/.local/share/Steam"; do
        [ -d "$r/steamapps" ] && printf '%s\n' "$(cd "$r" && pwd -P)"
    done | awk '!seen[$0]++'
}

steam_libraries() {
    steam_roots | while IFS= read -r root; do
        printf '%s\n' "$root"
        local vdf="$root/steamapps/libraryfolders.vdf"
        [ -f "$vdf" ] && sed -n 's/^[[:space:]]*"path"[[:space:]]*"\(.*\)"[[:space:]]*$/\1/p' "$vdf"
    done | awk '!seen[$0]++'
}

find_game() {
    if [ -n "${GAME:-}" ]; then
        [ -d "$GAME" ] || die "GAME is set but that directory does not exist: $GAME"
        return 0
    fi
    local lib
    while IFS= read -r lib; do
        if [ -d "$lib/steamapps/common/$APP_DIR" ]; then
            GAME="$lib/steamapps/common/$APP_DIR"
            return 0
        fi
    done < <(steam_libraries)
    die "Could not find \"$APP_DIR\" in any Steam library. Run again as: GAME=/path/to/the/game $0"
}

# Flatpak Steam runs with its own home: a library under
# ~/.var/app/com.valvesoftware.Steam is addressed without that prefix inside.
launch_path() {
    local p="$GAME/run_bepinex.sh" fp="$HOME/.var/app/com.valvesoftware.Steam"
    case "$p" in "$fp"/*) p="$HOME/${p#"$fp"/}" ;; esac
    printf '%s\n' "$p"
}

# ------------------------------------------------------------------- helpers
fetch() { curl -fL --progress-bar -o "$2.part" "$1" && mv "$2.part" "$2"; }

extract() {
    if command -v unzip >/dev/null 2>&1; then
        unzip -q -o "$1" -d "$2"
    else
        python3 -c 'import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])' "$1" "$2"
    fi
}

# ------------------------------------------------------------------------ go
[ "$(uname -s)" = Linux ] || die "This script is for Linux and Steam Deck. On Windows use install.bat."
find_game
if [ "$MODE" = print ]; then
    printf '%s\n' "$GAME"
    exit 0
fi

if [ "$MODE" = uninstall ]; then
    rm -rf "$GAME/BepInEx" "$GAME/libdoorstop.so" "$GAME/run_bepinex.sh" "$GAME/.doorstop_version" \
           "$GAME/steam_appid.txt" "$GAME/doorstop_config.ini" "$GAME/changelog.txt"
    say "Removed the patch and BepInEx from: $GAME"
    say "Clear the game's Launch Options in Steam as well."
    exit 0
fi

need curl
need sha256sum
command -v unzip >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1 \
    || die "'unzip' or 'python3' is required to unpack archives."

# Downloads go to vendor/ inside a clone (the build needs them there), else to a temp dir.
if [ -d "$HERE/tools/LanguagePatch" ]; then
    CACHE="$HERE/vendor"
else
    CACHE="$(mktemp -d)"
    trap 'rm -rf "$CACHE"' EXIT
fi
mkdir -p "$CACHE"

# 1. BepInEx
UNPACK="$CACHE/be5"
if [ ! -f "$UNPACK/run_bepinex.sh" ]; then
    if [ ! -f "$CACHE/$BEPINEX_ZIP" ]; then
        say "Downloading BepInEx $BEPINEX_VERSION ..."
        fetch "$BEPINEX_URL" "$CACHE/$BEPINEX_ZIP"
    fi
    echo "$BEPINEX_SHA256  $CACHE/$BEPINEX_ZIP" | sha256sum -c - >/dev/null \
        || die "$BEPINEX_ZIP does not match its published checksum; not installing it."
    rm -rf "$UNPACK"
    mkdir -p "$UNPACK"
    extract "$CACHE/$BEPINEX_ZIP" "$UNPACK"
fi
cp -r "$UNPACK/BepInEx" "$UNPACK/libdoorstop.so" "$UNPACK/run_bepinex.sh" "$UNPACK/.doorstop_version" "$GAME/"
chmod +x "$GAME/run_bepinex.sh"
# Lets the game init Steamworks directly instead of relaunching through Steam,
# which would drop the injection — matters for headless runs.
echo "$APP_ID" > "$GAME/steam_appid.txt"
mkdir -p "$GAME/BepInEx/plugins"
say "BepInEx $BEPINEX_VERSION installed in: $GAME"

# 2. the patch
if [ "$MODE" = install ]; then
    PLUGINS="$GAME/BepInEx/plugins"
    rm -rf "$PLUGINS/BlakeManorFR" "$PLUGINS/BlakeManorFR.dll"
    if [ -f "$HERE/BepInEx/plugins/BlakeManorFR.dll" ]; then
        cp -r "$HERE/BepInEx/plugins/." "$PLUGINS/"
        SOURCE="this archive"
    elif [ -f "$HERE/build/patch/BlakeManorFR.dll" ] && [ -f "$HERE/corpus/fr/language.json" ]; then
        # one folder per language: every corpus/<code>/ that carries a language.json
        cp "$HERE/build/patch/BlakeManorFR.dll" "$PLUGINS/"
        for d in "$HERE"/corpus/*/; do
            [ -f "$d/language.json" ] || continue
            code="$(basename "$d")"
            mkdir -p "$PLUGINS/BlakeManorFR/$code"
            cp "$d"/*.json "$PLUGINS/BlakeManorFR/$code/"
        done
        SOURCE="this clone's build"
    else
        say "Fetching the latest release ..."
        URL="$(curl -fsSL "$RELEASES_API" \
              | sed -n 's/.*"browser_download_url": *"\([^"]*\/BlakeManorFR-[^"/]*\.zip\)".*/\1/p' | head -1)"
        [ -n "$URL" ] || die "Could not find a release archive on GitHub."
        fetch "$URL" "$CACHE/patch.zip"
        rm -rf "$CACHE/patch"
        mkdir -p "$CACHE/patch"
        extract "$CACHE/patch.zip" "$CACHE/patch"
        cp -r "$CACHE/patch/BepInEx/plugins/." "$PLUGINS/"
        SOURCE="${URL##*/}"
    fi
    say "Patch installed from $SOURCE."
fi

# 3. the one step only Steam can do
say
say "Last step, in Steam: right-click the game > Properties > General > Launch Options,"
say "and paste this line, quotes included:"
say
say "  \"$(launch_path)\" %command%"
say
say "Then start the game. Options > Interface > Langue switches French / English."
