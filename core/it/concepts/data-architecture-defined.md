---
type: concept
title: 데이터 아키텍처의 정의
description: "데이터 아키텍처를 무엇이라 정의하며 무엇이 그것을 '좋다'고 만드는가 — 엔터프라이즈 아키텍처의 부분집합이라는 위치, TOGAF·Gartner·EABOK·DAMA의 정의와 저자들의 정의, 유연하고 되돌릴 수 있는 결정과 일방통행문·양방향문, 변경 관리, 운영 아키텍처와 기술 아키텍처의 분업, 그리고 나쁜 아키텍처의 형태, 그리고 아키텍처 쪽 소스가 같은 경계를 반대 방향에서 긋는 자리 — 데이터가 체계보다 오래 산다는 전제와 모든 소프트웨어 아키텍처가 데이터에 봉사한다는 판정, 경계 컨텍스트가 데이터베이스를 서비스 안으로 옮기면서 데이터가 아키텍처 관심사가 되었다는 기제, 운영 데이터와 분석 데이터의 가름, 그리고 이 페이지가 인용하는 가장 덜 나쁜 아키텍처라는 경구의 원문, 그리고 그 경구의 출처가 같은 저자들의 선행서 4장 트레이드오프 절이라는 실측과 2판 문면이 이 페이지의 인용과 낱말이 다르다는 판정"
generated: { by: "claude-opus-5", at: "2026-08-15T18:00:00Z" }
sources:
  - { id: reis2022, resource: /it/sources/reis2022.md }
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: richards2025, resource: /it/sources/richards2025.md }
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
- [아키텍처 쪽에서 같은 경계를 긋는 소스](#아키텍처-쪽에서-같은-경계를-긋는-소스)
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

- **TOGAF**(The Open Group Architecture Framework) — **2022년 저술 시점에 가장 널리 쓰이는 아키텍처
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
- 저자들의 엔터프라이즈 아키텍처 정의 — 2022년 저술 시점의 빠르게 움직이는 데이터 지형에 더 적합하다고
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

## 아키텍처 쪽에서 같은 경계를 긋는 소스

**이 페이지는 데이터 쪽에서 아키텍처를 본다. 반대 방향에서 같은 경계를 긋는 소스가 이 KB에
있다** — 분산 아키텍처의 절충을 다루는 책이 **데이터의 중요성**에 한 절을 쓴다.

- **그쪽이 여는 인용** (1장 §"The Importance of Data in Architecture",
  p.4):[^ford2021-hard-parts]

  > Data is a precious thing and will last longer than the systems themselves.
  >
  > —Tim Berners-Lee

  - **이 KB는 버너스리의 원문을 확인하지 않았다.**
- **그쪽의 전제가 이 페이지의 전제와 같다** — 어떤 체계를 짓든 데이터를 다뤄야 하고, 데이터는
  **체계나 아키텍처보다 오래 사는 경향이 있어 부지런한 사고와 설계를 요구한다** (1장,
  p.4).[^ford2021-hard-parts]
  - 그리고 **긴장 하나를 지목한다** — **데이터 아키텍트의 본능 다수가 단단히 결합된 체계를
    짓는 쪽이고, 그것이 2021년 저술 시점 분산 아키텍처 안에서 충돌을 만든다** (1장,
    p.4).[^ford2021-hard-parts] 위 §""좋은" 데이터 아키텍처"가 **단단히 결합됨**을 나쁜
    아키텍처의 첫 성질로 드는 것과 같은 방향이다.
- **그쪽이 내리는 판정이 이 페이지보다 강하다** — **데이터가 회사의 가장 중요한 자산이라는 말이
  있어 왔고**, 기업의 모든 부분이 이제 데이터로 움직인다. 그 의존이 뜻하는 것은 **모든
  소프트웨어 아키텍처가 데이터에 봉사한다(all software architecture is in the service of
  data)**는 것이다 (1장, p.4).[^ford2021-hard-parts]
- **왜 2021년 저술 시점에 결정이 더 어려워졌는가에 대한 그쪽의 진단** — 수십 년 전 분산 체계를 지을 때는
  **대개 여전히 단일 관계형 데이터베이스에 데이터를 영속화했다.** 그런데 마이크로서비스와,
  구현 세부 결합의 범위를 제한하는 수단으로서의 **경계 컨텍스트에 대한 철학적 고수**가 들어오며
  **데이터가 트랜잭션성과 함께 아키텍처 관심사로 옮겨 왔다.** 2021년 저술 시점 아키텍처의 하드 파트 다수가
  **데이터와 아키텍처 관심사 사이의 긴장에서 나온다** (1장, p.4).[^ford2021-hard-parts]
  - 같은 진단을 2장이 되풀이한다 — **데이터베이스를 서비스 경계 안으로 옮기면서 데이터 관심사가
    아키텍처 관심사로 옮겨 온다** (2장, p.26).[^ford2021-hard-parts]
- **그쪽이 책 전체에 걸쳐 쓰는 가름 하나** (1장, pp.4–5):[^ford2021-hard-parts]

| 갈래 | 규정 |
|---|---|
| 운영 데이터(operational data) | 업무의 운영에 쓰이는 데이터 — 판매·거래 데이터·재고 따위다. **회사가 그 위에서 돌아가는 데이터이고, 무언가 이것을 끊으면 조직은 오래 기능하지 못한다.** 온라인 트랜잭션 처리(Online Transactional Processing, OLTP)로 정의되는 유형이며 대개 데이터베이스의 삽입·갱신·삭제를 수반한다 |
| 분석 데이터(analytical data) | 데이터 과학자와 업무 분석가가 예측·추세 분석과 그 밖의 비즈니스 인텔리전스에 쓰는 데이터 — **대개 트랜잭션성이 아니고 흔히 관계형도 아니며**, 그래프 데이터베이스에 있거나 원래의 거래 형태와 다른 형식의 스냅샷일 수 있다. **일상 운영에 결정적이지 않고 장기 전략 방향과 결정에 쓰인다** |

  - **이 KB의 데이터 축이 같은 가름 위에 서 있다** —
    [분석 데이터 아키텍처 세대론](../concepts/analytical-data-architecture-generations.md)이 그 가름을
    전제로 세 세대를 세고, [데이터 퀀텀](data-quantum.md)이 분석 쪽을 나누는 단위를 규정한다.
    **아키텍처 쪽 소스가 같은 가름을 자기 용어 목록에 넣는다는 사실이 여기서 확인된다.**
- **위 §""좋은" 데이터 아키텍처"가 여는 경구의 원문이 이 소스에 있다.** 이 페이지가 인용하는
  것은 **"Never shoot for the best architecture, but rather the least worst architecture.
  —Mark Richards and Neal Ford"**인데, 그 두 사람이 자기 책에 적은 문장은 이것이다 (1장,
  p.2):[^ford2021-hard-parts]

  > Don't try to find the *best* design in software architecture; instead, strive for the
  > *least worst* combination of trade-offs.

  - **두 문장이 같지 않다.** 대상이 **아키텍처**에서 **설계**로, 목적어가 **아키텍처**에서
    **절충의 조합**으로 다르다. 그 문장이 놓인 논증의 전문은
    [진화적 아키텍트의 역할](evolutionary-architect-role.md) §"아키텍트의 일 — 최선이 아니라
    가장 덜 나쁜 조합"에 있다.
- **위 §""좋은" 데이터 아키텍처"의 인용이 어느 책에서 왔는지가 이제 확인된다.** 이 페이지가
  인용하는 문장은 대상이 **아키텍처**이고, 그 두 사람이 **아키텍처**를 대상으로 이 낱말을
  조문으로 세우는 자리는 같은 저자들의 앞 책 *Fundamentals of Software Architecture* **4장
  §"Trade-Offs and Least Worst Architecture"**다. 그 책 2판(2025)이 인쇄하는 문면은 이것이다
  (4장, p.65):[^richards2025]

  > Never strive for the *best* architecture; aim for the *least worst* architecture.

  - **낱말까지 같지는 않다.** 이 페이지의 인용은 `shoot for`와 `but rather`를 쓰고 2판은
    `strive for`와 세미콜론 뒤의 `aim for`를 쓴다. **가리키는 주장은 같다.**
  - **이 페이지의 인용이 1판(2020) 문면일 가능성이 남는다.** 이 데이터 공학 책은 2022년에
    나왔으므로 2판을 인용했을 수 없고, **이 KB는 1판 실물을 갖고 있지 않아 1판 문면을 확인하지
    못했다.** 그래서 **"낱말까지 같은 인용인가"는 여전히 판정하지 않는다.** #hypothesis
  - **확정된 것은 출처의 책과 장과 절이다** — 이 페이지가 "어느 책인지 모른다"고 적어 온 상태는
    여기서 닫힌다. 그 절의 논증 전문(왜 소수의 특성만 떠받칠 수 있는가의 이유 넷과 헬리콥터
    비유)은 [가장 덜 나쁜 아키텍처](least-worst-architecture.md)에 있다.

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
- [분석 데이터 아키텍처 세대론](../concepts/analytical-data-architecture-generations.md) —
  같은 목록을 시간 순으로 세 세대로 끊고 그 공통 가정을 진단하는 쪽
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이벤트 기반 아키텍처가 놓인 자리

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 1장 "What Happens When There
    Are No 'Best Practices'?" 도입(p.2)과 §"The Importance of Data in Architecture"(pp.4–5),
    그리고 2장 "Discerning Coupling in Software Architecture" 도입(p.26). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 18, 실측). 직인용 둘(버너스리의 제사 · 가장 덜 나쁜 절충 조합)은
    `pdftotext -layout` 추출로 문자 단위 대조했고 원문이 이탤릭으로 조판한 강조를 유지했다.
    위 운영·분석 데이터 표는 **원문의 들여쓴 정의 항목 둘을 이 KB가 표로 옮긴 것**이다.
    이 구간에 도판도 코드 목록도 없다. 저자들이 대는 바깥 것들(Tim Berners-Lee ·
    *Fundamentals of Software Architecture*)은 **이 KB가 확인한 원전이 아니다** — 다만 그
    책은 2026년 KB 작성 시점에 2판이 이 KB에 들어와 있고, 아래 각주가 그 자리다.

[^reis2022]: Reis & Housley 2022, 3장 "Designing Good Data Architecture"

[^richards2025]: Richards·Ford 2025(2판), 4장 "Architectural Characteristics Defined"
    §"Trade-Offs and Least Worst Architecture"(pp.64–65). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 24,
    실측). 직인용 하나(가장 덜 나쁜 아키텍처 경구)는 `pdftotext` 추출로 문자 단위 대조했고
    원문이 이탤릭으로 조판한 강조를 유지했다. **이 각주가 닿는 것은 위 인용의 출처 확인
    한 자리뿐이고**, 그 절의 논증 전문은
    [가장 덜 나쁜 아키텍처](least-worst-architecture.md)가 갖는다.
