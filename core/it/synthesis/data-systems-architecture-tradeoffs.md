---
type: synthesis
title: 데이터 시스템 아키텍처 트레이드오프
description: 운영계와 분석계, 클라우드와 자체 호스팅, 분산과 단일 노드와 마이크로서비스(경계·통신·계약·저장소 배치·전달·UI 경계), 그리고 사업의 요구와 사용자의 요구 사이의 선택을 모으는 허브
generated: { by: "human:me", at: "2026-08-10T21:00:00Z" }
---

# 데이터 시스템 아키텍처 트레이드오프

정답이 하나가 아닌 선택들을 모은다. 각 페이지가 한 축을 맡고, 그 축의
장단점과 언제 어느 쪽을 고르는지를 다룬다.

## 무엇을 아키텍처라 부르는가

- [데이터 아키텍처의 정의](../concepts/data-architecture-defined.md) — 엔터프라이즈 아키텍처의 부분집합이라는 위치, 일방통행문과 양방향문, 운영 아키텍처와 기술 아키텍처
- [좋은 데이터 아키텍처의 아홉 원칙](../concepts/good-data-architecture-principles.md) — 공통 구성 요소·실패 계획·확장성·리더십·되돌릴 수 있는 결정·보안·FinOps
- [기술 선택의 기준](../concepts/technology-selection-criteria.md) — 아키텍처가 정해진 뒤 도구를 고르는 열 가지 축과 벤치마크 비판
- [FinOps와 비용 최적화](../concepts/finops-and-cost-optimization.md) — TCO·TOCO·capex와 opex, 그리고 지출을 운영으로 다루는 실무

## 아키텍처의 유형들

- [람다 아키텍처와 카파 아키텍처](../concepts/lambda-and-kappa-architecture.md) — 배치와 스트림을 합치려는 두 제안과 그 뒤를 이은 데이터플로 모델
- [데이터 메시](../concepts/data-mesh.md) — 중앙집중 플랫폼을 도메인 소유권으로 뒤집는 제안(개관). 원칙별 깊이는 [데이터 메시 원칙](data-mesh-principles.md) 허브가 받는다
- [IoT 데이터 아키텍처](../concepts/iot-data-architecture.md) — 사람이 아니라 장치가 데이터를 만드는 쪽

## 운영계와 분석계

- [EDW](../concepts/enterprise-data-warehouse.md) — 운영계와 분석계를 왜 가르며 어떤 아키텍처들이 그 요구를 감당했나
- [데이터 레이크](../concepts/data-lake.md) — 스키마를 강제하지 않는 분석 저장소와 원시 데이터 우선 원칙
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 무엇이 정본이고 무엇이 다시 만들 수 있는 사본인가

## 클라우드와 자체 호스팅

- [클라우드와 자체 호스팅](../concepts/cloud-versus-self-hosting.md) — 만들 것인가 살 것인가, 그리고 통제권을 잃는 대가
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 서비스 계층화, 저장과 연산의 분리, 멀티테넌시

## 분산과 단일 노드

- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 여러 기계로 갈 아홉 가지 이유와 가지 말아야 할 이유
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 서비스마다 자기 데이터베이스를 두는 이유와 그 대가
- [모놀리스와 모듈](../concepts/monolith-versus-modular.md) — 한 지붕 아래 다 둘 것인가 갈아 끼울 수 있는 조각으로 쪼갤 것인가, 그리고 모놀리스의 세 종류
- [독립 배포 가능성](../concepts/independent-deployability.md) — 마이크로서비스를 정의하는 성질이자 쪼개기의 목표
- [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md) — 쪼갠다면 경계를 어디에 그을 것인가
- [마이크로서비스의 고통과 채택 판단](../concepts/microservice-pain-points-and-adoption.md) — 그 쪼개기가 청구하는 비용과 누구에게 맞는가의 판단
- [마이크로서비스 경계의 대안 넷](../concepts/microservice-boundary-alternatives.md) — 업무 도메인 말고 무엇으로 가를 수 있는가(변동성·데이터·기술·조직)와 섞어 쓰기
- [서비스 결합의 네 종류](../concepts/service-coupling-types.md) — 서비스 경계를 넘는 결합의 목록과 무엇이 불가피하고 무엇이 병리적인가
- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 쪼갠 서비스들이 무엇으로 말하는가. 동기 블로킹·비동기 논블로킹·요청-응답·이벤트 주도·공통 데이터라는 다섯과 각각을 언제 고르는가
- [마이크로서비스 인터페이스 기술의 다섯 조건](../concepts/microservice-interface-criteria.md) — 스타일을 정한 다음 기술에 요구할 것들. 후진 호환·명시적 인터페이스·기술 중립·소비자 편의·내부 은닉
- [모놀리스 분해 패턴](../concepts/monolith-decomposition-patterns.md) — 쪼개기로 했을 때 무엇을 먼저 뽑고 어떤 장치로 옮기는가. 교살자 무화과·병행 운영·기능 토글
- [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md) — 데이터베이스를 쪼개면 깨지는 것들(조인·무결성·트랜잭션·도구)과 리포팅 데이터베이스
- [계약을 깨는 변경의 관리](../concepts/managing-breaking-api-changes.md) — 서비스 계약을 깨는 변경이 불가피할 때의 선택지 셋(보조 맞춘 배포·판 공존·옛 인터페이스 흉내)과 유예를 미리 합의하는 사회적 계약
- [API 게이트웨이와 서비스 메시](../concepts/api-gateway-and-service-mesh.md) — 테두리를 넘는 남북 트래픽과 안쪽의 동서 트래픽에 각각 놓이는 중개자, 그리고 거기에 업무 로직을 넣지 말라는 규칙
- [마이크로서비스 소스와 빌드의 배치](../concepts/microservice-source-layout.md) — 쪼갠 서비스들의 소스 코드와 빌드를 저장소 하나에 둘 것인가 서비스마다 둘 것인가, 그리고 그 선택이 독립 배포 가능성에 거는 조항
- [지속적 통합과 지속적 전달](../concepts/continuous-integration-and-delivery.md) — 그 배치가 촉발하는 통합과 파이프라인. 도구를 들여놓은 것과 실천하는 것을 가르는 세 물음, 아티팩트를 한 번만 만든다는 조항
- [마이크로서비스 배포의 다섯 원칙](../concepts/microservice-deployment-principles.md) — 그 파이프라인이 실어 나른 것을 실제로 놓을 때 지키는 조문 다섯. 격리 실행, 자동화 집중, 코드형 인프라, 무중단 배포, 원하는 상태 관리
- [마이크로서비스 배포 선택지](../concepts/microservice-deployment-options.md) — 그 조문으로 재는 수단의 사다리. 물리 기계부터 가상 기계와 컨테이너와 PaaS와 FaaS까지, 그리고 FaaS가 마이크로서비스를 논리 개념으로 바꾸는 자리
- [컨테이너 오케스트레이션과 쿠버네티스](../concepts/container-orchestration-and-kubernetes.md) — 컨테이너를 여러 기계에 걸쳐 돌리는 층이 떠맡는 일과 쿠버네티스의 핵심 개념, 그리고 들일 것인가의 판단
- [프로덕션에서의 테스트](../concepts/testing-in-production.md) — 그렇게 놓은 것을 프로덕션에서 시험한다는 것. 이미 하면서 테스트라 부르지 않던 넷과 그것을 안전하게 만드는 조건, 그리고 테스트를 더 쌓는 노력과 빨리 고치는 능력 사이의 저울
- [회복력의 네 개념](../concepts/resilience-four-concepts.md) — 그렇게 놓은 것이 얼마나 잘 버티는가를 재는 틀. 견고함·되튐·우아한 확장성·지속적 적응력으로 가르고, 쪼갠 구조가 사 오는 것이 거의 견고함뿐이라는 판정
- [확장의 네 축](../concepts/four-axes-of-scaling.md) — 그렇게 놓은 것이 부하를 받게 됐을 때 무엇을 움직이는가. 기계를 키우는 것과 같은 것을 여럿 두는 것과 데이터의 속성으로 가르는 것과 일의 종류로 가르는 것, 그리고 다른 가능성을 소진하기 전에는 쪼개지 말라는 순서
- [분산 체계에서의 캐싱](../concepts/caching-in-distributed-systems.md) — 그 확장과 별개로 앞선 결과를 들고 있는 최적화. 클라이언트 쪽과 서버 쪽과 요청 캐시, 무효화 다섯, 그리고 가능한 한 적은 자리에 캐시하라는 황금률
- [안정성 패턴](../concepts/stability-patterns.md) — 그 견고함을 실제로 사 오는 기제 여덟. 하류 하나의 느림이 체계 전체를 끌어내리지 않게 하는 시간 초과·재시도·벌크헤드·서킷 브레이커·격리·중복·미들웨어·멱등성
- [관측 가능성과 모니터링](../concepts/observability-versus-monitoring.md) — 그렇게 놓은 것이 프로덕션에서 무엇을 하고 있는지 알아내는 능력. 모니터링이라는 활동과 관측 가능성이라는 성질을 가르는 축과, 도구를 고르는 다섯 기준
- [지표의 카디널리티](../concepts/metrics-cardinality.md) — 그 성질을 지표 쪽에서 떠받치는 조건. 나중에 지을 질문을 위해 무엇을 몇 차원으로 저장해 둘 것인가
- [마이크로서비스 보안의 원칙과 기본기](../concepts/microservice-security-principles.md) — 쪼개면 공격 표면이 넓어지는 동시에 심층 방어의 자리도 늘어난다는 역설과, 그 위에 세우는 원칙들과 기본기 셋
- [자격 증명과 비밀의 수명 주기](../concepts/credentials-and-secrets-lifecycle.md) — 쪼개면 사람 수는 그대로인데 자격 증명만 폭증한다는 문제와 그것을 다루는 수명 주기
- [암묵적 신뢰와 제로 트러스트](../concepts/zero-trust-and-implicit-trust.md) — 서비스 사이 호출을 어디까지 믿을 것인가의 두 사고방식과 그 사이의 정도
- [전송 중 데이터와 정지 데이터의 보호](../concepts/securing-data-in-transit-and-at-rest.md) — 쪼개면 데이터가 더 많이 돌아다닌다는 대가와 그것을 흐를 때와 앉아 있을 때 각각 지키는 법
- [서비스 사이 인증과 인가](../concepts/service-to-service-authentication-and-authorization.md) — 인가를 상류 게이트웨이에 모으면 독립 배포 가능성이 깨진다는 판정과 그것을 내려보내는 수단
- [사용자 인터페이스 분해 패턴](../concepts/ui-decomposition-patterns.md) — **이 축의 UI 경계 페이지.** 쪼갠 서비스 앞의 화면을 누가 소유하고 무엇을 단위로 쪼개는가. 모놀리식 프런트엔드와 마이크로 프런트엔드와 페이지 기반과 위젯 기반, 그리고 각각을 언제 쓰는가까지만 담고 프런트엔드 공학 자체는 담지 않는다
- [프런트엔드를 위한 백엔드](../concepts/backend-for-frontend.md) — **같은 UI 경계의 서버 쪽 절반.** UI마다 다른 호출 집계와 걸러 내기를 어디에 둘 것인가. 중앙 집약 게이트웨이가 앓는 문제 셋과 사용자 경험 하나에 백엔드 하나를 두는 답, 그리고 게이트웨이에 집계를 넣지 말라는 조문이 여기서 풀리는 경계

## 사업의 요구와 사용자의 요구

데이터를 더 모을수록 얻는 것이 있고, 그 데이터의 대상이 되는 사람이 잃는 것이 있다.
이 축은 성능이 아니라 사람을 저울에 올린다.

- [공학 윤리와 책임](../concepts/engineering-ethics-and-responsibility.md) — 시스템을 만드는 사람이 그 결과에 지는 책임과 윤리가 체크리스트가 아닌 이유
- [예측 분석과 알고리즘의 해악](../concepts/predictive-analytics-and-algorithmic-harm.md) — 데이터로 사람에 대한 결정을 자동화할 때의 편향·책무·피드백 루프
- [감시와 동의](../concepts/surveillance-and-consent.md) — 행동 추적이 감시가 되는 지점과 "안 쓰면 된다"가 성립하지 않는 이유
- [결정권으로서의 프라이버시](../concepts/privacy-as-a-decision-right.md) — 프라이버시가 비밀 유지가 아니라 선택권이라는 정의와 그 권리의 이전
- [위험 자산으로서의 데이터](../concepts/data-as-a-hazardous-asset.md) — 쌓아 둔 개인 데이터가 지는 위험, 산업혁명 비유, 데이터 최소화와 규제

## 이어지는 허브

- [데이터플로 아키텍처](dataflow-architecture.md) — 여러 시스템을 이어 붙이기로 했을 때의 그다음 선택들
- [데이터 메시 원칙](data-mesh-principles.md) — 위 유형 중 하나를 원전 수준으로 펼친 쪽
