---
type: book
title: "Building Event-Driven Microservices: Leveraging Organizational Data at Scale"
author:
  - family: "Bellemare"
    given: "Adam"
issued: "2025"
edition: "2"
publisher: "O'Reilly Media"
ISBN: "978-1-098-15987-0"
snapshot: /it/archive/bellemare2025/
snapshot_sha256: "0ca30d627f98ab4a83ed63378571ef9cfb14d151d6ee674e4e77abf9f8481754"
accessed: "2026-09-18"
---

# bellemare2025

애덤 벨마어의 이벤트 기반 마이크로서비스 구축 2판(2025-09, 초판 2020-08). 4부 22장: I부 서론(왜
이벤트 기반인가·이벤트와 이벤트 스트림의 기초·이벤트 기반 마이크로서비스의 기초), II부 이벤트와
이벤트 스트림(스키마와 데이터 계약·이벤트 설계·기존 시스템과의 통합·비정규화와 이벤트화·상태
있는 마이크로서비스·결정적 스트림 처리·워크플로), III부 프레임워크(기본 프로듀서/컨슈머·중량·경량·
스트리밍 SQL·FaaS), IV부 정합성·불량 데이터·도구(최종 일관성·요청-응답과의 통합·불량 데이터·
지원 도구·테스트·배포·결론).

- 이 KB에서 맡는 자리는 **Kafka를 서비스 간 통합 기반으로 보는 틀의 첫 소스(L2)**다. 2026-09 실측에서
  KB의 Kafka 페이지(shapira2021·kafka2025-kraft)는 전부 내부·운영 시각이었고 "서비스 통합 기반"
  시각은 0건이었다. 정박점: [shapira2021](shapira2021.md)(Kafka 원리), [kleppmann2026](kleppmann2026.md)
  (로그·파생 데이터·이벤트 소싱), [khononov2021](khononov2021.md) 15장(EDA)·9장(아웃박스·사가),
  [newman2021](newman2021.md) 4장(통신 스타일), [ford2021-hard-parts](ford2021-hard-parts.md) 12장
  (사가 8패턴), [hohpe2004](hohpe2004.md)(메시징 패턴), [evans2003](evans2003.md)(바운디드 컨텍스트).
- 층: 1~3장 L1/L2(이벤트·스트림의 기초) · 4~10장 L2(설계·상태·결정성·워크플로) · **11~15장 프레임워크
  (경량·중량·스트리밍 SQL·FaaS)는 L3 — 얇게, 버전 조건** · 16~18장 L2 · **19~21장 도구·테스트·배포 L3**
  (얇게) · 22장 L2. 2025년판이라 이 배치에서 가장 신선하다.
- 원서만 반입했다. 한국어판은 **1판 번역**(『이벤트 기반 마이크로서비스 구축』 한빛미디어 2021, 이일웅 역)
  뿐이라 판이 어긋난다 — kleppmann2026 선례대로 역어 참조원으로 쓰지 않는다.
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 24**(실측). locator는 인쇄판 쪽으로
  적는다. 텍스트 레이어 판정과 반입 재개점의 정본은 `it/archive/bellemare2025/_progress.yaml`이다.
