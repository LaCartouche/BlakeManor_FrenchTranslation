#!/usr/bin/env bash
# Sourced by the other scripts: locates the Steam install of the game.
#
#   blake_find_game     sets GAME (a preset GAME is honoured), returns 1 if not found
#   blake_launch_path   prints run_bepinex.sh's path as Steam itself sees it
#
# Looks through every Steam library the client knows about (libraryfolders.vdf),
# starting from the usual roots: native, symlinked, Flatpak and Snap installs.
APP_DIR="The Seance of Blake Manor"

blake_steam_roots() {
    local r
    for r in "$HOME/.local/share/Steam" "$HOME/.steam/steam" "$HOME/.steam/root" \
             "$HOME/.var/app/com.valvesoftware.Steam/.local/share/Steam" \
             "$HOME/snap/steam/common/.local/share/Steam"; do
        [ -d "$r/steamapps" ] && printf '%s\n' "$(cd "$r" && pwd -P)"
    done | awk '!seen[$0]++'
}

blake_libraries() {
    blake_steam_roots | while IFS= read -r root; do
        printf '%s\n' "$root"
        local vdf="$root/steamapps/libraryfolders.vdf"
        [ -f "$vdf" ] && sed -n 's/^[[:space:]]*"path"[[:space:]]*"\(.*\)"[[:space:]]*$/\1/p' "$vdf"
    done | awk '!seen[$0]++'
}

blake_find_game() {
    if [ -n "${GAME:-}" ]; then
        [ -d "$GAME" ] && return 0
        echo "GAME is set but that directory does not exist: $GAME" >&2
        return 1
    fi
    local lib
    while IFS= read -r lib; do
        if [ -d "$lib/steamapps/common/$APP_DIR" ]; then
            GAME="$lib/steamapps/common/$APP_DIR"
            export GAME
            return 0
        fi
    done < <(blake_libraries)
    echo "Could not find \"$APP_DIR\" in any Steam library." >&2
    echo "Set GAME=/path/to/the/game and run this again." >&2
    return 1
}

# Flatpak Steam runs with its own home, so a library under
# ~/.var/app/com.valvesoftware.Steam is addressed without that prefix inside.
blake_launch_path() {
    local p="$GAME/run_bepinex.sh"
    local fp="$HOME/.var/app/com.valvesoftware.Steam"
    case "$p" in "$fp"/*) p="$HOME/${p#"$fp"/}" ;; esac
    printf '%s\n' "$p"
}
