#!/usr/bin/env bash
# Install skills into ~/.claude/skills. Usage: ./install.sh [skill-name ...]
set -euo pipefail
src_dir="$(cd "$(dirname "$0")" && pwd)/skills"
dest_dir="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest_dir"
if [[ $# -gt 0 ]]; then skills=("$@"); else mapfile -t skills < <(ls "$src_dir"); fi
for skill in "${skills[@]}"; do
    if [[ ! -f "$src_dir/$skill/SKILL.md" ]]; then
        echo "[WARN] Unknown skill: $skill" >&2
        continue
    fi
    rm -rf "${dest_dir:?}/$skill"
    cp -R "$src_dir/$skill" "$dest_dir/$skill"
    echo "[OK] $skill -> $dest_dir/$skill"
done
