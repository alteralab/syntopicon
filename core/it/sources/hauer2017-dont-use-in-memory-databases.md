---
type: post-weblog
title: "Don't use In-Memory Databases (H2, Fongo) for Tests"
author: [{family: Hauer, given: Philipp}]
issued: "2017-08-21"
container-title: "Philipp Hauer's Blog (phauer.com)"
URL: "https://phauer.com/2017/dont-use-in-memory-databases-tests-h2/"
snapshot: /it/archive/hauer2017-dont-use-in-memory-databases/
snapshot_sha256: "8d67ef4aa1e445579be495c3c08d99776efac49fa4939604fbe981f2b8201ee4"
accessed: "2026-08-20"
---

# Don't use In-Memory Databases (H2, Fongo) for Tests

**인메모리(in-memory) 데이터베이스를 테스트에 쓰지 말고 실물 데이터베이스를 컨테이너로
띄우라는 처방과 그 처방의 실행 방법 둘을 적은 글.** 이 KB가 이 글을 들이는 이유는 진단이
아니라 **처방이 실행 가능한 층까지 내려와 있다는 것**이다 — 같은 진단을 적은 다른 두 소스와
달리 이 글은 `TestContainers`를 고른 이유와 그 대가(피드백 지연 10~15초)까지 적는다.

## 지위 — 실무자의 경험이고 측정이 없다

- **근거 등급 표기는 `practitioner-norm`이다.** 실험도 표본도 측정도 없다. 인용할 수 있는
  수치는 컨테이너 기동 시간의 어림(`This takes some time (10 - 15 s)`) 하나뿐이고 그것도
  측정 절차가 없다. **참고문헌 절이 없고**, 근거로 드는 것은 저자 팀의 사례다
  (`Let me give a very simple example from my experience`).
- **대장(queue.yaml)에 `evidence_grade:` 기재가 없다.** 이 등급은 **이 반입이 문면을 보고
  붙인 것**이다.
- **자기 규정이 1인칭으로 반복된다** — `I explain my reservations`, `For me, this is fine`,
  `I recommend this approach`, `TestContainers convinced me in practice`. 곧 이 글은 규범이
  아니라 **한 사람의 선택과 그 이유**로 자기를 규정한다.

## 판과 서지 — 문면에 인쇄된 것

- **게시일과 갱신일이 둘 다 문면에 있다**: 제목 아래 `Posted on Aug 21, 2017. Updated on
  Jun 12, 2022`. 메타 태그의 `article:published_time`은 `2017-08-21`,
  `article:modified_time`·`og:updated_time`은 `2022-06-12`다. **`issued`는 게시 연도이고,
  확보본의 문면은 2022년 갱신을 거친 판이다** — 어느 문장이 2017년 것이고 어느 문장이 2022년에
  손질된 것인지는 **문면으로 구분되지 않는다.**
- **경로가 바뀐 이력이 있다.** 대장이 적어 둔 대로 옛 `philipphauer.de` 경로는 404이고
  현행 정본은 `phauer.com/2017/dont-use-in-memory-databases-tests-h2/`다(재검증 2026-08-20).
- **저자 표시가 문면에 있다** — 사이트 제목이 `Philipp Hauer's Blog`이고 말미 소개 문단이
  저자를 밝힌다. 메타 태그 `author`·`article:author`도 `Philipp Hauer`다.
- **확보 시점은 2026-08-20이다**(`accessed`). 스냅샷 고정은 2026-08-24이고 바이트가 같은
  사본이다. **살아 있는 페이지이므로 현행판 재취득·대조는 하지 않았다.**
- 확보본은 Hugo 0.86.1이 찍은 HTML 한 장이다. 사이트 껍데기·카테고리 목록·최근 글 목록·
  광고 스크립트가 함께 들어 있다.

## 인용할 때 지킬 것

- **학술 근거로 쓰지 않는다.** 조항에 쓸 때는 저자의 자기 규정(한 팀의 사례·한 사람의 추천)을
  함께 옮긴다.
- **낱말의 층은 제목이 가장 세다.** 제목이 `Don't use…`이고 TL;DR의 처방이 `Throw H2 and
  Fongo away`다. **그러나 본문 어디에도 예외 없는 금지 선언은 없고**, 논증은 전부 대가와
  선택지의 나열이다(`What are our unpleasant options…`). 제목의 명령형만 떼어 인용하지 않는다.
- **도구 이름과 버전은 2017~2022년 지형이다.** `H2`·`Fongo`·`gradle-dcompose-plugin 0.9.1`·
  `io.fabric8:docker-maven-plugin 0.21.0`·`mysql:5.5.53`·`MySQLContainer`가 그 시점의 것이고,
  **빌드 플러그인 예제 둘은 이 KB가 개념 페이지로 옮기지 않는다**(도구 사용법은 승격 대상이
  아니다). 원문 낱말은 `TestContainers`이고 태그에는 `Testcontainers` 표기도 함께 있다.
- **엔진별 사례는 그 엔진의 것이다.** MySQL 5.7.6의 `virtual` 예약어, H2에 없는
  `unix_timestamp()`, 오라클 트리거, 포스트그레스의 윈도 함수와 JSON 타입, Fongo의 정렬·
  배열 필터 차이는 각각 그 엔진 쌍의 사례이고 일반 명제가 아니다.

## 옮기지 않은 것

사이트 껍데기(헤더·사이드바·광고·푸터·카테고리와 태그 목록·관련 글·최근 글), 그리고
`Gradle Implementation`·`Maven Implementation` 두 절의 빌드 스크립트 전문이다. 그 절이
답하는 것은 **컨테이너를 어떻게 붙이는가**이고 이 KB가 옮긴 것은 **왜 컨테이너인가**뿐이다.
본문이 거는 바깥 링크(TestContainers 사이트·저자의 예제 저장소 셋·H2 호환성 문서)는
**열지 않았다.**

## 이 소스가 닿을 자리

- [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md) —
  이 글이 다른 두 소스와 함께 답하는 자리. **이 글이 그 페이지의 처방 층을 소유한다**
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — 응용 전용
  데이터베이스는 실물을 쓰라는 처방. 이 글은 그 "실물"을 어떻게 세우는가를 적는다
