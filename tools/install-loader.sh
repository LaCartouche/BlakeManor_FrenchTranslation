#!/usr/bin/env bash
# Developer shortcut: BepInEx alone, unpacked into vendor/be5 for the build and
# installed into the game. Players use ./install.sh at the root (or install.bat).
exec "$(cd "$(dirname "$0")/.." && pwd)/install.sh" --loader-only "$@"
