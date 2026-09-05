---
type: concept
title: 결과를 보고 일찍 끝내는 커스텀 조이너
description: onComplete가 true를 돌려주는 순간 남은 서브태스크가 취소되고 스코프가 끝난다는 성질을 쓰는 두 조이너 — 성공이 정족수에 닿으면 끝내는 쪽과 실패율이 문턱을 넘으면 끝내는 쪽, 각각이 세는 상태와 그 상태를 스레드 사이에서 안전하게 두는 수단, 그리고 저자의 실행 출력이 조기 종료를 보이지 못한 자리
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 결과를 보고 일찍 끝내는 커스텀 조이너

- [버전 조건](#버전-조건)
- [끝을 앞당기는 스위치](#끝을-앞당기는-스위치)
- [정족수에 닿으면 끝내기](#정족수에-닿으면-끝내기)
- [분산 데이터베이스 쓰기라는 실물](#분산-데이터베이스-쓰기라는-실물)
- [실패율이 문턱을 넘으면 끝내기](#실패율이-문턱을-넘으면-끝내기)
- [웹 크롤러라는 실물과 그 출력이 보이지 못한 것](#웹-크롤러라는-실물과-그-출력이-보이지-못한-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **지금까지 온 결과를 보고 남은 서브태스크를 그만두게 하려면 조이너에 무엇을
쓰는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 인터페이스와 상태 이름은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다.

## 끝을 앞당기는 스위치

- 조이너(Joiner)의 `onComplete`가 서브태스크(subtask)마다 불리면서 `true`를 돌려주면 남은 태스크가
  취소되고 스코프가 끝난다. 그 계약은
  [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md)에 있다.
- 이 페이지의 두 조이너는 그 스위치를 **지금까지 본 결과의 누적**으로 켠다. 하나는 성공을 세고
  하나는 실패 비율을 재는데, 둘 다 개별 서브태스크가 아니라 조이너 자신이 들고 있는 집계 상태를
  본다는 점이 같다.

## 정족수에 닿으면 끝내기

- 저자가 분산 시스템에서 착안한 조이너다. 서브태스크의 정족수(quorum)가 성공하면 완료한다. 진행하기
  전에 일정 개수의 확인이 필요한 상황에 쓸모 있다 (4장 §"Quorum-based completion",
  p.189).[^rahman2025]

  ```java
  public class QuorumJoiner<T> implements StructuredTaskScope.Joiner<T, Boolean> {

    private final int requiredSuccesses;
    private final AtomicInteger successCount = new AtomicInteger(0);
    private final AtomicInteger totalCount = new AtomicInteger(0);
    private volatile boolean quorumReached = false;

    public QuorumJoiner(int requiredSuccesses) {
      this.requiredSuccesses = requiredSuccesses;
    }

    @Override
    public Boolean result() {
      return quorumReached;
    }

    @Override
    public boolean onFork(StructuredTaskScope.Subtask<? extends T> subtask) {
      totalCount.incrementAndGet();
      return false;
    }

    @Override
    public boolean onComplete(StructuredTaskScope.Subtask<? extends T> subtask) {
      if (subtask.state() == StructuredTaskScope.Subtask.State.SUCCESS) {
        int currentSuccess = successCount.incrementAndGet();
        if (currentSuccess >= requiredSuccesses) {
          quorumReached = true;
          return true;
        }
      }
      return false;
    }
  }
  ```

- 저자가 이 조이너에서 짚는 것이 여럿이다 (4장, p.190):[^rahman2025]
  - 성공적으로 완료된 서브태스크 수를 세는 데 원자적 카운터(`AtomicInteger`)를 쓰는 이유가 스레드
    안전성이다.
  - 갈라 놓은 서브태스크 수를 따로 세는 것은 완료 비율이나 남은 태스크를 셈하는 데 쓸모 있어서다.
  - 정족수 도달 여부를 담은 `boolean`을 `volatile`로 둔 이유는 스레드 사이의 가시성 확보다.
  - `onFork`는 총 개수만 올리고 `false`를 돌려준다. 갈라 놓는 시점에 태스크 생성을 막고 싶지
    않아서다.
  - `onComplete`는 성공일 때만 카운터를 올리고, 요구 개수에 닿으면 플래그를 세운 뒤 `true`를
    돌려 남은 태스크를 취소하고 스코프를 끝낸다. 아직 모자라면 `false`를 돌려 다른 태스크가 계속
    돌게 둔다.
- 원자적 연산과 `volatile`이 왜 그 자리에 있는지는
  [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md)에
  있다.

## 분산 데이터베이스 쓰기라는 실물

- 저자가 꾸민 상황은 노드 다섯 개짜리 클러스터에 값을 쓰는 것이고, 정족수는 다섯 중 셋이다. 그
  크기가 주는 것은 가용성을 지키면서 얻는 장애 내성으로, **노드 두 개까지의 장애를 견딘다** (4장,
  p.191).[^rahman2025]
- 흉내는 두 가지로 꾸며진다 — 노드마다 100밀리초에서 300밀리초 사이의 무작위 지연을 두어 망을 건너는
  쓰기 지연을 흉내 내고, 20퍼센트의 실패율을 넣어 망 분단이나 디스크 고장이나 노드 붕괴 같은
  실제 분산 시스템의 어려움을 흉내 낸다 (4장, p.192).[^rahman2025]
- 저자가 이 예제에서 얻었다고 말하는 것은 추상화다 — 이 상위 수준 API가 분산 조율의 복잡함을 모두
  감추고 호출자에게는 단순한 동기 인터페이스를 내보인다 (4장, p.192).[^rahman2025]
- 실행 출력에서는 노드 다섯 중 셋이 성공하고 하나가 실패한 시점에 쓰기 연산이 성공으로 끝난다
  (4장, p.192).[^rahman2025]
- 정족수라는 개념 자체는 복제 쪽에서 온 것이고, 그 산수는
  [정족수 읽기와 쓰기](../concepts/quorum-reads-and-writes.md)에 있다.

## 실패율이 문턱을 넘으면 끝내기

- 둘째 조이너는 보고 있는 결과에 따라 완료 논리를 맞춘다 — 실패가 너무 많이 보이면 일찍 끝낸다
  (4장 §"Adaptive completion", p.192).[^rahman2025]
- 받는 것은 최대 실패율(`maxFailureRate`)과 최소 표본 크기(`minSampleSize`) 둘이다. `onComplete`가
  성공과 실패를 각각 큐에 담은 뒤, **표본이 최소 크기에 닿았을 때만** 실패율을 계산해 그것이 문턱을
  넘으면 `true`를 돌려준다 (4장, pp.192–193).[^rahman2025]
- 저자가 그 설계에서 짚는 것이 넷이다 (4장, p.193):[^rahman2025] 성공과 실패를 일어나는 대로
  모으고, 뜻있는 판단을 내릴 만큼 자료가 쌓인 뒤에야 실패율을 따지며, 실패율이 문턱을 넘으면 실패할
  가능성이 큰 연산에 자원을 더 쓰지 않으려고 일찍 끝내고, 실패율이 받아들일 만하거나 자료가 아직
  모자라면 계속 처리한다.
- `result()`는 앞 절의 조이너가 쓰던 결과 레코드를 그대로 재사용해 성공 목록과 실패 목록을
  돌려준다 (4장, p.193).[^rahman2025]

## 웹 크롤러라는 실물과 그 출력이 보이지 못한 것

- 실물 쓰임의 이름이 회로 차단기(circuit breaker)다 — API 끝점 다섯 개를 크롤링하면서 최대 실패율
  30퍼센트와 최소 표본 다섯을 건다. 저자는 그 조합이 반응성과 안정성 사이의 좋은 균형이라고
  말한다 (4장, pp.194–195).[^rahman2025]
- 흉내에 시간에 따른 악화가 들어 있다 — 요청마다 200밀리초에 무작위 값을 더한 지연을 두고, 실패가
  한 번 날 때마다 시스템 실패율을 0.05씩 올려 연쇄 장애나 메모리 누수처럼 부하 아래에서 나빠지는
  상황을 흉내 낸다 (4장, pp.194–195).[^rahman2025]
- 세 시나리오로 돌린다 — 정상 운영(초기 실패율 0.1), 부하 아래(0.4), 연쇄 장애(0.6) (4장,
  p.195).[^rahman2025]
- **실린 실행 출력 셋 가운데 어느 것도 조기 종료를 보이지 못한다.** 성공과 실패의 합이 세
  시나리오에서 각각 5·5·5이고, 마지막 시나리오의 출력은 "처리하지 못하고 남은 URL: 0"으로 끝난다
  (4장, pp.195–196).[^rahman2025] #hypothesis 최소 표본 크기(5)가 끝점 개수(5)와 같아서, 실패율을
  따지기 시작하는 시점에 이미 모든 서브태스크가 완료되어 취소할 것이 남지 않았을 수 있다. 저자는 이
  점을 언급하지 않는다.

## 이어지는 페이지

- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — 이 두 조이너가 지키는 계약
- [fork 시점의 시작 통제](../concepts/fork-time-admission-control.md) — 같은 `boolean`을 반대
  자리에서 쓰는 쪽
- [첫 성공으로 끝내는 경주](../concepts/racing-subtasks-for-first-result.md) — 성공 하나에서
  끝내는 준비된 정책
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — 조이너를
  만들지 않고 같은 일을 하는 더 싼 길
- [정족수 읽기와 쓰기](../concepts/quorum-reads-and-writes.md) — 정족수라는 개념이 온 자리
- [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md) —
  원자적 카운터와 `volatile`이 보장하는 것
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" §"Custom Joiners" —
    "Quorum-based completion"(pp.189–192), "Adaptive completion"(pp.192–196). 인용한 코드는
    pp.189–190의 `QuorumJoiner`이고, 조판 줄바꿈을 폈으며 원문 주석 한 줄과 뒤에 붙은
    `getSuccessCount`·`getTotalCount` 두 접근자를 깎았다. 개념당 대표 코드 하나 규칙에 따라
    남긴 것: `DistributedDatabase` 전문과 실행 출력(pp.190–192), `AdaptiveJoiner`
    전문(pp.192–193), `WebCrawlerWithCircuitBreaker` 전문과 실행 출력(pp.194–196).
    실행 출력의 수치 가운데 본문이 말하지 않은 것은 옮기지 않았고, 조기 종료가 보이지 않는다는
    관찰만 남겼다.
