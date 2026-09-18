---
type: book
title: "Mastering API Architecture: Design, Operate, and Evolve API-Based Systems"
author:
  - family: "Gough"
    given: "James"
  - family: "Bryant"
    given: "Daniel"
  - family: "Auburn"
    given: "Matthew"
issued: "2022"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-492-09063-2"
snapshot: /it/archive/gough2022/
snapshot_sha256: "df32cb351aaaa123ffbf6176a84558684f97a01b10a75a413cc99a83de87cb5b"
accessed: "2026-09-19"
---

# gough2022

제임스 고프·대니얼 브라이언트·매튜 오번의 API 아키텍처 운영서(초판 2022-10-17, 추천사 세라 웰스).
서론(사례 연구 회의 시스템·ADR·C4)과 4부 10장 — I부 API 설계·구축·테스트(1~2장), II부 API 트래픽
관리(3장 API 게이트웨이 = 인그레스, 4장 서비스 메시 = 서비스 간), III부 운영과 보안(5장 배포와
릴리스, 6장 위협 모델링, 7장 인증·인가와 OAuth2), IV부 진화적 아키텍처(8장 API 주도 재설계, 9장
클라우드 플랫폼으로의 진화, 10장 마무리).

- 이 KB에서 맡는 자리는 **API 스타일 비교층([dynowski2025](dynowski2025.md)) 위의 운영층(L2)**이다 —
  게이트웨이·메시·배포·보안의 원리와 선택 기준을 준다. 3~4장의 제품 서술(Kong, Ambassador, Istio,
  Linkerd 등)과 5장 배포 도구는 L3라 얇게 들이고 "2022년 저술 시점" 버전 조건을 단다.
- 1장의 REST·RPC 서술은 dynowski2025·fielding2022-rfc9110에 정박시키고, 2장 테스트는 newman2021 9장과
  `consumer-driven-contracts`에, 3~4장은 기존 `api-gateway-and-service-mesh`(newman2021)에, 7장은
  뉴먼의 서비스 간 인증 페이지에 교차한다. 6장 위협 모델링(STRIDE)과 OAuth2 흐름은 KB에 원전이 없던
  자리다.
- **2판은 없다**(2026-09-19 O'Reilly 카탈로그 확인 — "Second/Fourth Early Release"는 1판 얼리 릴리스
  회차). 원서만 반입했다. 한국어판은 O'Reilly AI 번역판만 확인됐고 정식 국내판은 미확인.
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 38**, 앞부속 로마자 쪽 = PDF − 2(실측).
  부 도비라에 산문이 있다(I부 p.1 실측). locator는 인쇄판 쪽으로 적는다. 텍스트 레이어 판정과 반입
  재개점의 정본은 `it/archive/gough2022/_progress.yaml`이다.
