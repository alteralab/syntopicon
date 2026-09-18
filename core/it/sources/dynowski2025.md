---
type: book
title: "Learning API Styles: Understanding the Trade-Offs of Common APIs and Choosing the Correct Solutions"
author:
  - family: "Dynowski"
    given: "Lukasz"
  - family: "Dulak"
    given: "Marcin"
issued: "2025"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-098-15399-1"
snapshot: /it/archive/dynowski2025/
snapshot_sha256: "8ddd700957b300ba8e10b4fe335d1c63b8d7cc0b9348b8be1e911f6cd7e8d299"
accessed: "2026-09-18"
---

# dynowski2025

루카시 디노프스키·마르친 둘라크의 API 스타일 비교서(초판 2025-07-11, 추천사 재키 리드). 11장 —
API 개념(1장)과 API 설계 패턴(2장), 네트워크(3장)와 웹 프로토콜(4장, HTTP/1.1·2·3), 그리고
스타일 일곱: REST(5장)·GraphQL(6장)·웹 피드(7장)·gRPC(8장)·웹훅(9장)·WebSocket(10장)·메시징(11장).
각 스타일 장은 구조적 트레이드오프와 파이썬 라이브러리 예제로 짜여 있다.

- 이 KB에서 맡는 자리는 **스타일 비교층(L1/L2)**이다 — HTTP 의미론의 원전은
  [fielding2022-rfc9110](fielding2022-rfc9110.md)(허브 `http-semantics` 계열)이 갖고, 이 책은
  "같은 문제를 스타일마다 어떻게 다르게 푸는가"(요청-응답·구독·스트리밍·메시징의 선택 기준)를
  준다. 3~4장의 프로토콜 서술은 L1이되 HTTP/2·3 지원 현황은 버전 조건("2025년 저술 시점")을 단다.
  스타일 장의 라이브러리·제품 예제는 L3라 얇게 들인다.
- 메시징(11장)은 [bellemare2025](bellemare2025.md)·[hohpe2004](hohpe2004.md)와, 서비스 간 통신은
  [newman2021](newman2021.md) 4장과 교차한다. gRPC·GraphQL은 이 KB에 원전이 없거나 얇았던 자리다.
- 원서만 반입했다. 한국어판은 확인되지 않았다(2026-09-18 시점).
- **citekey는 제1저자 Dynowski를 따른다** — 계획서와 PDF 파일명이 Dulak을 앞세운 것은 서지
  오류였고 표지·O'Reilly 서지로 교정했다(2026-09-18).
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 28**, 앞부속 로마자 쪽 = PDF − 2(실측).
  locator는 인쇄판 쪽으로 적는다. 텍스트 레이어 판정과 반입 재개점의 정본은
  `it/archive/dynowski2025/_progress.yaml`이다.
