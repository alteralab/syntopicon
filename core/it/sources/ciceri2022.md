---
type: book
title: "Software Architecture Metrics: Case Studies to Improve the Quality of Your Architecture"
author:
  - family: "Ciceri"
    given: "Christian"
  - family: "Farley"
    given: "Dave"
  - family: "Ford"
    given: "Neal"
  - family: "Harmel-Law"
    given: "Andrew"
  - family: "Keeling"
    given: "Michael"
  - family: "Lilienthal"
    given: "Carola"
  - family: "Rosa"
    given: "João"
  - family: "Weiss"
    given: "Rene"
  - family: "Woods"
    given: "Eoin"
  - family: "von Zitzewitz"
    given: "Alexander"
issued: "2022"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-098-11223-3"
snapshot: /it/archive/ciceri2022/
snapshot_sha256: "34cd5ead73ad40ab8aadf9176880d84d33410bc8bad6340d9c608c0fa3860669"
accessed: "2026-09-23"
---

# ciceri2022

열 사람이 한 장씩 쓴 아키텍처 측정 사례집(초판 첫 릴리스 2022-05-18, 판권 Apiumhub S.L.). 장마다
저자가 다르다 — 1장 네 핵심 지표를 풀어 놓기(하멜로) · 2장 적합도 함수 테스트 피라미드(바이스) ·
3장 테스트 가능성과 배포 가능성이라는 안내자(팔리) · 4장 기술 부채와 모듈성 성숙도 지수(릴리엔탈) ·
5장 프라이빗 빌드와 그 지표(치체리) · 6장 아키텍처 표류와 지표로 안내되는 의도성(로사) ·
7장 아키텍처에서 측정의 역할(우즈) · 8장 지표에서 공학으로(포드) · 9장 구조 침식과 지표 기반 피드백
고리·유지보수성 지표·리팩터링 후보를 찾는 지표(폰 치체비츠) · 10장 목표-질문-지표(GQM) 접근법(킬링).
**위 열 줄은 이 KB가 그 장에서 낸 페이지의 제목과 맞춘 것이다**(2장·3장은 "시험"이 아니라
페이지 표기인 "테스트"를 쓰고, 4·5·6·9장은 한 장이 여러 페이지로 갈렸다).
**각주는 소스 하나로 걸되 locator에 장 저자를 밝힌다**(`1장(하멜로), p.PP`) — 저자 귀속이 claim의
뜻을 바꾸는 사례집이기 때문이다. 이 책에서 난 페이지 열다섯은 자식 허브
[소프트웨어 아키텍처 지표](../synthesis/software-architecture-metrics.md)에 장 저자 단위로 모여 있다.

- 이 KB에서 맡는 자리는 **아키텍처 측정층의 원전(L2)**이다 — ford2022-evolutionary의 적합도 함수와
  DORA Four Key Metrics(forsgren2018 원전 유무 실측)의 측정 실무, 릴리엔탈 MMI·폰 치체비츠 유지보수성
  지표·킬링 GQM은 KB 첫 자리. 1장 저자가 harmellaw2024의 그 하멜로이고 8장이 ford라 두 원전과 직접
  교차한다. 5장 프라이빗 빌드는 도구 층이라 L3로 얇게.
- **편집 구조(서문 실측)** — 열 저자를 다시 모은 계기는 Global Software Architecture Summit이고,
  집필·출판 과정을 관리하고 서론을 쓴 사람은 Apiumhub의 CMO 예카테리나 노보셀체바(Ekaterina
  Novoseltseva)다(서문, pp.vii, x). 서문은 이 책을 이론이 아니라 **실천과 구현, 이미 시도되어
  통한 것**에 관한 책으로 규정하고, 엮은 동기를 **아키텍처 지표 자료의 수요는 강한데 이용할 수
  있는 것이 매우 적다**는 설문 결과로 적는다(p.vii). 독자는 **소프트웨어 아키텍트가 쓰고
  소프트웨어 아키텍트를 위해 쓴 책**으로 규정되고, **맡은 일에 따라 어떤 장이 더 관련 있게
  느껴질 수 있다**고 적어 통독을 전제하지 않는다(p.viii). **장 순서의 근거는 서문에 없다** —
  적히는 것은 서로 다른 산업과 도전에서 예를 골랐다는 것뿐이다(p.vii). 장별 저자 소속과 사례
  조직은 서문의 감사 글이 밝힌다(pp.x–xii).
- **권말 저자 소개 실측(2026-09-23 전권 감사)** — **색인(pp.189–199) 뒤에 About the Authors가
  세 쪽(pp.200–202) 있고 그 뒤가 판권 페이지(Colophon)다.** 저자 소개 세 쪽과 판권 페이지에는
  **쪽 번호가 인쇄돼 있지 않아** 위 쪽 번호는 색인 마지막 쪽과 쪽 오프셋에서 셈한 값이다.
  차례는 **표제지의 저자 목록과 같은 성 알파벳 순**이다. 소속이 밝혀지는 장 저자 열 사람은
  치체리(Apiumhub 공동 창업자, VYou 소프트웨어 아키텍처 총괄) · 팔리(회사 없이 컨설팅과
  유튜브 채널) · 포드(Thoughtworks) · 하멜로(Thoughtworks) · 킬링(Kiavi, 이전 IBM Watson
  Discovery Service) · 릴리엔탈(WPS, Workplace Solutions) · 로사(Xebia) ·
  폰 치체비츠(hello2morrow 공동 창업자이자 이사 — Sonargraph를 만든 회사) · 바이스(Finabro
  CTO) · 우즈(Endava CTO)다.
  - **감사 글(pp.x–xii)과 대조해 어긋나는 자리는 없고, 다만 감사 글이 소속을 대지 않는 저자가
    둘(킬링·바이스) 있어 그 둘의 소속은 저자 소개에서만 확인된다.** 나머지 여덟은 두 자리가
    같은 조직을 가리킨다.
  - **9장 저자의 이해관계가 저자 소개에 그대로 적혀 있다** — 그 장이 반복해 이름을 대는
    Sonargraph 제품군을 만든 회사의 공동 창업자이자 이사다. 그 사실은
    [구조 침식과 지표 기반 피드백 고리](../concepts/structural-erosion-and-metric-feedback-loops.md)가
    페이지 안에 적는다.
- 원서만 반입했다. 한국어판은 확인되지 않았다(2026-09-23). 2판 없음.
- 아카이브 스냅샷은 출판사 PDF이고 **인쇄판 쪽 = PDF 쪽 − 14**, 앞부속 로마자 쪽 = PDF − 2(실측).
  **서문은 pp.vii–xii(PDF 9–14)이고 추천사·부 구분은 없다.** locator는 인쇄판 쪽으로 적는다.
  텍스트 레이어 판정과 반입 재개점의 정본은 `it/archive/ciceri2022/_progress.yaml`이다.
