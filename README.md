# h-kit v5 — AI와 함께 데이터 업무 서비스를 만드는 작업 키트

Codex로 업무 과제를 풀 때 쓰는 작업 규칙(AGENTS.md), 단계 명령(Skill) 6개, 문서 양식, 방법 카드를 담은 키트입니다. 과제 결과물이나 과제용 코드는 들어 있지 않습니다.

## 설치 (과제 작업 폴더에서)
```
# Linux / macOS
git clone --depth 1 https://github.com/Hantastic-02/h-kit.git ~/kit && python3 ~/kit/setup.py
# Windows (cmd)
git clone --depth 1 https://github.com/Hantastic-02/h-kit.git %USERPROFILE%\kit
python %USERPROFILE%\kit\setup.py
```
setup은 작업 폴더에 `AGENTS.md`, `.agents/skills/kit-*`(단계 명령 6개), `.agents/kit/`(양식·방법 카드)를 넣습니다. 이미 있는 파일은 건드리지 않습니다. git 저장소가 아니면 `git init`도 합니다. 설치 뒤 codex를 새로 시작해야 적용됩니다.

## 흐름
| 단계 | 명령 | 하는 일 | 멈춤 |
|---|---|---|---|
| 시작 | `$kit-start` | 환경 확인, 자료·데이터 파악, 담당자 질문, 문제 후보 | 담당자 답 기다림 |
| 계획 | `$kit-plan` | 합의 메시지, 방법 선택, 빌드 체크리스트 | 사용자 승인 |
| 빌드 | `$kit-build` | 뼈대 → 핵심 계산 → (확인 지점) → 나머지 → 자기 검토·안전 점검 → 문서 | 확인 지점 한 번 |
| 검토 | `$kit-check` | 다른 세션에서 독립 검토(읽기 전용) | — |
| 수정 | `$kit-fix` | 검토 결과·변경 요청을 모아 한 번에 고치고 재검사 | — |
| 마무리 | `$kit-wrap` | 처음부터 재실행, 문서 정합, 시연 순서, 제출 점검 | — |

중간에 "마무리해"라고 하면 남은 기능을 멈추고 자기 검토와 문서로 갑니다.

## 파일
| 파일 | 내용 |
|---|---|
| AGENTS.md | 작업 규칙 (작업 폴더에 복사됨) |
| skills/ | 단계 명령 6개 |
| templates/ | PLAN · DECISIONS · HANDOFF · REVIEW · GUIDE · DEMO 양식 |
| cards/ | 방법 카드: 판정·모니터링, 두 그룹 비교, 출처 맞추기·보고서, 선택지 비교·배정, 원인 찾기·분석 보고, 웹 서비스 기본 |

## 버전
- v5 (2026-11-09): 단계 명령 6개, GUIDE.md, 안전 점검(E6), 방법 카드 5장.
- v5 보강 (2026-11-10): 결론을 뒤집을 수 있는 처리 선택과 결론 민감도(kit-plan·kit-build·kit-check), 작은 층·가중 합·시작일(compare-groups, judge-monitor), 계정 표와 화면 기본(web-service), REVIEW 양식, 결론에 영향을 주는 선택은 담당자 질문 먼저, 순서·기간을 바꾼 입력 실행.
- v5 보강 2 (2026-11-10 저녁): 첫 질문(함께 쓰는 사람 수, 반올림·하루 시작 시각·시간대, 안전·법적 의무), 문서 예시와 규칙이 다른 곳 신호, 기존 코드 전·후 비교와 기존 테스트 점검, 확인 지점 뒤 중간 공유 메시지, 새 데이터 파일에도 데이터 신호, 원인 찾기 카드.
