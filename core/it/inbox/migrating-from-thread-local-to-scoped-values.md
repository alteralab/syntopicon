---
type: concept
title: ThreadLocal에서 스코프 값으로 옮기기
description: 저자가 옮기기 전에 확인하라고 드는 다섯 가지(JDK 업그레이드, 나눌 데이터의 불변성, where와 run으로 스코프를 명시하기, null 대신 예외가 나오는 차이, 도입 뒤의 테스트)와 장을 닫으며 밝히는 정식화의 뜻, 그리고 같은 절 안에서 미리 보기라고 적는 문장이 어긋나는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# ThreadLocal에서 스코프 값으로 옮기기

- [버전 조건](#버전-조건)
- [옮기기 전에 확인할 다섯](#옮기기-전에-확인할-다섯)
- [저자가 장을 닫으며 내리는 판정](#저자가-장을-닫으며-내리는-판정)
- [같은 장 안에서 어긋나는 문장](#같은-장-안에서-어긋나는-문장)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`ThreadLocal` 기반 코드를 스코프 값으로 옮기기 전에 무엇을 확인해야 하는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상에서 정식 API다. JDK 21부터 24까지는 미리 보기(preview) 기능이라
> 컴파일과 실행에 `--enable-preview`가 필요하다 (5장, pp.217·226).[^rahman2025] 만료일은 달지
> 않는다 — 정식 API라 다음 릴리스를 재심 시점으로 잡을 근거가 없다.

## 옮기기 전에 확인할 다섯

저자가 이전을 결정하기 전에 고려할 것들을 든다 (5장 §"Migrating to Scoped Values",
pp.244–245).[^rahman2025]

- JDK 이전이 먼저다 — `ScopedValue`는 최신 JDK에서만 쓸 수 있으므로 더 새로운 JDK로 옮기는 일이
  핵심 고려 사항이다. 업그레이드 전에 마주칠 제약을 미리 평가해 매끄러운 전환을 확보하라 (5장,
  pp.244–245).[^rahman2025]
- 나눌 데이터가 불변인지 확인하라 — `ScopedValue`가 불변성을 강제하기 때문이다. 쓰임새가 가변
  데이터를 요구한다면 `ScopedValue`가 맞지 않을 수 있다 (5장, p.245).[^rahman2025] 이것이 이
  이전에서 가장 먼저 걸릴 수 있는 조건이다. `ThreadLocal`은 아무 데서나 `set()`을 허용했으므로,
  그 자유에 기대어 쓰인 코드는 그대로 옮겨지지 않는다.
- 공유 데이터의 스코프를 `where()`와 `run()`으로 명시적으로 정의하는 일이 똑같이 중요하다.
  그래야 데이터가 의도한 문맥 안에서만 접근되고 의도치 않은 부작용이 생기지 않는다 (5장,
  p.245).[^rahman2025]
- null 처리의 차이에 유의하라 — `ScopedValue`는 묶이지 않은 값에 접근하면
  `NoSuchElementException`을 던지고 `ThreadLocal`은 `null`을 돌려준다. 이 명시적 오류 처리가
  문제를 일찍 잡는 데 도움이 되지만 이전 과정에서 세심한 주의를 요구한다 (5장,
  p.245).[^rahman2025]
- 마지막이 테스트다 — `ScopedValue`를 도입한 뒤에는 동시성과 데이터 일관성이 지켜지는지 확인하고
  예상 못 한 문제를 다루기 위해 애플리케이션을 충분히 테스트하는 것이 필수다 (5장,
  p.245).[^rahman2025]

## 저자가 장을 닫으며 내리는 판정

- 결론이 먼저 요약된다 — `ScopedValue`는 호출 사슬 전반에 문맥을 나누는 일에서 `ThreadLocal`보다
  깔끔하고 안전하고 효율적인 대안을 준다. 불변이고 잘 정의된 동적 스코프에 묶임으로써
  `ThreadLocal`의 결함인 무제한 가변성, 무제한 수명, 메모리 부담을 다룬다 (5장,
  p.245).[^rahman2025]
- 어디에 특히 맞는지도 다시 적힌다 — 가벼운 성질이 가상 스레드 및 구조적 동시성과 특히 잘 맞아,
  동시 태스크를 대량으로 띄울 때 자원 사용을 줄이는 데 도움이 된다 (5장, p.245).[^rahman2025]
- 그리고 상태가 못 박힌다 — **JDK 25부터 `ScopedValue`는 미리 보기 상태를 졸업해 안정된 API가
  되었고 운영 환경에 쓸 준비가 되었다** (5장, p.245).[^rahman2025]
- 그 안정화의 뜻이 둘로 이어진다 — 이 안정화가 `ScopedValue`를 현대 자바 애플리케이션에서 문맥
  전파의 권장 해법으로 만들며, 기존 `ThreadLocal` 기반 코드를 API 변경 걱정 없이 옮길 수 있다
  (5장, p.245).[^rahman2025]

## 같은 장 안에서 어긋나는 문장

- 그런데 같은 절의 앞쪽 문장은 반대로 적는다 — 이전 고려 사항을 열면서 **"the API is still in
  preview"**라고 하고, 미리 보기 플래그 없이 JDK에서 쓸 수 있게 될 때까지 익혀 두라고 권한다
  (5장, p.244).[^rahman2025]
- 이 문장은 같은 장의 세 자리와 어긋난다 — 장을 여는 문장의 "finalized in JDK 25"(p.217),
  곁글의 "available since JDK 25"(p.226), 그리고 바로 다음 쪽의 정식화 선언(p.245)이다
  (5장, pp.217·226·244·245).[^rahman2025]
- #hypothesis 개정 과정에서 남은 옛 문장으로 보인다. `ScopedValue`가 실제로 여러 릴리스에 걸쳐
  미리 보기였다가 JDK 25에서 확정되었으므로, 확정 전에 쓰인 문단이 갱신되지 않은 채 남았을 수
  있다. 저자가 이 어긋남을 언급하지 않으므로 단정하지 않는다.
- 이 KB는 다수 쪽을 따라 **JDK 25 이상에서 정식**으로 적고, 어긋나는 한 문장을 지우지 않고 이
  절에 남긴다. 어느 쪽이 맞는지는 릴리스 노트로 확인할 문제이고 이 소스 안에서는 갈리지 않는다.

## 이어지는 페이지

- [ScopedValue가 ThreadLocal보다 나은 이유](../concepts/scoped-value-vs-thread-local.md) — 옮길 이유 쪽
- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 옮겨서 벗어나려는 것
- [재귀 감지와 평탄화 트랜잭션](../concepts/scoped-value-recursion-detection.md) — 같은 절의 앞부분이 드는
  두 쓰임
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 옮긴 뒤 쓰게 되는 API
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 같은 책이
  스레드 쪽 이전에 대해 적은 것
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Migrating to Scoped Values"의 뒷부분
    (pp.244–245)과 §"In Closing"(p.245). 어긋나는 문장의 자리는 같은 장 p.217, p.226,
    p.244, p.245다. 이 구간에는 코드가 실려 있지 않아 코드 펜스가 없다.
