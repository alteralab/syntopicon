---
type: book
title: "Architecture Patterns with Python: Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices"
author: [{family: Percival, given: Harry}, {family: Gregory, given: Bob}]
issued: "2020"
publisher: "O'Reilly Media"
ISBN: "9781492052203"
URL: "https://www.cosmicpython.com/"
snapshot: /it/archive/percival2020/
snapshot_sha256: "26ed535d312f9615fecf3fdf6d5c2cf6faf4fcb71445f3e56627571df8a950f0"
accessed: "2026-08-17"
---

# Architecture Patterns with Python

가구 소매업체 MADE.com의 재고 할당 시스템 하나를 처음부터 끝까지 만들면서, 도메인 모델을
인프라에서 떼어 내는 패턴들을 파이썬으로 구현해 보이는 책. 저자들은 이 책을 **cosmicpython**
이라 부르고 전문을 [cosmicpython.com](https://www.cosmicpython.com/)에 무료로 공개해 두었다
(URL 필드가 그것이다 — 종이책과 같은 본문이다).

이 KB에서 **코드 품질·소프트웨어 설계 축의 파이썬 구체화**다. 이 축의 원전 셋이 원리를
말한다면 —
[A Philosophy of Software Design](ousterhout2021.md)이 "무엇이 좋은 설계인가",
[Refactoring](fowler2018.md)이 "어떻게 옮기는가",
[Tidy First?](beck2023.md)가 "언제 얼마나 하는가" —
이 책은 그 원리들이 **파이썬 코드로 어떤 모양이 되는지**를 보인다. `dataclass`가 값 객체가
되고, 추상 기반 클래스나 덕 타이핑이 포트가 되며, 컨텍스트 매니저가 작업 단위가 되는 식이다.

- **책 전체가 의존성 역전 원칙(DIP)을 한 애플리케이션에 끝까지 적용한 예제**다. 저자들이
  서론에서 그렇게 규정한다 — 3층 아키텍처를 "안팎으로 뒤집는" 것이 1부의 목표이고, 그
  뒤집기의 재료가 Repository·Service Layer·Unit of Work·Aggregate 네 패턴이다.
- **패턴마다 비용을 함께 적는 것이 이 책의 형식이다.** 장마다 장단점 표가 붙고, 저자들이
  Rich Hickey를 인용해 그 이유를 밝힌다 — "프로그래머는 모든 것의 이득은 알고 절충은
  모른다". 그래서 "단순한 CRUD 앱이면 이 패턴들이 필요 없다"는 단서가 반복해서 나온다.
- **DDD 책이 아니라고 저자들이 명시한다.** Entity·Value Object·Aggregate·Repository는
  DDD 전통에서 왔지만, 이 책이 하는 것은 그 모델을 외부 제약에서 자유롭게 두는 아키텍처를
  짜는 것까지이고, 모델링 자체는 Evans의 파란 책과 Vernon의 빨간 책으로 미룬다.
- **예제 코드는 전부 파이썬 3이고 Flask·SQLAlchemy·pytest·Redis·Postgres를 쓴다.**
  장마다 GitHub 브랜치(`chapter_02_repository` 같은)가 대응하며, 본문 코드는 그 브랜치의
  발췌다. 코드가 2020년 시점의 라이브러리 API에 매여 있다 — SQLAlchemy 1.x의
  `mapper()`·`session.query()`가 그 예다.
- 원서만 반입했다 — 번역서 참조원은 쓰지 않았다.
- 아카이브 스냅샷은 **EPUB**이다. **인쇄판 쪽 앵커가 없어 locator는 장 단위**다 —
  검증 절차와 근거는 `it/archive/percival2020/_progress.yaml` 머리말이 정본이다.
- 본문의 그림(Figure)은 대부분 이미지로 조판된 구성도·시퀀스도이므로 산문 서술로만 옮겼다.
  다만 여러 그림이 원본 ditaa·plantuml 소스를 본문에 함께 담고 있어 구조 판독은 가능했다.
- 반입 재개점의 정본은 `it/archive/percival2020/_progress.yaml`이다.
