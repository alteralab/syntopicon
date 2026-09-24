---
type: book
title: "Building Multi-Tenant SaaS Architectures: Principles, Practices, and Patterns Using AWS"
author:
  - family: "Golding"
    given: "Tod"
issued: "2024"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-098-14064-9"
snapshot: /it/archive/golding2024/
snapshot_sha256: "13ce1878c6c9d1bc450ef3cddce27c0db08757a1faa51af41ef6ec09c7ebbdcd"
accessed: "2026-09-24"
---

# golding2024

토드 골딩의 멀티테넌트 SaaS 아키텍처 원전(초판 첫 릴리스 2024-04-24). 부 구분 없이 17장 — 1장 SaaS 사고방식,
2장 멀티테넌트 아키텍처 기초, 3장 배포 모델(사일로·풀), 4장 온보딩과 신원, 5장 테넌트 관리, 6장 테넌트
인증과 라우팅, 7장 멀티테넌트 서비스 구축, 8장 데이터 파티셔닝, 9장 테넌트 격리, 10장 EKS SaaS, 11장 서버리스
SaaS, 12장 테넌트 인지 운영, 13장 SaaS 이전 전략, 14장 티어링 전략, 15장 SaaS Anywhere, 16장 생성형 AI와
멀티테넌시, 17장 안내 원칙.

- 이 KB에서 맡는 자리는 **멀티테넌트 SaaS 축의 첫 원전(신설 축)**이다 — 1~3장 L1/L2(사일로·풀 배포
  모델), 4~9장 온보딩·라우팅·파티셔닝·격리 L2, **10~11장 EKS·서버리스와 16장 생성형 AI는 AWS 구현 비중이
  커 L3로 얇게**(2024년 조건), 12~15장 운영·이전·티어링 L2, 17장 원칙 L2. 테넌트 격리는 보안 축, 데이터
  파티셔닝은 ford Hard Parts 데이터 분해·kleppmann 파티셔닝과, 라우팅은 API 축과 교차한다.
- **"브리지(bridge)"라는 낱말은 이 책 전체에 0회다**(전권 `pdftotext -layout` 실측 2026-09-24) — 반입
  계획과 이 메타의 초판 산문이 3장을 "사일로·풀·브리지"라 적은 것은 오기다. 3장이 세우는 것은 사일로와
  풀 둘이고, 그 위에 풀 스택 사일로·풀 스택 풀·하이브리드 풀 스택·혼합 모드·포드라는 배포 모델이 선다.
- **저자 배경**(책 끝 "About the Author", PDF 486 실측) — 클라우드 애플리케이션 아키텍트이고 **AWS의
  글로벌 SaaS 리드**로서 SaaS 모범 관행 지침을 강연·집필·기업 자문으로 내놓아 왔다. 기술 리더·아키텍트·
  개발자로 20년 넘게 일했고 스타트업과 대형 기술 기업(AWS·eBay·Microsoft) 양쪽을 거쳤다. *Professional
  .NET Generics*의 저자이며 *Better Software* 잡지의 칼럼니스트였다. **곧 이 책의 AWS 편향은 저자의
  소속에서 온다** — 서문의 편향 곁상자와 같은 사실을 가리킨다.
- 원서만 반입했다. 한국어판은 확인되지 않았다(2026-09-24). 2판 없음.
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 26**, 앞부속 로마자 쪽 = PDF − 4(실측). 추천사
  없음, 부 도비라 없음. locator는 인쇄판 쪽으로 적는다. 텍스트 레이어 판정과 반입 재개점의 정본은
  `it/archive/golding2024/_progress.yaml`이다.
