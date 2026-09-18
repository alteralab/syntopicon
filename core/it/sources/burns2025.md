---
type: book
title: "Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Systems"
author:
  - family: "Burns"
    given: "Brendan"
issued: "2025"
edition: "2"
publisher: "O'Reilly Media"
ISBN: "978-1-098-15635-0"
snapshot: /it/archive/burns2025/
snapshot_sha256: "bdbf7b73d273766e89553c5ffd2057a8a094d34ecbd4dd00e3c9e870072ca968"
accessed: "2026-09-19"
---

# burns2025

브렌던 번스의 분산 시스템 패턴 카탈로그 2판(2판 첫 릴리스 2024-12-04, 판권 2025). 5부 16장 + 결론 —
I부 기초(1장 서론, 2장 분산 시스템 개념), II부 단일 노드 패턴(3장 사이드카, 4장 앰배서더, 5장 어댑터),
III부 서빙 패턴(6장 복제 로드 밸런스 서비스, 7장 샤딩, 8장 스캐터/개더, 9장 함수와 이벤트 기반 처리,
10장 소유권 선출), IV부 배치 계산 패턴(11장 워크 큐, 12장 이벤트 기반 배치, 13장 조율 배치), V부 보편
개념(14장 모니터링과 관측, 15장 AI 추론과 서빙, 16장 흔한 실패 패턴), 결론.

- 이 KB에서 맡는 자리는 **컨테이너 단위의 분산 시스템 패턴 카탈로그(L2)**다 — 패턴의 규정·동기·
  트레이드오프가 claim이고, 각 장의 "Hands On" 쿠버네티스 매니페스트는 L3라 얇게 들이며 "2025년
  저술 시점" 버전 조건을 단다. 15장 AI 추론 서빙은 L3(급변)라 얇게.
- **동음이의가 이 책의 본체다** — 사이드카·앰배서더·어댑터는 gough2022 4장(서비스 메시)·newman2021,
  스캐터/개더·워크 큐·발행-구독은 hohpe2004 EIP, 워크 큐는 rahman2025 자바 실행기, 이벤트 기반
  처리는 bellemare2025, 샤딩·리더 선출은 kleppmann2026, 실패 패턴은 bronson2021 준안정 실패와 같은
  이름 다른 층이다. 신설보다 **같은 낱말 다른 뜻의 분리와 상호 링크**가 반입의 중심이다.
- 원서만 반입했다. 한국어판은 확인되지 않았다(1판 한국어판도 검색 미확인, 2026-09-19).
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 18**, 앞부속 로마자 쪽 = PDF − 2(실측).
  추천사 없음. 부 도비라에 산문이 있다(I부 pp.1–2 실측). locator는 인쇄판 쪽으로 적는다. 텍스트
  레이어 판정과 반입 재개점의 정본은 `it/archive/burns2025/_progress.yaml`이다.
