#!/usr/bin/env python3
"""기록·제출물 점검 (표준 라이브러리만 사용, 파일을 고치지 않음).

사용: python3 ~/kit/bin/check.py [과제 폴더, 기본=현재 폴더]
종료 코드: 0 문제 없음 / 1 경고 있음 / 2 점검할 대상이 없음
"""
import os
import re
import subprocess
import sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
warn, info = [], []
checked = 0
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
TEXT_EXT = {".md", ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".json", ".txt", ".sql", ".sh"}


def files(exts):
    for d, dirs, names in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for n in names:
            if os.path.splitext(n)[1].lower() in exts:
                yield os.path.join(d, n)


def read(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def rel(p):
    return os.path.relpath(p, root)


# 1. 키트가 작업 폴더 안에 섞였는지
if kit.startswith(root + os.sep):
    warn.append(f"키트 폴더가 작업 폴더 안에 있음: {rel(kit)} (제출물에 섞일 수 있음)")
for p in files({".md"}):
    if os.path.basename(p) == "SKILL.md":
        warn.append(f"작업 폴더 안에 스킬 파일: {rel(p)}")
checked += 1

# 2. WORKLOG 출처 점검
wl = os.path.join(root, "WORKLOG.md")
if os.path.exists(wl):
    text = read(wl)
    checked += 1
    q_ids = set(re.findall(r"^\|\s*(Q-?\d+)\s*\|", text, re.M))
    q_norm = {q.replace("-", "") for q in q_ids}
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("<!--"):
            continue
        if "확정" in line and "미확정" not in line and "[담당자 Q" not in line \
                and not re.match(r"^\|\s*Q-?\d+", line):
            warn.append(f"WORKLOG.md:{i} 담당자 원문 번호 없이 '확정': {line.strip()[:70]}")
        for ref in re.findall(r"\[담당자 (Q-?\d+)\]", line):
            if ref.replace("-", "") not in q_norm:
                warn.append(f"WORKLOG.md:{i} 문답 표에 없는 {ref}를 인용")
    nocomment = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    unresolved = re.findall(r"\[미확정[^\]]*\]", nocomment)
    if unresolved:
        info.append(f"미확정 항목 {len(unresolved)}개: 인계 문서의 한계에 적었는지 확인")
    for title in ("합의", "동작 흐름"):
        m = re.search(rf"## {title}[^\n]*\n(.*?)(\n## |\Z)", text, re.S)
        if m:
            body = [l for l in m.group(1).splitlines() if l.strip() and not l.strip().startswith("<!--")]
            filled = [l for l in body if l.strip() != "-" and not re.fullmatch(r"-\s*[^:]{0,20}:\s*", l.strip())]
            if not filled:
                warn.append(f"WORKLOG '{title}' 칸이 비어 있음 (내가 직접 쓸 칸)")
else:
    warn.append("WORKLOG.md 없음 (과제 지정 문서를 쓰는 중이면 무시)")

# 3. 남은 자리표시·TODO
pat = re.compile(r"\b(TODO|FIXME|TBD|XXX)\b|<커밋 해시>|자리표시")
for p in files(TEXT_EXT):
    if os.path.abspath(p).startswith(kit + os.sep):
        continue
    for i, line in enumerate(read(p).splitlines(), 1):
        if pat.search(line):
            warn.append(f"{rel(p)}:{i} 남은 표시: {line.strip()[:60]}")
checked += 1

# 4. git 상태
is_git = False
try:
    inside = subprocess.run(["git", "-C", root, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True, timeout=10)
    if inside.returncode == 0:
        is_git = True
        checked += 1
        st = subprocess.run(["git", "-C", root, "status", "--porcelain"],
                            capture_output=True, text=True, timeout=10).stdout.strip()
        if st:
            warn.append(f"커밋 안 된 변경 {len(st.splitlines())}개 (git status)")
        n = subprocess.run(["git", "-C", root, "rev-list", "--count", "HEAD"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        info.append(f"커밋 수: {n or '0'}")
    else:
        warn.append("git 저장소가 아님")
except (OSError, subprocess.TimeoutExpired):
    warn.append("git을 실행할 수 없음")

print(f"[check] 대상: {root}")
for w in warn:
    print("  경고:", w)
for x in info:
    print("  참고:", x)
if not os.path.exists(wl) and not is_git:
    print("[check] 점검할 기록이 없음 → 통과로 보지 않음")
    sys.exit(2)
print(f"[check] 경고 {len(warn)}개")
sys.exit(1 if warn else 0)
