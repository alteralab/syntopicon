---
type: concept
title: 모듈 임포트 선언
description: import module 한 줄이 지정한 모듈이 내보내는 모든 패키지의 공개 최상위 타입을 온디맨드로 들여온다는 JDK 25 문법, java.base의 경우 그것이 몇 개의 패키지 임포트에 해당하는지, 그리고 전이적으로 읽히는 모듈까지 함께 들어온다는 범위
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 모듈 임포트 선언

- [버전 조건](#버전-조건)
- [무엇을 들여오는가](#무엇을-들여오는가)
- [왜 예제 코드에 나오는가](#왜-예제-코드에-나오는가)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`import module java.base;` 한 줄은 무엇을 들여오는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상. 이 소스가 모듈 임포트 선언(module import declaration)을 JDK 25에
> 들어온 것으로 소개한다. 앞선 판에는 없는 문법이다.

## 무엇을 들여오는가

- `import module java.base;`는 모듈 임포트 선언이고, 두 자리에서 공개 최상위 클래스와 인터페이스를
  온디맨드로 들여온다 — 지정한 모듈이 현재 모듈에 내보내는 패키지들, 그리고 그 모듈을 읽음으로써
  전이적으로 읽히는 모듈들이 내보내는 패키지들이다 (4장 §"Module Import Declaration (JDK 25+)",
  p.159).[^rahman2025]
- `java.base`의 경우 그 효과가 **54개의 온디맨드 패키지 임포트**와 같다. `java.base`가 내보내는
  패키지마다 하나씩이고, `java.io`·`java.util`·`java.time`·`java.util.concurrent` 등을 별표로
  들여오는 것과 같다 (4장, p.159).[^rahman2025]
- 그래서 얻는 것은 간결함이다 — 기본적인 자바 API를 쓸 때 개별 패키지 임포트를 여러 줄 적을 필요가
  없어진다 (4장, p.159).[^rahman2025]

## 왜 예제 코드에 나오는가

- 이 소스의 4장 예제 클래스들이 그 한 줄로 임포트를 대신한다. 저자는 지면의 코드를 간결하게 유지하려고
  `StructuredTaskScope`의 중첩 클래스와 `open()` 메서드도 정적 임포트로 들여온다 (4장, p.158,
  p.160).[^rahman2025]
- 그러니 이 KB가 옮긴 4장의 코드 펜스에서 클래스 이름이 임포트 없이 바로 쓰이는 것은 이 문법과 정적
  임포트를 전제로 한 것이다. 그 펜스들은
  [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) 아래 페이지들에 있다.

## 이어지는 페이지

- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — 이
  문법이 처음 등장하는 예제
- [자바 언어 진화 프로젝트](../concepts/java-language-evolution-projects.md) — 이런 구문 개선이
  나오는 자리
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 걸린 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — 곁글 §"Module Import Declaration
    (JDK 25+)"(p.159), 그리고 정적 임포트 언급은 pp.158·160·165. 이 페이지는 동시성이 아니라
    언어 문법에 대한 것이라 얇게 두었다.
