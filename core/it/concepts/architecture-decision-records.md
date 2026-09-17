---
type: concept
title: 아키텍처 결정 기록
description: 아키텍처 결정을 짧은 텍스트 파일 하나로 남기는 형식과 그 형식이 요구하는 네 자리 — 결정을 명사구로 적는 제목과 문제와 대안을 한두 문장으로 적는 맥락과 결정 자체와 그 정당화, 그리고 적용 뒤의 귀결과 고려한 절충을 적는 자리, 승인된 것만 적는다는 전제, 마이클 나이가드의 블로그 글이 원전이고 소트웍스 기술 레이더가 채택으로 올렸다는 계보, 평문도 되지만 대개 AsciiDoc이나 마크다운이나 위키 템플릿을 쓴다는 관행, 책 한 권의 ADR을 부록에 색인한다는 조판과 그 부록이 모은 열셋의 제목과 쪽 그리고 목록 첫 항목이 결정이 아니라 견본이라는 관찰, 같은 책이 리팩터링을 적을 때는 ADR이 아니라 아키텍처 스토리를 쓰며 한 장 전체에 ADR 상자가 없다는 대조, 그리고 결정을 문서화하는 일과 그 결정의 올바른 쓰임을 거버넌스하는 일이 별개라는 경계와 그 별개를 적합도 함수가 받는다는 배치
generated: { by: "claude-opus-5", at: "2026-09-17T17:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 아키텍처 결정 기록

- [무엇인가](#무엇인가)
- [계보](#계보)
- [무엇으로 쓰는가](#무엇으로-쓰는가)
- [형식 — 네 자리](#형식--네-자리)
- [승인된 것만 적는다는 전제](#승인된-것만-적는다는-전제)
- [책 한 권의 ADR을 색인하는 방식](#책-한-권의-adr을-색인하는-방식)
- [이 책의 ADR 열셋과 목록에 빠진 하나](#이-책의-adr-열셋과-목록에-빠진-하나)
- [이 책이 리팩터링을 적는 다른 형식](#이-책이-리팩터링을-적는-다른-형식)
- [문서화와 거버넌스는 별개다](#문서화와-거버넌스는-별개다)
- [이 KB의 다른 소스가 이 형식을 쓰는 자리](#이-kb의-다른-소스가-이-형식을-쓰는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **아키텍처 결정을 나중에 읽을 수 있게 남기려면 무엇을 적어야 하는가.**

## 무엇인가

- **저자들의 규정** — **아키텍처 결정 기록(Architectural Decision Records, ADR)은 아키텍처
  결정을 문서화하는 가장 효과적인 방법 중 하나**다 (1장 §"Architectural Decision Records",
  p.5).[^ford2021-hard-parts]
- **한 건의 크기가 규정의 일부다** — ADR 하나는 **짧은 텍스트 파일 하나(대개 한두 쪽 길이)로
  특정 아키텍처 결정 하나를 기술한다** (1장, p.5).[^ford2021-hard-parts]
  - **"결정 하나"와 "한두 쪽"이 같이 붙어 있다는 것이 이 형식의 성격이다.** 결정 여럿을 한
    문서에 모으는 설계 문서와 반대 방향이고, 그래서 결정마다 파일이 하나씩 쌓인다.

## 계보

- **원전은 마이클 나이가드(Michael Nygard)의 블로그 글**이다. 저자들은 그가 **처음 전파했고**
  나중에 **소트웍스 기술 레이더(Thoughtworks Technology Radar)에서 "채택(adopt)"으로 표시**
  됐다고 적는다 (1장, p.5).[^ford2021-hard-parts]
  - **이 KB는 그 블로그 글과 기술 레이더 항목을 확인하지 않았다** — 귀속은 이 책이 그렇게
    귀속한다까지로 둔다.
  - 나이가드는 이 KB에 다른 자리로도 들어와 있다 — [안정성 패턴](stability-patterns.md)이
    그의 *Release It!*을 출처로 든다. **두 자리가 같은 사람이라는 것은 이 KB가 대조한 것이고
    이 책은 그 사실을 적지 않는다.** #hypothesis
- **저자들의 앞 책이 이 주제에 한 장을 할애했다** — *Fundamentals of Software
  Architecture*(오라일리)다 (1장, p.5).[^ford2021-hard-parts] **이 KB가 확인한 원전이
  아니다.**

## 무엇으로 쓰는가

- **평문으로도 쓸 수 있지만 대개는 AsciiDoc이나 마크다운 같은 텍스트 문서 형식으로 쓴다.**
  대안으로 **위키 페이지 템플릿**을 쓸 수도 있다 (1장, p.5).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점. 저자들이 도구를 지목하지 않고 형식만 든다.
  - **텍스트 파일을 먼저 드는 것이 우연이 아니다** — 결정 기록을 소스와 같은 저장소에 두면
    같은 이력 도구가 적용된다. **그 귀결을 이 책이 적지는 않는다.** #hypothesis

## 형식 — 네 자리

- **저자들이 이 책 전체에서 쓰는 형식이다** (1장, p.5):[^ford2021-hard-parts]

  > *ADR: A short noun phrase containing the architecture decision*
  >
  > *Context*
  >
  > In this section of the ADR we will add a short one- or two-sentence description of the
  > problem, and list the alternative solutions.
  >
  > *Decision*
  >
  > In this section we will state the architecture decision and provide a detailed
  > justification of the decision.
  >
  > *Consequences*
  >
  > In this section of the ADR we will describe any consequences after the decision is
  > applied, and also discuss the trade-offs that were considered.

- **네 자리가 각각 다른 것을 막는다.**
  - **제목이 명사구다** — 문장이 아니라 명사구이므로 결정 자체가 이름이 되고, 목록으로 훑을 수
    있게 된다.
  - **맥락이 대안을 함께 요구한다** — 문제 서술 한두 문장에 **대안 해법의 목록**이 붙는다.
    고르지 않은 길을 적어 두지 않으면 나중에 그 결정이 왜 좁혀졌는지 복원되지 않는다.
  - **결정 자리에 정당화가 함께 들어간다** — "무엇을 정했다"만이 아니라 **왜 그것인가의 상세한
    정당화**다.
  - **귀결 자리가 절충을 받는다** — 적용 뒤에 생기는 귀결과 **고려했던 절충**을 함께 적는다.
    이 책의 축이 절충 분석이므로 이 칸이 이 형식을 이 책의 것으로 만든다.

## 승인된 것만 적는다는 전제

- **저자들이 형식을 소개하며 전제 하나를 명시한다** — **각 ADR이 승인되었다는 가정 아래** 이
  형식을 쓴다 (1장, p.5).[^ford2021-hard-parts]
  - **그래서 이 책의 ADR에는 상태(status) 칸이 없다.** 제안·승인·대체 같은 생애 주기를 적는
    칸을 두는 판이 흔하지만, 이 책은 승인된 결정만 싣는다는 전제로 그 칸을 뺐다.
  - **결정이 뒤집히는 경우를 이 형식이 어떻게 다루는지를 이 책이 적지 않는다.**

## 책 한 권의 ADR을 색인하는 방식

- **이 책은 본문에서 내려지는 여러 아키텍처 결정을 ADR로 문서화하고**, 만들어진 모든 ADR의
  목록을 **부록 B**에 모은다 (1장, p.5).[^ford2021-hard-parts]
  - **결정을 만드는 자리와 색인하는 자리를 가른 조판**이다. 결정은 그것이 내려진 장의 흐름
    안에 상자로 놓이고, 훑기는 부록이 맡는다.
  - 그 결정들이 대입되는 체계는 [Sysops Squad 사례](sysops-squad-case.md)다.

## 이 책의 ADR 열셋과 목록에 빠진 하나

**부록 B가 이 책의 ADR을 한자리에 모은다.** 제목과 인쇄판 쪽을 원문 그대로 옮긴다 (부록 B
"Architecture Decision Record References", pp.419–420).[^ford2021-hard-parts]

| 인쇄판 쪽 | ADR 제목 |
|---|---|
| 5 | ADR: A short noun phrase containing the architecture decision |
| 61 | ADR: Migrate Sysops Squad Application to a Distributed Architecture |
| 79 | ADR: Migration Using the Component-Based Decomposition Approach |
| 184 | ADR: Use of Document Database for Customer Survey |
| 211 | ADR: Consolidated Service for Ticket Assignment and Routing |
| 215 | ADR: Consolidated Service for Customer-Related Functionality |
| 241 | ADR: Using a Sidecar for Operational Coupling |
| 247 | ADR: Use of a Shared Library for Common Ticketing Database Logic |
| 280 | ADR: Single Table Ownership for Bounded Contexts |
| 281 | ADR: Survey Service Owns the Survey Table |
| 297 | ADR: Use of In-Memory Replicated Caching for Expert Profile Data |
| 321 | ADR: Use Orchestration for Primary Ticket Workflow |
| 380 | ADR: Loose Contract for Sysops Squad Expert Mobile Application |

- **그런데 목록이 이 책의 ADR 상자를 전부 담고 있지 않다.** 부록의 안내 문장은 **이 책의 각
  Sysops Squad 결정에 대응하는 ADR이 딸려 있었고 그것들을 여기 모았다**고 적는데, **14장
  p.397에 열넷째 ADR 상자가 하나 더 있다** (14장, p.397, ADR):[^ford2021-hard-parts]

| 인쇄판 쪽 | ADR 제목 | 목록에 있는가 |
|---|---|---|
| 397 | `ADR: Ensure that Expert Supply DPQ Sources Supply an Entire Day's Data or None` | **없다** |

  - **이 KB가 책 전체에서 `ADR:` 상자를 전수로 훑어 확인했다.** 부록의 열셋과 본문의 상자를
    맞대면 남는 것이 이 하나이고, **저자들이 그 누락을 적지 않는다.** #hypothesis
  - **그 ADR만 형식이 하나 더 길다** — 맥락·결정·결과 뒤에 **`Fitness functions:`** 항목이
    붙어 둘을 적는다(완전한 일별 스냅샷을 검사하는 것과, Ticket DPQ와 Expert Supply DPQ 사이의
    소비자 주도 계약). **이 책에서 ADR에 적합도 함수가 딸리는 자리는 여기뿐이다** — 위
    [형식 — 네 자리](#형식--네-자리)가 적는 넷에 없던 다섯째 칸이다. #hypothesis 그 장면의
    전문은 [Sysops Squad 사례](sysops-squad-case.md)에 있다.
- **목록 자체가 위 [형식 — 네 자리](#형식--네-자리)의 첫째 규칙을 검증한다.** 열셋 전부가
  명사구이고 문장이 하나도 없다. **`Migrate`·`Use`로 시작하는 것들도 동사가 아니라 명사구의
  머리다**(이행 그 자체를 가리킨다).
- **부록의 안내 문장과 목록이 한 칸 어긋난다.** 부록은 **이 책의 각 Sysops Squad 결정에
  대응하는 아키텍처 결정 기록이 딸려 있었고 그것들을 여기 모았다**고 적는데, 목록의 첫
  항목(p.5)은 결정이 아니라 **형식을 보이는 견본**이다. 그래서 실제 결정은 열둘이다.
  **이 관찰은 이 KB가 원문을 대조해 적는 것이고 책이 그 어긋남을 말하지 않는다.** #hypothesis
- **목록의 넷째(p.184)가 형식의 규정에서 한 자리 벗어난다** — `ADR: Use of Document Database
  for Customer Survey`의 맥락 칸이 **대안 해법의 목록**을 담지 않는다. 관계형을 유지한다는
  대안이 **설문이 현재 관계형 데이터베이스에 저장돼 있지만 팀은 JSON을 쓰는 문서 데이터베이스로
  옮기고 싶어 한다**는 문장 안에 암시될 뿐이다 (6장, p.184, ADR).[^ford2021-hard-parts]
  - **결정 칸은 규정대로다** — 첫 문단이 결정이고 뒤의 두 문단이 정당화(마케팅 부서가 요구하는
    유연성과 적시성, 그리고 사용자 인터페이스의 단순화)다.
  - **귀결 칸이 서로 다른 층의 둘을 한 자리에 담는다** — 하나는 **설계 선택의 영구적 대가**(단일
    애그리게이트를 쓰므로 공통 질문이 바뀌면 여러 문서를 고쳐야 한다)이고, 다른 하나는 **이행
    한 번의 비용**(이관 동안 설문 기능을 내려야 한다)이다. **저자들이 그 구분을 적지
    않는다.** #hypothesis
  - **이 ADR이 만들어진 이유를 본문이 명시한다** — **이 결정의 어려움과 데이터를 바꾸는 일의
    구조적 성격 때문**이다 (6장, p.184, 사가).[^ford2021-hard-parts] **무엇을 ADR로 적을지의
    판정 기준이 이 책에서 드물게 드러나는 자리다** — 어려움과 구조적 성격 둘이다. 그 결정의
    전문과 별점표는 [데이터베이스 종류 고르기](selecting-a-database-type.md)에 있다.
- **목록의 다섯째와 여섯째(p.211·p.215)가 같은 장의 두 ADR인데 귀결 칸을 다르게 채운다.**
  - `ADR: Consolidated Service for Ticket Assignment and Routing`(7장, pp.211–212, ADR)의
    귀결 칸에는 **귀결만 있고 절충 논의가 없다** — 정기적으로 일어나는 배정 알고리즘 변경과 드문
    라우팅 변경이 두 기능 모두의 시험과 배포를 요구해 **시험 범위가 늘고 배포 위험이 커진다**는
    한 문단이다.[^ford2021-hard-parts] **절충 분석은 사가 서사 안에서 이루어지고 상자로 넘어오지
    않았다.**
  - `ADR: Consolidated Service for Customer-Related Functionality`(7장, pp.215–216, ADR)의
    귀결 칸에는 **절충 문장이 들어 있다** — **논의된 절충이 트랜잭션성 대 보안**이라고 명시하고,
    쪼개면 보안 접근이 나아지지만 등록과 탈퇴에 필요한 전부 또는 전무 트랜잭션을 지원하지 못하며
    보안 우려는 맞춤 라이브러리로 완화된다고 적는다.[^ford2021-hard-parts]
  - **같은 장의 두 상자가 같은 칸을 다르게 채우는 것을 저자들이 말하지 않는다.** 위
    [형식 — 네 자리](#형식--네-자리)가 요구하는 넷째 칸의 절반(고려했던 절충)이 앞 것에는
    없다. **이 관찰은 이 KB가 원문을 형식과 대조해 적는 것이다.** #hypothesis
  - **둘 다 맥락 칸의 요구는 지킨다** — 앞은 대안 둘(합쳐진 서비스 하나 대 배정과 라우팅의 별도
    서비스)을, 뒤는 대안 셋(합쳐진 하나·기능마다 별도·민감과 비민감을 가른 둘)을 나열한다
    (7장, pp.211·215, ADR).[^ford2021-hard-parts] 위 p.184 ADR이 대안 목록을 빠뜨린 것과 대비된다.
  - **두 상자 모두 결정 칸에 정당화가 여러 문단 붙는다** — 앞은 넷(단단한 결합·같은 확장 수요·
    완전한 상호 의존·워크플로가 부르는 문제), 뒤는 둘(단일 원자적 작업 단위 요구·보안
    라이브러리에 의한 위험 완화)이다. 두 결정의 전문과 그 장면은
    [서비스 세분도](service-granularity.md)에 있다.
  - **문법이 어긋나는 자리 둘을 원문 그대로 두고 표시한다** — 앞 ADR의 `dependent each other`
    (on 누락, p.212)와 뒤 ADR의 `through the use the custom`(of 누락, p.216)이다.
- **목록의 일곱째와 여덟째(p.241·p.247)가 같은 장의 두 ADR인데 맥락 칸을 다르게 채운다.**
  - `ADR: Using a Sidecar for Operational Coupling`(8장, p.241, ADR)의 맥락 칸에는 **대안
    목록이 없다** — 각 서비스가 공통되고 일관된 운영 행위를 요구하는데 그 책임을 팀마다 맡기면
    **불일치와 조율 문제**가 생긴다는 문제 진술뿐이다.[^ford2021-hard-parts] 위
    [형식 — 네 자리](#형식--네-자리)가 요구하는 대안 목록이 빠진 셋째 자리이고, 앞의 둘은
    p.184와 그 뒤에 적은 어긋남이다.
  - `ADR: Use of a Shared Library for Common Ticketing Database Logic`(8장, p.247, ADR)의
    맥락 칸에는 **선택지 둘이 명시된다** — **공유 라이브러리를 쓰는 것과 공유 데이터 서비스를
    만드는 것**이다.[^ford2021-hard-parts] **같은 장의 두 상자가 같은 칸을 다르게 채우는 것을
    저자들이 말하지 않는다.** 7장의 두 ADR이 귀결 칸에서 갈린 것과 같은 모양이고 이번에는
    맥락 칸이다. #hypothesis
- **앞 ADR의 귀결 칸이 이 책에서 드물게 금지를 적는다** — **팀은 사이드카에 도메인 클래스를
  더하지 말아야 한다. 그것이 부적절한 결합을 조장한다**는 것이다 (8장, p.241,
  ADR).[^ford2021-hard-parts] 다른 ADR들의 귀결 칸은 **일어날 일**을 적는데 이 칸은 **하지 말
  것**을 적는다. #hypothesis
  - **그 결정 칸에는 제공 목록이 들어 있다** — 사이드카가 제공할 것 다섯을 불릿으로
    나열한다(`Monitoring`·`Logging`·`Service discovery`·`Authentication`·`Authorization`).
    **열셋 가운데 결정 칸에 목록을 담는 유일한 ADR이다.** #hypothesis
- **뒤 ADR의 결정 칸이 정당화 셋을 담고 그중 하나에 논리가 어긋나는 자리가 있다** —
  **`change is less risky for the common database logic because services would need to be
  tested and redeployed`**라고 적는데, 시험과 재배포가 필요하다는 것은 위험이 낮은 **이유**가
  아니라 같은 ADR이 귀결 칸에 적는 **대가**다 (8장, p.247, ADR).[^ford2021-hard-parts] 원문
  그대로 두고 표시한다. #hypothesis
  - 두 결정의 전문과 그 장면은 [코드 재사용 패턴 넷](code-reuse-patterns.md)에 있다.
- **목록의 아홉째와 열째(p.280·p.281)가 같은 장의 두 ADR인데 겨냥하는 범위가 다르다.**
  - `ADR: Single Table Ownership for Bounded Contexts`(9장, p.280, ADR)를 본문이 **일반
    아키텍처 결정 기록**이라고 부른다 — 등장인물이 단일 테이블 소유권 시나리오에서 무엇을 할지
    서술하는 일반 ADR을 만들었다는 것이다 (9장, p.279, 사가).[^ford2021-hard-parts]
    **열셋 가운데 스스로를 일반 규칙이라 밝히는 유일한 ADR이다.** #hypothesis 나머지는 전부
    이 사례의 특정 결정이다.
    - 그래서 **맥락 칸도 특정 상황이 아니라 규칙이 걸리는 자리를 적는다** — 서비스와 데이터
      사이에 경계 컨텍스트를 이룰 때 테이블은 특정 서비스나 서비스 무리에 소유권이 배정돼야
      한다는 것이다.[^ford2021-hard-parts]
    - **결정 칸이 규칙 하나에 금지 하나를 붙인다** — 한 서비스만 테이블에 쓰면 그 서비스가
      소유하고, **다른 경계 컨텍스트의 테이블에 읽기 전용 접근이 필요한 서비스는 그 테이블이
      든 데이터베이스나 스키마에 직접 접근할 수 없다**는 것이다.[^ford2021-hard-parts] 위
      p.241 ADR에 이어 **귀결 칸이 아니라 결정 칸에 금지가 놓이는 자리**다. #hypothesis
    - **귀결 칸은 대가를 조건부로 적는다** — **쓰는 기법에 따라** 다른 경계 컨텍스트의 데이터에
      접근할 때 성능과 내결함성 문제를 겪을 수 있다는 것이다.[^ford2021-hard-parts] 그 기법들의
      상세를 저자들이 10장으로 넘긴다.
  - `ADR: Survey Service Owns the Survey Table`(9장, p.281, ADR)은 이 사례의 결정이고 **맥락
    칸에 선택지와 기각 사유가 함께 들어간다** — 공동 소유권이므로 대안은 공통 공유 데이터
    도메인과 위임 기법이고, **테이블 쪼개기는 설문 테이블의 구조 때문에 선택지가 아니다**라고
    적는다.[^ford2021-hard-parts] **열셋 가운데 맥락 칸에서 대안 하나를 미리 기각하는 유일한
    ADR이다.** #hypothesis
  - **귀결 칸이 다시 두 층을 담는다** — 하나는 **인터페이스의 영구적 대가**(필요한 데이터를
    설문 프로세스를 띄우는 페이로드에 실어야 한다)이고, 다른 하나는 **업무 절차의 이동**
    (모놀리스에서 완료 처리의 일부였던 설문 레코드 생성이 별도 활동이 되어 Survey 서비스가
    맡는다)이다.[^ford2021-hard-parts] p.184 ADR이 설계의 대가와 이행 한 번의 비용을 섞은 것과
    **다른 종류의 섞임**이다. #hypothesis
  - 두 결정의 전문과 그 장면은 [서비스의 데이터 소유권](service-data-ownership.md)에 있다.
- **목록의 열한째와 열두째(p.297·p.321)가 맥락 칸을 형식대로 채우는 드문 둘이다.**
  - `ADR: Use of In-Memory Replicated Caching for Expert Profile Data`(10장, p.297, ADR)의
    맥락 칸이 **대안 셋을 명시한다** — 서비스 간 통신·인메모리 복제 캐싱·공통 데이터
    도메인이다.[^ford2021-hard-parts] **그리고 결정 칸이 그중 하나를 기각한 근거까지 적는다** —
    티켓 배정 서비스가 이미 다른 스키마에 붙어 있고 두 기능이 별도 도메인이라 공통 데이터
    도메인이 선택지가 아니라는 것이다. **맥락에서 세고 결정에서 지우는 이 짜임은 열셋 가운데
    이 하나뿐이다.** #hypothesis
    - **귀결 칸이 다시 두 층을 담는다** — 하나는 **운영 제약**(티켓 배정 서비스의 첫 인스턴스를
      띄울 때 User Management 서비스의 인스턴스가 최소 하나는 돌고 있어야 한다)이고 다른 하나는
      **비용**(캐싱 제품의 라이선스)이다.[^ford2021-hard-parts] p.184와 p.281 ADR의 같은
      버릇이고 섞이는 종류가 또 다르다. #hypothesis
  - `ADR: Use Orchestration for Primary Ticket Workflow`(11장, p.321, ADR)의 맥락 칸은 **대안
    둘을 그림 번호로 지목하고 둘 다 작동한다고 적는다** — 그림 11-16의 오케스트레이션 해법이든
    그림 11-15의 코레오그래피 해법이든 된다는 것이다.[^ford2021-hard-parts] **대안이 둘 다
    성립한다고 맥락 칸이 밝히는 유일한 ADR이다.** #hypothesis
    - **결정 칸이 표를 근거로 지목한다** — 두 해법을 모형화해 **표 11-8의 절충에 이르렀다**고
      적는다.[^ford2021-hard-parts] **열셋 가운데 결정의 근거로 이 책의 표 하나를 이름으로
      부르는 유일한 자리다.** #hypothesis 다른 ADR들은 근거를 산문으로 적는다.
    - **귀결 칸이 재고 조건을 적는다** — 단일 오케스트레이터를 둘러싼 확장성 문제가 있을 수
      있고 **현재의 확장성 요구가 바뀌면 재고해야 한다**는 것이다.[^ford2021-hard-parts]
      **귀결 칸에 재심 조건을 적는 유일한 ADR이다.** #hypothesis 다른 자리들은 대가나 금지나
      비용을 적는다.
  - 두 결정의 전문과 그 장면은
    [분산 데이터 접근 패턴 넷](distributed-data-access-patterns.md)과
    [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md)에 있다.
- **쪽 번호가 결정이 내려진 자리를 가리킨다** — 위
  [책 한 권의 ADR을 색인하는 방식](#책-한-권의-adr을-색인하는-방식)이 적는 조판 규약의 실물이다.
  결정은 그 장의 흐름 안 상자에 놓이고 부록이 훑기를 맡는다.

## 이 책이 리팩터링을 적는 다른 형식

**같은 책이 ADR과 나란히 쓰는 형식이 하나 더 있고, 한 장 전체가 그쪽만 쓴다.**

- **5장은 사가의 코드 리팩터링을 아키텍처 스토리(architecture story)로 기록한다** — 사용자
  스토리가 구현하거나 바꿔야 할 기능을 서술하는 것과 달리, 아키텍처 스토리는 **애플리케이션의
  전체 구조에 영향을 주면서 어떤 업무 구동 요인을 만족시키는 특정 코드 리팩터링**을 서술한다
  (5장, p.84, 곁상자).[^ford2021-hard-parts] 형식과 예문은
  [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md)
  §"아키텍처 스토리 — 리팩터링을 적는 단위"에 있다.
- **그 장에는 ADR 상자가 없다.** 위 [이 책의 ADR 열셋과 목록에 빠진 하나](#이-책의-adr-열셋과-목록에-빠진-하나)에서 인쇄판 p.79 다음
  항목이 p.184이고, 5장의 쪽 범위(pp.81–130)에 드는 항목이 하나도 없다 (부록 B,
  pp.419–420).[^ford2021-hard-parts]
  - **이 대조는 이 KB가 부록 목록과 본문 쪽 범위를 맞대어 본 것이고, 저자들이 "이 장에는 ADR을
    두지 않는다"고 적지는 않는다.** #hypothesis
- **ADR이 없는 장이 5장만은 아니다.** 같은 방식으로 목록과 쪽 범위를 맞대면 **12장
  "Transactional Sagas"(pp.323–364)에도 항목이 하나도 없다** — 목록이 11장 p.321 다음에 곧바로
  13장 p.380으로 건너뛴다 (부록 B, pp.419–420).[^ford2021-hard-parts]
  - **12장은 사가 상자를 둘 갖는데(여는 p.323, 닫는 pp.358–364) 결정 기록은 남기지 않는다.**
    닫는 사가는 문제를 진단하고 대안 둘을 이름으로 들되 **"원자성에 문제가 생기면 그 패턴들을
    살펴볼 수 있다"는 조건부 예고**로 끝난다 (12장, p.364, 사가).[^ford2021-hard-parts]
  - **이것이 위 [승인된 것만 적는다는 전제](#승인된-것만-적는다는-전제)와 같은 방향이다** —
    아직 고르지 않은 것은 ADR이 되지 않는다. 저자들이 그 연결을 적지는 않는다. #hypothesis
  - 그 장면의 전문은 [Sysops Squad 사례](sysops-squad-case.md)와
    [트랜잭셔널 사가 패턴](transactional-saga-patterns.md)이 갖는다.
- **15장에도 ADR이 없고, 부록 B의 목록도 13장 p.380에서 끝난다** (부록 B, pp.419–420 · 15장,
  pp.399–416).[^ford2021-hard-parts] 마지막 장은 결정을 내리는 대신 앞의 결정들을 만든 절차를
  회고하므로 **기록할 결정이 없다.** #hypothesis
  - **그런데 그 회고가 이 형식을 조직의 습관으로 세운다** — 이 속도를 어떻게 유지하느냐는 물음에
    수석 아키텍트가 **규율**이라 답하며 셋을 드는데, 그 둘째가 **결정을 아키텍처 결정 기록으로
    문서화하고 전달하는 일을 계속하는 것**이다 (15장, p.400, 사가).[^ford2021-hard-parts]
    나머지 둘은 모든 결정에 절충 표를 만드는 것과 다른 팀과 협업하는 것이고, 그 첫째의 전문은
    [트레이드오프 분석 방법](trade-off-analysis-method.md)이 갖는다.
- **두 형식이 담는 것이 다르다는 읽기가 가능하다** — ADR은 **선택지 가운데 하나를 고른 결정**과
  그 맥락과 귀결을 담고, 아키텍처 스토리는 **실행할 리팩터링 작업**을 담아 개발자에게 배정된다.
  5장의 사가들이 하는 일이 대부분 "어느 코드를 어디로 옮길 것인가"라 후자에 해당한다. #hypothesis
  - **그래서 이 페이지의 형식이 모든 아키텍처 산출물을 덮지는 않는다.** 결정이 아닌 것은 다른
    양식으로 간다는 것이 이 책이 보이는 실물이다.

## 문서화와 거버넌스는 별개다

- **저자들이 이 절을 닫으며 경계를 하나 긋는다** — **결정을 문서화하는 일은 아키텍트에게
  중요하지만, 그 결정이 제대로 쓰이는지를 거버넌스하는 것은 별개의 주제**다. 다행히 현대
  공학 실천은 **아키텍처 적합도 함수를 써서 흔한 거버넌스 관심사 다수를 자동화**할 수 있게
  한다 (1장, p.5).[^ford2021-hard-parts]
  - **이 한 줄이 이 페이지와 [아키텍처 적합도 함수](architecture-fitness-functions.md)를
    잇는다** — 기록은 사람이 읽는 것이고, 그 기록대로 되는지를 기계가 확인한다.
  - **결정을 적는 일과 그 결정을 지키는 일이 다른 사람의 일일 수도 있다는 함의**까지 이 책이
    적지는 않는다.

## 이 KB의 다른 소스가 이 형식을 쓰는 자리

- **같은 저자들의 다른 책이 ADR을 적합도 함수의 문서화 수단으로 든다** — 결정 문서에 **거기
  담긴 설계 결정을 어떻게 거버넌스하는지를 적는 절을 더한다**는 것이다. 그쪽은 **ADR의 형식
  자체를 규정하지 않고** 그 한 줄이 전부다 ([자동화된 아키텍처
  거버넌스](automated-architectural-governance.md) §"적합도 함수를 문서화하기"). **그래서
  이 페이지가 그쪽이 전제하고 지나간 형식을 담는다.**
- **결정을 누가 어떤 과정으로 내리는가는 다른 페이지가 갖는다** —
  [전략 설계 결정하기](strategic-decision-making.md)가 2003년 원전 쪽에서 그 물음에 답하고,
  [전략 목표와 원칙과 실천](strategic-goals-principles-practices.md)이 결정을 틀 지우는 세
  층을 세운다. **이 페이지는 그 결정이 내려진 뒤 무엇을 적는가만 다룬다.**
  - **세 자리가 겹치지 않는 이유**: 권위(누가)와 틀(무엇에 비추어)과 기록(무엇을 남기는가)은
    서로를 전제하지 않는다. 권위가 정해져도 기록 형식은 비어 있을 수 있고, 형식이 있어도
    권위가 흩어져 있을 수 있다. **이 배치는 이 KB가 세운 것이고 세 소스는 서로를 호명하지
    않는다.** #hypothesis
- **결정의 되돌릴 수 있음을 먼저 재는 소스도 있다** — [되돌릴 수 있는 설계 결정](reversible-design-decisions.md)과
  [데이터 아키텍처의 규정](data-architecture-defined.md) §"일방통행문과 양방향문"이 그것이다.
  **되돌릴 수 없는 결정일수록 맥락과 대안을 적어 둘 값이 크다는 것은 이 KB의 읽기이고 어느
  소스도 그 연결을 적지 않는다.** #hypothesis

## 이어지는 페이지

- [아키텍처 적합도 함수](architecture-fitness-functions.md) — 문서화 다음의 거버넌스
- [자동화된 아키텍처 거버넌스](automated-architectural-governance.md) — 그 거버넌스를 실제로
  거는 일과 ADR을 그 문서로 쓰는 한 줄
- [전략 설계 결정하기](strategic-decision-making.md) — 결정을 누가 어떤 과정으로 내리는가
- [전략 목표와 원칙과 실천](strategic-goals-principles-practices.md) — 결정을 틀 지우는 세 층
- [진화적 아키텍트의 역할](evolutionary-architect-role.md) — 그 결정을 하는 사람
- [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md) — 같은 책이 결정
  아닌 리팩터링을 적는 다른 형식이 사는 자리
- [Sysops Squad 사례](sysops-squad-case.md) — 이 책의 ADR들이 대입되는 체계
- [데이터베이스 종류 고르기](selecting-a-database-type.md) — 6장의 유일한 ADR이 놓이는 결정
- [서비스 세분도](service-granularity.md) — 7장의 ADR 둘이 놓이는 결정. 같은 장의 두 상자가
  귀결 칸을 다르게 채우는 자리
- [코드 재사용 패턴 넷](code-reuse-patterns.md) — 8장의 ADR 둘이 놓이는 결정. 같은 장의 두
  상자가 맥락 칸을 다르게 채우는 자리
- [되돌릴 수 있는 설계 결정](reversible-design-decisions.md) — 무엇을 적어 둘 값이 큰가의 다른 축
- [데이터 아키텍처의 규정](data-architecture-defined.md) — 되돌릴 수 있는 결정과 없는 결정
- [조직과 아키텍트](../synthesis/organizations-and-architects.md) — 이 실천이 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 1장 "What Happens When There
    Are No 'Best Practices'?" §"Architectural Decision Records"(p.5) 한 절이 전부다. 쪽은
    인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 직인용 하나(ADR 형식 네 자리)는 `pdftotext -layout`
    추출로 문자 단위 대조했고, 원문이 이탤릭으로 조판한 항목 이름은 인용 안에서 이탤릭을
    유지했다. 원문은 이 형식을 들여쓴 정의 목록으로 조판하는데 인용 블록으로 옮기며 항목
    사이에 빈 줄을 넣었다 — 낱말은 보태거나 빼지 않았다. 이 절에는 도판도 표도 코드 목록도
    없다. 저자들이 대는 바깥 것들(Michael Nygard의 블로그 글 · Thoughtworks Technology Radar ·
    *Fundamentals of Software Architecture*)은 **이 KB가 확인한 원전이 아니다** —
    귀속은 이 책이 그렇게 귀속한다까지로 둔다. 굵은 글씨는 원문 문장의 한국어 재서술이고
    괄호 안이 그 쪽이다.
    **부록 B "Architecture Decision Record References"(pp.419–420)가 ADR 목록 절에
    합류했다.** 그 부록은 열세 줄의 제목과 쪽 번호가 전부이고, 제목과 쪽을 **영어 그대로**
    옮겼다 — 이 책이 인쇄한 제목 자체가 식별자라 번역하면 본문의 상자와 맞춰 볼 수 없다.
    원문은 각 제목을 굽은 따옴표로 감싸고 `on page NN`을 붙이는데, 표로 옮기며 따옴표를
    빼고 쪽을 열로 갈랐다 — 낱말은 보태거나 빼지 않았다. 대조는 `pdftotext -layout`
    추출로 했다. 부록 B에 도판도 코드 목록도 없다.
    **14장 §"Sysops Squad Saga: Data Mesh"의 ADR 상자(p.397)가 같은 절에 합류했다** — 그것이
    부록 B 목록에 없다는 판정은 **이 KB가 책 전체의 `pdftotext -layout` 전문에서 `ADR:` 로
    시작하는 상자를 전수로 훑어** 부록의 열셋과 맞대 본 실측이다. 제목은 영어 그대로 옮겼고
    본문 넷과 적합도 함수 둘의 내용은 [Sysops Squad 사례](sysops-squad-case.md)가 갖는다.
    그 상자에 도판도 코드 목록도 없다.
    **5장 곁상자 "Architecture Stories"(p.84)가 다른 형식 절에 합류했다.** 그 곁상자의
    직인용은 [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md)이
    갖고, 여기서 옮긴 것은 두 형식의 대조다. 5장에 ADR 상자가 없다는 관찰은 **이 KB가 부록 B의
    쪽 목록과 5장의 쪽 범위(pp.81–130, 책 목차 실측)를 맞대어 본 것**이다.
    **6장의 ADR 하나(p.184, §"Sysops Squad Saga: Polyglot Databases" 안의 상자)가 목록 절에
    합류했다.** 위 관찰 셋은 그 상자의 원문과 1장 p.5의 형식 규정을 맞대어 본 것이고, ADR
    전문의 직인용은 [데이터베이스 종류 고르기](selecting-a-database-type.md)가 갖는다 —
    여기서는 형식과 어긋나는 자리만 적었다. 6장에 ADR이 이 하나뿐이라는 것도 같은 방식으로
    부록 B의 쪽 목록(p.79 다음이 p.184)과 6장의 쪽 범위(pp.131–184)를 맞대어 확인했다.
    **7장의 ADR 둘(p.211 · p.215, 각각 §"Sysops Squad Saga: Ticket Assignment Granularity"와
    §"Sysops Squad Saga: Customer Registration Granularity" 안의 상자)도 목록 절에 합류했다.**
    위 관찰 넷은 두 상자의 원문과 1장 p.5의 형식 규정을 맞대어 본 것이고, 두 ADR 전문과 그
    장면은 [서비스 세분도](service-granularity.md)가 갖는다 — 여기서는 형식과 맞물리는 자리만
    적었다. 두 상자에 딸린 문법 오식 둘(`dependent each other` p.212 · `through the use the
    custom` p.216)은 원문 그대로 옮기고 표시했다. 7장에 ADR이 이 둘뿐이라는 것도 부록 B의 쪽
    목록(p.184 다음이 p.211·p.215이고 그다음이 p.241)과 7장의 쪽 범위(pp.185–216)를 맞대어
    확인했다.
    **8장의 ADR 둘(p.241 · p.247, 각각 §"Sysops Squad Saga: Common Infrastructure Logic"과
    §"Sysops Squad Saga: Shared Domain Functionality" 안의 상자)도 목록 절에 합류했다.**
    위 관찰 넷은 두 상자의 원문과 1장 p.5의 형식 규정을 맞대어 본 것이고, 두 ADR 전문과 그
    장면은 [코드 재사용 패턴 넷](code-reuse-patterns.md)이 갖는다 — 여기서는 형식과 맞물리는
    자리만 적었다. **직인용 조각 하나(p.247 결정 칸의 어긋나는 절)만 원문 그대로 인라인 코드로
    옮겼다** — `pdftotext -layout` 추출로 문자 단위 대조했다. 8장에 ADR이 이 둘뿐이라는 것도
    부록 B의 쪽 목록(p.215 다음이 p.241·p.247이고 그다음이 p.280)과 8장의 쪽
    범위(pp.219–247)를 맞대어 확인했다. 두 상자에 도판도 코드 목록도 없다.
    **10장의 ADR 하나(p.297, §"Sysops Squad Saga: Data Access for Ticket Assignment" 안의
    상자)와 11장의 ADR 하나(p.321, §"Sysops Squad Saga: Managing Workflows" 안의 상자)도 목록
    절에 합류했다.** 위 관찰 여섯은 두 상자의 원문과 1장 p.5의 형식 규정을 맞대어 본 것이고, 두
    ADR 전문과 그 장면은
    [분산 데이터 접근 패턴 넷](distributed-data-access-patterns.md)과
    [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md)가 갖는다 — 여기서는
    형식과 맞물리는 자리만 적었다. 두 상자에 직인용도 도판도 코드 목록도 두지 않았다. 두 장에
    ADR이 각각 하나뿐이라는 것도 부록 B의 쪽 목록(p.281 다음이 p.297이고 그다음이 p.321이며
    그다음이 p.380)과 두 장의 쪽 범위(pp.283–298 · pp.299–322)를 맞대어 확인했다.

    **9장의 ADR 둘(p.280 · p.281, 둘 다 §"Sysops Squad Saga: Data Ownership for Ticket
    Processing" 안의 상자)도 목록 절에 합류했다.** 위 관찰 다섯은 두 상자의 원문과 1장 p.5의
    형식 규정을 맞대어 본 것이고, 두 ADR 전문과 그 장면은
    [서비스의 데이터 소유권](service-data-ownership.md)이 갖는다 — 여기서는 형식과 맞물리는
    자리만 적었다. 이 둘에는 직인용을 두지 않았다. 9장에 ADR이 이 둘뿐이라는 것도 부록 B의 쪽
    목록(p.247 다음이 p.280·p.281이고 그다음이 p.297)과 9장의 쪽 범위(pp.249–282)를 맞대어
    확인했다. 두 상자에 도판도 코드 목록도 없다. **첫째 ADR을 "일반 아키텍처 결정 기록"이라
    부르는 것은 본문의 낱말이고**(p.279), 그것이 열셋 가운데 유일하다는 판정은 부록 B 목록
    전부를 훑어 이 KB가 세운 것이다.

    **12장 "Transactional Sagas"(pp.323–364)에 ADR 상자가 없다는 관찰이 다른 형식 절에
    합류했다.** 부록 B의 쪽 목록(p.321 다음이 p.380)과 12장의 쪽 범위를 맞대어 확인했고, 닫는
    사가 §"Sysops Squad Saga: Atomic Transactions and Compensating Updates"(pp.358–364)를 읽어
    그 자리에 결정이 아니라 조건부 예고가 있다는 것도 확인했다. 그 사가에 직인용을 두지 않았고,
    도판 셋(그림 12-22·12-23·12-24)은 재현하지 않았다. **ADR 없는 장이 5장과 12장 둘이라는
    대조는 이 KB가 세운 것이고 저자들이 어느 쪽도 적지 않는다.**
    **15장 여는 사가(p.400)의 규율 세 조목이 이 절에 합류했다** — 직인용을 두지 않았고 옮긴
    것이 장면의 판정이다. 15장에 ADR 상자가 없다는 관찰은 부록 B의 쪽 목록이 13장 p.380에서
    끝난다는 것과 이 KB가 책 전체에서 `ADR:` 상자를 전수로 훑은 실측이 함께 뒷받침한다.
