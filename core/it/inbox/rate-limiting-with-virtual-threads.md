---
type: concept
title: 가상 스레드 시대의 속도 제한
description: 스레드 풀이 별도 장치 없이 해 주던 부하 제한이 가상 스레드에서는 사라진다는 문제, 그래서 접근하는 자원마다 속도 제한을 따로 넣어야 한다는 답, 세마포어로 동시 요청 수를 묶는 방식, 그리고 가상 스레드에서는 블로킹이 싸기 때문에 의도적 병목의 대가가 작다는 것
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
---

# 가상 스레드 시대의 속도 제한

- [버전 조건](#버전-조건)
- [스레드 풀이 대신 해 주던 일](#스레드-풀이-대신-해-주던-일)
- [답은 자원별 속도 제한이다](#답은-자원별-속도-제한이다)
- [세마포어라는 문](#세마포어라는-문)
- [의도적 병목의 대가가 작다](#의도적-병목의-대가가-작다)
- [세마포어의 딜레마](#세마포어의-딜레마)
- [이 장치에 다른 축에서 붙은 이름](#이-장치에-다른-축에서-붙은-이름)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **동시성 상한이 사라지면 밑에 있는 자원은 무엇이 지켜 주는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 이 문제 자체가 가상 스레드를 쓸 때 생긴다.

## 스레드 풀이 대신 해 주던 일

- 문제의 뿌리는 이점 그 자체다 — 가상 스레드는 사실상 무제한 동시성으로 가는 열린 문이며, 전례
  없는 수의 태스크를 동시에 다룰 잠재력을 준다 (2장, p.51).[^rahman2025]
- 그런데 소프트웨어의 모든 부분이 같은 양의 부하를 감당하지는 못한다. 우리가 만드는 웹
  애플리케이션은 백만 요청을 받아 백만 개의 가상 스레드를 만들 수 있지만, 밑에 있는 데이터베이스는
  그만큼의 요청을 감당하지 못할 수 있다 (2장, p.51).[^rahman2025]
- **잃어버린 안전장치가 무엇이었는지가 핵심이다** — 가상 스레드 이전에는 스레드 풀이 별도의 장치를
  구현할 필요 없이 요청을 제한해 주었다. 풀에 스레드가 1,000개면 밑의 자원이 받는 동시 부하는
  많아야 1,000이었지 그 이상이 아니었다 (2장, p.51).[^rahman2025] 그 풀의 구조는
  [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)에 있다.
- 그래서 난제가 생긴다 — 가상 스레드는 사실상 무제한일 수 있으므로, 질문이 "가상 스레드를 쓸 때
  서비스에 과부하가 걸리는 것을 어떻게 막는가"로 바뀐다 (2장, p.51).[^rahman2025]

## 답은 자원별 속도 제한이다

- 답은 접근하는 자원에 특화된 속도 제한(rate limiting) 장치를 구현하는 데 있다. 그 장치는 자원의
  성격과 지켜야 하는 서비스 수준 협약(SLA)에 따라 단순할 수도 복잡할 수도 있다 (2장,
  p.51).[^rahman2025]

## 세마포어라는 문

- 저자가 드는 예가 세마포어로 웹 서비스에 대한 동시 요청 수를 통제하는 것이고, 여기서 초점은
  속도 제한의 원리에 있다고 못 박는다 (2장, p.51).[^rahman2025] 문의 실물은 퍼밋 수를 정해 둔
  세마포어 하나이고, 요청을 보내기 전에 퍼밋을 얻고 `finally`에서 돌려준다 (2장, p.52).

  ```java
  private static final int MAX_PARALLEL = 10;
  private static final Semaphore gate = new Semaphore(MAX_PARALLEL);

  private static String fetchJoke() throws Exception {
      HttpRequest req = HttpRequest.newBuilder(URI.create(API_URL))
          .GET()
          .timeout(Duration.ofSeconds(30))
          .build();
      try {
          gate.acquire();
          HttpResponse<String> res = CLIENT.send(req, HttpResponse.BodyHandlers.ofString());
          if (res.statusCode() != 200) throw new RuntimeException("API error " + res.statusCode());
          return parseJoke(res.body());
      } finally {
          gate.release();
      }
  }
  ```

- 태스크를 돌리는 쪽은 여전히 태스크마다 가상 스레드를 만드는 실행자다. 저자는 속도 제한을 넘어서는
  50건을 일부러 던져 세마포어가 동시성을 어떻게 누르는지 보인다 (2장, p.53).[^rahman2025]
- 요청마다 30초 타임아웃을 걸어 개별 요청이 무한정 블로킹되지 않게 하고, 공유 `HttpClient`에는
  10초 연결 타임아웃을 둔다 (2장, p.53).[^rahman2025]

## 의도적 병목의 대가가 작다

- 동작은 단순하다 — 세마포어의 수를 10으로 두면 동시 태스크가 10으로 제한되고, 한도에 닿은 뒤 새
  태스크가 퍼밋을 얻으려 하면 블로킹된다 (2장, pp.53–54).[^rahman2025]
- **그런데 가상 스레드에서는 블로킹이 싸다** — 속도 제한을 위해 의도적인 병목을 들이더라도 가상
  스레드의 효율 덕분에 애플리케이션 전체 성능에 주는 악영향이 작다는 것이 저자가 꼽는 실무적
  함의다 (2장, p.54).[^rahman2025] 싼 이유는
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)의
  언마운트다.

## 세마포어의 딜레마

- 이전 지침 쪽에서 같은 도구에 경고가 붙는다 — 세마포어로 핀닝이 잦은 코드 구간에 들어가는 가상
  스레드 수를 제한할 수 있지만 아주 조심해서 써야 한다. 한도를 너무 낮게 잡으면 애플리케이션의
  동시성을 질식시켜 가상 스레드의 이점을 없앤다 (2장, p.87).[^rahman2025]
- 같은 결의 유보가 하나 더 있다 — 가상 스레드로 더 많은 태스크를 동시에 돌릴 수 있게 되면 다른
  자원에서 병목이 생길 수 있으므로 사용량을 제한할 방법이 여전히 필요할 수 있다 (2장,
  p.87).[^rahman2025]

## 이 장치에 다른 축에서 붙은 이름

- **마이크로서비스 아키텍처 쪽에서는 같은 구조를 벌크헤드(bulkhead)라 부른다.** 배에서 물이
  새면 문을 닫아 봉하는 칸에서 온 이름이고, 처방의 실물은 **하류 연결마다 커넥션 풀을 따로
  두어 풀 하나가 말라도 다른 연결이 영향받지 않게 하는 것**이다 (12장 §"Bulkheads",
  pp.400–401).[^newman2021]
- **자원이 마르기 전에 칸을 나눈다는 취지가 위 절과 같다.** 그쪽이 그 패턴을 목록에서 가장
  중요하다고 꼽는 이유도 순서에 있다 — 시간 초과와 서킷 브레이커는 자원이 **마르기 시작했을
  때** 풀어 주는 쪽이고 벌크헤드는 **애초에 마르지 않게** 하는 쪽이라는 것이다 (12장,
  p.401).[^newman2021]
- **그쪽은 요청을 거절하는 쪽에도 이름을 붙인다** — 자원이 더 포화되지 않게 특정 조건에서
  요청을 거절하는 것을 **부하 떨어내기(load shedding)** 라 부른다 (12장,
  p.401).[^newman2021] 위 세마포어는 퍼밋을 기다리게 하는 쪽이라 **거절이 아니라 대기**이고,
  그 차이가 두 장치의 갈리는 자리다 #hypothesis — 두 소스 어느 쪽도 상대를 가리키지 않으므로
  이 대조는 이 KB의 읽기다.
- **그쪽에는 구현이 없고 이쪽에는 목록이 없다.** 기제 여덟의 목록과 각각을 어디에 쓰는가는
  [안정성 패턴](stability-patterns.md)에 있다.

## 이어지는 페이지

- [자바 세마포어와 퍼밋](../concepts/java-semaphore-permits.md) — 여기 쓴 도구의 규칙과 함정
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 상한을
  대신해 주던 구조
- [가상 스레드가 확장을 주는 자리](../concepts/virtual-thread-scalability-limits.md) — 무제한
  동시성이 실제로 무엇을 주는가
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 이 딜레마가
  이전 계획에서 놓이는 자리
- [공유 상태는 잘못된 상태다](../concepts/shared-state-is-incorrect-state.md) — 자원 접근을 한
  자리로 모으라는 같은 결의 조언
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브
- [안정성 패턴](stability-patterns.md) — 같은 장치를 벌크헤드라 부르는 목록과 그 이웃 기제들

[^newman2021]: Newman 2021, *Building Microservices* 2판(O'Reilly, 2021) 12장 "Resiliency"
    §"Bulkheads"(pp.400–401). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 이 페이지가 그 절에서
    든 것은 이름과 취지와 부하 떨어내기의 규정까지이고 직인용은 없다 — 그 절에 코드는 없고
    도판 하나(Figure 12-4)는 이미지라 본문이 그것에 대해 적는 것만 옮겼다.
    **이 소스는 이 축의 원전이 아니라 소비자**다.
[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Managing Resource
    Constraints with Rate Limiting"(pp.51–54), "Practical Tips for Migrating to Virtual
    Threads"(p.87). 인용한 코드는 `ResourceAwareRateLimitExample`에서 속도 제한의 문에
    해당하는 두 필드와 `fetchJoke` 메서드만 떼어 온 것이고, `main`·`fetchJokes`·`parseJoke`·
    `join`과 `HttpClient` 선언(pp.51–53)은 미수록이다 — 문맥 의존부를 덜어 냈을 뿐 없는 줄을
    보태지는 않았다.
