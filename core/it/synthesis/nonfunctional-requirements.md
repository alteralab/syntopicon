---
type: synthesis
title: 비기능 요건
description: 기능 목록 바깥에서 시스템의 값어치를 정하는 요건들을 모으는 허브 — 성능을 재는 지표와 분포, 그 지표를 얻으려고 부하를 거는 실험의 설계, 그 분포의 꼬리를 없애는 대신 견디는 기법들, 트리거가 사라져도 스스로 유지되는 과부하라는 실패 모델, 잘못돼도 계속 도는 것과 그것을 사 오는 기제들, 악의적 당사자를 상정했을 때 지켜야 하는 것, 부하가 늘 때 대처하는 능력, 오래 살려 두는 비용, 그 전부를 프로덕션에서 알아낼 수 있게 만드는 성질, 그리고 이 이름이 아키텍처 특성과 같은 것을 가리킨다는 사실과 그 특성이 퇴화하지 않았는지 재는 기제
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
---

# 비기능 요건

애플리케이션이 **무엇을 하는가**가 아니라 **얼마나 빠른가·얼마나 잘 버티는가·얼마나
자라는가·얼마나 오래 손볼 만한가**를 다루는 페이지들을 모은다. 어느 것도 하나의 수로
답해지지 않으며, 각 페이지가 그 어휘를 정의한다.

**이 허브의 이름과 "아키텍처 특성"은 같은 것을 가리킨다.** 한 소스가 그 동일성을 명시한다 —
비기능 요건, 횡단 요구사항, 시스템 품질 속성, 아키텍처 특성은 조직마다 다른 이름을 쓸 뿐
서로 다른 개념이 아니라는 것이다.

- [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md) — **여기 모인 속성들이
  시간에 따라 퇴화하지 않았다는 것을 객관적으로 확인하는 기제.** 정의와 여섯 분류 축, 그리고
  모니터링 도구를 쓰는 것만으로는 이것이 되지 않는다는 경계. 이 허브의 성능·신뢰성·보안·확장성
  절 전부가 그 기제의 적용 대상이다
- [진화적 아키텍처](../concepts/evolutionary-architecture.md) — 그 기제가 떠받치는 규정. 진화
  가능성을 **다른 모든 특성을 감싸는 메타 특성**으로 놓는 배치가 이 허브의 구성과 맞닿는다
- 두 페이지의 자리는 [소프트웨어 아키텍처](software-architecture.md)의 진화와 거버넌스 절이고,
  여기서는 이 허브의 속성들을 재는 쪽으로만 가리킨다

## 성능

- [응답 시간과 처리량](../concepts/response-time-and-throughput.md) — 두 지표의 정의, 큐잉이
  만드는 곡선, 지연과 응답 시간을 갈라 쓰는 어휘
- [지연의 백분위](../concepts/latency-percentiles.md) — 평균 대신 중앙값과 p95·p99를 보는
  이유, 꼬리 지연 증폭, 백분위를 계산하는 법
- [서비스 수준 목표](../concepts/service-level-objectives.md) — 지표를 약속으로 바꾸는
  SLI·SLO·SLA·OLA와 소진율 경보
- [분산 체계에서의 캐싱](../concepts/caching-in-distributed-systems.md) — 앞선 결과를 저장해
  다시 계산하지 않는 최적화. 어디에 두고 언제 버릴 것인가, 그리고 캐시를 겹치면 낡음이
  누적된다는 셈

## 부하를 어떻게 걸어 재는가

- [개방 부하 모델과 폐쇄 부하 모델](../concepts/open-and-closed-load-models.md) — 다음 요청을
  무엇이 낳는가로 갈리는 세 모델, 각 모델에서 서버 부하가 무엇의 곱인가
- [부하 모델을 공정히 비교하는 실험 설계](../concepts/load-model-experiment-design.md) — 무엇을
  고정하고 무엇을 움직여야 두 모델을 같은 조건에서 견줄 수 있는가
- [응답 시간을 가르는 세 원칙](../concepts/open-vs-closed-response-time-principles.md) — 같은
  부하에서 응답 시간이 자릿수로 갈리는 이유, 수렴 속도, 변동성의 비대칭
- [스케줄링 효과가 부하 모델에 따라 갈리는 자리](../concepts/scheduling-under-open-and-closed-models.md) —
  짧은 작업 우선이 개방에서만 크게 듣는 이유
- [부분 개방 모델과 세션 길이](../concepts/partly-open-model-and-session-length.md) — 세션당
  요청 수로 어느 모델이 맞는지 고르는 법, 사고 시간이 무관하다는 발견

## 꼬리 지연을 견디는 법

- [꼬리 내성이라는 설계 태도](../concepts/tail-tolerance-as-a-design-stance.md) — 가변성을 없애는
  대신 견디자는 입장, 기법을 요청 안과 요청 사이로 가르는 두 시간 척도, 그 대가의 크기
- [지연 가변성이 생기는 자리](../concepts/latency-variability-sources.md) — 공유 자원과 배경
  데몬부터 전력 한계와 절전 모드까지, 부품이 흔들리는 원인 목록
- [부품의 가변성을 줄이는 공학](../concepts/reducing-component-variability.md) — 서비스 등급과
  얕은 큐, 요청 쪼개기, 배경 활동 동기화, 캐시가 꼬리를 다루지 못하는 이유
- [요청 안에서의 단기 적응](../concepts/tail-tolerant-short-term-adaptations.md) — 헤지 요청과
  묶인 요청, 그 부하를 묶는 지연 발송과 서버 간 취소
- [요청 사이의 장기 적응](../concepts/tail-tolerant-long-term-adaptations.md) — 마이크로 파티션,
  선택적 복제, 느린 기계를 빼되 그림자 요청으로 계속 재는 격리
- ["충분히 좋은" 결과와 카나리 요청](../concepts/good-enough-results-and-canary-requests.md) —
  결과가 부정확해도 되는 시스템에만 열리는 두 기법

## 과부하가 스스로 유지될 때

- [메타안정 장애의 정의와 세 상태](../concepts/metastable-failure-definition.md) — 트리거가
  사라져도 낫지 않는 과부하의 정의, 안정 상태와 취약 상태와 장애 상태의 경계
- [메타안정 장애의 트리거](../concepts/metastable-failure-triggers.md) — 부하를 올리는 트리거와
  용량을 내리는 트리거, 크기와 지속 시간이 회복과 장애를 가르는 폭
- [지속 효과와 증폭 기제](../concepts/sustaining-effects-and-amplification.md) — 재시도와 캐시
  미스와 느린 오류 처리와 가비지 컬렉션, 부하를 키우는 증폭과 용량을 깎는 증폭
- [취약 상태를 알아보는 법](../concepts/detecting-the-vulnerable-state.md) — 숨은 용량과 공표
  용량, 특성 지표, 취약도가 이분법이 아니라 정도라는 실험
- [공개 사후 분석에서 본 메타안정 장애](../concepts/metastable-failures-in-incident-reports.md) —
  열한 개 조직의 사건을 이 틀로 분류한 실증 표와 지속 시간 분포
- [메타안정 장애에서 복구하기](../concepts/recovering-from-metastable-failures.md) — 부하를
  안정 문턱 아래로 내리는 쪽과 문턱 자체를 올리는 쪽, 그리고 각각의 한계

## 신뢰성

- [신뢰성과 내결함성](../concepts/reliability-and-fault-tolerance.md) — 결함과 장애의 층위
  구분, 단일 장애점, 결함 주입과 카오스 엔지니어링
- [하드웨어·소프트웨어·사람의 결함](../concepts/hardware-software-and-human-faults.md) —
  세 원천의 발생률과 상관 구조, 무비난 사후 분석
- [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md) — 원격 통신에 대한
  가정들, 연쇄 장애와 메타안정 장애
- [프로덕션에서의 테스트](../concepts/testing-in-production.md) — 실패 확률을 0으로 내릴 수
  없다는 전제 위에서 복구 쪽에 노력을 거는 저울(MTBF 대 MTTR)과 프로덕션에서 무엇을 어떻게
  확인하는가
- [회복력의 네 개념](../concepts/resilience-four-concepts.md) — 회복력을 견고함·되튐·우아한
  확장성·지속적 적응력으로 가른 틀과, 소프트웨어 아키텍처가 그중 하나에만 답한다는 판정
- [안정성 패턴](../concepts/stability-patterns.md) — 그 견고함에 답하는 기제 여덟. 시간
  초과·재시도·벌크헤드·서킷 브레이커·격리·중복·미들웨어·멱등성과 각각을 어디에 쓰는가

## 관측 가능성

- [관측 가능성과 모니터링](../concepts/observability-versus-monitoring.md) — 프로덕션에서
  무슨 일이 벌어지는지 알아내는 능력을 활동이 아니라 체계의 성질로 다루는 자리, 그리고 그
  성질을 로그·지표·트레이스 "세 기둥"으로 환원하지 말라는 반대
- [로그와 트레이스](../concepts/logs-and-traces.md) — 흩어진 기록을 모으는 집계와 상관 ID,
  시계가 어긋나 순서를 믿을 수 없다는 한계, 그리고 그 한계를 받는 분산 추적
- [지표의 카디널리티](../concepts/metrics-cardinality.md) — 수치를 어떤 구조로 모아 두어야
  나중에 생각해 낸 질문을 던질 수 있는가

## 보안

- [마이크로서비스 보안의 원칙과 기본기](../concepts/microservice-security-principles.md) — 최소
  권한과 심층 방어, 보안 통제를 예방·탐지·대응으로 가르는 분류, 사이버 보안의 다섯 기능, 그리고
  패치와 백업과 재구축
- [자격 증명과 비밀의 수명 주기](../concepts/credentials-and-secrets-lifecycle.md) — 비밀의
  생성부터 폐기까지, 교체가 아픈 이유와 범위를 좁히는 일의 대가
- [암묵적 신뢰와 제로 트러스트](../concepts/zero-trust-and-implicit-trust.md) — 네트워크 안의
  호출을 어디까지 믿을 것인가, 그리고 그것이 양자택일이 아니라 정도라는 주장
- [전송 중 데이터와 정지 데이터의 보호](../concepts/securing-data-in-transit-and-at-rest.md) —
  네트워크를 흐를 때의 관심사 넷과 디스크에 앉아 있을 때의 조문 넷
- [서비스 사이 인증과 인가](../concepts/service-to-service-authentication-and-authorization.md) —
  단일 사인온과 혼란한 대리인 문제, 인가를 상류에 모을 것인가 내려보낼 것인가
- [밖은 위험하다](../concepts/stay-safe-out-there.md) — 같은 물음의 개발자 실천 층. 공격 표면과
  안전한 기본값과 비밀번호 안티패턴

## 확장성

- [확장성과 부하](../concepts/scalability-and-load.md) — 부하를 서술하는 법, 선형 확장성,
  공유 메모리·공유 디스크·무공유, 만능 비법이 없다는 전제 위의 원칙들
- [확장의 네 축](../concepts/four-axes-of-scaling.md) — 같은 물음을 결정 목록으로 가른 분류.
  기계를 키우는 것과 같은 것을 여럿 두는 것과 데이터로 가르는 것과 일의 종류로 가르는 것,
  각각이 성능과 견고함 가운데 무엇을 사 오는가, 그리고 오토스케일링과 다시 짓기
- [소셜 네트워크 홈 타임라인 사례](../concepts/social-network-home-timelines.md) — 읽을 때
  조인할 것인가 쓸 때 미리 만들 것인가를 수로 따진 사례

## 거버넌스

- [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md) — 위의 특성들이
  퇴화하지 않았다는 것을 객관적으로 확인하는 기제의 정의와 여섯 분류 축. **이 허브의 거의 모든
  절이 그 대상이 된다** — 저자들이 비기능 요건·횡단 요구사항·시스템 품질 속성·아키텍처 특성을
  서로 다른 개념이 아니라고 적기 때문이다
- [자동화된 아키텍처 거버넌스](../concepts/automated-architectural-governance.md) — 그 확인을
  수작업 검토가 아니라 빌드에서 도는 검사로 거는 일, 그리고 그 층위들

## 유지보수성

- [유지보수성](../concepts/maintainability.md) — 운영성·단순성·진화성, 추상화, 되돌릴 수 없음
