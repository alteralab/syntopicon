---
type: concept
title: 전부 기다리기와 부분 성공
description: awaitAll 정책이 성공과 실패를 가리지 않고 모든 서브태스크의 완료를 기다리며 실패를 취소 신호로 삼지 않는다는 것, 그래서 부수 효과를 남기거나 가능한 만큼 모으는 일과 오류를 연결마다 가두는 서버에 맞는다는 것, 그리고 join의 반환값이 이 책 안에서 세 자리로 갈렸다가 JDK 25 API 문서로 null이라고 닫힌 자리
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-06T00:20:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
  - { id: oracle2025-structuredtaskscope-javadoc, resource: /it/sources/oracle2025-structuredtaskscope-javadoc.md }
---

# 전부 기다리기와 부분 성공

- [버전 조건](#버전-조건)
- [실패를 취소 신호로 삼지 않는다](#실패를-취소-신호로-삼지-않는다)
- [join이 무엇을 돌려주는가](#join이-무엇을-돌려주는가)
- [어디에 쓰는가](#어디에-쓰는가)
- [여러 통로로 알림을 보내는 예제](#여러-통로로-알림을-보내는-예제)
- [연결마다 오류를 가두는 서버](#연결마다-오류를-가두는-서버)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **일부가 실패해도 나머지를 끝까지 돌려야 할 때 스코프를 어떻게 조인하는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 팩토리 이름과 반환 모양은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다. 반환 타입을 대조한 규격은 JDK 25 API 문서 기준(프리뷰)이다.

## 실패를 취소 신호로 삼지 않는다

- `awaitAll()` 정책은 앞의 두 정책과 다른 길을 간다 — 성공했든 실패했든 **모든 서브태스크(subtask)가
  완료될 때까지** 기다린다 (4장 §"Wait for all", p.154).[^rahman2025]
- `allSuccessfulOrThrow()`와 달리 하나가 실패해도 도는 서브태스크를 절대 취소하지 않는다. 갈라 놓은
  태스크 전부가 끝까지 실행되도록 허용된다 (4장, p.154).[^rahman2025]
- 그래서 이 정책의 값은 회복력이다 — 일부 연산이 실패할 수 있지만 성공한 것들을 처리하는 이득은
  여전히 원할 때, `awaitAll()`은 어떤 일도 헛되이 버려지지 않게 한다 (4장,
  p.154).[^rahman2025]
- 예외 쪽의 귀결이 하나 더 있다 — **`awaitAll()`에서는 `join()`이 결코 `FailedException`을 던지지
  않는다.** 일부가 실패해도 모든 태스크가 끝나기를 기다릴 뿐이다 (4장, p.177).[^rahman2025]
- 그래서 대가가 붙는다. 성공과 실패를 **모두 모으려면 각 서브태스크 안에서 예외를 다뤄야 한다**
  (4장, p.177).[^rahman2025] 그 방법은
  [구조적 스코프의 예외 처리](../concepts/exception-handling-in-structured-scopes.md)에 있고,
  같은 일을 조이너 쪽에서 한 번에 하는 길은
  [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md)에 있다.

## join이 무엇을 돌려주는가

- 이 절은 `scope.join()`이 **언제나 `null`을 돌려준다**고 적는다. 이 조이너는 결과를 모으는 것이
  아니라 태스크의 완료에 집중하기 때문이라는 이유가 붙는다 (4장, p.154).[^rahman2025]
- **그런데 같은 책의 정책 카탈로그는 다르게 적는다.** 거기서는 `awaitAll()`의 `scope.join()`이
  각 서브태스크의 상태와 결과와 예외를 살펴볼 수 있는 `Stream<Subtask>`를 돌려준다고 되어 있다
  (4장, p.140).[^rahman2025]
- 판단 재료는 예제 코드다 — 이 절의 예제는 `Void result = scope.join();`으로 받고 그 위에
  "`awaitAll()`에서는 `join()`이 언제나 `null`을 돌려준다"는 주석이 달려 있다 (4장,
  p.156).[^rahman2025]
- **규격이 이 물음을 닫는다.** `awaitAll()`의 선언은 `Joiner<T,Void>`이고, 그 조이너의 `result()`
  메서드는 `null`을 돌려준다. `join()`이 돌려주는 것이 곧 `result()`의 값이므로 `join()`은
  `null`이다 (`java.base`, `StructuredTaskScope.Joiner` 항).[^oracle2025-structuredtaskscope-javadoc]
- 그래서 **p.154 본문과 p.156 예제가 맞고 p.140 카탈로그가 오기다.** 이 KB가 앞서 세워 둔 추측 —
  카탈로그 항목이 바로 아래 `allUntil` 항목의 반환값을 잘못 옮겼으리라는 것 — 도 함께 확인된다.
  스트림을 돌려주는 선언은 `allUntil(Predicate)`과 `allSuccessfulOrThrow()` 둘뿐이고 둘 다
  `Joiner<T, Stream<Subtask<T>>>`다.[^oracle2025-structuredtaskscope-javadoc]
- **이것은 두 소스의 모순이 아니라 해설서의 오기다.** 규격이 API 선언 그 자체이므로 대립하는 두
  주장이 아니고, 그래서 `contradicts`를 걸지 않는다. 책의 세 서술은 위에 그대로 남겨 둔다 —
  같은 책을 읽는 사람이 이 자리에서 걸릴 것이기 때문이다.

## 어디에 쓰는가

- 저자가 드는 자리는 둘이다 — 서브태스크가 부수 효과(로그 남기기, 지표 수집, 파일 처리 같은 것)를
  일으킬 때, 그리고 일부 소스를 못 쓰더라도 가능한 만큼 데이터를 모아야 할 때다 (4장,
  p.154).[^rahman2025]
- 특히 쓸모 있는 계열로 모니터링 시스템, 일괄 처리 작업, 그리고 부분 성공이 받아들여지고 값이 있는
  팬인(fan-in) 서버 구조를 든다 (4장, p.154).[^rahman2025]

## 여러 통로로 알림을 보내는 예제

- 저자가 꾸민 상황은 중대한 시스템 사건을 이메일과 문자와 푸시 세 통로로 알리는 것이다. 최대한 널리
  닿는 것이 목적이라 한 통로가 실패해도 나머지는 계속 전달해야 한다 (4장, p.154).[^rahman2025]

  ```java
  public void sendCriticalAlert(String alertMessage) throws InterruptedException {
    log("Sending critical alert: " + alertMessage);

      try (var scope = open(Joiner.<Void>awaitAll())) {
        scope.fork(() -> {
          sendEmailNotification(alertMessage);
          return null;
        });
        scope.fork(() -> {
          sendSmsNotification(alertMessage);
          return null;
        });
        scope.fork(() -> {
          sendPushNotification(alertMessage);
          return null;
        });
        Void result = scope.join();
        logNotificationSummary();
  ```

- 결과를 모으는 자리가 공유 상태다 — 흉내 메서드들이 `CopyOnWriteArrayList`에 결과를 담고
  `AtomicInteger` 둘로 성공과 실패를 센다 (4장, pp.154–155).[^rahman2025] 원자적 카운터가 왜
  락보다 나은지는
  [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md)의 CAS 절에 있다.
- 흉내는 통로마다 다른 신뢰도로 꾸며진다 — 이메일 90퍼센트, 문자 70퍼센트, 푸시 95퍼센트의 성공률이다
  (4장, pp.155–156).[^rahman2025]
- 실행에서는 세 알림이 나란히 돌다가 문자가 게이트웨이 시간 초과로 실패했는데도 이메일과 푸시는 계속
  돌아 성공으로 끝난다. 메인 스레드는 결말과 무관하게 모두 끝날 때까지 `join()`에서 기다리고,
  세 통로 중 둘이 전달에 성공했다는 요약이 남는다 (4장, pp.159–160).[^rahman2025]
- 관찰의 핵심은 `allSuccessfulOrThrow()`와 갈리는 한 줄이다 — **실패한 태스크가 도는 다른 태스크를
  결코 취소하지 않는다.** 통로마다 전달을 시도할 기회를 공평하게 받고, 부분 전달이 아예 전달 못 하는
  것보다 무한히 나은 경보 시스템에서 이 성질이 결정적이다 (4장, p.160).[^rahman2025]

## 연결마다 오류를 가두는 서버

- 저자가 드는 또 하나의 자리가 회복력 있는 동시 서버다. 연결 처리기 하나가 오류를 만나도 다른 활성
  연결이 영향을 받지 않아야 하는데, `awaitAll()`은 실패한 클라이언트 하나가 서버의 다른 연결 처리
  능력을 무너뜨리거나 앞당겨 멈추는 일을 막는다. `allSuccessfulOrThrow()`였다면 하나가 실패할 때
  활성 연결이 전부 취소되었을 것이다 (4장 §"Resilient concurrent server",
  p.160).[^rahman2025]
- 그 값의 이름이 오류 격리(fault isolation)다 — 개별 연결 처리기가 만나는 오류(네트워크 시간 초과,
  잘못된 요청, 클라이언트 연결 끊김)가 그 연결 안에 갇히고 다른 활성 연결로 번지지 않는다. 그래서
  가동 시간과 신뢰성이 중요한 서버 애플리케이션에 맞는 선택이다 (4장, p.160).[^rahman2025]
- 실물은 에코 서버다 — 스코프를 연 채 받아들이기 루프를 돌며 연결마다 하나씩 갈라 놓고, 루프를
  빠져나온 뒤 `scope.join()`으로 모든 연결이 끝나기를 기다린다. 각 처리기는 `finally`에서 자원을
  닫아 오류가 나도 누수가 없다 (4장, pp.161–162).[^rahman2025]
- 두 터미널에서 접속해 본 실행 로그가 그 성질을 보인다 — 두 연결이 각자의 속도로 독립해 끝나고,
  서로 간섭하지 않는다 (4장, p.163).[^rahman2025]

## 이어지는 페이지

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 이 정책이 놓인 틀
- [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md) — 실패를 곧 취소로 삼는 쪽
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — 이 정책에
  중단 조건 하나를 얹는 쪽
- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — 성공과 실패를 조이너 쪽에서
  함께 모으는 쪽
- [구조적 스코프의 예외 처리](../concepts/exception-handling-in-structured-scopes.md) — 이
  정책에서 예외를 어디서 잡아야 하는가
- [모듈 임포트 선언](../concepts/module-import-declaration.md) — 이 절의 예제 클래스들이 쓰는 JDK
  25 문법
- [가상 스레드 시대의 속도 제한](../concepts/rate-limiting-with-virtual-threads.md) — 연결마다
  갈라 놓는 서버에서 부하를 무엇이 막는가
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Wait for all"(pp.154–160),
    §"Resilient concurrent server"(pp.160–163), 카탈로그 쪽 서술은 §"Common Joining
    Policies"(p.140), 그리고 `join()`이 `FailedException`을 던지지 않는다는 규정과 그 대가는
    §"Understanding how different joiners handle exceptions"(p.177) — 그 절의 예제
    `demonstrateAwaitAll`은 미수록이다. 인용한 코드는 pp.156–157의 `sendCriticalAlert`이고, 조판 줄바꿈을 폈으며
    원문 주석 네 줄과 `log` 호출 두 줄을 깎았다. **원문의 이 메서드는 `catch (InterruptedException)`
    블록까지 이어지는데, 지면이 두 쪽으로 갈리며 `try` 블록이 열린 채 끝나는 발췌라 이 KB도 같은
    범위만 옮겼다** — 그대로 복사하면 컴파일되지 않는다. 개념당 대표 코드 하나 규칙에 따라 남긴 것:
    `NotificationResult` 레코드와 공유 상태 선언(p.154), 세 알림 흉내 메서드(pp.155–156),
    `logNotificationSummary`(p.157), `AwaitAllDemo` 전문과 `main`(p.158),
    `ResilientServer`의 `serve`·`handleConnection`(pp.161–162), 텔넷 접속과 서버 실행
    출력(p.163).

[^oracle2025-structuredtaskscope-javadoc]: Oracle 2025, Java SE 25 & JDK 25 API 문서,
    `java.base`의 `java.util.concurrent.StructuredTaskScope.Joiner` — `awaitAll()` 항의 선언과
    `result()` 계약, 그리고 `result()` 항의 "이 메서드의 결과가 `join` 메서드의 반환값"이라는
    규정. 프리뷰 API 표시가 붙어 있다.
