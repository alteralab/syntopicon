---
type: synthesis
title: 가상 스레드의 내부와 운영
description: 가상 스레드를 안쪽에서 본 자리들의 진입점 — 플랫폼 스레드와의 갈림과 스케줄러, 캐리어에 얹고 내리는 기제와 그것을 떠받치는 후속문과 스택 복사와 I/O 폴러, 확장을 주는 조건과 그 한계인 핀닝과 ThreadLocal, 그리고 그 한계를 찾아내고 이전을 판단하는 운영 도구들
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
---

# 가상 스레드의 내부와 운영

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **가상 스레드 하나가 무엇으로 만들어져 어떻게 돌고,
어디서 막히며, 그것을 어떻게 재고 옮기는가**가 사는 자리다.

부모 허브인 [자바 동시 실행 모델](java-concurrent-execution-models.md)이 자바가 일을 동시에
시키려고 써 온 수단들을 나란히 놓는다면, 이 허브는 그중 가장 최근의 답 하나를 열어 안을 본다.
가상 머신이 스레드에게 보장하는 것 일반은 여전히
[자바 메모리 모델과 동시성](java-memory-model-and-concurrency.md)의 몫이다.

읽는 순서가 있다. 두 종류의 갈림을 먼저 보고, 만드는 법과 달라진 규칙을 지나, 안쪽 기제와 확장의
근거를 밟은 뒤, 한계와 그 한계를 다루는 운영 도구로 간다.

## 두 종류와 스케줄러

- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 관리
  주체와 매핑이 갈리는 자리, 그리고 무게와 스케줄링과 블로킹 감내와 통합이라는 네 가지 차이
- [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md) — 선입선출로 도는 작업 훔치기
  풀이며 병렬 스트림의 공용 풀과 다르다는 것, 병렬성 기본값과 그 손잡이

## 쓰는 법

- [가상 스레드를 만드는 방법](../concepts/creating-virtual-threads.md) — 네 가지 표기와 데몬
  기본값 함정
- [가상 스레드에서 달라지는 Thread API](../concepts/virtual-thread-api-semantics.md) — 그대로인
  인터럽트, 바꿀 수 없는 성질들, 새 메서드와 폐기된 메서드, 막혀 있는 조회
- [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)
  — 블로킹 get이 싸지면서 달라지는 코드 모양

## 안쪽 기제

- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 스택 프레임이 힙으로 간 뒤의 마운트와 언마운트, 그리고 투명성
- [자바의 후속문 API](../concepts/java-continuation-api.md) — 멈췄다 이어 가는 능력의 실물,
  그리고 그것이 공개 API가 아니라 내부 API라는 사실
- [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md) — 양보할 때 프레임이
  어디로 가는가, 전부를 되돌리지 않는 최적화와 반환 장벽
- [포크조인 풀이 가상 스레드 스케줄러가 된 이유](../concepts/fork-join-pool-as-virtual-thread-scheduler.md)
  — 병렬성 기본값과 CPU 대 I/O의 논거, 낮은 경합, 그리고 비동기 모드
- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — `park` 뒤의 경로와 그것을
  다시 깨우는 읽기 폴러와 쓰기 폴러
- [직접 만들어 본 가상 스레드](../concepts/nano-thread-from-scratch.md) — 후속문 위에 손으로
  얹어 본 실물과 워커가 바뀌는 출력

## 확장의 근거와 그 조건

- [리틀의 법칙과 처리량](../concepts/littles-law-and-throughput.md) — 처리량과 동시성과 응답
  시간을 잇는 관계식
- [가상 스레드가 확장을 주는 자리](../concepts/virtual-thread-scalability-limits.md) — 빠름이
  아니라 확장이라는 구분, 이득이 나는 두 조건과 나지 않는 자리

## 한계

- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 캐리어에서 내려오지 못하는 자리와
  그 해악, JDK 24가 바꾼 것과 남긴 것
- [가상 스레드와 ReentrantLock](../concepts/reentrant-lock-for-virtual-threads.md) — 동기화
  블록의 대안과 그것이 기대는 park/unpark 기제
- [네이티브 호출과 핀닝](../concepts/native-method-pinning.md) — 가상 머신이 들여다볼 수 없는
  코드 쪽의 핀닝과 그 완화책
- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 스레드마다
  값을 두던 방식이 수백만 개에서 부딪히는 것

## 자원을 지키는 쪽

- [가상 스레드 시대의 속도 제한](../concepts/rate-limiting-with-virtual-threads.md) — 스레드 풀이
  대신 해 주던 부하 제한이 사라진 자리
- [자바 세마포어와 퍼밋](../concepts/java-semaphore-permits.md) — 그 자리를 메우는 도구의 규칙과
  함정

## 재고 옮기는 쪽

- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 두 한계를 찾아내는 플래그와
  플라이트 레코더 이벤트
- [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md) — 한
  시점의 상태를 통째로 뜨는 길
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 순서와
  주의, 그리고 지켜볼 지표

## 경계에 있는 페이지

- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 같은
  대상을 쓰는 쪽에서만 본 자리
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 같은 대상을 가상 머신
  안쪽에서 본 자리
- [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md) — 스케줄러가
  물려받은 구조
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — 락과 스레드 로컬을
  가상 머신 쪽에서 본 자리
- [JFR과 JMC](../concepts/jfr-and-jmc.md) — 모니터링 도구의 전반

## 이어지는 허브

- [자바 동시 실행 모델](java-concurrent-execution-models.md) — 이 허브의 부모, 곧 가상 스레드가
  놓인 실행 모델들의 계보
- [자바의 구조적 동시성](structured-concurrency-in-java.md) — 이 스레드들 위에 얹히는 프로그래밍
  모델 쪽의 형제 허브
- [자바 메모리 모델과 동시성](java-memory-model-and-concurrency.md) — 가상 머신이 스레드에게
  보장하는 것
