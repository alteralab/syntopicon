---
type: book
title: "Domain-Driven Design: Tackling Complexity in the Heart of Software"
author: [{family: Evans, given: Eric}]
issued: "2003"
publisher: "Addison-Wesley"
ISBN: "9780321125217"
snapshot: /it/archive/evans2003/
snapshot_sha256: "61abfb217a45f88190f7552fc67ee3d07f2d5de7757713832a9db38da97e8ac6"
accessed: "2026-08-18"
---

# Domain-Driven Design

도메인 주도 설계라는 이름이 나온 책이고, 이 KB에서 **도메인 모델을 다루는 어휘의 원전**이다.
Entity·Value Object·Aggregate·Repository·Ubiquitous Language·Bounded Context가 전부 여기서
정의된다. 업계에서 "파란 책"(the blue book)이라 부른다.

이 KB의 코드 품질 축에서 이 소스가 맡는 자리는 좁고 분명하다 — **코드의 이름이 무엇을 담아야
하는가**에 대한 원전 근거다. 다른 원전들이 이름을 읽기 쉬움
([A Philosophy of Software Design](ousterhout2021.md))이나 팀 어휘
([The Pragmatic Programmer](thomas2020.md))의 문제로 다룬다면, 이 책은 이름을 **모델의 일부**로
놓는다. 이름을 바꾸는 것이 모델을 바꾸는 것이고, 그래서 이름이 틀리면 설계가 틀린 것이 된다.

- **패턴 책의 형식을 따른다.** 각 패턴이 문제 서술 → `Therefore:` → 처방 → `❊ ❊ ❊` →
  후속 논의로 구성되고, 처방 문단이 그 패턴의 정의다. 이 KB의 직인용은 대부분 그 문단에서
  왔다.
- **패턴 이름을 본문에서 작은 대문자로 조판한다**(UBIQUITOUS LANGUAGE, BOUNDED CONTEXT).
  직인용에서 이 표기를 유지했다 — 저자가 "이것은 이름 붙은 패턴이다"를 표시하는 장치이고,
  대소문자를 뭉개면 일반 명사와 구분이 사라진다.
- **예제 도메인이 둘이다.** 화물 운송(Cargo·Itinerary·Route Specification)이 책 전체를
  관통하고, 인쇄 회로 기판(PCB) 설계가 1·3장의 지식 정련 사례로 쓰인다.
- **코드는 Java이고 2003년 시점의 것이다.** 패턴은 언어와 무관하지만 예제의 관용은 낡았다
  (`Set` 원시 타입 사용, JUnit 3 스타일). 이 KB는 예제 코드를 펜스로 옮길 때 그 사실을
  각주에 적었다.
- **판형은 2015년 21쇄**(Twenty-First printing, July 2015)이고 본문은 2003년 초판 그대로다.
  판권장에 저작권 연도가 2004로 인쇄돼 있으나 표제지·ISBN·의회도서관 서지는 2003이므로
  `issued`는 2003으로 발급했다.
- 원서만 반입했다 — 번역서 참조원은 쓰지 않았다.
- 아카이브 스냅샷은 PDF이고 **인쇄판 쪽 = PDF 쪽 − 33**이다(실측). locator는 인쇄판 쪽으로
  적는다. 텍스트 레이어 판정과 반입 재개점의 정본은
  `it/archive/evans2003/_progress.yaml`이다.
