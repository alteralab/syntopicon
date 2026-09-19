---
type: concept
title: 이벤트 루프에서 가상 스레드로 덜어내기
description: 이벤트 루프 위에 선 프레임워크가 블로킹 작업을 다루는 방식 — 쿼커스가 Vert.x 위에서 전역이 아니라 엔드포인트 단위로 가상 스레드를 켜는 이유, @RunOnVirtualThread가 이벤트 루프의 응답성을 지키는 기제, 프레임워크가 대신 맡는 가상 스레드 수명 주기, 그리고 리액티브 반환값을 가상 스레드에서 막고 기다리는 자리
generated: { by: "claude-opus-5", at: "2026-09-05T23:30:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 이벤트 루프에서 가상 스레드로 덜어내기

- [버전 조건](#버전-조건)
- [이벤트 루프 위에 선 프레임워크](#이벤트-루프-위에-선-프레임워크)
- [전역이 아니라 선별](#전역이-아니라-선별)
- [이벤트 루프의 응답성을 지키는 기제](#이벤트-루프의-응답성을-지키는-기제)
- [리액티브 값을 가상 스레드에서 기다리기](#리액티브-값을-가상-스레드에서-기다리기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **이벤트 루프로 도는 프레임워크는 블로킹 작업을 어디로 보내며, 가상 스레드가
그 자리에 오면 무엇이 달라지는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 애너테이션 이름과 API 모양은 이 소스가 쓰는 쿼커스 판의 것이다.
> 소스가 쿼커스의 판 번호를 적지 않으므로 아래 서술의 프레임워크 쪽 경계는 확정할 수 없다 —
> 채택 전에 쓰는 판의 문서를 확인해야 한다.

## 이벤트 루프 위에 선 프레임워크

- 쿼커스(Quarkus)의 자리부터 저자가 짚는다 — 개발자 생산성과 빠른 기동 시간과 효율적인 성능을
  앞세운 2025년 저술 시점 자바 프레임워크이고, 마이크로서비스와 서버리스 애플리케이션에 알맞다. Vert.x 위에
  리액티브 프로그래밍 패러다임으로 지어졌으며, 가상 스레드 지원을 의도적이고 명시적으로 통합했다
  (7장, p.302).[^rahman2025] 그 패러다임의 정의는
  [리액티브 프로그래밍이라는 패러다임](../concepts/reactive-programming-paradigm-definition.md)에
  있다.
- **밑에 깔린 모델이 다르다는 것이 이 페이지의 전제다** — 쿼커스는 Vert.x를 밑바탕 리액티브 엔진으로
  쓰는데, Vert.x의 이벤트 루프 동시성 모델은 전통적인 요청당 스레드 모델과 다르다 (7장,
  p.303).[^rahman2025] 그 이벤트 루프의 부품은
  [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md)에, 그 위에서 지켜야 하는
  규율은 [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md)에
  있다.

## 전역이 아니라 선별

- 켜는 방식부터 갈린다 — 전역적인 접근과 달리 쿼커스는 특정 애너테이션을 통해 가상 스레드를 겨냥해
  들이는 길을 준다. 개발자가 메서드에 `@RunOnVirtualThread`를 붙여 특정 엔드포인트나 서비스에만
  선택적으로 가상 스레드를 켤 수 있고, 그 애너테이션은 붙은 메서드를 전통적인 플랫폼 스레드가 아니라
  가상 스레드에서 실행하라고 쿼커스에 지시한다 (7장, p.302).[^rahman2025] 다른 프레임워크의 켜는
  방식과 나란히 놓은 자리는
  [프레임워크가 가상 스레드를 켜는 방식](../concepts/enabling-virtual-threads-in-frameworks.md)에
  있다.
- 수명 주기는 프레임워크가 맡는다 — 쿼커스가 이 가상 스레드들의 생성과 실행과 수명 주기 관리를
  효율적으로 처리한다 (7장, p.302).[^rahman2025]
- 통합 경로도 리액티브 쪽이다 — 쿼커스는 주로 자기 리액티브 확장을 통해 가상 스레드를 통합해
  리액티브 프로그래밍과 가상 스레딩을 결합하며, 그것이 빠른 기동과 효율적인 자원 사용 덕에
  마이크로서비스와 서버리스 환경에 특히 알맞게 만든다는 것이 저자의 정리다 (7장,
  p.302).[^rahman2025]

## 이벤트 루프의 응답성을 지키는 기제

- **덜어내기가 이 애너테이션의 일이다** — `@RunOnVirtualThread`는 특정 태스크를 Vert.x 이벤트
  루프에서 가상 스레드로 덜어내게 해 주고, 그래서 블로킹 연산이 이벤트 루프의 응답성을 해치지
  못하게 막는다. 리액티브 프로그래밍과 가상 스레드의 이 결합이 동시성을 효율적으로 다루는 쿼커스의
  능력을 키운다 (7장, p.303).[^rahman2025]
- 이것이 [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md)이
  요구하던 것에 대한 답이다. 규율은 "루프 스레드에서 막지 마라"이고, 가상 스레드는 그 막힘을
  **옮겨 놓을 값싼 자리**를 준다.
- 실행 결과에서 그 자리가 드러난다 — 애너테이션을 붙인 메서드의 로그에 찍히는 스레드 이름이
  `quarkus-virtual-thread-N` 꼴이고, 그 스레드가 포크조인 풀의 워커 위에서 돈다 (7장,
  pp.303–304).[^rahman2025] 그 워커의 정체는
  [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md)에 있다.

## 리액티브 값을 가상 스레드에서 기다리기

- 저자가 쿼커스의 리액티브 프로그래밍 능력과 가상 스레드를 한 메서드 안에서 섞는다 (7장,
  pp.305–306).[^rahman2025]

  ```java
  @Path("/reactive")
  public class ReactiveResource {
      @Inject
      HelloService helloService;

      @GET
      @Path("/hello")
      @RunOnVirtualThread
      @Produces(MediaType.TEXT_PLAIN)
      public String hello() {
          return helloService.getHello()
                  .await()
                  .atMost(Duration.ofSeconds(5));
      }
  }
  ```

- 무슨 일이 벌어지는지를 저자가 풀어 적는다 — `ReactiveResource`의 `hello()` 메서드가 리액티브
  REST 클라이언트로 외부 서비스를 호출하고, `getHello()`는 지연된 계산을 나타내는 `Uni<String>`을
  돌려준다. `hello()` 안에서 `await().atMost(Duration.ofSeconds(5))`가 결과가 나오거나 시간이 다할
  때까지 가상 스레드를 막는다 (7장, p.306).[^rahman2025]
- **막는 쪽이 가상 스레드라는 것이 요점이다.** 리액티브 반환값을 기다리는 일이 이벤트 루프
  스레드였다면 규율 위반이지만, 값싼 가상 스레드 위에서라면 막아도 된다. 같은 맞바꿈을 저자가 책
  전체 규모로 재는 자리가
  [가상 스레드 시대에 리액티브가 남는 자리](../concepts/reactive-and-virtual-threads-coexistence.md)이고,
  저자가 그 장에서 꼽은 수렴의 조짐이 여기 실물로 나온 셈이다.

## 이어지는 페이지

- [프레임워크가 가상 스레드를 켜는 방식](../concepts/enabling-virtual-threads-in-frameworks.md) —
  선별 애너테이션이 놓인 세 갈래
- [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md) — 이
  덜어내기가 지키려는 규칙
- [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md) — 그 루프의 부품
- [가상 스레드 시대에 리액티브가 남는 자리](../concepts/reactive-and-virtual-threads-coexistence.md)
  — 두 길을 나란히 놓고 고르는 자리
- [리액티브 프로그래밍이라는 패러다임](../concepts/reactive-programming-paradigm-definition.md) —
  쿼커스가 서 있는 패러다임의 정의
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  이어지는 허브
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 7장 "Modern Frameworks Utilizing Virtual Threads" —
    "Quarkus"(pp.302–306). 인용한 `ReactiveResource`는 원문(p.306)에서 `import` 줄과 같은 파일에
    함께 실린 `HelloService`·`ExternalService` 선언을 덜어 냈다. 개념당 대표 코드 하나 규칙에 따라
    `VirtualThreadApp`(p.303), `RemoteService`(p.304), `SimpleHttpServer`(pp.304–305)는 옮기지
    않았다. 콘솔 로그 출력(pp.303–304)은 실행 결과이므로 서술로만 담았다. 이 절에는 그림이 없다.
