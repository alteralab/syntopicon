---
type: book
title: "Modern Concurrency in Java: Virtual Threads, Structured Concurrency, and Beyond"
author:
  - family: "Rahman"
    given: "A N M Bazlur"
issued: "2025"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-098-16541-3"
snapshot: /it/archive/rahman2025/
snapshot_sha256: "3c50e9238f70f933fb2bb4a84cdd24443d4b588283b71ca7fa4cc69c8bbb23ed"
accessed: "2026-09-05"
---

# rahman2025

바즐루르 라만의 모던 자바 동시성 — JDK 21에서 정식이 된 가상 스레드(virtual threads)와
그 위에 세운 구조적 동시성(structured concurrency)·스코프 값(scoped values)을 다루는 단행본
(초판 2025-09). 스레드 비용과 실행자 프레임워크에서 출발해 가상 스레드의 내부·핀닝·
모니터링, 스레드 풀·CompletableFuture의 역학, StructuredTaskScope와 Joiner, 리액티브 자바의
위치, 가상 스레드를 쓰는 프레임워크 순.

기준 JDK: 저자는 머리말(p.xi)에서 이 책의 예제와 개념이 최소 JDK 21을 요구한다고 밝힌다 —
가상 스레드가 정식으로 쓸 수 있게 된 릴리스이기 때문이다. 미리 보기 상태이거나 최근 확정된 기능을
다루는 장이 있어 24나 25 같은 더 새 JDK를 쓰면 예제와 논의를 최대로 활용할 수 있다고 덧붙이며,
구조적 동시성은 집필 시점에 여전히 미리 보기라고 명기한다(4장 소개, p.xii).

참조원: 한국어판 『모던 자바 동시성 프로그래밍』(온리북, 2026)을 아카이브에 동봉했다 —
역어 참조용이며 소스 메타는 원서에만 건다. 한국어판 PDF는 ABBYY FineReader OCR 레이어를
얹은 300dpi 스캔본이라 기계 추출이 아니라 시각 판독으로 읽는다.

KB 안의 자리: 가상 머신이 하는 일까지만 다루는 [자바 메모리 모델과 동시성](../synthesis/java-memory-model-and-concurrency.md)(zhou2024)이 비워 둔 `java.util.concurrent`
이후의 라이브러리·API 층을 이 소스가 채운다.
