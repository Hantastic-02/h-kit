"""h-kit v4 설치 (Windows·Linux 공통). 과제 작업 폴더에서 실행한다.

  Linux(실제 시험):        python3 ~/kit/setup.py
  Windows(연습장 cmd):     python %USERPROFILE%\\kit\\setup.py

작업 폴더 안에 넣는 것 (이미 있으면 건너뛴다):
  .agents/skills/kit-*   단계 명령 6개 (작업 폴더 안 스킬만 읽는 환경에서도 동작, 제출물에도 포함)
  .agents/kit/           규칙 양식(templates)과 설계 카드(design)
  AGENTS.md, MEMO.md
"""
import shutil, subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
TASK = Path.cwd()


def say(msg):
    print("[setup] " + msg, flush=True)


def copy_dir(src, dst, label):
    if dst.exists():
        say(f"있음(건너뜀): {label}")
        return
    shutil.copytree(src, dst)
    say(f"설치: {label}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    say(f"h-kit v4: {KIT}")
    say(f"작업 폴더: {TASK}")
    if TASK == KIT or KIT in TASK.parents:
        say("주의: 작업 폴더가 kit 안입니다. 과제 폴더로 이동한 뒤 다시 실행하세요.")
        return 1
    if TASK in KIT.parents:
        say("주의: kit이 작업 폴더 안에 있습니다. 홈 폴더(~/kit)에 받는 것을 권장합니다.")
    for s in sorted((KIT / "skills").iterdir()):
        if (s / "SKILL.md").exists():
            copy_dir(s, TASK / ".agents" / "skills" / s.name, f".agents/skills/{s.name}")
    for d in ("templates", "design"):
        copy_dir(KIT / d, TASK / ".agents" / "kit" / d, f".agents/kit/{d}")
    if (TASK / "AGENTS.md").exists():
        say("과제에 AGENTS.md가 이미 있음(건드리지 않음) → codex 첫 입력: .agents/kit 안내대로 ~/kit/AGENTS.md도 읽고 따라. 과제 쪽이 우선이야.")
    else:
        shutil.copy2(KIT / "AGENTS.md", TASK / "AGENTS.md")
        say("복사: AGENTS.md")
    if (TASK / "MEMO.md").exists():
        say("있음(건너뜀): MEMO.md")
    else:
        shutil.copy2(KIT / "templates" / "MEMO.md", TASK / "MEMO.md")
        say("복사: MEMO.md")
    for tool in ("git", "docker", "node"):
        say(f"{tool}: {'있음' if shutil.which(tool) else '없음'}")
    try:
        inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=TASK,
                                capture_output=True, text=True).stdout.strip() == "true"
    except OSError:
        inside = False
    if inside:
        say("git 저장소: 예")
    else:
        try:
            ok = subprocess.run(["git", "init"], cwd=TASK, capture_output=True, text=True).returncode == 0
        except OSError:
            ok = False
        say("git 저장소 아님 → git init 완료 (첫 커밋은 $kit-start가 함)" if ok else "git 저장소 아님 → git init 실패. 직접 git init 하세요")
    say("끝. codex를 지금 새로 시작하세요(이미 켜져 있었다면 /exit 후 다시). 시작 화면이나 /skills에 kit-start·kit-plan·kit-build·kit-fix·kit-check·kit-explain 6개가 보이면 성공입니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
