---
type: concept
title: 골든 소스
description: 특정 맥락에서 데이터의 권위 있는 출처(authoritative source)가 되는 애플리케이션
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 골든 소스

분산된 환경에서 "이 데이터의 진짜 출처가 어디인가"에 답하는 개념. 골든 소스(golden
source)는 **특정 맥락 안에서 진정한 데이터가 관리되는 권위 있는 애플리케이션**이다.

> this is the authoritative application where all authentic data is managed within a
> particular context.

## 왜 먼저 정하는가

- 골든 소스 식별이 데이터 거버넌스의 **출발점**이다 — 도메인들이 같은 물리 데이터셋과
  데이터 설계의 소유권을 서로 주장하는 일이 실제로 벌어지기 때문이다
  (2장 Application Design Starting Points, p.27).[^strengholt2023-dms]
- 데이터 품질의 수선 지점이기도 하다. 골든 소스에서 고치면 다른 곳에서 같은 문제가
  다시 튀어나오지 않는다 — 배포가 항상 그 지점에서 출발하기 때문이다
  (2장 Application Design Starting Points, p.27).[^strengholt2023-dms]
- 유일한 데이터를 **골든 소스에서 직접만** 취득하면 책임 소재가 정확하고 일관되게
  유지된다 (2장 Application Design Starting Points, p.27).[^strengholt2023-dms]

## 운영 규칙

- 원본 데이터의 변경은 도메인 안의 골든 소스에서, 소유자의 승인을 받아서만 한다
  (2장 Principles for Distributed and Domain-Oriented Data Management,
  p.50).[^strengholt2023-dms]
- 골든 소스 목록을 **공개적으로 알려야** 한다 — 중앙 등록부나 카탈로그로 관리한다
  (2장 Principles…, p.50).[^strengholt2023-dms]
- 소비하던 애플리케이션이 데이터를 바꿔 **새 사실(new facts)** 을 만들면 그 시점에
  새 골든 소스가 되고 새 소유권이 생긴다. 다만 필터·합집합·대소문자 변환·필드 개명 같은
  "구문적 변환(syntactic transformations)"은 사실을 바꾸지 않으므로 새 소유권을
  만들지 않는다 (2장 Principles…, p.51).[^strengholt2023-dms]
- 중간 계층을 끼우지 않는다. 크로스 도메인 가상화 계층 같은 것은 골든 소스를 가리고
  계보 추적을 어렵게 한다 (2장 Principles…, p.52-53).[^strengholt2023-dms]

## 관련 용어

- 저자는 `system of record`(SOR)를 같은 뜻의 다른 표기로 언급한다
  (2장 각주 2, p.27).[^strengholt2023-dms]
- #hypothesis 권위 있는 애플리케이션을 찾는 일 자체가 쉽지 않다는 서술이 있는데
  (복잡한 패턴 뒤에 숨어 있을 수 있다 — 2장 각주 3, p.27), 이 책은 그 식별 절차를
  구체적으로 주지 않는다.[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"
