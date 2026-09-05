---
type: concept
title: allUntil로 만드는 중단 조건
description: 서브태스크가 완료될 때마다 검사되는 술어를 받아 스코프를 언제 취소할지 직접 정하는 정책, 술어가 끝까지 참이 되지 않으면 전부 기다리기와 같아진다는 것, join이 갈라 놓은 모든 서브태스크의 스트림을 돌려준다는 것, 그리고 첫 성공에서 멈추는 백업 예제
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-06T00:20:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
  - { id: oracle2025-structuredtaskscope-javadoc, resource: /it/sources/oracle2025-structuredtaskscope-javadoc.md }
---

# allUntil로 만드는 중단 조건

- [버전 조건](#버전-조건)
- [조건을 직접 쓰는 자리](#조건을-직접-쓰는-자리)
- [첫 성공에서 멈추는 백업](#첫-성공에서-멈추는-백업)
- [술어가 보는 것은 공유 상태다](#술어가-보는-것은-공유-상태다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **미리 준비된 정책에 없는 중단 조건을 어떻게 붙이는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 팩토리 이름과 반환 모양은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다. 반환 타입을 대조한 규격은 JDK 25 API 문서 기준(프리뷰)이다.

## 조건을 직접 쓰는 자리

- `Joiner.allUntil(Predicate<Subtask> isDone)`은 가장 유연한 팩토리 메서드로, 사용자 정의 취소
  논리를 허용한다 (4장 §"Common Joining Policies", p.140).[^rahman2025]
- 절차는 이렇다 — 받은 술어(Predicate)가 서브태스크(subtask)마다 그것이 완료될 때 검사되고, 술어가
  `true`를 돌려주면 스코프가 취소된다. 그래서 "서브태스크 둘이 실패하면 취소" 같은 복잡한 정책을
  세울 수 있다 (4장, p.140).[^rahman2025]
- 술어가 끝까지 `true`를 돌려주지 않으면 `awaitAll()`처럼 동작해 모든 서브태스크가 끝나기를
  기다린다 (4장, p.140).[^rahman2025] 그 정책은
  [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md)에 있다.
- 어느 쪽이든 `scope.join()`은 **갈라 놓은 모든 서브태스크가 담긴 `Stream<Subtask>`를**
  돌려준다 (4장, p.140).[^rahman2025]
- 규격이 이 쪽을 뒷받침한다 — `allUntil(Predicate)`의 선언은 `Joiner<T, Stream<Subtask<T>>>`이고,
  `result()`는 갈라 놓은 순서대로 모든 서브태스크의 스트림을 돌려준다. 그 스트림에는 완료된
  서브태스크뿐 아니라, 전부 갈라지거나 완료되기 전에 스코프가 취소되었다면 아직 결과가 없는
  서브태스크도 들어 있다 (`java.base`, `StructuredTaskScope.Joiner` 항).[^oracle2025-structuredtaskscope-javadoc]
- **같은 쪽(p.140)이 `awaitAll()`에도 이 스트림 반환을 적은 것은 책의 오기다.** 규격의
  `awaitAll()` 선언은 `Joiner<T,Void>`이고 `result()`는 `null`을 돌려준다 — 스트림을 돌려주는
  것은 여기 `allUntil` 쪽뿐이다.[^oracle2025-structuredtaskscope-javadoc] 그 자리의 사정은
  [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md)에 있다.
- 저자가 4장에서 이 메서드로 만들어 보이는 조건은 "첫 성공에서 멈추기"다 (4장 §"After first
  success", p.163).[^rahman2025]

## 첫 성공에서 멈추는 백업

- 저자가 꾸민 상황은 데이터를 여러 곳에 백업하다가 어느 한 곳이 성공하는 즉시 나머지를 그만두는
  백업 서비스다 (4장, p.163).[^rahman2025] 클라우드와 USB와 네트워크 드라이브 세 곳이고, 각각
  500밀리초·300밀리초·400밀리초가 걸리며 성공률은 모두 50퍼센트로 꾸며져 있다 (4장,
  p.164).[^rahman2025]

  ```java
  public void performBackup(String data) throws InterruptedException {
    log("Starting backup to multiple locations...");

      try (var scope = open(Joiner.<BackupResult>allUntil(subtask -> {
        boolean shouldStop = hasSuccess.get();
        if (shouldStop) {
          log("Backup successful! Canceling other attempts...");
        }
        return shouldStop;
      }))) {

          scope.fork(() -> backupToCloud(data));
          scope.fork(() -> backupToUSB(data));
          scope.fork(() -> backupToNetwork(data));

          scope.join();

          if (hasSuccess.get()) {
            log("Backup completed successfully!");
          } else {
            log("All backup attempts failed!");
          }
      }
  }
  ```

- 이 술어가 하는 일은 하나다 — 성공이 이미 있으면 실행을 멈추게 한다. `join()` 뒤에는 성공 여부에
  따라 완료와 전부 실패가 갈린다 (4장, p.165).[^rahman2025]

## 술어가 보는 것은 공유 상태다

- 술어에 넘어오는 인자는 완료된 서브태스크지만, 이 예제의 술어는 그 인자를 보지 않고 `AtomicBoolean`
  하나(`hasSuccess`)를 읽는다 (4장, pp.163–165).[^rahman2025]
- 그 플래그를 세우는 것은 백업 메서드들 자신이다 — 각 메서드가 성공했을 때 `hasSuccess.set(true)`를
  부른 뒤 결과를 돌려준다 (4장, p.164).[^rahman2025]
- 그러니까 중단 조건이 서브태스크의 상태가 아니라 **서브태스크들이 함께 쓰는 상태**로 표현된 예다.
  공유 상태를 여러 스레드가 건드릴 때의 규칙은
  [공유 상태는 틀린 상태다](../concepts/shared-state-is-incorrect-state.md)에 있다.

## 이어지는 페이지

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 이 정책이 놓인 틀
- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — 술어가
  참이 되지 않을 때 이 정책이 되는 것
- [첫 성공으로 끝내는 경주](../concepts/racing-subtasks-for-first-result.md) — 같은 "첫 성공에서
  멈춤"을 준비된 정책으로 얻는 쪽
- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — 술어 하나로 안 될 때 조이너를
  통째로 만드는 쪽
- [결과를 보고 일찍 끝내는 커스텀 조이너](../concepts/early-completion-custom-joiners.md) —
  같은 조기 종료를 조이너 안에서 구현한 실물
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Common Joining
    Policies"(p.140), §"After first success"(pp.163–165). 인용한 코드는 p.165의
    `performBackup`이고, 조판 줄바꿈을 폈으며 로그 문구 앞의 체크 표시 그림 문자 하나를 지웠다.
    개념당 대표 코드 하나 규칙에 따라 남긴 것: `BackupResult` 레코드와 `hasSuccess` 선언(p.163),
    세 백업 흉내 메서드(p.164), `BackupDemo`의 `main`(p.165). 이 절에는 실행 출력이 실려 있지
    않아 이 예제의 실측 시간은 원문에도 없다.

[^oracle2025-structuredtaskscope-javadoc]: Oracle 2025, Java SE 25 & JDK 25 API 문서,
    `java.base`의 `java.util.concurrent.StructuredTaskScope.Joiner` — `allUntil(Predicate)` 항과
    `awaitAll()` 항의 선언과 `result()` 계약. 프리뷰 API 표시가 붙어 있다.
