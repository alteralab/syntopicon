---
type: concept
title: Data Vault Link
description: 허브 사이의 관계를 다대다로만 담는 엔티티 — 시간성 배제·입도·driving key 규칙과 same-as·계층·비이력·계산 링크 응용
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault Link

- [다대다만 존재한다](#다대다만-존재한다)
- [입도와 재입도 변경](#입도와-재입도-변경)
- [엔티티 구조](#엔티티-구조)
- [응용 — link-on-link는 피한다](#응용--link-on-link는-피한다)
- [응용 — same-as link (SAL)](#응용--same-as-link-sal)
- [응용 — hierarchical link](#응용--hierarchical-link)
- [응용 — nonhistorized link (구 transactional link)](#응용--nonhistorized-link-구-transactional-link)
- [응용 — nondescriptive link](#응용--nondescriptive-link)
- [응용 — computed aggregate link와 exploration link](#응용--computed-aggregate-link와-exploration-link)

Link는 [Hub](../concepts/data-vault-hub.md)들 사이의 관계·트랜잭션·계층을 담는
[Data Vault](../concepts/data-vault-modeling.md) 엔티티다 (§4.4, pp.121–122).[^linstedt2016]

> Links capture and record the past, present, and future relationships
> between data elements at the lowest possible granularity.

## 다대다만 존재한다

- Link는 항상 다대다 테이블로 구현한다. 링크 하나가 1:m·m:n·m:1·1:1을 정의
  변경 없이 모두 수용하므로, 업무 규칙이 바뀌어도(예: "공항당 단일 항공사" →
  "복수 항공사") ETL 재공학이 필요 없다 — 전통 모델에서는 관계 정의 변경이
  곧 재공학이다 (§4.4.1–2, pp.124–126).[^linstedt2016]
- Link에는 시간성(temporality)을 두지 않는다 — Begin/End Date를 링크에 넣으면
  관계를 단일 타임라인에 묶어 "시작·종료가 한 번뿐"이라는 성립하지 않는 제약을
  강제하게 된다. 관계의 활성 여부는 맥락이므로 [Satellite](data-vault-satellite.md)가
  담는다. 예외는 기술·정보 목적의 Load Date뿐 (§4.4, pp.121–122).[^linstedt2016]

## 입도와 재입도 변경

- Link의 입도(granularity)는 연결한 Hub 수로 정해진다 — Hub를 하나 더 참조하면
  입도가 내려간다. [팩트 테이블](../concepts/fact-table.md)에 차원을 더하는 것과 같은
  원리다 (§4.4.3, pp.128–129).[^linstedt2016]
- **운영 중인 Link 구조의 수정은 DV 2.0에서 더 이상 허용되지 않는다** — 기존
  링크에 Hub 참조를 더하면 이력 데이터를 임의 값으로 채워야 해서(원천은 NULL을
  준 적이 없다) 감사 가능성이 깨진다. 대신 옛 링크를 닫고 새 링크를 만들며,
  서로 다른 입도의 병합 방법은 업무 규칙(SQL)으로 정보 마트 쪽에서 정의한다 (§4.4.3, pp.128–129).[^linstedt2016]
- **unit-of-work**: 함께 도착한 키 집합은 함께 유지해야 한다. 링크를 정규화
  명목으로 잘게 쪼개면 재조인 시 원천에 없던 레코드가 생긴다 — 관계형 모델링의
  다치 종속(multivalued dependency) 문제다 (§4.4.4, pp.130–131).[^linstedt2016]

## 엔티티 구조

- 필수: 해시 키(연결된 모든 업무 키의 조합을 해시)·Load Date·Record Source +
  참조 Hub들의 해시 키. 선택: last seen date, 종속 자식 키 (§4.4.5, pp.131–132).[^linstedt2016]
- **종속 자식 키(dependent child key)** — 송장 라인번호처럼 홀로 서지 못하고
  다른 맥락 안에서만 유일한 퇴화 필드(degenerate field). 링크의 입도와 유일성에
  참여하므로 해시 키 계산에 포함된다 (§4.4.5.2, p.132).[^linstedt2016]
- **driving key** — 링크의 Hub 참조 중 "지속되는 대상"을 식별하는 부분 집합.
  driving key 밖의 키(예: 노선은 같은데 바뀐 항공편 번호)가 변하면 새 링크
  엔트리가 생기고, 새틀라이트의 이전 엔트리는 다음 레코드의 load date로
  end-date된다. 모델 다이어그램에는 보이지 않는 논리적 구성물이라 적재 절차에서
  구현해야 한다 (§4.5.5, pp.140–143).[^linstedt2016]

## 응용 — link-on-link는 피한다

- 링크가 다른 링크를 참조하는 구조(link-on-link)는 만들 수 있지만(예: 원 항공편
  링크를 참조하는 회항 링크), 두 링크 사이의 의존성이 대용량·고속(big data)
  상황에서 확장·성능 모두 나빠지고, 부모 링크의 변경이 모든 종속 자식 링크에
  연쇄(cascade)돼 스프린트 안에 변경을 끝내지 못하게 한다 (§5.2.1, pp.149–150).[^linstedt2016]
- 권장은 link-to-link 참조를 삼가고 각 링크를 독립적으로 구현하는 것 —
  데이터 모델링에서 말하는 비정규화(denormalization)다. 그러면 각 링크를
  독립적으로 수정할 수 있다 (§5.2.1, p.150).[^linstedt2016]

## 응용 — same-as link (SAL)

- 하나의 Hub 안에서 **같은 업무 객체를 식별하는 중복 업무 키들**을 표시하는
  링크. master 해시 키와 duplicate 해시 키 두 개가 같은 Hub를 참조한다. 원천
  미통합·조직 합병 등으로 같은 고객이 시스템마다 다른 식별 번호를 갖는 상황을
  Hub 통합을 깨지 않고 해결한다 (§5.1·§5.2.2, pp.145–147, 150–151).[^linstedt2016]
- 레코드는 고객 중복 제거(de-duplication) 알고리즘이나 업무가 제공하는 매핑
  테이블에서 계산될 수 있다. 원천 시스템에서 끌어오지 않고 사람 개입·알고리즘이
  유지하는 한 same-as link는 실질적으로 Business Vault 엔티티다 (§5.1.1·§5.2.2, pp.147–148, 150–151).[^linstedt2016]
- 적재 관점에서 master 해시 키 컬럼에는 주도 원천 시스템(leading source system)의
  키가 와야 한다 — 그래야 주도 시스템 키로 종속 시스템 키를 조회할 수 있다 (§5.2.2, p.151).[^linstedt2016]

## 응용 — hierarchical link

- 부모-자식 계층(예: BOM, bill of material)을 담는 링크. parent와 child 참조가
  **같은 Hub**를 가리킨다. 계층 레벨마다 Hub를 따로 만들지 않고 하나의 Hub를
  쓴다 — 기술적으로는 레벨마다 grain이 달라 보이지만 업무는 레벨을 레벨로
  다루며, 각 레벨이 하위 레벨들로 구성된다는 논리 관점에서 레벨은 super-type
  이고 grain이 같다 (§5.2.3, pp.152–153).[^linstedt2016]
- 계층 링크는 표준 링크의 응용일 뿐이다 — 구조가 다르지 않고 링크 규칙을 어떤
  식으로도 위반하지 않는다 (§5.2.3, p.153).[^linstedt2016]

## 응용 — nonhistorized link (구 transactional link)

- 트랜잭션·센서 데이터처럼 **한번 쓰이면 절대 수정되지 않는** 데이터를 담는
  링크. 갱신이 불가능하며, 트랜잭션 취소는 원천에서 역트랜잭션(reverse
  transaction)을 만들어 적재한다. 오류 교정도 Data Vault 안에서 하지 않는다.
  "transactional link"라는 옛 이름은 오해 소지가 있다 — CCTV 사진 스트림처럼
  트랜잭션이 아니어도 무갱신인 관계를 담을 수 있어 2016년 저술 시점에는 nonhistorized link라
  부른다 (§5.2.4, p.154).[^linstedt2016]
- 트랜잭션 식별자(예: 송장 번호)는 종속 자식 키로 링크 자체에 붙고, 해시 키는
  참조 Hub들의 업무 키 + 트랜잭션 식별자에서 계산한다 (§5.2.4, p.155).[^linstedt2016]
- 물리 구현 1(권장): 표준 링크 + **LoadEndDate 없는 새틀라이트** — end-date할
  수 없으니 레코드의 새 버전 삽입 자체가 불가능해진다. 새틀라이트의 LoadDate는
  링크와 중복이라 생략할 수도 있지만, 두 엔티티가 다른 원천에서 밀리초 차이로
  도착하는 실시간 사례와 표준화(신규 인력의 이해 용이)를 위해 두는 편이다 (§5.2.4, pp.154–156).[^linstedt2016]
- 물리 구현 2(대부분 비권장): 새틀라이트 없이 트랜잭션 속성을 링크 구조에 직접
  넣는다. 설계 과정에 재량 결정이 개입돼 모델 복잡성과 유지비가 늘고 자동
  적재가 어려워진다. 밀리초 이하 적재 성능이 필수일 때만 가치가 있는데, 이때도
  행이 넓어지면 (행 지향 DBMS에서) DB 페이지당 레코드 수가 줄어 적재·조회
  성능이 되레 떨어진다 — 서술 필드는 소수만 링크에 두고, 많으면 복수
  새틀라이트로 분산해 행 폭을 좁게 유지한다 (§5.2.4, pp.156–158).[^linstedt2016]

## 응용 — nondescriptive link

- 새틀라이트가 하나도 없는 저가치(low-value) 링크 — 두 업무 키 사이에 관계가
  존재한다는 사실만 표시한다(예: 고객이 광고를 클릭해 특정 상품에 관심을 표함) (§5.2.5, p.158).[^linstedt2016]
- 다중상태(multistate)·역할 수행(role-playing) 관계에서 상태 하나당 링크
  하나로도 쓴다(예: 관심 링크와 별도로 캠페인 선정 링크). 새틀라이트 + 코드
  테이블 조합 등 다른 모델링 선택지도 있다 (§5.2.5, pp.158–159).[^linstedt2016]

## 응용 — computed aggregate link와 exploration link

- **computed aggregate link** — 기존 링크에서 Hub 하나를 제거하고 남은 관계로
  데이터를 집계한 링크(예: 항공편 번호 Hub를 빼고 "어느 항공사가 어느 공항
  연결을 운항하는가"만 남기고 편수는 집계). 계산된 데이터이므로 Business Vault
  소속이고 그 자체로는 감사 불가능하지만 원천 링크에서 언제든 재생성할 수 있다 —
  bridge table의 응용이다 (§5.2.6, pp.159–160).[^linstedt2016]
- 구분 기준은 **링크 데이터가 어디서 오는가**다: 링크 자체가 raw 데이터에서
  GROUP BY 등 업무 로직으로 계산되면 Business Vault 링크가 되고(계산 속성을
  링크 구조 안에 넣는 변형도 허용), 링크는 원천에서 오고 집계만 없으면 링크는
  Raw Data Vault에 남고 집계는 computed satellite로 붙인다 (§5.2.6, pp.160–161).[^linstedt2016]
- **exploration link** — 업무상 이유만으로 만든 계산 링크(Business Vault, 비감사).
  표준 링크 구조를 그대로 쓰며 수동으로 생성·유지한다(자동화 가능). 용도:
  원천에 없는 관계·동적 네트워크 탐지, 간접 관계의 직접화(두 링크의 비정규화
  버전 포함), 중복 키가 있는 Hub 사이 링크 통합, Hub 내 유사 엔트리 군집 식별,
  사기 탐지 같은 패턴 자동 발견 (§5.2.7, p.161).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"·5장 "Intermediate Data Vault Modeling"
