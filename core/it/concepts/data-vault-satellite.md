---
type: concept
title: Data Vault Satellite
description: 업무 키·관계의 맥락과 전체 변경 이력을 담는 엔티티 — 단일 부모·분할 규칙·불변 이력과 특수 새틀라이트 응용
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault Satellite

**목차**: [구조 제약](#구조-제약) · [이력은 불변이다](#이력은-불변이다) · [분할 규칙 — 한 덩어리로 두지 않는다](#분할-규칙-한-덩어리로-두지-않는다) · [메타데이터 속성](#메타데이터-속성) · [응용 — overloaded satellite는 문제를 만든다](#응용-overloaded-satellite는-문제를-만든다) · [응용 — multi-active satellite](#응용-multi-active-satellite) · [응용 — status tracking satellite](#응용-status-tracking-satellite) · [응용 — effectivity satellite](#응용-effectivity-satellite) · [응용 — record tracking satellite](#응용-record-tracking-satellite) · [응용 — computed satellite](#응용-computed-satellite)

Satellite는 [Hub](../concepts/data-vault-hub.md)나 [Link](../concepts/data-vault-link.md)에 맥락
(context) — 업무 객체·관계·트랜잭션을 서술하는 속성 — 을 붙이고 그 변경
이력을 추적하는 [Data Vault](../concepts/data-vault-modeling.md) 엔티티다 (§4.5, pp.133–135).[^linstedt2016]

> Satellites store all data that describes a business object, relationship,
> or transaction.

## 구조 제약

- Satellite의 부모는 **정확히 하나**(Hub 하나 또는 Link 하나)이고, 다른
  테이블의 부모가 될 수 없다(눈송이화 금지). 그래서 자체 해시 키를 만들지
  않으며, 식별은 부모 해시 키 + Load Date의 조합이다 (§4.5, pp.133–135).[^linstedt2016]
- 변경이 있는 원천 레코드만 새 엔트리로 쌓는 델타 구동이다 —
  [차원 모델링](../concepts/dimensional-modeling.md)의 Type II 차원에 비견된다
  (§4.5.1, pp.135–136).[^linstedt2016]
- 원천 포착이 목적이므로 서술 속성의 데이터 타입은 원천에 최대한 가깝게 두고
  NULL도 그대로 담는다 (§4.5, pp.133–135).[^linstedt2016]

## 이력은 불변이다

- 웨어하우스는 이력이 보관되는 유일한 장소(system of record)가 되므로,
  Satellite의 데이터는 갱신·수정이 금지된다. 유일한 예외는 이전 버전의
  **Load End Date** 갱신뿐이다 (§4.5.1, pp.135–136).[^linstedt2016]
- 구조를 재설계할 때도 기존 이력의 100%를 보존해야 감사를 통과한다 (§4.5.1, pp.135–136).[^linstedt2016]

## 분할 규칙 — 한 덩어리로 두지 않는다

권장은 1차로 **원천 시스템별**, 2차로 **변경 빈도별** 분할이다 (§4.5.2, p.136).[^linstedt2016]

- 원천별 분할의 이점: 기존 엔티티 무변경으로 새 원천 추가, 원천 데이터 무가공
  보존, 시스템별 감사 추적, 적재 병렬성 극대화(대상 경합 없음), 실시간 데이터의
  독립 통합 (§4.5.2.1, p.136).[^linstedt2016]
- 변경 빈도별 분할: 자주 변하는 속성(비행 마일리지)과 거의 안 변하는 속성
  (좌석 수)을 한 Satellite에 두면, 잦은 변경마다 안 변한 속성까지 새 레코드로
  복제된다 — 빈도 그룹별로 나눈다 (§4.5.2.2, p.137).[^linstedt2016]

## 메타데이터 속성

- 필수: 부모 해시 키 + Load Date(PK), Load End Date, Record Source.
  선택: Hash Diff, Extract Date (§4.5.3, p.137).[^linstedt2016]
- **Load Date는 웨어하우스가 처음 본 시각**이지 원천의 타임스탬프가 아니다 —
  원천 시각은 신뢰할 수 없으므로(시간대 미상 등) 서술 속성으로만 담는다.
  예외는 과거 데이터 초기 적재뿐: 이때는 원천 추출 시점으로 소급 설정해야
  같은 날 덮어써진 변경들이 살아남는다. 원천의 생성일·계획일 등 어떤 날짜도
  load date/load end date에 넣어선 안 된다 (§4.5.3.2–5, pp.138–139).[^linstedt2016]
- **Hash Diff** — 서술 속성 전체의 해시. 행 비교를 빠르게 해 변경이 있을 때만
  새 엔트리를 만들게 한다. 델타 적재만 오는 원천에는 불필요하다 (§4.5.3.4·§4.5.4, pp.138–140).[^linstedt2016]

## 응용 — overloaded satellite는 문제를 만든다

- 여러 원천의 데이터를 한 Satellite에 합쳐 넣은 것이 overloaded satellite다.
  원천별 분할 권장을 어기는 것으로, 타당한 이유가 있을 때도 있으나 내재적
  위험을 들여온다: 우선 원천마다 데이터 포맷이 다르면(이름·주소 필드 길이 등)
  데이터가 빠르게 오염된다 (§5.3.1, p.162).[^linstedt2016]
- 데이터를 보면 답할 수 없는 질문들이 쌓인다: 값이 모순될 때 어느 원천이
  마스터인가, 어떤 행이 다른 행을 대체하는가, 최신 행은 무엇인가, NULL만 주는
  원천은 어떻게 다루나, 적재 시 병합할 것인가 그대로 둘 것인가. 부모 해시 키 +
  Load Date 조합이 유일하지 않게 되어 Record Source를 PK에 넣어야 하는지도
  문제가 된다 (§5.3.1, p.162).[^linstedt2016]
- 이 문제들은 델타 감지를 매우 복잡하게 만든다 — 마스터 시스템만이 아니라
  모든 원천의 변경을 남기려 하기 때문이다 (§5.3.1, pp.162–163).[^linstedt2016]

## 응용 — multi-active satellite

- 부모 키 하나당 **다중 활성 엔트리**를 담는 Satellite. overloaded와 달리 여러
  원천이 아니라 COBOL copybook·XML 같은 비정규화된 단일 원천에서 온다 —
  예: 직원 한 명의 전화번호 여러 개. 구조 차이는 하위 항목을 식별하는 시퀀스
  속성(예: PhoneSeq)이 PK에 추가되는 것뿐이다 (§5.3.2, p.163).[^linstedt2016]
- 순서 의존성이 문제다: 원천 파일에서 전화번호 순서만 바뀌어도 그 부모의 데이터
  전체가 델타로 감지되어, 바뀐 것이 없는데도 구 레코드 전부가 end-date되고
  전부 재삽입된다 (§5.3.2, p.164).[^linstedt2016]
- 해결책은 위치 시퀀스 대신 **속성 값 자체(전화번호)를 시퀀스로** 쓰는 것 —
  델타 검사의 순서 의존이 사라진다. 대신 원천 도착 순서를 재현할 가능성은
  사라지므로, 순서가 중요하면 위치 서브시퀀싱뿐이다. 위치 서브시퀀싱은
  아키텍처상 최후 수단(architectural fallback)으로 활성 테이블 압축과 함께만
  쓴다 (§5.3.2, p.164).[^linstedt2016]
- 값-시퀀스의 제약: 그 속성이 NOT NULL이고 부모 맥락 안에서 유일해야 하며,
  시퀀스 컬럼이 숫자가 아닌 문자열이면 성능이 크게 나빠질 수 있다 — 그래도
  "나쁜 둘 중 나은 쪽(best worst-case)"이다. 시퀀스로 쓴 속성 값은 옮기지 않고
  서술 속성에도 복제해 두어야 다음 사용자가 이해하기 쉽다 (§5.3.2, p.165).[^linstedt2016]

## 응용 — status tracking satellite

- CDC(change data capture)나 감사 추적이 주는 **CRUD(또는 SCRUD) 연산 정보**를
  적재하는 Satellite. 서술 속성은 연산 종류를 담는 Status 하나뿐이고 나머지는
  메타데이터다. 원천 시스템이 연산 정보를 제공해야 성립한다 (§5.3.3, pp.165–166).[^linstedt2016]
- 업무 키 등 서술 데이터는 여기 담지 않는다 — 그것은 별도의 표준 Satellite
  몫이다. 상태와 상태 변경 시각만 추적하며, 그 외에는 표준 Satellite 레이아웃과
  규칙을 따르고 디스크 절약을 위해 압축을 켠다 (§5.3.3, p.166).[^linstedt2016]
- 여러 원천이 상태를 주면 마스터(주도) 시스템 것만 추적하거나, 원천별로 status
  tracking satellite를 분할한다 — 4장의 원천별 분할과 같은 관행이다 (§5.3.3, pp.166–167).[^linstedt2016]

## 응용 — effectivity satellite

- 주로 Link에 붙어 **관계가 업무상 언제 활성인지**를 begin/end date로 추적하는
  Satellite(Hub 업무 키의 유효성 추적에도 쓸 수 있다). Link 구조 자체에는
  end-date를 둘 수 없으므로 유효 기간은 이 Satellite가 담는다. 조직 전체
  관점에서 관계(또는 키)가 "삭제된 것으로 간주되는" 시점을 나타내곤 한다 (§5.3.4, p.167).[^linstedt2016]
- begin/end date는 시스템 생성이 아니라 **원천이 제공해야 한다** — MDM 감사
  추적·마스터 데이터의 유효 일자·CDC 등. 감사를 통과하려면 날짜를 원천까지
  소급 추적할 수 있어야 한다. 원천이 유효 일자를 주지 않는데 인공 날짜를
  만들어 붙이는 일은 피한다 — 원천이 제공할 때만 합리적인 엔티티다 (§5.3.4, p.167).[^linstedt2016]
- 링크 테이블 엔트리 하나당 활성 레코드 하나가 있고, 기간 연장 등 갱신은 새
  레코드 삽입으로 반영한다. 원천 시스템에 데이터가 존재하는지 여부는 여기가
  아니라 record tracking satellite가 추적한다 (§5.3.4, p.168).[^linstedt2016]

## 응용 — record tracking satellite

- **어느 원천이 어떤 키·관계를 어느 적재 주기에 공급했는지**를 추적하는
  Satellite. 매일 전체 덤프를 주는 원천에서 레코드가 규칙 없이 나타났다
  사라지는 문제(예: 업무 사용자가 편집 중이라 잠긴 레코드는 export에서 빠지는
  레거시 메인프레임) 때문에 필요하다 — CDC가 없으면 삭제를 확정할 수 없다 (§5.3.5, pp.168–169).[^linstedt2016]
- "며칠 안 보임"과 "삭제됨"의 구분은 업무 규칙으로 정한다(예: 7일 연속 미출현 =
  삭제로 간주 후 Satellite들을 end-date). Hub·Link의 last seen date와 같은
  이유·같은 갱신 관행이다 (§5.3.5, p.169).[^linstedt2016]
- 규칙을 굽힌 예외 엔티티다: 모든 레코드가 시스템 생성이라 **Record Source가
  없고**, 갱신 대신 주기마다 새 엔트리를 삽입하므로 **Load End Date도 없다**.
  그 결과 감사 불가능하지만, 전체 모델을 깨지 않으면서 규칙을 우회하게 해주므로
  문제가 되지 않는다 (§5.3.5, p.171).[^linstedt2016]
- 레이아웃 두 가지: (1) 비정규화 — 원천별 컬럼에 출현 여부 1/0. 분할·필터·조회에
  최적이지만 데이터가 아니라 원천 시스템 구조가 구동하는 설계라, 원천이 추가될
  때마다 컬럼 추가 + 기존 행 갱신이 필요하다. (2) 정규화 — Record Source 컬럼 +
  출현 여부(Appearance) 행. 원천 추가가 삽입만으로 끝나지만 분석은 PIVOT이
  필요해진다. 데이터 폭증을 막기 위해 압축하고, 오래된 데이터는 요약 후 제거
  하거나 저속 디스크·백업 테이프로 옮긴다 (§5.3.5, pp.170–171).[^linstedt2016]
- 레코드 소스를 상세히("CRM/Contact/Lead") 적으면 키가 원천 안 어디서 처음
  나타나 어디로 이동했는지까지 추적할 수 있다 — 뭉뚱그린 "CRM"으로는 불가능하다 (§5.3.5, pp.171–172).[^linstedt2016]

## 응용 — computed satellite

- 집계·요약·교정·평가의 결과, 즉 **업무 규칙으로 변경된 계산 데이터**를 담는
  Satellite로 Business Vault 소속이다(데이터 품질 루틴·클렌징·주소 교정 결과
  등). 마트마다 같은 연산을 반복하지 않도록 배포 전에 한 번만 계산해 저장하는
  용도다 (§5.3.6, p.172).[^linstedt2016]
- 구조는 표준 Satellite와 같고, 유일한 차이는 record source가 시스템 생성임을
  표시하는 것이다(계산을 수행한 함수·연산·애플리케이션을 함께 적을 수 있다).
  raw 원천이 없으므로 본질상 감사 불가능하지만, 감사자가 계산 로직과 마트로
  내려가기 전의 데이터를 검토할 수 있는 장소가 된다 (§5.3.6, p.172).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"·5장 "Intermediate Data Vault Modeling"
