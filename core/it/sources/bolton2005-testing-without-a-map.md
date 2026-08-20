---
type: article-journal
title: "Testing Without a Map"
author: [{family: Bolton, given: Michael}]
issued: "2005-01"
container-title: "Better Software"
page: "25-28"
URL: "http://www.developsense.com/articles/2005-01-TestingWithoutAMap.pdf"
snapshot: /it/archive/bolton2005-testing-without-a-map/
snapshot_sha256: "1604c493c08255ded8c43dabd71539f36720828d3475c7f3e2379596aee2f27c"
accessed: "2026-08-21"
---

# Testing Without a Map

**HICCUPPS 니모닉이 활자로 처음 나온 자리.** 잡지 기사이고, 논지는 부제가 그대로
말한다 — *"You don't always need to wait for complete specifications to start your
testing effort."* 명세 없이 오라클을 어디서 구하는가를 여덟 항목의 일관성 목록으로
답하고, 그 목록을 Nero Cover Designer 실사용 5분에 적용해 버그를 짚어 나가는
사례로 이어진다.

**근거 등급은 실무 휴리스틱(practitioner)이다.** 측정도 실험도 없고, 저자가
스스로 지위를 규정한다 — *"Remember: Heuristics are guidelines, not edicts; they're
fallible. They aren't universal—there are plenty of other ways by which we can decide
whether a product is acceptable or unacceptable."*(인쇄 26쪽)

**서지가 문면으로 확인되는 범위.** 표제지(인쇄 25쪽)에 제목 `Testing Without a
Map`과 책임 표시 `BY MICHAEL BOLTON`이 인쇄돼 있고, 쪽바닥에
`www.stickyminds.com  JANUARY 2005  BETTER SOFTWARE  25`가 있다. **권·호는 확보본
문면에 인쇄돼 있지 않다** — 그래서 `volume`·`issue`를 적지 않았다. `page`는
쪽바닥에 실인쇄된 폴리오 25·26·27·28이다.

- **PDF 쪽과 인쇄 쪽이 어긋난다.** PDF 1쪽은 폴리오 없는 전면 일러스트(기사 표제면의
  마주 쪽)이고, PDF 2–5쪽이 인쇄 25–28쪽이다. 인용 locator는 **인쇄 쪽**으로 적는다.
- **snapshot.py 판정은 `mixed`**(신뢰도 0.74, OCR 필요 1/5쪽)다. OCR이 필요한 1쪽은
  본문이 없는 일러스트 면이고, 본문 네 쪽은 텍스트 레이어가 살아 있다. 그럼에도 이
  소스의 직인용은 **쪽 이미지 육안 대조를 거친 것만** 쓴다(인쇄 25·26쪽 대조 완료).
- **다단 조판이라 기계 추출이 단을 섞는다.** 인쇄 28쪽은 세 단이 문장 중간에서 서로
  끼어든 채로 추출된다. 그 쪽을 인용하려면 이미지 판독이 필수다.
- **저자 약력이 소속을 밝힌다**(인쇄 28쪽) — *"Michael Bolton lives in Toronto and
  teaches heuristics and exploratory testing … as part of James Bach's Rapid Software
  Testing course."* 목록의 출처(Bach)와 필자의 관계가 문면에 있는 자리다.
- 후속판은 [FEW HICCUPPS](bolton2012-few-hiccupps.md)이고, 그쪽이 이 기사를 이름으로
  지목하며 계보를 잇는다.
