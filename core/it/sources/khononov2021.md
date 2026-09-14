---
type: book
title: "Learning Domain-Driven Design: Aligning Software Architecture and Business Strategy"
author:
  - family: "Khononov"
    given: "Vlad"
issued: "2021"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-098-10013-1"
snapshot: /it/archive/khononov2021/
snapshot_sha256: "5f5550557e4cfb0ada1fba0ec20669a231992f61d6e9f79cb4a18fbd95e81407"
accessed: "2026-09-14"
---

# khononov2021

블라드 코노노프의 도메인 주도 설계 입문 단행본(초판 2021-10). 에반스의 원전
([evans2003](evans2003.md))이 세운 어휘 위에 **2021년 시점의 실무 층**을 얹는다 — 전략
설계(비즈니스 도메인 분석, 하위 도메인 분류, 바운디드 컨텍스트 통합 패턴), 전술 설계(트랜잭션
스크립트·액티브 레코드·도메인 모델·이벤트 소싱 도메인 모델, 아키텍처·통신 패턴), 실천(설계
휴리스틱, 설계 결정의 진화, 이벤트스토밍), 그리고 마이크로서비스·이벤트 기반 아키텍처·데이터
메시와의 관계까지 4부 16장이다. 예제 도메인은 WolfDesk(헬프데스크 SaaS).

- 이 KB에서 맡는 자리는 **원전이 아니라 종합·실무서(L2)**다. 정의는 evans2003이 갖고, 이 책은
  "2021년 실무가 그 개념을 어떻게 고르고 쓰는가"(하위 도메인 세 종류의 판별, 비즈니스 로직
  구현 패턴 넷의 선택 기준, 아키텍처 패턴과의 대응)를 준다. claim이 에반스의 정의를 재진술하면
  각주는 evans2003에도 걸어 원전에 정박시킨다.
- 14~16장은 다른 축(마이크로서비스·EDA·데이터 메시)으로 가는 다리다 — 뒤 배치의 newman2021·
  bellemare2025·기존 dehghani2022와 교차 링크한다.
- 원서만 반입했다. 한국어판 『도메인 주도 설계 첫걸음』(위키북스 2022, 김민석·오창윤 역)은
  존재하나 실물이 확보되지 않아 역어 참조원으로 쓰지 않았다.
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 26**(실측). locator는 인쇄판 쪽으로
  적는다. 텍스트 레이어 판정과 반입 재개점의 정본은 `it/archive/khononov2021/_progress.yaml`이다.
