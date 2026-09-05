---
type: concept
title: CompletableFuture와 비동기 조합
description: Java 8이 조합 가능성과 사용 편의를 겨냥해 들인 비동기 API가 콜백 중심을 선언적 변환의 연속으로 바꾸는 방식과 포크조인 프레임워크 위에 선다는 사실, 오류 처리 메서드와 커스텀 실행자라는 통제 수단, 학습 투자와 여전히 막는 get과 다중 체인의 오류 전파와 역전된 실행 흐름의 디버깅이라는 대가, 그리고 값 하나에는 되고 데이터의 흐름에는 되지 않는다는 6장의 경계
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# CompletableFuture와 비동기 조합

- [무엇을 겨냥해 들어왔나](#무엇을-겨냥해-들어왔나)
- [체인으로 쓴 신용 점수 계산](#체인으로-쓴-신용-점수-계산)
- [장점](#장점)
- [단점과 한계](#단점과-한계)
- [기술 결정이 아니라 아키텍처 약속이다](#기술-결정이-아니라-아키텍처-약속이다)
- [값 하나에는 되고 흐름에는 되지 않는다](#값-하나에는-되고-흐름에는-되지-않는다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **비동기 작업을 이어 붙이는 일을 API가 대신해 주면 무엇이 쉬워지고 무엇이
어려워지는가.**

## 무엇을 겨냥해 들어왔나

- 실행자 프레임워크와 포크/조인 풀이 성능을 올려 주지만 복잡한 비동기 작업 흐름을 조합하는 일은
  여전히 번거롭다. 그 문제를 겨냥해 Java 8이 `CompletableFuture`를 들였고, 조합
  가능성(composability)과 쓰기 쉬움에 초점을 둔 클래스다 (1장, p.23).[^rahman2025]
  - 조합 가능성의 부재가 실행자의 남은 한계로 꼽힌 자리는
    [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)에 있다.
- 성격이 바뀐다 — 콜백이 많은 방식에서 선언적이고 함수형인 접근으로 옮겨 가고, 풍부한 API가 여러
  비동기 연산을 힘들이지 않고 이어 붙이게 해 준다. 저자는 그것이 읽기 쉬움과 유지보수성을 올린다고
  적는다 (1장, p.23).[^rahman2025]

## 체인으로 쓴 신용 점수 계산

- 앞의 예제를 이 API로 다시 쓰면 메서드 호출의 나열이 변환의 체인이 된다 (1장,
  p.23).[^rahman2025]

  ```java
  public Credit calculateCreditWithCompletableFuture(Long personId)
          throws InterruptedException, ExecutionException {
      return runAsync(() -> importantWork())
          .thenCompose(aVoid -> supplyAsync(() -> getPerson(personId)))
          .thenCombineAsync(supplyAsync(() -> getAssets(getPerson(personId))),
              (person, assets) -> calculateCredits(assets, getLiabilities(person)))
          .get();
  }
  ```

  - 버전 조건: Java 8 이상 — `CompletableFuture`가 들어온 릴리스다 (1장, p.23).[^rahman2025]
- 저자가 다섯 단계로 읽는다 — 독립적인 작업을 비동기로 시작하고, 그것이 끝나면 사람 데이터를 비동기로
  가져오기 시작하고, 그 사람 데이터를 병렬로 가져온 자산과 결합하고, 결합한 결과로 최종 점수를
  계산하고, 마지막에 막으면서 결과를 기다린다 (1장, pp.23–24).[^rahman2025]
- #hypothesis 이 예제 코드는 `getPerson`을 체인 안과 자산 조회 안에서 두 번 부르고 `getLiabilities`를
  결합 함수 안에서 동기로 부른다. 앞선 실행자판이 그 둘을 병렬로 보냈던 것과 다르며, 저자는 이
  차이를 언급하지 않고 측정값도 싣지 않는다. 원문 그대로 보존한다 (1장, p.23).[^rahman2025]

## 장점

- 저자가 꼽는 첫 이득이 구조다 — 엉킨 중첩 콜백이나 작업 객체의 방대한 클래스 계층 대신 작업 흐름을
  변환과 중간 계산의 연속으로 정의하게 된다. 읽기 쉬움과 유지보수성이 오르고, 비동기가 중심인
  애플리케이션에서 버그가 날 여지가 준다 (1장, p.24).[^rahman2025]
- 밑바탕이 포크/조인 프레임워크다 — 그 위에 서서 최적화된 작업 훔치기를 활용하므로 작업 분배가
  효율적이고 부하 아래에서 확장성이 낫다 (1장, p.24).[^rahman2025] 그 기제는
  [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md)에 있다.
- 오류 처리를 명시적으로 통제할 수단이 내장되어 있다 — `exceptionally`와 `handle`과
  `whenComplete`가 그것이다 (1장, p.24).[^rahman2025]
- 특정 작업 부하에 맞춰 스레드 관리를 조율하도록 커스텀 실행자를 넣을 수도 있다 (1장,
  p.24).[^rahman2025]
- 경계에서 막는 `get()`이 때로 필요하더라도 파이프라인의 대부분은 논블로킹으로 남을 수 있고, 그래서
  응답성과 자원 효율이 높은 코드가 된다 (1장, p.24).[^rahman2025]

## 단점과 한계

- 발상의 전환이 필요하다 — 명령형 스타일에 이미 익숙하다면 풍부한 API를 뜻있게 쓰기까지 상당한
  투자가 필요하고, 어느 메서드를 어디에 쓸지와 값 전달 기법을 알아내야 한다. 시간과 연습이 많이
  들고 그만큼 제대로 쓰지 못할 가능성도 따라온다 (1장, p.24).[^rahman2025]
- `get()`은 여전히 막는 메서드다. 필요하지만 아껴 쓰지 않으면 비동기 프로그래밍의 이점을 통째로
  무너뜨리는 막힘을 흐름에 들일 수 있다 (1장, p.24).[^rahman2025]
- 의존이 둘 이상인 다중 체인에서는 오류를 전파하고 확인해 복구해야 하는데, 설계를 제대로 하지 않으면
  디버깅이 큰 악몽이 될 수 있다 (1장, p.24).[^rahman2025]
- 체인 스타일 코드의 디버깅이 또 다른 난제다 — IDE의 기본 디버깅 도구에 익숙하다면 코드를 한 단계씩
  밟고 특정 지점에 중단점을 걸고 한 걸음 되돌아가 문맥을 보는 일이 매우 어려워진다. 비동기 코드의
  실행 흐름이 역전되고 모호해서, 줄 단위로 순서대로 실행되지 않기 때문이다 (1장,
  p.24).[^rahman2025]

## 기술 결정이 아니라 아키텍처 약속이다

- 저자가 별도의 상자에서 질문을 하나 세운다 — 비동기 프로그래밍의 이득은 분명하고
  `CompletableFuture`와 리액티브 프레임워크가 강력한 기능을 주지만, 우리 조직이 이 복잡성을 감당할
  준비가 되었는가 (1장, p.25).[^rahman2025]
- 근거가 셋이다 — 비동기 프로그래밍은 애플리케이션을 설계하고 디버깅하고 유지하는 방식을 근본에서
  바꾸며, 성능의 이득에는 인지 부담과 디버깅의 어려움과 아키텍처 복잡성이라는 큰 비용이 따른다.
  그래서 채택 전에 팀이 깨끗한 코드 원칙을 지키고 복잡한 오류 시나리오를 다루고 비동기 호출 체인을
  디버깅할 경험이 있는지를 따져 보라고 적는다 (1장, p.25).[^rahman2025]
- 결론이 강하다 — 이것은 단순한 기술적 결정이 아니라 애플리케이션 수명 주기의 모든 면에 영향을 주는
  아키텍처 수준의 약속이므로, 팀의 역량과 애플리케이션의 실제 성능 요구에 따라 신중히 고르라는
  것이다 (1장, p.25).[^rahman2025]

## 값 하나에는 되고 흐름에는 되지 않는다

6장이 이 API의 경계를 한 문장으로 긋는다.

- 저자가 콜백 지옥의 해법으로 이 API를 다시 데려온 뒤 스스로 묻는다 — 그러면 I/O 스레드를 막는
  문제가 풀린 것인가. 아직 고려하지 않은 것이 데이터의 흐름이라는 것이 그 답이다 (6장
  "Asynchronous APIs", p.278).[^rahman2025]
- 경계가 여기서 특정된다 — `CompletableFuture`는 값 하나를 돌려주는 메서드에는 아름답게 동작하지만,
  한 번의 응답이 아니라 결과의 연속을 다뤄야 할 때는 다르다. 저자는 그 자리가 리액티브 프레임워크가
  가장 빛나는 곳이라고 적는다 (6장, p.278).[^rahman2025] 그 다음 단계의 모양은
  [리액티브 스트림 규격과 네 구성 요소](../concepts/reactive-streams-specification-components.md)에
  있다.

## 이어지는 페이지

- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 이 API가
  겨냥한 조합 가능성의 부재
- [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md) — 이 API가 서는 밑바탕
- [자바 리액티브 프레임워크의 대가](../concepts/reactive-frameworks-tradeoffs-in-java.md) — 같은
  한계를 더 밀고 간 다음 패러다임
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 발상 전환
  없이 같은 효율을 노리는 쪽
- [비동기 API의 모양과 콜백 지옥](../concepts/async-api-shapes-and-callback-hell.md) — 이 API가
  정리해 주는 그 중첩
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 1장 "Introduction" — "Bringing Composability into Play with
    CompletableFuture"(pp.23–25), "Advantages of using CompletableFuture"(p.24),
    "Disadvantages and limitations"(p.24), 조직 준비도 상자(p.25); 6장 "The Relevance of
    Reactive Java in Light of Virtual Threads" — "Asynchronous APIs"(p.278). 인용한
    `calculateCreditWithCompletableFuture`는 원문 그대로이며 `import` 세 줄과 코드 옆 번호
    표식은 뺐다. 6장의 `CompletableFuture` 판 `chat`과 그 체인(p.278)은 옮기지 않았다.
