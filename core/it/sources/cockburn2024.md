---
type: book
title: "Hexagonal Architecture Explained: How the Ports & Adapters architecture simplifies your life, and how to implement it"
author:
  - family: "Cockburn"
    given: "Alistair"
  - family: "Garrido de Paz"
    given: "Juan Manuel"
issued: "2024"
edition: "1"
publisher: "Humans and Technology Press"
ISBN: "979-8-9985862-0-0"
snapshot: /it/archive/cockburn2024/
snapshot_sha256: "db3ec5562a2634e3d78471065ae3a7e0e1903e57ee3e1fc3225e2ffbd2b981c8"
accessed: "2026-09-25"
---

# cockburn2024

앨리스터 콕번이 후안 마누엘 가리도 데 파스와 함께 쓴 헥사고날(포트와 어댑터) 아키텍처의 **원전**
(초판 2024, 이 스냅샷은 갱신 1판 EPUB v1.1b 2025-04-20). 콕번이 2005년에 만들어 "포트와
어댑터"로 고쳐 부른 그 패턴을, 저자 자신이 규정·어휘·사례·FAQ·원문 재수록으로 정리한다. 7장 —
1장 서론(역사·이름의 유래·비용과 편익), 2장 규정(용어집, 요소 App·포트·액터·어댑터, 다섯째 요소
Configurator, 필수/선택/패턴 밖), 3장 코드 사례(세금 계산기·web-hexagon·BlueZone), 4장 FAQ 무엇을
어떻게(포트란 무엇인가·앱 경계·포트 수·앱 내부/어댑터 구조·개발 순서), 5장 FAQ 관련 개념(유스케이스·
워킹 스켈레톤·대칭/비대칭·시험 스위트의 자리·계층/양파/클린/헥사고날의 차이·DDD·부패 방지 계층·
중첩 헥사곤·CQRS), 6장 원문 재수록(2005년 원문·2023년 주석·후속 두 편), 7장 요약.

- 이 KB에서 맡는 자리는 **헥사고날의 원전(L1)**이다 — 지금까지 이 KB는 이 패턴을
  percival2020(파이썬 구현)·khononov2021(DDD 입문서의 8장 규정)을 경유한 2차 서술로만 가졌고,
  스물여섯 페이지가 그 자리를 비운 채 남을 인용했다([[dependency-inversion-principle]] 참조).
  이 책이 그 원전을 채운다. claim이 percival·khononov의 규정을 재진술하면 각주를 그쪽에도 걸어
  2차 서술과 원전을 잇는다.
- **핵심 대질**: khononov는 "헥사고날·양파·클린이 같은 패턴, 이름만 다르다"고 했으나, 콕번은
  5.5절에서 **포트와 어댑터가 계층·양파·클린과 두 가지로 다르다**고 못 박는다(두 층뿐·외부 액터를
  특정 포트에 묶는 요구). 원전과 2차 서술의 이 갈림이 반입의 값어치다.
- 원서만 반입했다. 한국어판은 확인되지 않았다(2026-09-25) — yes24의 국내 상품은 원서 POD 수입판이다.
- 아카이브 스냅샷은 **EPUB**(PDF 판 없음, Calibre 변환본)이다. **인쇄판 쪽 앵커가 없어 locator는
  장·절 번호 단위**(`N장 §"X.Y. 절 제목"`) — percival2020·strengholt2025 선례. 텍스트 레이어 판정과
  반입 재개점의 정본은 `it/archive/cockburn2024/_progress.yaml`이다.
