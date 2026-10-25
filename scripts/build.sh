#!/usr/bin/env bash
# Builds nesDS with the embedded rom slot. Run inside devkitpro/devkitarm (see the workflow).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPSTREAM_COMMIT=73b881baa7f92efef75c3bdfa8dbea1ce5ffcd9d
SRC="$ROOT/.work/nesDS"
DIST="$ROOT/dist"

rm -rf "$SRC" && mkdir -p "$(dirname "$SRC")" "$DIST"
git clone -q https://github.com/DS-Homebrew/nesDS.git "$SRC"
cd "$SRC"
git checkout -q "$UPSTREAM_COMMIT"
# the 6502 core (arm9/source/RP2A03) is a submodule
git submodule update --init --recursive
patch -p1 -l --forward --no-backup-if-mismatch < "$ROOT/patches/embed-rom.patch"

make
cp nesDS.nds "$DIST/nesDS-embed.nds"
ls -l "$DIST"
