---
type: concept
title: 디자인 패턴의 해부
status: draft
description: "데이터 엔지니어링 디자인 패턴이라는 형식 자체 — 레시피 비유가 정의하는 다섯 성질(미리 정의된 템플릿·맥락화·재사용성·결과·시간 절약과 공통 어휘), GoF 23개로는 왜 부족한가, 카탈로그가 범주와 패턴의 2층으로 조직된 이유, 패턴 하나가 문제·해법·결과·예제 네 절로 쓰이는 규약, 그리고 이 책의 모든 문제 서술이 놓이는 블로그 분석 플랫폼 사례 연구와 메달리온 3계층"
generated: { by: "claude-opus-5", at: "2026-08-15T10:00:00Z" }
sources:
  - { id: konieczny2025, resource: /it/sources/konieczny2025.md }
---

# 디자인 패턴의 해부

- [패턴이란 무엇인가 — 레시피 비유](#패턴이란-무엇인가--레시피-비유)
- [데이터 엔지니어링에 옮기면](#데이터-엔지니어링에-옮기면)
- [GoF 23개로는 왜 부족한가](#gof-23개로는-왜-부족한가)
- [카탈로그가 2층인 이유](#카탈로그가-2층인-이유)
- [패턴 하나를 쓰는 네 절](#패턴-하나를-쓰는-네-절)
- [사례 연구 — 블로그 분석 플랫폼](#사례-연구--블로그-분석-플랫폼)
- [저자가 고정한 낱말 — 백필](#저자가-고정한-낱말--백필)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **"패턴"이라는 형식이 데이터 엔지니어링에서 무엇을 약속하는가.**

이 페이지는 카탈로그 안의 개별 패턴이 아니라 **패턴이라는 그릇**을 다룬다. 개별 패턴은
[데이터 엔지니어링 디자인 패턴](../synthesis/data-engineering-design-patterns.md) 허브가
나눠 놓은 페이지들에 있다.

## 패턴이란 무엇인가 — 레시피 비유

저자는 소프트웨어 쪽 디자인 패턴(design pattern)의 정의를 데이터 엔지니어링으로 옮기기
전에, 기술을 전혀 쓰지 않는 비유 하나로 정의를 세운다 — 플랑(flan) 레시피다.

- 정의 그 자체 (1장, p.1):[^konieczny2025]

  > a recipe is a great representation of what a design pattern should be: a predefined
  > and customizable template for solving a problem

- 레시피가 패턴의 다섯 성질을 전부 갖는다는 것이 논증의 본체다 (1장, pp.1–2):[^konieczny2025]
  - **미리 정의된 템플릿(predefined template)** — 재료와 준비 단계는 지시를 주되 여전히
    맞춤 가능하다. 흰 설탕 대신 흑설탕을 쓰기로 정할 수 있다.
  - **맥락화(contextualization of a design pattern)** — 같은 플랑이 친구와 나누는 디저트일
    수도, 팔아서 돈을 버는 상품일 수도 있다. **디자인 패턴은 언제나 특정 문제에 응답한다.**
  - **재사용성(reusability of the pattern)** — 매번 바퀴를 다시 발명하지 않고 먹혔던 같은
    레시피에 의존한다.
  - **결과(consequences of a pattern)** — 플랑을 매일 준비하고 먹는 것은 삶과 건강에 영향을
    미친다. 운동할 시간이 줄고 장기적으로 건강 문제가 생길 수 있다.
  - **시간 절약과 공통 사전** — 레시피는 이미 많은 사람이 시험했으므로 **시간을 절약해 주고**,
    다른 사람과 논의할 때 삶을 편하게 만드는 **공통 사전(common dictionary)** 을 도입한다.
    저자의 예시가 이 성질을 정확히 짚는다 — 플랑 레시피를 찾는 것이 그보다 덜 알려진 이름인
    캐러멜 커스터드(caramel custard) 레시피를 찾는 것보다 쉽다.
- 다섯 성질 중 **결과**가 이 책의 골격이 되는 것을 미리 봐 두면 좋다. 아래
  [패턴 하나를 쓰는 네 절](#패턴-하나를-쓰는-네-절)에서 Consequences가 독립된 절을 차지한다.

## 데이터 엔지니어링에 옮기면

저자는 같은 다섯 성질을 데드레터링(dead-lettering) 하나에 그대로 대응시킨다.

- 맥락화 — **연속 실행 중인 잡에서 반정형(semi-structured) 데이터셋을 처리해야 하고, 때때로
  완전히 무효한 형식의 레코드가 예외를 던져 잡을 멈추게 한다. 그 단순한 잘못된 형식의 레코드
  하나 때문에 잡 전체가 실패하기를 바라지는 않는다** (1장, p.2).[^konieczny2025]
- 미리 정의된 템플릿 — 처리 로직에 모범 사례 집합을 적용한다. 위험한 변환을 `try-catch`
  블록으로 감싸 나쁜 레코드를 잡아 분석용 다른 목적지에 쓰는 것이 그것이다. **이것들은 당신의
  사용 사례에 맞게 적응시킬 수 있는 규칙이다** — 예컨대 나쁜 레코드를 다른 데이터베이스로
  보내지 않고 그냥 발생 횟수만 세기로 정할 수 있다 (1장, p.2).[^konieczny2025]
- 재사용성 — 파이프라인을 깨지 않고 오류 레코드를 다루는 이 예에는 **데드레터링이라는 구체적
  이름이 있다**. 조금 다른 맥락에서 같은 문제를 다시 만나면 — 가령 ELT 파이프라인에서 변환을
  데이터 웨어하우스에서 직접 수행하는 중이라면 — **같은 로직을 적용할 수 있다** (1장,
  p.2).[^konieczny2025]
- 결과 — **하지만 데드레터 패턴을 맹목적으로 따라서는 안 된다. 매일 플랑을 먹는 것과 마찬가지로
  패턴을 구현하는 데는 알고 있어야 할 결과가 따른다. 여기서는 코드베이스에 복잡성을 더하는
  추가 로직을 더하게 되고, 그것을 받아들일 준비가 되어 있어야 한다** (1장, p.2).[^konieczny2025]
- 그래서 저자의 결론 문장 (1장, p.2):[^konieczny2025]

  > a data engineering design pattern represents a holistic picture of a solution for a
  > given problem. It then saves you time and also introduces a common language that can
  > greatly simplify discussions with your teammates or data engineers you have just met

## GoF 23개로는 왜 부족한가

- 출발점은 GoF다 — **23개의 소프트웨어 엔지니어링 디자인 패턴이 Erich Gamma 외의 *Design
  Patterns: Elements of Reusable Object-Oriented Software*(Addison-Wesley Professional,
  1994)에서 도입되었고, 책의 네 저자 때문에 구어로 Gang of Four 디자인 패턴이라 불린다**
  (1장, p.3 각주 1).[^konieczny2025]
- 저자가 스스로 던지는 질문 — 데이터 엔지니어링 프로젝트에는 그것들로 충분하지 않은가?
  **불행히도 아니다** (1장, p.3).[^konieczny2025]
- 이유는 GoF 패턴이 다루는 대상이 코드이기 때문이다 — **소프트웨어 디자인 패턴은 유지보수
  가능한 코드베이스를 지키게 해 주는 레시피다. 패턴이 주어진 개념을 표현하는 표준화된 방식이므로
  프로젝트에 새로 온 누구라도 빠르게 이해할 수 있다** (1장, p.3).[^konieczny2025] 저자가 든 예가
  싱글턴(Singleton)이다 — 불필요한 객체 할당을 피하는 패턴이고, 그것을 아는 신참은 그 목적을
  빠르게 식별한다 (1장, p.3).[^konieczny2025]
- 그리고 부족분 (1장, p.3):[^konieczny2025]

  > Besides pure software aspects, you need to think about the data aspects, such as the
  > aforementioned failure management, backfilling, idempotency, and data correctness
  > aspects.

  **이 네 낱말이 이 책이 GoF 위에 얹는 층의 목록**이다 — 실패 관리·백필·멱등성·데이터 정확성.
  실제로 오류 관리(3장)와 멱등성(4장)이 각각 장 하나를 차지한다.

## 카탈로그가 2층인 이유

- 장의 배열이 프로젝트의 시간 순서다 — **이 책은 데이터 반입으로 시작해 일상 모니터링으로
  끝나는 고전적 데이터 엔지니어링 프로젝트의 워크플로를 따른다. 프로젝트의 단계들이 주요 장들에
  대응하므로, 장 안의 각 패턴이 어느 단계에 적용되는지 쉽게 식별할 수 있다** (서문,
  p.x).[^konieczny2025]
- 그 위에 2층 구조가 얹힌다 — **추가로 각 장은 2단계 구조를 가지며, 그 단계들은 디자인 패턴
  범주(design pattern categories)와 디자인 패턴 자체다** (서문, p.x).[^konieczny2025]
- 저자가 든 두 이유 (서문, p.x):[^konieczny2025]
  - **첫째, 주어진 데이터 엔지니어링 문제는 적어도 두 개의 가능한 해법을 가질 수 있고, 이 첫
    단계의 디자인 패턴 범주 없이는 그것들을 논리적으로 묶는 것이 불가능할 것이다.**
  - **둘째, 데이터 엔지니어링 디자인 패턴은 때로 신비롭게 들리는 자기 이름을 가지며, 디자인 패턴
    범주는 세부에 파고들 것을 요구하지 않고도 특정 패턴을 어디에 적용할지 알게 해 주는 추가적
    적용 맥락을 제공한다.**
  - 두 번째 이유가 이 카탈로그를 읽는 실무적 요령이다 — **Compactor·Readiness Marker처럼
    이름만으로는 자리를 모르는 패턴**이 "데이터 컴팩션"·"데이터 준비 상태"라는 범주 아래 놓여
    비로소 어디에 쓰는지 드러난다.
- 카탈로그 전체를 한자리에서 보는 표가 책 끝에 있다 — **이 책 끝에서 서술된 모든 패턴을 요약한
  표를 찾게 될 것이다** (서문, p.xi).[^konieczny2025] (부록 "Summary of Patterns", pp.333–338)

## 패턴 하나를 쓰는 네 절

- 모든 패턴이 같은 네 절로 쓰인다 (서문, pp.x–xi):[^konieczny2025]

  | 절 | 저자가 정한 역할 |
  |---|---|
  | 문제(Problem) | 패턴을 언제 쓸 수 있는지에 대한 **실세계 예제**를 제공한다 |
  | 해법(Solution) | 패턴을 더 기술적으로 상세히 서술한다. 보통 고수준 설명으로 시작해 기술적 구현 모델이 뒤따른다 |
  | 결과(Consequences) | **패턴은 맞교환을 갖는다.** 이 절은 구현 전에 무엇을 살펴야 하는지 설명하며, 가능한 한 각 함정마다 완화 해법을 붙인다 |
  | 예제(Examples) | 현대 데이터 엔지니어링 도구 안에서 패턴을 쓰는 법을 설명하는 코드 스니펫 |

- **결과 절에 완화책을 붙인다는 규약**이 이 카탈로그와 단순 기법 목록을 가르는 지점이다.
  아래 반입 패턴 페이지들에서 실제로 결과마다 완화책이 짝지어 나온다.
- 예제 절의 범위도 저자가 미리 좁혀 둔다 — **불행히도 존재하는 모든 데이터 도구에서 패턴의
  구현을 공유하는 것은 기술적으로 가능하지 않으므로, 이 책은 인기 있는 오픈 소스 프로젝트
  (Apache Spark, Apache Flink, Apache Airflow, PostgreSQL, Delta Lake)를 쓴다. 코드
  스니펫은 Python과 SQL로 쓰였고, Python 구현이 없으면 때로 Scala나 Java로 쓰였다** (서문,
  p.xi).[^konieczny2025]
  - 그래서 이 카탈로그의 claim을 읽을 때 **해법·결과는 기술 불가지(technology-agnostic)이고
    예제만 특정 제품에 매인다**고 봐야 한다. 이 KB가 옮길 가치가 있는 것은 앞의 두 절이다.

## 사례 연구 — 블로그 분석 플랫폼

- 왜 사례가 필요한가 — **이 책의 디자인 패턴은 하나의 특정 업무 도메인에 매여 있지 않다. 그러나
  아무런 업무 맥락 없이 그것들을 이해하는 것은, 특히 경험이 적은 독자에게는 어려울 것이다. 그런
  이유로 각 패턴은 우리의 사례 연구 프로젝트인 블로그 데이터 분석 플랫폼의 맥락에서 소개된다**
  (1장, p.5).[^konieczny2025]
- 저자가 그림 1-1에서 강조한 세 부분 (1장, pp.5–6):[^konieczny2025]
  - **온라인·오프라인 반입 구성 요소** — 온라인 부분은 플랫폼에 호스팅된 블로그와 사용자가
    상호작용하며 생성하는 데이터에, 오프라인 부분(그림에서 "Data provider")은 참조
    데이터셋(referential datasets) 같은 정적 외부·내부 데이터셋에 적용된다. 오프라인 쪽은
    방문 이벤트보다 덜 정규적인 일정으로 생산된다(예: 시간에 한 번).
  - **실시간 계층** — 스트리밍 브로커에서 온 이벤트 데이터를 처리하는 스트리밍 잡이 있는 곳.
    잡은 두 유형 중 하나다. 첫째는 실시간 세션 집계처럼 이해관계자를 위한 데이터를 생성하는
    **업무 대면 잡**, 둘째는 다른 업무 사용 사례의 기술적 조력자인 **기술 잡**(예: 애드혹 질의를
    위한 정지 데이터 저장과의 데이터 동기화).
  - **데이터 조직 계층** — 메달리온(Medallion) 아키텍처 원칙에 기반한, 이제는 흔해진 데이터셋
    구조를 따른다.
- 메달리온 3계층은 이 책의 문제 서술이 반복해 참조하는 좌표다 (1장, p.6):[^konieczny2025]
  - **Bronze 계층은 데이터를 원시 형식 그대로, 손대지 않은 채, 아마도 심각한 데이터 품질 이슈를
    가진 채 저장한다.**
  - **Silver 계층은 정제되고 풍부해진(cleansed and enriched) 데이터셋을 책임진다.**
  - **Gold 계층은 데이터 마트나 참조 데이터셋처럼 최종 사용자가 기대하는 형식으로 데이터를
    노출한다.**
  - 각 계층은 다른 데이터 성숙도 수준을 나타낸다.
- 저자가 이 3계층을 고른 이유가 패턴 카탈로그의 구조와 겹친다 — **각 계층은 여기 제시된 디자인
  패턴과 정확히 똑같이 다른 데이터 성숙도 수준을 나타낸다. 업무 가치에 영향을 주는 패턴은 대개
  Gold 계층에서 데이터를 노출하고, 나머지는 Bronze나 Silver 계층에 남는다. 패턴의 문제 서술
  절은 당신이 만나는 이슈를 더 잘 이해하도록 돕기 위해 그 계층들을 참조할 수 있다** (1장,
  p.6).[^konieczny2025]
  - 메달리온의 정본은 이 책이 아니다 — 저자는 *Delta Lake: The Definitive Guide*(Denny Lee 외,
    O'Reilly, 2024) 4장으로 넘긴다 (1장, p.6 각주 3).[^konieczny2025]
- 사례 연구 도식이 구현 세부를 뺀 것도 의도다 — **스키마는 의도적으로 어떤 구현 세부도 제시하지
  않는다. 거기에 초점을 맞추면 책의 주제인 보편적 패턴 기반 해법에서 기술로 초점이 옮겨 갈 수
  있기 때문이다** (1장, p.6).[^konieczny2025]

## 저자가 고정한 낱말 — 백필

- 이 책은 **재처리(reprocessing)와 백필(backfilling)을 구분하지 않고 쓰기로 선언한다** (1장,
  p.4 각주 2):[^konieczny2025]

  > This is known as reprocessing. So as not to confuse you, from this point forward, we'll
  > refer to any task processing past data as backfilling, whether the data has already been
  > processed or not. Technically, there is a small difference between reprocessing and
  > backfilling, which you can learn about in the glossary available on GitHub.

- **이것은 사실 주장이 아니라 이 책 안에서만 유효한 낱말 규약이다.** 저자 자신이 "기술적으로는
  작은 차이가 있다"고 인정한다. 그러므로 이 소스의 "백필"을 읽을 때는 **이미 처리된 데이터를
  다시 도는 경우까지 포함**한다고 읽어야 하고, 다른 소스의 재처리 서술과 낱말이 겹쳐도 같은
  것을 가리키지 않을 수 있다. 재처리 쪽의 서술은
  [재처리와 점진적 이관](../concepts/reprocessing-and-gradual-migration.md)에 있다.

## 이어지는 페이지

- [데이터 엔지니어링 디자인 패턴](../synthesis/data-engineering-design-patterns.md) — 이
  카탈로그의 허브. 범주와 패턴이 어디에 흩어졌는지
- [배치 반입 패턴](batch-ingestion-patterns.md) — 이 카탈로그의 첫 장이 원리 서술 위에 이름을
  붙이는 실물(Full Loader·Incremental Loader)
- [재처리와 점진적 이관](../concepts/reprocessing-and-gradual-migration.md) — 저자가 "백필"로
  통일해 버린 그 구분이 살아 있는 쪽
- [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md) — 장의 배열이 따르는
  그 "고전적 프로젝트 워크플로"의 다른 이름

[^konieczny2025]: Konieczny 2025, 서문 "The Structure of This Book"(pp.x–xi) · 1장 "Introducing
Data Engineering Design Patterns"(pp.1–6). 그림 1-1(블로그 분석 플랫폼)은 도식이므로 본문이
서술한 세 부분만 옮겼다.
