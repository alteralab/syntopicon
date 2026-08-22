---
type: paper-conference
title: "Mutation-Guided LLM-based Test Generation at Meta"
author:
  - { family: "Foster", given: "Christopher" }
  - { family: "Gulati", given: "Abhishek" }
  - { family: "Harman", given: "Mark" }
  - { family: "Harper", given: "Inna" }
  - { family: "Mao", given: "Ke" }
  - { family: "Ritchey", given: "Jillian" }
  - { family: "Robert", given: "Hervé" }
  - { family: "Sengupta", given: "Shubho" }
issued: "2025-01-22"
event-title: "FSE Companion '25"
number: "2501.12862"
version: "v1"
DOI: "10.1145/3696630.3728544"
URL: "https://arxiv.org/abs/2501.12862"
snapshot: /it/archive/foster2025-ach/
snapshot_sha256: "a037b8af2ba79d286ee30784eb3232fdfbd1b8b686bf468f8f10fab0cbcce6d1"
accessed: "2026-08-22"
---

# foster2025-ach

Meta의 **ACH**(Automated Compliance Hardener) 배포 보고다. 앞의 TestGen-LLM이 커버리지를
목표로 삼았다면 이쪽은 **먼저 결함을 만들고 그 결함을 잡는 테스트를 만든다** — 관심사(여기서는
개인정보)에 맞춘 뮤턴트를 생성하고, 기존 어느 테스트도 그것을 죽이지 못하는 것만 남겨 테스트
생성의 프롬프트로 쓴다. 이 KB에서는 **수용 조건을 커버리지에서 결함 검출로 옮긴 산업 실물**로
쓴다.

## 게재 지위 — 심사 게재이되 산업 자기 보고

- **문면이 게재 표면을 인쇄한다.** 1쪽 판권 블록에
  `FSE Companion ’25, 23 – 27, 2025, Trondheim, Norway`가, ACM Reference Format에
  `In Companion Proceedings of the 33rd ACM International Conference on the Foundations of
  Software Engineering (FSE Companion ’25), 23 – 27, 2025, Trondheim, Norway.`가 있다.
  `Companion`은 확보본 전문에서 15회 나온다.
- **그러나 같은 블록의 다른 값들이 낡아 있다.** 저작권 연도가 `© 2024`이고 ACM Reference
  Format의 발행 연도도 `2024`이며, 인쇄된 DOI는 `10.1145/3663529.3663839` — **이 KB가
  TestGen-LLM 쪽에 배정한 DOI와 같은 문자열**이다. 곧 확보본 1쪽의 ACM 템플릿 블록은 앞
  논문의 것을 물려받은 채 갱신되지 않았다. 이 페이지의 `DOI`는 문면이 아니라
  **대장·ACM DL 레코드 근거**이고, `issued`는 arXiv v1 등재일이다.
- **저자 8인은 실물이다** — 1쪽에 이름과 소속(Product Compliance and Privacy · Developer
  Infrastructure · WhatsApp · Messenger · FAIR)이 인쇄돼 있다.
- **`Assured`는 이 논문의 제목이 아니지만 본문에 산다.** 게재 제목은
  `Mutation-Guided LLM-based Test Generation at Meta`이고, `assured`는 대소문자 무시 검색에서
  **7회** 나온다 — §1 기여 목록과 도입 산문에 2회, §2 도입에 2회, §7 관련 연구에 2회,
  참고문헌 [7](Alshahwan et al. 2024, *Assured LLM-Based Software Engineering*, keynote
  paper)에 1회다. `assurance(s)`는 따로 8회다. **"게재작은 Assured LLMSE 논문이 아니다"는
  참이지만 "Assured 0회"는 거짓이다** — 이 논문은 자기 워크플로를 Assured LLMSE의 사례로
  규정하고 그 개념을 [7]에서 빌린다.
- **심사를 통과한 문서이되 실증의 성격은 산업 자기 보고다.** 대상은 Meta 내부 안드로이드
  코드베이스이고, 뮤턴트·테스트·리뷰 기록이 공개되지 않아 **제3자 재현이 불가능하다.**

## 인용 규칙 — 결과 절과 표만

- **초록과 §1의 값은 옮기지 않는다.** 초록은 `9,095 mutants and 571 ... test cases`를,
  §1 기여 목록은 `4,660 candidate mutants ... from 10,795 classes`를 적는데 둘 다 §3 결과
  절과 Table 2·8이 분모와 함께 다시 적는 값이다. 결과 절 쪽을 쓴다.
- **뮤턴트 수에는 층이 셋이고 섞이면 틀린 말이 된다** (Table 2): 생성된 총수 31,677 →
  빌드·통과하는 것 9,095(29%) → 등가가 아니라고 판정된 것 4,660(51%). 분모가 매번 다르다.
- **정밀도·재현율에는 판정 규칙이 붙는다** (Table 6). 같은 에이전트의 값이 규칙마다 넷이다
  — `unsure`를 세지 않으면 0.97/0.44, `unsure`를 등가로 세면 0.79/0.47, 구문 동일까지
  포함하면 0.90/0.69, 주석 제거 전처리까지 붙이면 0.95/0.96. **규칙을 안 붙인 단일 쌍은
  인용하지 않는다.**
- **`likely actual` 열은 추정치다** (Table 8). 네 플랫폼은 Table 5의 사람 판정 등가 비율로,
  나머지는 그 넷의 평균으로 보정한 값이라고 §6이 적는다. 이 KB는 `believed` 쪽 원값을 쓰고
  보정값은 추정임을 밝힐 때만 쓴다.
- **이 논문이 인용한 제3자 수치는 옮기지 않는다.** §3의 "규칙 기반 도구의 등가 뮤턴트
  비율이 대체로 10~15%", §7의 Copilot 수용률 약 30%, Tian의 F1 35% 개선은 전부 남의 값이다.
- **Figure 2는 리커트 척도 지시문의 화면 캡처**라 수치가 없다.

## 판본과 텍스트 레이어

텍스트 레이어 판정은 `text_based`(신뢰도 1.00, OCR 필요 0/12쪽)라 기계 추출로 읽었다.
**Table 2·4·5·7·8은 헤더가 여러 줄로 쪼개진 다단 조판이라 기본 추출에서 열과 값이
분리된다** — 표 값은 전부 `pdftotext -layout` 정렬본과 대조해 옮겼다. Figure 1(파이프라인
도해)은 도형 안 이름표가 흩어져 읽히므로 §2 산문과 Table 1(프롬프트 셋)이 적는 것만 옮겼다.
재개점은 `_progress.yaml`이 정본이다.

## 대장이 적어 둔 것 — 이 KB가 확인하지 않은 것

확보 대장은 이 파일이 **UCL Discovery의 저자 기탁본(Published Version, pp.180–191)과
sha256이 같다**고 적는다(`a2ec8f7d…`, 확보본 파일 해시로 대조 확인). 그러나 이 KB는 UCL
Discovery 레코드를 직접 조회하지 않았으므로 **쪽수 pp.180–191은 대장 기재이지 문면 근거가
아니다.** camera-ready 문면과의 대조도 수행되지 않았다.
