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
**전권 반입 완료(2026-09-19, 아홉 런).**

- 이 KB에서 맡는 자리는 **스타일 비교층(L1/L2)**이다 — HTTP 의미론의 원전은
  [fielding2022-rfc9110](fielding2022-rfc9110.md)(허브 `http-semantics` 계열)이 갖고, 이 책은
  "같은 문제를 스타일마다 어떻게 다르게 푸는가"(요청-응답·구독·스트리밍·콜백·양방향·메시징의
  선택 기준)를 준다. 3~4장의 프로토콜 서술은 L1이되 HTTP/2·3 지원 현황은 버전 조건("2025년 저술
  시점")을 단다. 스타일 장의 라이브러리·제품 예제는 L3라 얇게 들였다.
- **이 책이 이 KB에 혼자 갖고 온 자리가 다섯이다** — gRPC와 프로토버프 계약, 웹 피드(RSS·Atom),
  웹훅과 콜백, WebSocket 프로토콜, 그리고 RabbitMQ와 AMQP다. 다섯 다 반입 전에는 다른 소스의
  예시로만 이름이 들어와 있었다. 반대로 **이 책이 얇게만 더한 자리**는 REST와 GraphQL과 메시징
  패턴이다 — 그쪽은 [fielding2022-rfc9110](fielding2022-rfc9110.md)·[hohpe2004](hohpe2004.md)·
  [bellemare2025](bellemare2025.md)·[shapira2021](shapira2021.md)·[kleppmann2026](kleppmann2026.md)이
  이미 두껍고, 이 책의 몫은 그 위에 **스타일 하나씩의 경계와 절충**을 얹는 것이었다.
- **긴장은 모순으로 세우지 않았다.** 아홉 런에서 `contradicts` 쌍을 하나도 만들지 않았고, 대신
  같은 낱말이 다른 대상을 가리키는 자리들을 각 페이지 안의 대조로 적었다 — "스타일"이 이 KB에서
  최소 셋을 가리킨다는 것(1장), "스트림"이 넷을 가리킨다는 것(10장), "채널"이 RabbitMQ와
  AsyncAPI와 Redis에서 각각 다르다는 것(10·11장), 결합의 규정이 2004년 카탈로그와 다른 층이라는
  것(11장), 그리고 전달 보증 칸이 확인 응답 설정의 함수라는 것(11장)이다.
- **코드 펜스는 전권에서 하나만 썼다** — 8장 예제 8-8(.proto 서비스 정의)이다. 나머지 예제는
  파이썬·장고·Starlette·pika·도커에 매인 구현과 실행 기록이라, 예제에 번호로 붙은 설명을 claim으로
  옮기고 코드는 옮기지 않았다. **원문에 표가 없던 자리에 이 KB가 만든 표**는 아홉
  페이지에 있고 전부 표 아래나 각주에 선언되어 있다.
- 원서만 반입했다. 한국어판은 확인되지 않았다(2026-09-18 시점).
- **citekey는 제1저자 Dynowski를 따른다** — 계획서와 PDF 파일명이 Dulak을 앞세운 것은 서지
  오류였고 표지·O'Reilly 서지로 교정했다(2026-09-18).
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 28**, 앞부속 로마자 쪽 = PDF − 2(실측).
  locator는 인쇄판 쪽으로 적는다. 텍스트 레이어 판정과 반입 재개점의 정본은
  `it/archive/dynowski2025/_progress.yaml`이고, 런별 리뷰 브리프는
  `it/archive/dynowski2025/_review-briefs/`다. **승급 후 사람이 결정할 것의 정본은 그 가운데
  `review-dynowski2025-09.md` 말미의 목록**이다.
