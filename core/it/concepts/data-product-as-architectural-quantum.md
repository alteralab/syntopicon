---
type: concept
title: 아키텍처 양자로서의 데이터 제품
description: 서비스 메시에서 데이터 메시로 넘어올 때 무엇이 최소 단위가 되는가
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 아키텍처 양자로서의 데이터 제품

데이터 메시(data mesh)라는 말을 만든 Zhamak Dehghani는 **마이크로서비스에서 영감을
얻었다.** 이 페이지는 그 유추가 어디까지 성립하고 어디서 깨지는지를 다룬다
(2장 Inspirations from Software Architecture, p.29).[^strengholt2023-dms]

## 유추의 사슬

- 마이크로서비스가 늘수록 관리가 어려워진다. 서비스들이 서로 직접 통신하면 하나가
  오작동할 때 **파급 효과가 전체로 번지는 취약한 시스템**이 된다
  (2장 Inspirations…, p.30).[^strengholt2023-dms]
  - 커뮤니티 용어로는 이런 구조를 `distributed big ball of mud`라 부른다. 서로 통신하는
    마이크로서비스 landscape는 복잡한 상태 기계처럼 굴고, 커질수록 결과가 예측
    불가능해진다 (2장 각주 5, p.30).[^strengholt2023-dms]
- 대응이 **서비스 메시(service mesh)** 다. 서비스 간 통신을 지배하는 로직을 개별
  서비스에서 빼내 별도 계층으로 추상화한다. 모니터링·발견성·우아한 종료·정책 집행
  같은 기능을 제공한다 (2장 Inspirations…, p.30).[^strengholt2023-dms]
- 이때 마이크로서비스는 **기능적 응집**을 기준으로 묶인다. 그룹(안전 경계) 안에서는
  직접 통신하되 다른 그룹과는 서비스 메시를 거친다 — 메시가 안전한 프록시로 행동한다
  (2장 Inspirations…, p.30).[^strengholt2023-dms]
- 서비스 메시는 **동기 요청/응답**을 위한 것이고, 비동기 통신에는 이벤트 브로커로
  쉽게 대체된다. 필요에 따라 둘을 나란히 쓸 수도 있다
  (2장 Inspirations…, p.31).[^strengholt2023-dms]

## 데이터 메시로 넘어오는 지점

- 이 마이크로서비스 설계에 **빠져 있는 것이 분석 데이터 아키텍처**다
  (2장 Inspirations…, p.31).[^strengholt2023-dms]
- 대응 관계: 서비스 메시에서는 프록시를 통해 서비스 요청이 라우팅된다면, 데이터
  메시에서는 **분석 데이터가 데이터 제품(data product)을 통해 제공**된다. 데이터 제품이
  데이터를 변환하고, 무결성을 유지하고, 정책을 지배하고, 최종적으로 서빙한다
  (2장 Inspirations…, p.31).[^strengholt2023-dms]
- Dehghani의 표현을 저자가 인용한다 (2장 Inspirations…, p.32):[^strengholt2023-dms]

  > a new architectural quantum… the smallest unit of your architecture that has all
  > of the structural components to do its job.

## 유추가 깨지는 지점

- 저자는 이 발상을 "brilliant"라고 평가하면서도 곧바로 한계를 짚는다: **모든
  아키텍처가 마이크로서비스로만 이루어져 있지는 않다.** 오늘날 기업 아키텍처에는
  대형 레거시, COTS 제품, SaaS, 운영 데이터 스토어, MDM 스토어, 데이터 웨어하우스가
  섞여 있고 상당수가 사용자·조직 단위 간에 공유된다
  (2장 Inspirations…, p.32).[^strengholt2023-dms]
- 그래서 이 책의 질문은 "데이터 제품을 최소 단위로 삼자"가 아니라 **"이런 대규모
  데이터 아키텍처에서 경계를 어떻게 제대로 긋는가"** 로 옮겨 간다
  (2장 Inspirations…, p.32).[^strengholt2023-dms]
- 저자는 데이터 메시가 강하게 주장하는 **"단일 데이터 모델은 없다"** 에도 유보를 단다 —
  현실에는 사업 전반에 걸친 명확하고 공유된 관계가 있고, 그것을 무시하면 도메인 간
  통합이 불가능한 데이터가 된다 (2장 Design Principles for Data Domains,
  p.53).[^strengholt2023-dms]

## 소비를 위한 형태

데이터 제품이 갖춰야 할 성질은 데이터 제공자 모범 사례로 서술된다
(2장 Best Practices for Data Providers, p.53-54):[^strengholt2023-dms]

- **애플리케이션 기술 세부를 감춘다** — 소비자가 물리 데이터 모델의 전문가가 되거나
  애플리케이션 기능을 재구현할 필요가 없어야 한다. 마이그레이션 정보·로깅·스키마 같은
  내부 기술 데이터는 걸러 낸다.[^strengholt2023-dms]
- **집중적 소비에 최적화한다** — 끝없는 부모/자식 구조의 고도 정규화 데이터를 넘기지
  않는다. 더 비정규화하고 직관적으로 묶으며, 이름 규칙과 형식 불일치는 미리 해소한다.[^strengholt2023-dms]
- **인터페이스는 성숙하고 안정적이어야** 한다 — 자주 바뀌는 도메인 범위는 더 안정적인
  범위로 추상화하고, 스키마는 일정 수준의 호환성을 제공한다.[^strengholt2023-dms]
- **패턴 전반에서 데이터가 일관**되어야 한다 — 같은 데이터가 여러 번 노출되더라도
  `customer address` 같은 요소는 모든 패턴에서 같아야 한다.[^strengholt2023-dms]

이것이 데이터 레이크와 갈리는 지점이다. 레이크는 원천에서 1대1 복사한 원시 데이터를
그대로 하류에 쓰게 하므로 데이터와 인터페이스가 원천 시스템에 강하게 결합되고,
**원천이 바뀌면 프로덕션 파이프라인이 즉시 깨진다**
(2장 Best Practices for Data Providers, p.54).[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"
