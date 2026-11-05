# h-kit v4 — 한 번에 빌드, 남은 시간은 공부

AI 해커톤(Cofa Probe) 응시용 작업 키트입니다. 과제 결과물이나 과제용 코드는 들어 있지 않습니다.

이 키트의 생각:
- **계획 = 체크리스트.** `$kit-plan`이 P0/P1/P2 기능 + 자기 검토 + 문서까지 15~25개 항목으로 적고, 대조표로 빠진 것을 스스로 점검한다. 승인이 사실상 유일한 중간 조종 지점이다.
- **빌드는 한 번.** `$kit-build`는 체크리스트를 다 채울 때까지 멈추지 않는다. 자기 검토와 즉시 수정, REVIEW.md·GUIDE.md·HANDOFF.md 작성까지 포함한다. 중간에 바로 반영할 것이 생기면 그냥 말하면 된다.
- **검토는 직접, 수정은 한 번.** REVIEW.md("정상이면 보이는 것")로 화면을 보고, 터미널이 남으면 `$kit-check`를 병렬로. 모아서 `$kit-fix` 한 번.
- **남은 시간은 공부.** GUIDE.md는 빌드가 블록마다 채우고, 0절(5분 요약)과 9절(서술형 카드)부터 읽는다. `$kit-explain`은 내가 먼저 답하는 연습.
- **시간은 내가 조절한다.** 스킬은 시각을 강제하지 않는다. 기준선은 `TIMING.md`.

## 설치 (과제 작업 폴더에서)
```
# Linux (실제 시험)
git clone --depth 1 https://github.com/Hantastic-02/h-kit.git ~/kit && python3 ~/kit/setup.py
# Windows 연습장 (cmd)
git clone --depth 1 https://github.com/Hantastic-02/h-kit.git %USERPROFILE%\kit
python %USERPROFILE%\kit\setup.py
```
setup은 작업 폴더에 `AGENTS.md`, `MEMO.md`, `.agents/skills/kit-*`(단계 명령 6개), `.agents/kit/`(양식·설계 카드)를 넣는다. 이미 있는 파일은 건드리지 않는다. git 저장소가 아니면 `git init`도 한다. 설치 뒤 codex를 새로 시작해야 적용된다.

## 흐름
| 단계 | 내가 할 것 | 부를 것 |
|---|---|---|
| 정의 | README 같이 읽기, 운영 조건 질문 먼저 → 데이터 질문 연달아 전송 | `$kit-start` |
| 계획 | P0 제목·가정·대조표 검토, 아이디어 추가, 승인 | `$kit-plan` |
| 빌드 | MEMO.md 쓰기, 추가 질문 전송, 가끔 빌드 터미널 보기 | `$kit-build` |
| 검토 | REVIEW.md 따라 화면 직접 보기 | (선택) 새 터미널 `$kit-check` |
| 수정 | 본 것·이상한 점·새 담당자 답을 한꺼번에 | `$kit-fix` |
| 공부 | GUIDE 정독, 서술형 직접 답하기, 마무리 커밋 | 새 터미널 `$kit-explain` |

## 파일
| 파일 | 누가 읽나 | 내용 |
|---|---|---|
| AGENTS.md | Codex | 작업 규칙 (작업 폴더에 복사됨) |
| CARD.md | 나 | 순서·입력할 말·막혔을 때·서술형 답 틀 |
| TIMING.md | 나 | 이상적인 시간 배분 기준선(참고용) |
| skills/ | Codex | 단계별 지시 6개 |
| templates/PLAN.md | Codex | 환경·요구·가정·빌드 체크리스트·대조표 양식 |
| templates/REVIEW.md | Codex → 나 | 내가 직접 볼 순서와 "정상이면 보이는 것" |
| templates/GUIDE.md | Codex → 나 | 쉬운 설명서 목차 (0절 5분 요약, 9절 서술형 카드) |
| templates/MEMO.md | 나 | 보낸 질문·내 결정·AI를 고친 순간 |
| templates/EASY.md | Codex | 쉽게 이해되는 설명 수순·규칙·점검 |
| design/web-service.md | Codex | 웹 서비스 설계: "항상 필수"와 "요구할 때만" 점검표 |
