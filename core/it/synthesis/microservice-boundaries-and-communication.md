---
type: synthesis
title: 마이크로서비스 경계와 통신
description: 한 지붕 아래 둘 것인가 쪼갤 것인가의 판단과 독립 배포 가능성이라는 목표와 쪼개기가 청구하는 비용, 경계를 업무 도메인에 맞추는 어림법과 변동성·데이터·기술·조직이라는 대안 넷과 경계를 넘는 결합의 네 종류, 교살자 무화과와 병행 운영과 기능 토글로 뽑아내는 분해 절차와 데이터베이스를 가를 때 깨지는 조인·무결성·트랜잭션·도구, 쪼갠 서비스들이 무엇으로 말하는가의 다섯 스타일과 기술에 요구할 다섯 조건과 주소를 찾는 디스커버리와 남북·동서 트래픽의 중개자, 계약을 깨는 변경의 선택지 셋과 소비자 주도 계약, 그리고 쪼갠 서비스 앞의 화면을 누가 소유하는가의 UI 분해와 그 서버 쪽 절반인 프런트엔드를 위한 백엔드를 모으는 허브
generated: { by: "claude-opus-5", at: "2026-09-17T01:20:00Z" }
---

# 마이크로서비스 경계와 통신

- [이 허브의 범위](#이-허브의-범위) — 무엇이 여기 있고 무엇이 형제 허브의 몫인가
- [쪼갤 것인가](#쪼갤-것인가) — 한 지붕 아래 둘 것인가의 판단과 그 대가
- [경계를 어디에 긋는가](#경계를-어디에-긋는가) — 어림법과 대안 넷, 그리고 경계를 넘는 결합
- [쪼개는 절차](#쪼개는-절차) — 무엇을 먼저 뽑고 데이터베이스를 가를 때 무엇이 깨지는가
- [무엇으로 말하는가](#무엇으로-말하는가) — 통신 스타일과 기술 조건과 중개자
- [계약이 바뀔 때](#계약이-바뀔-때) — 깨는 변경의 선택지와 그것을 잡는 계약
- [화면 쪽 경계](#화면-쪽-경계) — UI 분해와 그 서버 쪽 절반
- [이웃 허브](#이웃-허브) — 이 허브가 맞닿는 축들

## 이 허브의 범위

여기 모인 것은 **조각의 경계를 어디에 긋고 그 조각들이 무엇으로 말하는가**다. 조각을 만들어
나르는 일은 [빌드와 배포와 전달](build-deploy-and-delivery.md)이, 그 조각을 돌보고 지키는 일은
[비기능 요건](nonfunctional-requirements.md)이, 그 일을 하는 사람은
[조직과 아키텍트](organizations-and-architects.md)가 맡는다. 부모 허브는
[소프트웨어 아키텍처](software-architecture.md)다.

## 쪼갤 것인가

- [모놀리스와 모듈](../concepts/monolith-versus-modular.md) — 한 지붕 아래 다 둘 것인가 갈아
  끼울 수 있는 조각으로 쪼갤 것인가, 그리고 모놀리스의 세 종류
- [독립 배포 가능성](../concepts/independent-deployability.md) — 마이크로서비스를 정의하는
  성질이자 쪼개기의 목표
- [마이크로서비스의 고통과 채택 판단](../concepts/microservice-pain-points-and-adoption.md) —
  그 쪼개기가 청구하는 비용과 누구에게 맞는가의 판단
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — **정본 자리는
  데이터 쪽이다.** 서비스마다 자기 데이터베이스를 두는 이유와 그 대가를 데이터 시스템의 물음으로
  세우고, [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md)에 산다
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — **정본 자리는 같은
  데이터 쪽 허브다.** 여러 기계로 갈 아홉 가지 이유와 가지 말아야 할 이유

## 경계를 어디에 긋는가

- [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md) — 쪼갠다면 경계를
  어디에 그을 것인가. 경계 컨텍스트가 가장 넓은 유효 경계이고 애그리게이트가 가장 좁으며 하위
  도메인이 안전한 기본값이라는 배치. **모델 쪽 어휘의 정본은
  [DDD 전략 설계](ddd-strategic-design.md)에 있다**
- [마이크로서비스 경계의 대안 넷](../concepts/microservice-boundary-alternatives.md) — 업무 도메인
  말고 무엇으로 가를 수 있는가(변동성·데이터·기술·조직)와 섞어 쓰기
- [서비스 결합의 네 종류](../concepts/service-coupling-types.md) — 서비스 경계를 넘는 결합의
  목록과 무엇이 불가피하고 무엇이 병리적인가. **이 어휘가 네트워크로 갈리기 전의 층은
  [복잡성과 모듈 설계](complexity-and-modular-design.md)에 있다**

- [아키텍처 퀀텀](../concepts/architectural-quantum.md) — **정본 자리는 부모 허브의 진화와 거버넌스
  절이다.** 같은 경계를 모델이 아니라 **독립 배포 가능한 단위와 그것이 끌고 가는 결합 지점**으로
  세는 잣대이고, 공유 데이터베이스나 단단히 결합된 화면 하나가 배포 단위 전체를 하나로 떨어뜨린다는
  셈법을 준다. 이 양식을 진화적 아키텍처의 모범으로 대 보는 사례도 그쪽에 있다
## 쪼개는 절차

- [모놀리스 분해 패턴](../concepts/monolith-decomposition-patterns.md) — 쪼개기로 했을 때 무엇을
  먼저 뽑고 어떤 장치로 옮기는가. 교살자 무화과·병행 운영·기능 토글
- [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md) — 데이터베이스를
  쪼개면 깨지는 것들(조인·무결성·트랜잭션·도구)과 리포팅 데이터베이스
- [아키텍처를 점진적으로 들이기](../concepts/adopting-architecture-incrementally.md) — 같은
  교살자 패턴을 레거시 이행의 절차로 적는 쪽. **정본 자리는
  [도메인 모델과 애플리케이션 계층](domain-model-and-application-layers.md)이다**

## 무엇으로 말하는가

- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 쪼갠
  서비스들이 무엇으로 말하는가. 동기 블로킹·비동기 논블로킹·요청-응답·이벤트 주도·공통
  데이터라는 다섯과 각각을 언제 고르는가
- [마이크로서비스 인터페이스 기술의 다섯 조건](../concepts/microservice-interface-criteria.md) —
  스타일을 정한 다음 기술에 요구할 것들. 후진 호환·명시적 인터페이스·기술 중립·소비자 편의·내부 은닉
- [서비스 디스커버리와 로드 밸런싱](../concepts/service-discovery-and-load-balancing.md) —
  주소를 찾고 부하를 나누는 다섯 가지 해법. **정본 자리는
  [인코딩과 진화](encoding-and-evolution.md)다**
- [API 게이트웨이와 서비스 메시](../concepts/api-gateway-and-service-mesh.md) — 테두리를 넘는
  남북 트래픽과 안쪽의 동서 트래픽에 각각 놓이는 중개자, 그리고 거기에 업무 로직을 넣지 말라는 규칙
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 동기 쪽에서 가장 흔히 고르는 것의
  설계 원칙과 채점. **정본 자리는 [인코딩과 진화](encoding-and-evolution.md)다**
- [사가 패턴](../concepts/saga-pattern.md) — 여러 서비스에 걸치는 업무 프로세스를 한 트랜잭션으로
  묶지 않고 푸는 쪽. **정본 자리는 [메시징 패턴](messaging-patterns.md)이고 같은 낱말을 다르게
  쓰는 두 소스의 대조표가 그 페이지에 있다**

## 계약이 바뀔 때

- [계약을 깨는 변경의 관리](../concepts/managing-breaking-api-changes.md) — 서비스 계약을 깨는
  변경이 불가피할 때의 선택지 셋(보조 맞춘 배포·판 공존·옛 인터페이스 흉내)과 유예를 미리
  합의하는 사회적 계약
- [소비자 주도 계약](../concepts/consumer-driven-contracts.md) — 그 계약이 실제로 깨졌는지를
  누가 어디서 잡는가. **정본 자리는 [인코딩과 진화](encoding-and-evolution.md)이고, 판정 근거의
  독립성 쪽 읽기는 [검증자 독립성](verifier-independence.md)에 있다**

## 화면 쪽 경계

- [사용자 인터페이스 분해 패턴](../concepts/ui-decomposition-patterns.md) — 쪼갠 서비스 앞의
  화면을 누가 소유하고 무엇을 단위로 쪼개는가. 모놀리식 프런트엔드와 마이크로 프런트엔드와
  페이지 기반과 위젯 기반, 그리고 각각을 언제 쓰는가까지만 담고 프런트엔드 공학 자체는 담지 않는다
- [프런트엔드를 위한 백엔드](../concepts/backend-for-frontend.md) — 같은 UI 경계의 서버 쪽 절반.
  UI마다 다른 호출 집계와 걸러 내기를 어디에 둘 것인가, 중앙 집약 게이트웨이가 앓는 문제 셋,
  그리고 게이트웨이에 집계를 넣지 말라는 조문이 여기서 풀리는 경계

## 이웃 허브

- [소프트웨어 아키텍처](software-architecture.md) — 부모 허브
- [빌드와 배포와 전달](build-deploy-and-delivery.md) — 그어 놓은 경계를 실제 배포 단위로 만드는 쪽
- [조직과 아키텍트](organizations-and-architects.md) — 그 경계가 팀 경계와 서로를 복제한다는 쪽
- [DDD 전략 설계](ddd-strategic-design.md) — 같은 경계를 모델이 통하는 범위로 긋는 축
- [메시징 패턴](messaging-patterns.md) — 비동기를 고른 뒤의 기제 층
- [데이터베이스 트랜잭션](database-transactions.md) — 쪼갠 데이터에 원자성이 남지 않는 쪽
