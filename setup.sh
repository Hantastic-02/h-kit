#!/usr/bin/env bash
# 사용: 과제 작업 폴더에서  bash ~/kit/setup.sh
# 지우거나 덮어쓰지 않는다. 이미 있으면 건너뛰고 알린다.
set -u
KIT="$(cd "$(dirname "$0")" && pwd)"
TASK="$(pwd)"
echo "[setup] kit v2: $KIT @ $(git -C "$KIT" rev-parse --short HEAD 2>/dev/null || echo '?')"
echo "[setup] 작업 폴더: $TASK"

case "$KIT/" in "$TASK"/*) echo "[setup] 주의: kit이 작업 폴더 안에 있음. 작업 폴더 밖(~/kit)에 받는 것을 권장";; esac

mkdir -p "$HOME/.agents/skills" 2>/dev/null
for s in "$KIT"/skills/*/; do
  name="$(basename "$s")"
  if [ -e "$HOME/.agents/skills/$name" ]; then
    echo "[setup] 스킬 있음(건너뜀): $name  ← v1이 남아 있으면 지우고 다시 설치"
  elif cp -r "$s" "$HOME/.agents/skills/$name" 2>/dev/null; then
    echo "[setup] 스킬 설치: $name"
  else
    echo "[setup] 스킬 복사 실패: $name → '~/kit/skills/$name/SKILL.md를 읽고 따라'로 사용"
  fi
done

if [ -e "$TASK/AGENTS.md" ]; then
  echo "[setup] 과제에 AGENTS.md가 이미 있음(건드리지 않음)."
  echo "        codex 첫 입력: ~/kit/AGENTS.md를 읽고 따라. 과제의 AGENTS.md와 충돌하면 과제 쪽이 우선이야."
else
  cp "$KIT/AGENTS.md" "$TASK/AGENTS.md" && echo "[setup] AGENTS.md 복사"
fi

for f in WORKLOG.md STUDY.md; do
  if [ -e "$TASK/$f" ]; then
    echo "[setup] $f 있음(건너뜀)"
  else
    cp "$KIT/templates/$f" "$TASK/$f" && echo "[setup] $f 복사"
  fi
done

command -v python3 >/dev/null && echo "[setup] python3: $(python3 -V 2>&1)" || echo "[setup] python3 없음 → check.py 대신 CARD의 수동 점검"
git -C "$TASK" rev-parse --is-inside-work-tree >/dev/null 2>&1 && echo "[setup] git 저장소: 예" || echo "[setup] git 저장소 아님 → 과제 안내 확인 후 git init"
echo "[setup] 렌즈: $(ls "$KIT/lenses" | tr '\n' ' ')"
echo "[setup] 끝. codex를 새로 시작하세요 (AGENTS.md는 시작할 때 읽힘)."
