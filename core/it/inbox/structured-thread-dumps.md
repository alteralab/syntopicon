---
type: concept
title: 구조가 드러나는 스레드 덤프
description: 구조적 동시성이 강제한 태스크 위계가 JSON 스레드 덤프에 스레드 컨테이너로 그대로 나온다는 것, 그 위계를 읽으려면 스코프와 스레드에 이름을 붙여야 한다는 것, 덤프에서 읽어야 할 네 가지, 그 트리를 그려 주는 도구, 그리고 스코프 안에서 예외가 났을 때 프로그램이 스스로 덤프를 뜨는 패턴
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조가 드러나는 스레드 덤프

- [버전 조건](#버전-조건)
- [왜 구조가 디버깅을 바꾸는가](#왜-구조가-디버깅을-바꾸는가)
- [읽히게 만들려면 이름을 붙인다](#읽히게-만들려면-이름을-붙인다)
- [덤프에서 읽는 네 가지](#덤프에서-읽는-네-가지)
- [예외가 났을 때 스스로 뜨기](#예외가-났을-때-스스로-뜨기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프와 서브태스크의 위계가 스레드 덤프에 어떻게 나타나고 무엇을 읽어야
하는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 덤프에 스코프가 별도 컨테이너로 나오는 것은 이 미리 보기 API를 쓸 때의 이야기이고,
> 미리 보기 기능이라 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년
> 3월)를 재심 시점으로 잡은 것이다. 덤프를 뜨는 `jcmd`와 JSON 형식 자체는 이 미리 보기와 무관하고,
> 그쪽은 [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md)에
> 있다.

## 왜 구조가 디버깅을 바꾸는가

- 구조적 동시성은 태스크와 서브태스크(subtask) 사이에 명확한 위계 관계를 강제하는 고유한 구조를
  주고, **그 위계가 코드의 중첩 구조를 그대로 비춘다.** 그래서 동시 실행의 흐름을 이해하고 따지기가
  훨씬 쉬워진다 (4장 §"Observability", p.209).[^rahman2025]
- 그 나무 꼴 구조가 디버깅에서 값을 낸다 — 전통적인 스레드 덤프는 관계가 드러나지 않는 스레드들의
  뒤엉킴을 내놓지만, 구조화된 스레드 덤프는 동시성 시스템의 위계를 보여 주어 문제를 짚어 내기
  쉽게 한다 (4장, p.209).[^rahman2025]
- 뜨는 법은 앞 장과 같다 — `jcmd <pid> Thread.dump_to_file -format=json <output_file>`이고, 이
  덤프에 **태스크 위계와 서브태스크 상태**를 비롯한 값진 정보가 담긴다 (4장,
  p.209).[^rahman2025]

## 읽히게 만들려면 이름을 붙인다

- 저자는 덤프를 보이기 위해 앞 절의 문서 처리기를 두 군데 손본다 — 스코프에 뜻이 담긴 이름을 주고,
  이름 붙은 스레드를 만드는 사용자 정의 `ThreadFactory`를 준다. 그래야 덤프에서 알아보기
  쉬워진다 (4장, p.210).[^rahman2025] 그 두 손질의 문법은
  [스코프 구성](../concepts/structured-task-scope-configuration.md)에 있다.
- 나머지 손질은 시간 벌기다 — 흉내 메서드가 각각 10초씩 자도록 바꿔 덤프를 뜰 시간을 만든다 (4장,
  p.210).[^rahman2025]

## 덤프에서 읽는 네 가지

저자가 JSON 덤프에서 짚는 것이 넷이다 (4장, p.212).[^rahman2025]

- 이름 붙인 스코프가 **별도의 스레드 컨테이너**로 나오고, 그 부모가 최상위 컨테이너이며 소유자가
  주 스레드의 식별자다.
- 세 서브태스크가 모두 그 문서 수집 스코프 아래에 묶여 나와, 어느 스레드가 어느 논리적 연산에
  속하는지 알기 쉽다.
- 각 스레드의 스택 트레이스가 지금 무슨 연산을 하는지 그대로 보여 준다 — 머리말 가져오기, 본문
  가져오기, 메타데이터 가져오기가 각각 드러난다.
- 소유자 항목이 주 스레드가 이 스코프를 소유한다는 것을 밝혀 부모-자식 관계를 분명히 세운다.
- 도구가 그 위를 탄다 — Threadly 같은 간단한 도구가 이 JSON 덤프를 파싱해 구조적 동시성의 트리
  구조를 시각화해 주고, 그래서 위계 관계를 이해하고 복잡한 동시 애플리케이션을 디버깅하기가 더
  쉬워진다 (4장, p.212).[^rahman2025]

## 예외가 났을 때 스스로 뜨기

- `jcmd`가 편하지만 더 많은 통제가 필요하거나 절차를 자동화하고 싶을 때가 있다. 그 자리를
  `HotSpotDiagnosticMXBean`이 맡아, **스코프 안에서 예외가 나는 것 같은 특정 조건이 생길 때**
  프로그램이 스스로 덤프를 뜨게 할 수 있다 (4장, pp.212–213).[^rahman2025]
- 저자의 형태는 이렇다 — 이름 붙인 스코프를 열어 태스크를 갈라 놓고, `FailedException`을 잡는 catch
  블록에서 `ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class)`로 빈을 얻은 뒤
  `dumpThreads(경로, ThreadDumpFormat.JSON)`으로 덤프를 파일에 떨어뜨리고, 그러고 나서 예외를 다시
  던진다 (4장, p.213).[^rahman2025] 그 빈의 규칙(형식 열거형과 절대 경로 요구)은
  [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md)에 있다.
- 저자의 결론은 하나다 — 구조적 동시성은 동시성 프로그래밍을 단순하게 만들 뿐 아니라 태스크 실행과
  그 관계를 더 명확히 보여 주어 디버깅과 유지 보수까지 개선한다 (4장, p.213).[^rahman2025]

## 이어지는 페이지

- [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md) — 덤프를
  뜨는 법과 형식과 담기지 않는 것
- [중첩 스코프](../concepts/nested-structured-scopes.md) — 덤프에 나타나는 그 위계를 만드는 쪽
- [스코프 구성](../concepts/structured-task-scope-configuration.md) — 이름과 스레드 팩토리를
  붙이는 문법
- [구조적 동시성의 원칙](../concepts/structured-concurrency-principle.md) — 관측 가능성이 이
  원칙의 효과 가운데 하나로 꼽히는 자리
- [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md) — 구조가 없을 때
  덤프에서 사라지던 것
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 흐름을 계속 기록하는 다른 길
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Observability"(pp.209–213).
    이 페이지에는 코드 펜스를 두지 않았다 — 덤프를 뜨는 명령과 `HotSpotDiagnosticMXBean`
    사용법은 [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md)가
    이미 담고 있고, 이름 붙이는 구성 문법은 [스코프 구성](../concepts/structured-task-scope-configuration.md)이
    담고 있어 겹치기 때문이다. 미수록: 이름을 붙인 `DocumentProcessor` 전문(pp.209–210),
    JSON 스레드 덤프 전문(pp.211–212), `processWithErrorHandling` 전문(p.213).
    JSON 덤프에서 읽어야 할 단서는 본문에 옮겼다.
