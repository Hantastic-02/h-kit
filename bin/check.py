#!/usr/bin/env python3
"""기록·제출물 점검 (kit v2.2 lite,표준 라이브러리만 사용, 파일을 고치지 않음).

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
WORKLOG_MAX = 150
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


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def section(text, title):
    """'## title...' 부터 다음 '## ' 전까지 (### 하위 절 포함)."""
    m = re.search(rf"^## {re.escape(title)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def filled(body):
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    return [l for l in lines if l != "-" and not re.fullmatch(r"-\s*[^:]{0,24}:\s*", l)]


# 1. 키트가 작업 폴더 안에 섞였는지
if kit.startswith(root + os.sep):
    warn.append(f"키트 폴더가 작업 폴더 안에 있음: {rel(kit)} (제출물에 섞일 수 있음)")
for p in files({".md"}):
    if os.path.basename(p) == "SKILL.md":
        warn.append(f"작업 폴더 안에 스킬 파일: {rel(p)}")

# 2. WORKLOG
wl = os.path.join(root, "WORKLOG.md")
done_stages = []
if os.path.exists(wl):
    raw = read(wl)
    text = strip_comments(raw)
    n_lines = len(raw.splitlines())
    if n_lines > WORKLOG_MAX:
        warn.append(f"WORKLOG.md {n_lines}줄 (상한 {WORKLOG_MAX}줄): 완료 단계 할 일을 한 줄로 접기")
    else:
        info.append(f"WORKLOG.md {n_lines}줄")

    m_src = re.search(r"^- 사용 자료:(.*)$", text, re.M)
    if m_src and not re.search(r"\b[0-9a-f]{7,40}\b", m_src.group(1)):
        warn.append("WORKLOG 사용 자료 칸에 kit 커밋 해시가 없음 (git -C ~/kit rev-parse HEAD)")

    for title in ("합의", "동작 흐름"):
        body = section(text, title)
        if body is not None and not filled(body):
            warn.append(f"WORKLOG '{title}' 칸이 비어 있음 (내가 직접 쓸 칸)")

    plan = section(text, "PLAN")
    if plan is None:
        warn.append("WORKLOG에 PLAN 절이 없음")
    else:
        stages = re.split(r"^### ", plan, flags=re.M)[1:]
        real = [s for s in stages if re.match(r"S\d+", s)]
        if not real:
            warn.append("PLAN에 S 단계가 없음")
        status_count = {}
        for s in stages:
            head = s.splitlines()[0]
            name = head.split("—")[0].strip()
            unchecked = len(re.findall(r"^\s*- \[ \]", s, re.M))
            checked = len(re.findall(r"^\s*- \[[xX]\]", s, re.M))
            m = re.search(r"상태:\s*([^—|]+)", head)
            status = m.group(1).strip() if m else ""
            if name.startswith("S"):
                key = status.split()[0] if status else "?"
                status_count[key] = status_count.get(key, 0) + 1
                if status.startswith("완료"):
                    done_stages.append(name.split()[0])
                    if unchecked:
                        warn.append(f"PLAN {name}: 상태는 완료인데 미체크 {unchecked}개")
                if status.startswith("완료") and not re.search(r"[0-9a-f]{7}", status):
                    warn.append(f"PLAN {name}: 완료 상태에 커밋 해시가 없음")
            elif name.startswith("마무리"):
                info.append(f"마무리 체크 {checked}/{checked + unchecked}")
        if status_count:
            info.append("PLAN 단계 상태: " + ", ".join(f"{k} {v}" for k, v in status_count.items()))

    q_ids = {q.replace("-", "") for q in re.findall(r"^\|\s*(Q-?\d+)\s*\|", text, re.M)}
    for i, line in enumerate(raw.splitlines(), 1):
        for ref in re.findall(r"\[담당자 (Q-?\d+)\]", line):
            if ref.replace("-", "") not in q_ids:
                warn.append(f"WORKLOG.md:{i} 문답 표에 없는 {ref}를 인용")
    dec = section(text, "결정") or ""
    for line in dec.splitlines():
        if line.startswith("|") and "확정" in line and "미확정" not in line and "[담당자 Q" not in line:
            warn.append(f"WORKLOG 결정 표: 담당자 원문 번호 없이 '확정': {line.strip()[:70]}")
    unresolved = re.findall(r"\[미확정[^\]]*\]", text)
    if unresolved:
        info.append(f"미확정 표시 {len(unresolved)}곳: 인계 문서의 한계에 적었는지 확인")
else:
    warn.append("WORKLOG.md 없음 (과제 지정 문서를 쓰는 중이면 무시)")

# 3. REVIEW_NOTES
st_path = os.path.join(root, "REVIEW_NOTES.md")
if os.path.exists(st_path):
    st = strip_comments(read(st_path))
    bank = section(st, "검토 질문") or ""
    bank_rows = [[c.strip() for c in l.strip().strip("|").split("|")]
                 for l in bank.splitlines() if re.match(r"^\|\s*\d+\s*\|", l)]
    if bank_rows:
        no_concl = [r[0] for r in bank_rows if len(r) > 3 and not r[3]]
        no_mat = [r[0] for r in bank_rows if len(r) > 4 and not r[4]]
        info.append(f"검토 질문 {len(bank_rows)}개: 내 판단 빈칸 {len(no_concl)}개, 근거 빈칸 {len(no_mat)}개")
        if done_stages and len(no_concl) == len(bank_rows):
            warn.append("검토 질문 '내 판단'이 하나도 없음: 판단 한 줄은 직접 쓰기 (#" + ",#".join(no_concl[:5]) + " …)")
    wrong = section(st, "바로잡은 이해") or ""
    n_wrong = len([l for l in wrong.splitlines() if l.startswith("|") and not re.match(r"^\|[\s|:-]*\|$", l)]) - 1
    if n_wrong > 0:
        info.append(f"'바로잡은 이해' {n_wrong}건: 제출 직전 다시 읽기, wrap 리허설에서 다시 답하기")
    card = section(st, "영향 숫자") or ""
    rows = [l for l in card.splitlines() if l.startswith("|") and not re.match(r"^\|[\s|:-]*\|$", l)]
    if len(rows) <= 1:
        info.append("REVIEW_NOTES 영향 숫자가 비어 있음 (kit-wrap에서 채움)")
elif done_stages:
    warn.append("REVIEW_NOTES.md 없음 (검토 질문·바로잡은 이해를 남길 곳)")

# 4. 남은 자리표시·TODO
pat = re.compile(r"\b(TODO|FIXME|TBD|XXX)\b|<커밋 해시>|자리표시|__분")
for p in files(TEXT_EXT):
    if os.path.abspath(p).startswith(kit + os.sep):
        continue
    body = read(p)
    if p.endswith(".md"):  # 주석 안의 양식 예시는 건너뛰되 줄 번호는 유지
        body = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), body, flags=re.S)
    for i, line in enumerate(body.splitlines(), 1):
        if pat.search(line):
            warn.append(f"{rel(p)}:{i} 남은 표시: {line.strip()[:60]}")

# 5. git 상태
is_git = False
try:
    inside = subprocess.run(["git", "-C", root, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True, timeout=10)
    if inside.returncode == 0:
        is_git = True
        st_out = subprocess.run(["git", "-C", root, "status", "--porcelain"],
                                capture_output=True, text=True, timeout=10).stdout.strip()
        if st_out:
            warn.append(f"커밋 안 된 변경 {len(st_out.splitlines())}개 (git status)")
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
