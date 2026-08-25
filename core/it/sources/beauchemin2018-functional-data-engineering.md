---
type: post-weblog
title: "Functional Data Engineering — a modern paradigm for batch data processing"
author: [{family: Beauchemin, given: Maxime}]
issued: "2018-01-08"
container-title: "Medium"
URL: "https://medium.com/@maximebeauchemin/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a"
snapshot: /it/archive/beauchemin2018-functional-data-engineering/
snapshot_sha256: "f040513e00d2472ea9d3af1395bae8ecb76bffb10384e4781b7e98f32b17bbab"
accessed: "2026-08-25"
custom: {archive-url: "https://web.archive.org/web/20180806/https://medium.com/@maximebeauchemin/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a"}
---

# Functional Data Engineering — a modern paradigm for batch data processing

**배치 데이터 처리에 함수형 프로그래밍의 어휘를 붙인 실무자 에세이.** 이 KB가 이 글을
들이는 이유는 하나다 — [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md)이 이미
담고 있는 다섯 패턴의 **'왜'** 가 여기 있고, 그 페이지가 인용하는 Konieczny가 멱등성을
대중화한 글로 지목하는 것이 바로 이 글이기 때문이다. 지금까지 이 KB에서 이 글은 남의 문장
안의 이름이었고, 이제 원문 앵커를 갖는다.

## 지위 — 실무자 에세이이고 측정이 없다

- **근거 등급은 `essay`다.** 대장에 `evidence_grade:`가 기재돼 있지 않아 이 반입이 판정한
  값이다. 근거는 문면 자체다 — 실험도, 통제도, 표본도, 참고문헌 목록도 없다. 바깥 문헌으로
  걸린 링크는 위키백과 항목들과 킴벌 책의 서점 링크 하나뿐이다.
- **글 자신의 자기 규정이 그 지위를 말한다.** 서두: *"This post distills fragments of
  wisdom accumulated while working at Yahoo, Facebook, Airbnb and Lyft, with the
  perspective of well over a decade of data warehousing and data engineering
  experience."* 곧 **경험의 증류**이지 측정의 보고가 아니다.
- **마지막 절이 새로움도 스스로 부인한다** — *"While this post may be a first in
  formalizing the functional approach to data engineering, these practices aren't
  experimental or new by any means."* 이어지는 근거는 *"Large, data driven, analytically
  mature corporations have been applying these methods for years"* 로, **어느 회사가
  무엇을 얼마나 했는지는 적히지 않는다.** 이 문장을 실증으로 옮기면 원문이 하지 않은
  주장이 된다.
- **이해 상충을 저자가 스스로 밝힌다** — Airflow를 논하는 자리에서 *"Full disclosure is
  due here, the author of this post happens to be the creator of Airflow, so no wonder
  the tooling works well with the methodology prescribed here."* 도구 평가를 이 글에
  기대어 옮길 때 이 문장을 함께 옮긴다.
- **Yahoo·Facebook·Airbnb·Lyft는 일화다.** 회사 이름은 저자의 경력 서술로만 등장하고, 그
  회사들에서 무엇이 어떻게 됐는지의 서술이 본문에 없다. 사례로 인용할 때 **일화**라고 적는다.

## 판본 — 현행판 미대조, 2018-08-06 아카이브본 기준

- **이 KB가 보증하는 것은 아카이브본 한 벌의 문면뿐이다.** 확보본은 Wayback 2018-08-06
  캡처이고, `custom.archive-url`은 **그 날짜 기준의 조회 URL**이지 캡처의 정확한
  타임스탬프가 아니다. 파일 안에 Wayback 배너도 재작성된 링크도 없어 원본 바이트에 가깝다.
- **개정판이 존재한다는 것은 확보본 자신이 증언한다.** 파일에 심긴 JSON-LD에
  `"datePublished":"2018-01-08T06:00:49.181Z"` 와 함께
  `"dateModified":"2018-06-20T15:27:48.650Z"` 가 있다. 곧 **이 캡처 자체가 최초 발행 다섯
  달 뒤의 개정본**이다. 무엇이 고쳐졌는지는 이 확보본으로 알 수 없다.
- **현행 Medium 판은 대조하지 않았다.** 이 반입 시점에 현행판을 받을 수단이 이 환경에
  없다(2026-08-23 결정). 그러므로 **2018-08-06 이후의 개정 여부와 그 내용은 미지**이고, 이
  소스에 기댄 서술은 전부 그 아카이브본에 대한 것이다. 현행판에만 있는 문장을 이 소스로
  인용하는 일은 오인용이다.
- 문면에 인쇄된 서지:
  - `<title>`·`og:title` = 위 제목. `<link rel="canonical">` = 위 `URL`.
  - `meta property="author"` = `Maxime Beauchemin`, `twitter:creator` = `@mistercrunch`.
  - 바이라인 표시는 `Jan 7`이고 그 `<time datetime>` 속성은 `2018-01-08T06:00:49.181Z`다
    (표시는 현지 시각이고 `issued`는 그 UTC 값의 날짜를 따랐다).
  - 매체는 Medium 개인 프로필이다 — 확보본 JSON의 `approvedHomeCollectionId`가 빈
    문자열이라 **어떤 퍼블리케이션에도 실리지 않았다.** 저자 소개 줄은 *"Data engineer
    extraordinaire at Lyft, creator of Apache Airflow and Apache Superset"* 이다.
  - 글 끝에 Mark Grover를 드는 사사 한 줄이 있다.
  - 확보본 JSON의 `wordCount`는 `3503`, `imageCount`는 `5`, 표시 읽기 시간은
    `15 min read`다.
  - **킴벌 책 이름이 오식이다** — 링크 글자가 *"The Datawerouse Toolkit"* 이다(가리키는
    주소는 *The Data Warehouse Toolkit* 서점 페이지). 옮길 때 원문 표기를 고치지 않는다.

## 인용할 때 지킬 것

- **측정 수치가 0건이다.** 본문 전체에 단위 붙은 측정값이 없다. 나오는 숫자는 예시의
  연도(2017·2018), 예시의 기간(*"3 years of history"*·*"daily snapshot"*), 예시의 규모
  어림(*"the depth of the resulting graph grows beyond a thousand"*), 완화책의 폭
  (*"say 2–3 partitions"*)뿐이고 전부 **가정된 시나리오**다. 확보본에 보이는 박수 수·응답
  수는 캡처 시점의 소셜 지표이지 이 글의 내용이 아니다. **이 소스에 기대어 수치를 적는
  일은 어떤 경우에도 오인용이다.**
- **정의문은 인용 블록으로 옮긴다.** 순수 태스크의 규정(*"A pure task should be
  deterministic and idempotent…"*)처럼 낱말이 곧 내용인 자리가 그렇다.
- **함수형 프로그래밍의 정의는 이 글의 것이 아니다.** 글머리의 긴 정의 블록은 저자가
  *"from the functional programming Wikipedia page"* 라고 밝히고 통째로 옮긴 위키백과
  인용이다. 그 문단의 서술을 이 저자의 정의로 귀속시키지 않는다 — **2차 경유**다.
- **`f(f(x)) = f(x)` 는 이 글에 없다.** 확보본 전수 검색으로 확인했다. 글이 옮긴 위키백과
  문면은 *"calling a function f twice with the same value for an argument x produces the
  same result f(x) each time"* 로, 이는 **결정성**의 서술이지 멱등 항등식이 아니다. 이
  KB에서 그 항등식의 출처는 Konieczny(`absolute(-1) == absolute(absolute(absolute(-1)))`)
  이지 이 글이 아니다.
- **`INSERT OVERWRITE` 도 이 글에 없다.** 확보본에 등장하는 DML 낱말은 `UPDATE`·`APPEND`·
  `DELETE`·`INSERT`·`UPSERT`·`TRUNCATE PARTITION`·`UNION ALL`이다. 덮어쓰기의 처방은
  *"systematically overwriting partitions"* 와 *"systematically DELETE prior to
  INSERTing"* 이라는 산문으로 적혀 있다.
- **메타모픽(metamorphic)이라는 낱말도, 검증·테스트라는 틀도 이 글에 없다.** 저자가 드는
  멱등성의 정당화 축은 **재현 가능성**(reproducibility)과 **운영성**(operability)이다.
  멱등을 재실행 동치성 **검사**로 읽는 것은 이 KB의 읽기이고, 그 자리에는 `#hypothesis`가
  붙는다.
- **이 글의 각주로 알려진 세 문헌은 이 글에 없다.** 대장이 각주로 적어 둔 Ufford의
  Write-Audit-Publish, Gong & Campbell, Pipeline Debt는 확보본 전수 검색에서 **0건**이다
  (`Ufford`·`WAP`·`Write-Audit-Publish`·`Gong`·`Campbell`·`pipeline debt` 각 0회). 이
  글이 실제로 다는 바깥 링크는 위키백과 항목들(대부분 위 인용 블록 안), 저자 자신의 이전
  글 하나(주소 슬러그 `the-downfall-of-the-data-engineer`), 킴벌 책 서점 링크, 사사 대상의
  프로필이 전부다. **2018-08-06 아카이브본 기준의 판정**이고, 이후 개정판에서 추가됐을
  가능성은 대조하지 않았으므로 미지다.

## 이 소스가 닿을 자리

- [함수형 데이터 엔지니어링](../concepts/functional-data-engineering.md) — 이 소스가 세우는
  유일한 페이지
