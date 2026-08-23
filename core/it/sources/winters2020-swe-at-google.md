---
type: book
title: "Software Engineering at Google: Lessons Learned from Programming Over Time"
author:
  - { family: "Winters", given: "Titus" }
  - { family: "Manshreck", given: "Tom" }
  - { family: "Wright", given: "Hyrum" }
issued: "2020"
publisher: "O'Reilly Media"
URL: "https://abseil.io/resources/swe-book"
snapshot: /it/archive/winters2020-swe-at-google/
snapshot_sha256: "949af1892e5546d9867b30793c440531fee53981e2e10eabe43315d1d32cb723"
accessed: "2026-08-23"
---

# winters2020-swe-at-google

**한 회사가 자기 테스트 실무를 스스로 적은 책.** O'Reilly에서 2020년에 나왔고 같은 해
`abseil.io`가 CC BY-NC-ND 4.0으로 HTML 전문을 공개했다. 이 KB가 읽은 것은 그 공개판이다.

## 지위 — 산업 규범이지 실증이 아니다

- **근거 등급은 `industry-norm`이다.** 테스트 장 넷(11~14장)에 통제도 표본도 재현 절차도
  없다. 실린 수치는 회사가 정한 목표치이거나 사내 계측의 요약 진술이고, **분모와 집계
  절차가 인쇄된 것은 한 건뿐이다**(11장의 불안정 비율 — 그마저 분모의 경계를 14장이 따로
  적는다). 이 KB는 이 책을 "학술 근거"로 쓰지 않는다.
- **규모 전제를 떼면 옮겨지지 않는다.** 11장이 스스로 적는 조건이 20억 줄이 넘는 단일
  저장소, 주당 2,500만 줄 규모의 변경, 지점을 쓰지 않고 저장소 머리에 바로 커밋하는 관행,
  그리고 그 위에 선 사내 지속 통합 체계(TAP)다. 13장의 반-목 논거는 여기에 더해 한 API가
  **수만 번 목으로 대체된다**는 조건, 실물의 소유팀이 가짜를 만들어 유지한다는 조건,
  정적 분석 도구가 그것을 집행한다는 조건에 기댄다.
- **책 자신이 헤지를 단다.** 테스트 비중 권고에 `As a very rough guideline`,
  `we tend to aim to have`, `every team's mix will be a little different`가 붙어 있고,
  그 다음 문단이 `When considering your own mix, you might want a different balance`로
  시작한다. 이 값들을 측정값으로 인용하지 않는다.

## 판과 서지 — 무엇이 문면에 인쇄돼 있는가

- **출간과 큐레이터**: 공개판 안내면(`index.html`)이 `In March, 2020, we published a book
  titled "Software Engineering at Google" curated by Titus Winters, Tom Manshreck and
  Hyrum Wright`라고 적는다. 세 사람이 CSL `author`에 든 것은 이 문면 근거다.
- **공개판의 지위**: 같은 면이 `we are providing a digital version of this book in HTML
  free of charge`와 `Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
  International Public License`를 적고, 각 장 하단에 `CC BY-NC-ND 4.0`이 찍혀 있다.
  종이본 구매 링크가 O'Reilly로 걸려 있어 `publisher`를 그렇게 적었다.
- **ISBN은 이 확보본에 인쇄돼 있지 않다.** 그래서 적지 않는다.
- **열람일 스탬프**: 2026-08-23. 확보 시점은 2026-08-20이고, 이 KB의 직인용은 위
  `snapshot_sha256`이 가리키는 판본에 대한 것이다.
- **장별 저자가 따로 인쇄돼 있다.** 이 KB가 읽은 넷은 11장 Adam Bender, 12장 Erik
  Kuefler, 13장 Andrew Trenk·Dillon Bly, 14장 Joseph Graves이고 넷 다 편집자가 Tom
  Manshreck이다. **각 장의 주장을 세 큐레이터 개인의 말로 옮기지 않는다.**
  - 11장 저자는 이 KB의 다른 소스 [arguelles2020-coverage](arguelles2020-coverage.md)의
    공저자이기도 하다. 두 문헌의 커버리지 서술이 같은 방향인 것은 우연이 아니다.

## locator는 장과 절 제목이다

**공개판 HTML에 쪽 번호가 없다.** 그래서 이 KB의 각주는 `11장 §"Test Size"`처럼 **장
번호 + 원문 절 제목**으로 자리를 적는다. 절 제목은 원문 표기 그대로 옮긴다(번역하면 다시
찾을 수 없다). 그림·표 번호가 있는 자리는 그것도 함께 적는다.

## 반입 범위 — 확보는 전체, 증류는 넷

확보본은 `ch01`~`ch25`와 안내면까지 26개 파일 전부다. **읽고 옮긴 것은 11~14장뿐이고**,
나머지 21개 장은 이 KB의 검증 축에 호출자가 없어 열지 않았다. 진행의 정본은
`it/archive/winters2020-swe-at-google/_progress.yaml`이다.

- 11장 `Testing Overview` — 크기와 범위의 구분, small·medium·large의 제약, 불안정 비율,
  피라미드 비중, 커버리지 각주, 회사 규모 서술, 테스트 문화의 내력
- 12장 `Unit Testing` — 단위 테스트 비중의 어림 규칙, 변하지 않는 테스트, 공개 API로
  테스트하기, 상태 대 상호작용, DAMP 대 DRY
- 13장 `Test Doubles` — 실물·가짜·스텁·상호작용 검증의 선호 순서와 각각의 조건
- 14장 `Larger Testing` — 큰 테스트의 정의와 종류, SUT 형태, TAP 적격성, 소유권

## 인용할 때 지킬 것

- **80/15/5와 80/20은 측정값이 아니다.** 11장의 그림 11-3 설명이 그 비율을
  `Google's version of Mike Cohn's test pyramid`라 적고 각주 6이 출처를 Mike Cohn,
  *Succeeding with Agile*(2009)로 단다. **출처가 회사 데이터가 아니라 다른 책의
  피라미드다.** 인용할 때는 목표치라는 지위와 헤지 셋을 함께 적는다.
- **크기 어휘(small·medium·large)의 최초 공개는 이 책이 아니다.** 10년 앞선
  [stewart2010-test-sizes](stewart2010-test-sizes.md)가 정의 표를 먼저 냈다. 책은 정본
  서술이고 블로그는 계보 각주다 — 둘의 정의가 어디서 갈리는지는 개념 페이지에 있다.
- **"불안정 0 정책"은 이 책에 없다.** 11~14장의 `flak*` 문장을 전수 대조했고 그런 조문이
  없다. 오히려 11장이 자동 재실행을 조건부로 승인하고, 14장은 큰 테스트 상당수가
  `nonhermetic, too flaky` 라서 TAP 밖에 있다고 적는다. 0.15%라는 값은 **그 밖으로
  나간 것을 뺀 분모** 위의 값이다.
- **0.15%와 1.5%를 섞지 않는다.** 이 책의 값은 11장의 0.15%다. 확보본 전 25장에 `1.5%`는
  없다(`grep` 확인). 다른 문헌의 1.5%를 이 책 경유로 옮기지 않는다.
- **13장의 반-목 논거를 규모 전제 없이 옮기지 않는다.** 같은 장이 가짜의 값어치를 사용자
  수의 함수로 적는다 — 손에 꼽을 사용자뿐이면 만들 값이 없을 수 있다고 쓴다.

## 옮기지 않은 것

11~14장 밖의 21개 장 전부, 각 장의 그림(도판은 HTML에 이미지로만 있다), 코드 예제 가운데
개념 설명에 필요하지 않은 것, 그리고 안내면의 사이트 껍데기다.
