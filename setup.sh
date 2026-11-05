#!/usr/bin/env bash
# 사용: 과제 작업 폴더에서  bash ~/kit/setup.sh   (내용은 setup.py와 같다)
KIT="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then exec python3 "$KIT/setup.py"; fi
if command -v python  >/dev/null 2>&1; then exec python  "$KIT/setup.py"; fi
# 파이썬이 없을 때: 같은 일을 셸로
set -u
TASK="$(pwd)"
echo "[setup] python 없음 → 셸로 설치. 작업 폴더: $TASK"
mkdir -p "$TASK/.agents/skills" "$TASK/.agents/kit"
for s in "$KIT"/skills/*/; do
  n="$(basename "$s")"
  [ -e "$TASK/.agents/skills/$n" ] && echo "[setup] 있음: $n" || { cp -r "$s" "$TASK/.agents/skills/$n" && echo "[setup] 설치: $n"; }
done
for d in templates design; do [ -e "$TASK/.agents/kit/$d" ] || cp -r "$KIT/$d" "$TASK/.agents/kit/$d"; done
[ -e "$TASK/AGENTS.md" ] && echo "[setup] AGENTS.md 있음(건드리지 않음)" || cp "$KIT/AGENTS.md" "$TASK/AGENTS.md"
[ -e "$TASK/MEMO.md" ] || cp "$KIT/templates/MEMO.md" "$TASK/MEMO.md"
echo "[setup] 끝. codex를 새로 시작하세요."
