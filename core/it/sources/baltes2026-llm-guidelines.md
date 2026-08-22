---
type: article-journal
title: "Guidelines for Empirical Studies in Software Engineering involving Large Language Models"
author:
  - { family: "Baltes", given: "Sebastian" }
  - { family: "Angermeir", given: "Florian" }
  - { family: "Arora", given: "Chetan" }
  - { family: "Muñoz Barón", given: "Marvin" }
  - { family: "Chen", given: "Chunyang" }
  - { family: "Böhme", given: "Lukas" }
  - { family: "Calefato", given: "Fabio" }
  - { family: "Ernst", given: "Neil" }
  - { family: "Falessi", given: "Davide" }
  - { family: "Fitzgerald", given: "Brian" }
  - { family: "Fucci", given: "Davide" }
  - { family: "He", given: "Junda" }
  - { family: "Treude", given: "Christoph" }
  - { family: "Kalinowski", given: "Marcos" }
  - { family: "Lambiase", given: "Stefano" }
  - { family: "Russo", given: "Daniel" }
  - { family: "Lungu", given: "Mircea" }
  - { family: "Martinez Montes", given: "Cristina" }
  - { family: "Prechelt", given: "Lutz" }
  - { family: "Ralph", given: "Paul" }
  - { family: "van Tonder", given: "Rijnard" }
  - { family: "Wagner", given: "Stefan" }
issued: "2026"
container-title: "Empirical Software Engineering"
number: "2508.15503"
version: "2026.06"
URL: "https://llm-guidelines.org"
snapshot: /it/archive/baltes2026-llm-guidelines/
snapshot_sha256: "99afe14b91b2280dc0bec71ec8bc6410e6df547e0a8b50733202b7bb1c22c5c6"
accessed: "2026-08-20"
---

# baltes2026-llm-guidelines

LLM이 들어간 소프트웨어 공학 실증 연구를 **어떻게 설계하고 무엇을 보고할 것인가**를
22인이 함께 쓴 지침 문서다. 연구 유형 일곱 개의 분류와 지침 여덟 개로 이루어져 있고
지침마다 요구(must)와 권고(should)를 갈라 적는다. 이 KB에서는 **LLM 실측 페이지에 버전
조건 블록을 다는 관행의 규범 근거**로 쓴다.

## 게재 지위 — 심사는 통과했으나 실측이 아니다

**확보본 1쪽에 `Empirical Software Engineering (accepted manuscript)`가 인쇄돼 있다.**
같은 쪽에 투고 2025-08-26과 개정 세 번(2026-02-27, 2026-05-05, 2026-06-11)이 찍혀 있고
§3 방법론이 저널 심사를 직접 서술한다.

> After completing the internal review, we invited external experts in empirical SE to
> review the study types and guidelines. During the review process of the *Empirical
> Software Engineering* journal, the structure and content were improved based on
> reviewers' suggestions.

그래서 등급은 `preprint`가 아니라 `peer-reviewed`다 — 반입 대장이 확보 전에 `preprint`로
두었던 것을 확보본 문면이 뒤집는다. **그러나 `peer-reviewed`가 절반만 맞다.** 이 문서에는 **결과 절이 없다** — 구성이
서론·범위·방법론·연구 유형·지침 5.1~5.8·결론이고 자기가 잰 값이 하나도 없다. §3이
밝히는 산출 과정은 실측이 아니라 **전문가 합의**다(ISERN 2024 세션 → CHASEAI 2024
워크스트림 → 격주 회의 → 저자 쌍 집필과 교차 검토 → 외부 전문가 검토 → 저널 심사).
계보도 임상시험의 CONSORT와 의료의 TRIPOD-LLM이라고 §2·§3이 직접 적고, 예시 논문
선정도 저자들이 `illustrative, not the result of a systematic review`라고 자인한다(§3).

곧 `evidence_grade` 열거값이 감당하지 못하는 조합이다 — **심사 통과 + 규범**. 등급
필드가 독립된 두 사실(심사를 통과했는가 / 실측인가 규범인가)을 하나로 지고 있어서
생기는 일이고, **이 KB는 새 열거값을 만들지 않았다.** 같은 조합의 소스가 셋째로 나타나면
그때 등급 체계를 두 축으로 쪼갠다. 그전까지는 아래 인용 규칙이 그 구멍을 막는다.

## 인용 규칙 — 규범만 인용하고 수치는 한 건도 옮기지 않는다

**이 소스에는 자기 측정값이 없다.** 인용 대상은 두 가지뿐이다.

- 여덟 지침의 요구(must)와 권고(should) **문면**
- 일곱 연구 유형의 분류(Table 1)

**이 논문에 실린 수치는 전부 남의 것이다.** §4.3의 비용 절감 폭, §5.5 Challenges의
벤치마크 실태 조사 비율, 프롬프트 형식이 성능을 얼마나 흔드는지 같은 값이 그렇고 전부
대괄호 참조번호가 붙어 있다. **그것을 이 논문 경유로 조항에 박으면 2차 경유 사실
조작이다** — 이 저장소가 이미 두 번 당한 자리다. 필요하면 원전으로 직접 간다.
`peer-reviewed`가 여는 것은 그 소스가 **스스로 잰 값**뿐이고 이 소스에는 그런 값이 없다.
§5.7의 일치도 문턱값도 Krippendorff의 것이지 이 논문의 측정값이 아니다.

## 판본 — 살아있는 문서라 판을 박는다

확보본은 두 벌이다. **`llm-empirics-hygiene.pdf`**는 86쪽이고 1쪽 좌측에
`arXiv:2508.15503v7 [cs.SE] 12 Jun 2026`이 인쇄돼 있다. arXiv에 v1부터 v7까지 있고
`/pdf/` 엔드포인트는 최신판을 주므로 **`2508.15503`만 적으면 어느 판인지 사라진다** —
판 번호와 날짜를 함께 적는다. **`llm-empirics-hygiene--llm-guidelines-org.html`**은
llm-guidelines.org 랜딩이고 서버 렌더된 본문이며(JS 셸이 아니다) 머리말에 사이트 판
태그 **2026.06**이 붙어 있다.

사이트가 개정마다 `YYYY.MM` 태그를 매기고 그 태그로 특정 판을 참조할 수 있다고 스스로
적으므로 이 KB는 **인용에 태그를 박는다.** arXiv v7(2026-06-12)과 사이트 태그 2026.06이
서로 일치한다. 열람은 2026-08-20T17:26:35Z이고 `accessed`는 그 열람일이다 — KB
스냅샷을 고정한 날이 아니라 살아있는 문서를 실제로 받은 날을 적는다. 사이트가 싣는
BibTeX도 프리프린트가 아니라 **수용 저널 논문**으로 세워져 있어(`@article`,
`journal = {Empirical Software Engineering}`, `year = {2026}`) 이 KB의 인용 키도 같은
지위로 세웠다. 텍스트 레이어 판정은 `text_based`(신뢰도 1.00, OCR 필요 0쪽)이고
재개점은 `_progress.yaml`이 정본이다.
