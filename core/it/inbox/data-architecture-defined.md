---
type: concept
title: 데이터 아키텍처의 정의
status: draft
description: "데이터 아키텍처를 무엇이라 정의하며 무엇이 그것을 '좋다'고 만드는가 — 엔터프라이즈 아키텍처의 부분집합이라는 위치, TOGAF·Gartner·EABOK·DAMA의 정의와 저자들의 정의, 유연하고 되돌릴 수 있는 결정과 일방통행문·양방향문, 변경 관리, 운영 아키텍처와 기술 아키텍처의 분업, 그리고 나쁜 아키텍처의 형태"
generated: { by: "claude-opus-5", at: "2026-08-15T18:00:00Z" }
sources:
  - { id: reis2022, resource: /it/sources/reis2022.md }
---

# 데이터 아키텍처의 정의

- [엔터프라이즈 아키텍처라는 상위 범주](#엔터프라이즈-아키텍처라는-상위-범주)
- [세 기관의 정의](#세-기관의-정의)
- [저자들의 정의 — 유연하고 되돌릴 수 있는 결정](#저자들의-정의--유연하고-되돌릴-수-있는-결정)
- [일방통행문과 양방향문](#일방통행문과-양방향문)
- [변경 관리](#변경-관리)
- [기술은 업무 목표를 위해 존재한다](#기술은-업무-목표를-위해-존재한다)
- [데이터 아키텍처의 정의](#데이터-아키텍처의-정의-1)
- [운영 아키텍처와 기술 아키텍처](#운영-아키텍처와-기술-아키텍처)
- ["좋은" 데이터 아키텍처](#좋은-데이터-아키텍처)
- [누가 설계하는가](#누가-설계하는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **데이터 아키텍처(data architecture)를 무엇이라 정의해야 설계 결정으로
옮길 수 있고, 무엇이 그것을 "좋다"고 만드는가.**

## 엔터프라이즈 아키텍처라는 상위 범주

- 왜 정의부터 시작하는가 — **데이터 아키텍처를 파헤치기 시작하면 주제가 다소 흐릿해진다.
  데이터 아키텍처를 연구하면 일관성 없고 흔히 낡은 정의가 많이 나온다. 1장에서 데이터
  엔지니어링을 정의했을 때와 비슷하다 — 합의가 없다. 끊임없이 바뀌는 분야에서 이는 예상할
  만한 일이다** (3장, p.71).[^reis2022]
- 위치 — **엔터프라이즈 아키텍처(enterprise architecture)는 업무·기술·애플리케이션·데이터를
  포함한 여러 부분집합을 갖는다. 그런 만큼 많은 프레임워크와 자료가 엔터프라이즈 아키텍처에
  바쳐져 있다. 사실 아키텍처는 놀랄 만큼 논쟁적인 주제다** (3장, p.72).[^reis2022]
  - 그림 3-1이 말하는 포함 관계는 **데이터 아키텍처가 엔터프라이즈 아키텍처의 부분집합**이라는
    것이다 (3장, p.72).[^reis2022]
- 낱말에 붙은 반응까지 저자들이 인정한다 — **엔터프라이즈라는 용어는 엇갈린 반응을 얻는다.
  삭막한 기업 사무실, 명령-통제식 폭포수 계획, 정체된 기업 문화, 공허한 캐치프레이즈를
  떠올리게 한다. 그럼에도 우리는 여기서 몇 가지를 배울 수 있다** (3장, p.72).[^reis2022]

## 세 기관의 정의

저자들은 정의를 짓기 전에 TOGAF·Gartner·EABOK 셋을 나란히 놓는다 (3장,
pp.72–73).[^reis2022] 왜곡을 피하려 원문을 직인용한다.

- **TOGAF**(The Open Group Architecture Framework) — **오늘날 가장 널리 쓰이는 아키텍처
  프레임워크로 선전된다** (3장, p.72).[^reis2022]

> The term "enterprise" in the context of "enterprise architecture" can denote an entire
> enterprise—encompassing all of its information and technology services, processes,
> and infrastructure—or a specific domain within the enterprise. In both cases, the
> architecture crosses multiple systems, and multiple functional groups within the
> enterprise.

- **Gartner** — **엔터프라이즈 관련 추세를 다루는 연구 기사와 리포트를 내는 글로벌 리서치·자문
  회사이고, 무엇보다 그 (악)명 높은 Gartner 하이프 사이클을 책임지고 있다** (3장,
  p.72).[^reis2022]

> Enterprise architecture (EA) is a discipline for proactively and holistically leading
> enterprise responses to disruptive forces by identifying and analyzing the execution of
> change toward desired business vision and outcomes. EA delivers value by presenting
> business and IT leaders with signature-ready recommendations for adjusting policies
> and projects to achieve targeted business outcomes that capitalize on relevant business
> disruptions.

- **EABOK**(Enterprise Architecture Book of Knowledge) — **MITRE Corporation이 만든
  엔터프라이즈 아키텍처 참고서다. 2004년에 미완성 초안으로 나온 뒤 갱신되지 않았다. 겉보기에
  낡았음에도 엔터프라이즈 아키텍처를 서술할 때 자주 참조되며, 저자들은 이 책을 쓰는 동안 그
  발상 다수가 도움이 됐다고 적는다** (3장, p.73).[^reis2022]

> Enterprise Architecture (EA) is an organizational model; an abstract representation of
> an Enterprise that aligns strategy, operations, and technology to create a roadmap for
> success.

## 저자들의 정의 — 유연하고 되돌릴 수 있는 결정

- 공통 실을 뽑는다 — **이 정의들에서 몇 가지 공통 갈래를 추출한다: 변화(change)·정렬
  (alignment)·조직(organization)·문제 해결(problem-solving)·기회(opportunities)·이주
  (migration)** (3장, p.73).[^reis2022]
- 저자들의 엔터프라이즈 아키텍처 정의 — 오늘날의 빠르게 움직이는 데이터 지형에 더 적합하다고
  느끼는 쪽이다 (3장, p.73):[^reis2022]

> Enterprise architecture is the design of systems to support *change in the enterprise*,
> achieved by *flexible and reversible decisions* reached through careful *evaluation of
> trade-offs*.

- 유연하고 되돌릴 수 있는 결정이 필수인 두 이유 (3장, p.73):[^reis2022]
  - **첫째, 세계는 끊임없이 변하고 미래를 예측하는 것은 불가능하다. 되돌릴 수 있는 결정은
    세계가 변하고 새 정보를 모으는 동안 진로를 조정하게 해 준다.**
  - **둘째, 조직이 커지면서 엔터프라이즈가 경화(ossification)되는 자연스러운 경향이 있다.
    되돌릴 수 있는 결정의 문화를 채택하는 것은 결정에 붙은 위험을 줄여 이 경향을 이겨 내도록
    돕는다.**

## 일방통행문과 양방향문

- 비유의 출처 — **제프 베조스가 일방통행문(one-way door)과 양방향문(two-way door)의 발상을
  낸 것으로 알려져 있다** (3장, p.73).[^reis2022]
- **일방통행문은 되돌리기가 거의 불가능한 결정이다. 예컨대 아마존은 AWS를 팔거나 닫기로
  결정할 수 있었다. 그런 조치 뒤에 같은 시장 지위를 가진 퍼블릭 클라우드를 아마존이 다시
  세우기란 거의 불가능할 것이다** (3장, pp.73–74).[^reis2022]
- **양방향문은 쉽게 되돌릴 수 있는 결정이다 — 문을 통과해 지나가서 방 안에서 본 것이 마음에
  들면 계속 가고, 아니면 문을 도로 나와 물러선다. 아마존이 새 마이크로서비스 데이터베이스에
  DynamoDB 사용을 요구하기로 정했다고 하자. 이 정책이 통하지 않으면 아마존에는 그것을 되돌리고
  일부 서비스를 다른 데이터베이스를 쓰도록 리팩터링할 선택지가 있다. 되돌릴 수 있는 결정(양방향문)
  각각에 붙은 판돈이 낮으므로 조직은 더 많은 결정을 내리고, 반복하고, 개선하고, 데이터를 빠르게
  모을 수 있다** (3장, p.74).[^reis2022]

## 변경 관리

- **변경 관리(change management)는 되돌릴 수 있는 결정과 밀접히 관련되며 엔터프라이즈 아키텍처
  프레임워크의 중심 주제다. 되돌릴 수 있는 결정을 강조하더라도 엔터프라이즈는 흔히 큰 이니셔티브를
  수행할 필요가 있다. 그것들은 이상적으로 더 작은 변경으로 쪼개지고, 각각이 그 자체로 되돌릴 수
  있는 결정이다** (3장, p.74).[^reis2022]
- 실물 — **아마존으로 돌아가면, DynamoDB 개념에 대한 논문 발표에서 베르너 포겔스가 AWS의
  DynamoDB 서비스를 발표하기까지 5년(2007–2012)의 간격이 있었다. 무대 뒤에서 팀들은 DynamoDB를
  AWS 고객에게 구체적 현실로 만들기 위해 수많은 작은 조치를 취했다. 그런 작은 조치들을 관리하는
  것이 변경 관리의 핵심에 있다** (3장, p.74).[^reis2022]

## 기술은 업무 목표를 위해 존재한다

- 아키텍트의 일 — **아키텍트는 단순히 IT 프로세스를 그려 내고 먼 유토피아적 미래를 막연히
  바라보는 사람이 아니다. 그들은 업무 문제를 능동적으로 풀고 새 기회를 만든다. 아키텍트는
  현재 상태의 문제(부실한 데이터 품질·확장성 한계·손실을 내는 사업 부문)를 식별하고, 원하는
  미래 상태(애자일한 데이터 품질 개선·확장 가능한 클라우드 데이터 솔루션·개선된 업무 프로세스)를
  정의하고, 작고 구체적인 단계의 실행을 통해 이니셔티브를 실현한다** (3장, p.74).[^reis2022]
  - 저자들이 반복할 값어치가 있다며 따로 떼어 놓은 한 줄이다 (3장, p.74):[^reis2022]

> Technical solutions exist not for their own sake but in support of business goals.

- 트레이드오프에는 물리적 바닥이 있다 — **소프트웨어와 데이터의 상대적으로 유동적인 성질은
  때때로 우리가 차갑고 단단한 물리 세계의 엔지니어가 마주하는 제약에서 자유롭다고 믿게 만든다.
  실제로 이는 부분적으로 참이다 — 소프트웨어 버그를 패치하는 것은 비행기 날개를 다시 설계하고
  교체하는 것보다 훨씬 쉽다. 그러나 디지털 시스템도 결국 지연 시간·신뢰성·밀도·에너지 소비 같은
  물리적 한계에 제약된다. 엔지니어는 프로그래밍 언어와 프레임워크의 특성, 복잡성·예산 관리의 실무적
  제약 같은 다양한 비기능적 한계에도 부딪힌다. 마법적 사고는 부실한 엔지니어링으로 귀결된다.
  데이터 엔지니어는 고금리 기술 부채를 최소화하면서 최적의 시스템을 설계하기 위해 모든 단계에서
  트레이드오프를 계산에 넣어야 한다** (3장, p.74).[^reis2022]
- 균형은 계속 다시 잡는다 — **엔터프라이즈 아키텍처는 유연성과 트레이드오프의 균형을 잡는다.
  이는 늘 쉬운 균형이 아니며, 아키텍트는 세계가 동적이라는 인식 아래 끊임없이 평가하고 재평가해야
  한다. 엔터프라이즈가 마주한 변화의 속도를 고려하면 조직은 — 그리고 그 아키텍처는 — 가만히 서
  있을 여유가 없다** (3장, p.75).[^reis2022]

## 데이터 아키텍처의 정의

- 상속 관계 — **데이터 아키텍처는 엔터프라이즈 아키텍처의 부분집합으로서 그 속성을 물려받는다:
  프로세스·전략·변경 관리·트레이드오프 평가** (3장, p.75).[^reis2022]
- **TOGAF의 데이터 아키텍처 정의** (3장, p.75):[^reis2022]

> A description of the structure and interaction of the enterprise's major types and sources
> of data, logical data assets, physical data assets, and data management resources.

- **DAMA DMBOK의 정의** (3장, p.75):[^reis2022]

> Identifying the data needs of the enterprise (regardless of structure) and designing and
> maintaining the master blueprints to meet those needs. Using master blueprints to
> guide data integration, control data assets, and align data investments with business
> strategy.

- **저자들의 정의** (3장, p.75):[^reis2022]

> Data architecture is the design of systems to support the evolving data needs of an
> enterprise, achieved by flexible and reversible decisions reached through a careful
> evaluation of trade-offs.

- 수명 주기와의 층위 관계 — **데이터 엔지니어링 수명 주기가 데이터 수명 주기의 부분집합인 것과
  꼭 같이, 데이터 엔지니어링 아키텍처(data engineering architecture)는 일반 데이터 아키텍처의
  부분집합이다. 데이터 엔지니어링 아키텍처는 데이터 엔지니어링 수명 주기의 핵심 절들을 이루는
  시스템과 프레임워크다. 이 책 전체에서 데이터 아키텍처와 데이터 엔지니어링 아키텍처를 서로
  바꿔 쓴다** (3장, pp.75–76).[^reis2022] 그 수명 주기는
  [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md)에 있다.

## 운영 아키텍처와 기술 아키텍처

- **운영 아키텍처(operational architecture)는 사람·프로세스·기술에 관련해 무엇이 일어나야 하는지의
  기능적 요구사항을 아우른다. 예컨대 데이터가 어떤 업무 프로세스를 섬기는가? 조직이 데이터 품질을
  어떻게 관리하는가? 데이터가 생산된 시점부터 질의 가능해지기까지의 지연 시간 요구는 무엇인가?**
  (3장, p.76).[^reis2022]
- **기술 아키텍처(technical architecture)는 데이터 엔지니어링 수명 주기를 따라 데이터가 어떻게
  반입·저장·변환·서빙되는지를 서술한다. 예컨대 시간당 10TB의 데이터를 원천 데이터베이스에서 데이터
  레이크로 어떻게 옮길 것인가?** (3장, p.76).[^reis2022]
- 한 줄로 가른다 — **요컨대 운영 아키텍처는 무엇(what)이 이뤄져야 하는지를 서술하고, 기술
  아키텍처는 그것이 어떻게(how) 일어날지를 상세화한다** (3장, p.76).[^reis2022]

## "좋은" 데이터 아키텍처

- 저자들이 여는 인용 (3장, p.76):[^reis2022]

> Never shoot for the best architecture, but rather the least worst architecture.
> —Mark Richards and Neal Ford

- Booch의 정의 — **"아키텍처는 시스템을 형성하는 유의한 설계 결정을 나타내며, 여기서 유의함은
  변경 비용으로 측정된다."** 데이터 아키텍트는 기본 수준에서 좋은 아키텍처로 이어질 유의한
  결정을 내리는 것을 목표로 한다 (3장, p.76).[^reis2022]
- **좋은 데이터 아키텍처는 공통되고 널리 재사용 가능한 구성 요소 집합으로 업무 요구사항을
  섬기면서 유연성을 유지하고 적절한 트레이드오프를 만든다. 나쁜 아키텍처는 권위주의적이고
  만능(one-size-fits-all) 결정 한 뭉치를 큰 진흙 공(big ball of mud)에 욱여넣으려 한다**
  (3장, p.76).[^reis2022]
- 토대는 애자일성이다 — **애자일성이 좋은 데이터 아키텍처의 토대다. 그것은 세계가 유동적임을
  인정한다. 좋은 데이터 아키텍처는 유연하고 유지보수하기 쉽다. 그것은 업무 안의 변화에, 그리고
  미래에 더 많은 가치를 열어 줄지 모르는 새 기술과 실무에 반응해 진화한다. 작년의 데이터
  아키텍처가 오늘에 충분하지 않을 수 있고 내년은 말할 것도 없다** (3장, p.77).[^reis2022]
- **나쁜 데이터 아키텍처는 단단히 결합돼(tightly coupled) 있고, 경직돼 있고, 지나치게 중앙집중적이거나,
  그 일에 맞지 않는 도구를 쓰며, 개발과 변경 관리를 방해한다. 이상적으로는 되돌릴 수 있음
  (reversibility)을 염두에 두고 아키텍처를 설계함으로써 변경 비용이 덜 든다** (3장,
  p.77).[^reis2022]
- 저류가 토대다 — **데이터 엔지니어링 수명 주기의 저류가 데이터 성숙도의 어느 단계에 있는
  회사에나 좋은 데이터 아키텍처의 토대를 이룬다** (3장, p.77).[^reis2022] 여섯 저류의 목록은
  [데이터 엔지니어링의 저류](../concepts/data-engineering-undercurrents.md)에 있다.
- 끝나지 않는다 — **좋은 데이터 아키텍처는 살아 있고 숨 쉬는 것이다. 그것은 결코 완성되지
  않는다. 사실 저자들의 정의상 변화와 진화가 데이터 아키텍처의 의미와 목적의 중심에 있다**
  (3장, p.77).[^reis2022]

## 누가 설계하는가

- **데이터 아키텍처는 진공 속에서 설계되지 않는다. 더 큰 회사는 여전히 데이터 아키텍트를
  고용할 수 있지만, 그 아키텍트는 기술과 데이터의 현재 상태에 깊이 조율돼 있고 최신이어야 한다.
  상아탑 데이터 아키텍처의 시대는 갔다. 과거에 아키텍처는 대체로 엔지니어링과 직교했다. 데이터
  엔지니어링이, 그리고 일반적으로 엔지니어링이 빠르게 진화하며 더 애자일해지고 엔지니어링과
  아키텍처의 분리가 줄면서 이 구분은 사라질 것으로 본다** (3장, p.111).[^reis2022]
- **이상적으로 데이터 엔지니어는 전담 데이터 아키텍트와 나란히 일한다. 그러나 회사가 작거나
  데이터 성숙도 수준이 낮으면 데이터 엔지니어가 아키텍트 역할을 겸할 수 있다. 데이터 아키텍처는
  데이터 엔지니어링 수명 주기의 저류이므로, 데이터 엔지니어는 "좋은" 아키텍처와 여러 유형의
  데이터 아키텍처를 이해해야 한다** (3장, p.111).[^reis2022]
- **아키텍처를 설계할 때는 업무 이해관계자와 나란히 일하며 트레이드오프를 평가하게 된다. 클라우드
  데이터 웨어하우스 대 데이터 레이크를 채택하는 데 내재한 트레이드오프는 무엇인가? 여러 클라우드
  플랫폼의 트레이드오프는 무엇인가? 통합 배치/스트리밍 프레임워크(빔·플링크)는 언제 적절한
  선택인가? 이 선택들을 추상적으로 공부해 두는 것이 구체적이고 가치 있는 결정을 내릴 준비를
  해 준다** (3장, p.111).[^reis2022]

## 이어지는 페이지

- [좋은 데이터 아키텍처의 아홉 원칙](../concepts/good-data-architecture-principles.md) — 이 정의를 설계
  판단으로 옮긴 조문들
- [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md) — 이 아키텍처가
  섬기는 단계들
- [데이터 엔지니어링의 저류](../concepts/data-engineering-undercurrents.md) — 좋은 아키텍처의 토대로
  세어지는 여섯
- [유지보수성](../concepts/maintainability.md) — 되돌릴 수 있는 결정이 진화성이라는 이름으로
  다시 나오는 자리
- [데이터 시스템 아키텍처 트레이드오프](../synthesis/data-systems-architecture-tradeoffs.md) —
  "트레이드오프 평가"가 실제 축으로 펼쳐지는 허브

아키텍처의 유형들 — 이 책이 예로 드는 것들이 각각 자리 잡은 페이지다.

- [EDW](../concepts/enterprise-data-warehouse.md) — 데이터 웨어하우스·데이터 마트·클라우드 DW
- [데이터 레이크](../concepts/data-lake.md) — 데이터 레이크 1.0, 레이크하우스, 모던 데이터 스택
- [람다 아키텍처와 카파 아키텍처](../concepts/lambda-and-kappa-architecture.md) — 배치와
  스트림을 합치려는 두 제안
- [IoT 데이터 아키텍처](../concepts/iot-data-architecture.md) — 장치가 데이터를 만드는 쪽
- [데이터 메시](../concepts/data-mesh.md) — 도메인 소유권을 뒤집는 쪽
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이벤트 기반 아키텍처가 놓인 자리

[^reis2022]: Reis & Housley 2022, 3장 "Designing Good Data Architecture"
