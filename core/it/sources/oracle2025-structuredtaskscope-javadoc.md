---
type: webpage
title: "StructuredTaskScope.Joiner (Java SE 25 & JDK 25 API, Preview)"
author:
  - { literal: "Oracle" }
issued: "2025"
container-title: "Java SE 25 & JDK 25 API Specification"
version: "25"
URL: "https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/StructuredTaskScope.Joiner.html"
snapshot: /it/archive/oracle2025-structuredtaskscope-javadoc/
snapshot_sha256: "612140f046572e2b2a8225f5c4030a484d6b9643ea27916a822e01e19574ca0b"
accessed: "2026-09-06"
---

# StructuredTaskScope.Joiner — JDK 25 API 문서

- [무엇을 들이려고 이 문서를 여는가](#무엇을-들이려고-이-문서를-여는가)
- [이 문서의 지위와 판](#이-문서의-지위와-판)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [닿은 자리](#닿은-자리)

**JDK 25 API 문서의 `java.base` 모듈 `java.util.concurrent.StructuredTaskScope.Joiner`
페이지. 프리뷰(preview) API로 표시되어 있다.** 조이너 팩토리 다섯 개의 선언과 `result()`
계약이 이 한 쪽에 다 들어 있다.

## 무엇을 들이려고 이 문서를 여는가

이 KB는 [모던 자바 동시성](rahman2025.md)을 반입하면서 미해소 항목 하나를 안고 있었다 —
`Joiner.awaitAll()`의 `join()`이 무엇을 돌려주는지가 그 책 안에서 세 자리로 갈렸다. 책의 다른
장은 그 물음을 다시 다루지 않아 **소스 하나로는 닫히지 않는 자리**였다. 규격이 답하는 물음이므로
규격을 들인다.

## 이 문서의 지위와 판

- **만든 쪽이 낸 규격 문서다.** 실무자 관찰이나 해설이 아니라 API 선언 그 자체이므로, 반환 타입과
  계약 문장에 관한 한 이 KB 안에서 가장 높은 근거다.
- **판 표기는 두 겹이다.** 문서 머리는 `Java SE 25 & JDK 25`이고, 문서 안 링크·타입 이름에
  `PREVIEW` 표시가 붙는다. 프리뷰 API라 **정식화되면서 바뀔 수 있다** — 이 문서에서 온 claim은
  버전 조건 "JDK 25 API 문서 기준(프리뷰)"을 함께 진다.
- **living doc이라 판이 조용히 갈릴 수 있다.** 스냅샷의 페이지 메타에 찍힌 갱신 표기는
  `2026-07-21`이다. 다시 인용할 때는 `accessed`가 아니라 스냅샷 사본을 본다.

## 인용할 때 지킬 것

- **반환 타입은 문서에 적힌 선언 그대로 옮긴다.** 옮겨 적는 과정에서 `Void`와
  `Stream<Subtask<T>>`가 섞이는 것이 애초의 문제였다.
- **책과 어긋나는 자리는 `contradicts`가 아니다.** 규격과 해설서가 같은 API를 두고 다른 값을
  말하면 그것은 두 주장의 대립이 아니라 **해설서의 오기**다. 페이지에는 책의 서술을 그대로 두고
  규격을 각주로 나란히 둔다.
- **이 문서가 답하지 않는 것은 끌어오지 않는다.** 조이너 팩토리 다섯 개의 선언과 계약이 범위이고,
  스코프의 수명 주기·취소 전파는 `StructuredTaskScope` 쪽 페이지의 몫이라 이 스냅샷에 없다.

## 닿은 자리

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 다섯 정책 카탈로그
- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — `awaitAll`
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — `allUntil`
- [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md) — 실패에서 접는 두 정책
