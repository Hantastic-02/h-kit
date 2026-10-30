# kit v2.2 lite

AI 해커톤 응시용 작업 방법 키트입니다. 작업 규칙(AGENTS.md), 단계별 절차(Codex Skills 4개), 과제 유형별 관점(lenses/), 기록 양식(templates/), 기록 점검 스크립트(bin/check.py)를 담았습니다.
과제 결과물이나 과제용 코드는 포함하지 않습니다. 대회 결과 통지 전까지 공개 상태로 유지합니다.

설치: `git clone --depth 1 https://github.com/Hantastic-02/h-kit.git ~/kit && bash ~/kit/setup.sh`

흐름: `$kit-frame` → 담당자 질문 → `$kit-plan` → `$kit-build S1…Sn` → 새 세션 검토(CARD의 검토 프롬프트) → `$kit-wrap`

원칙: 모델이 스스로 잘하는 계획·테스트·검증 요령은 적지 않는다. 키트는 시험 규칙, 사람이 결정하는 순간, 채점자가 읽는 기록, 서술형 대비만 맡는다.

| 파일 | 역할 |
|---|---|
| AGENTS.md | 역할·결정·기록·검증 규칙 (작업 폴더에 복사) |
| templates/WORKLOG.md | 현재 상태 문서: 합의·PLAN 체크리스트·문답·결정 (덮어쓰기, 150줄 이내) |
| templates/STUDY.md | 서술형 질문 은행 15개·내가 틀렸던 것·숫자 카드 |
| lenses/*.md | 데이터 처리 / 웹 / 기존 코드 수정 / 원인 분석별 함정·사용 질문·사용 시나리오 |
| bin/check.py | WORKLOG 길이·PLAN 체크 상태·사용 자료 해시·질문 은행 빈칸·자리표시·git 상태 점검 |
