---
type: concept
title: 중첩 스코프
description: StructuredTaskScope 안에서 또 하나의 스코프를 여는 것이 부모-자식 트리를 만든다는 것, 부모가 자식 스코프의 수명 주기를 책임진다는 것, 오류와 취소가 그 위계를 타고 위로 전파되고 취소는 아래로 연쇄한다는 것, 그리고 저자의 두 단계 문서 처리 예제와 그 예제가 서술과 어긋나는 자리
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 중첩 스코프

- [버전 조건](#버전-조건)
- [중첩이 만드는 것은 트리다](#중첩이-만드는-것은-트리다)
- [오류는 위로, 취소는 아래로](#오류는-위로-취소는-아래로)
- [두 단계 문서 처리](#두-단계-문서-처리)
- [서술과 예제가 어긋나는 자리](#서술과-예제가-어긋나는-자리)
- [닫는 순서는 강제된다](#닫는-순서는-강제된다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프 안에서 또 하나의 스코프를 열면 무엇이 보장되는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 메서드 이름과 예외 이름은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다.

## 중첩이 만드는 것은 트리다

- 메서드 안에 코드 블록을 중첩하듯 `StructuredTaskScope` 인스턴스도 중첩할 수 있고, 그러면 동시
  태스크의 여러 층으로 된 위계가 생긴다 (4장 §"Nested Scopes", p.205).[^rahman2025]
- 쓸모의 자리가 명시된다 — 중첩 스코프(nested scope)는 태스크가 자연스럽게 여러 층의
  서브태스크(subtask)로 나뉘는 복잡한 작업 흐름을 다룰 때 값지다. 각 중첩 스코프는 자기 완결적이라
  자기 서브태스크의 수명 주기와 오류 처리를 캡슐화한다 (4장, p.205).[^rahman2025]
- 관계가 서는 조건과 그 결과가 하나다 — **서브태스크가 자기 `StructuredTaskScope`를 만들면
  부모-자식 관계가 서고 트리 구조가 만들어진다.** 그때 부모 스코프가 자식 스코프의 수명 주기를
  책임지며, 거기에는 자식의 종료와 자식 서브태스크의 완료가 포함된다 (4장,
  p.205).[^rahman2025]

## 오류는 위로, 취소는 아래로

- 이 위계 구조가 오류와 취소를 위로 전파한다 — 중첩 스코프 안의 서브태스크가 실패하면 오류는 먼저
  그 직속 부모 스코프에서 다뤄지고, 다뤄지거나 최상위 스코프에 닿을 때까지 사슬을 타고 올라간다
  (4장, p.205).[^rahman2025]
- 저자가 절을 닫으며 정리하는 것이 넷이다 — 각 스코프가 자기 수명 주기와 자원을 관리하므로 깔끔한
  위계가 만들어지고, 실패가 자연스럽게 전파되며, 자원이 자동으로 정리되고, **취소가 부모에서 자식
  쪽으로 제대로 연쇄한다** (4장, p.209).[^rahman2025]
- 그러니까 방향이 둘이다. 오류는 아래에서 위로 올라가고, 취소는 위에서 아래로 내려간다.

## 두 단계 문서 처리

- 저자가 드는 실물은 여러 소스에서 문서 내용을 모은 뒤 그것을 분석하는 문서 처리기다 (4장,
  p.206).[^rahman2025]

  ```java
  public DocumentReport processDocument(String documentId) throws InterruptedException {
    try (var gatheringScope = open(StructuredTaskScope.Joiner
        .<String>allSuccessfulOrThrow())) {

      var headerTask = gatheringScope.fork(() -> fetchHeader(documentId));
      var bodyTask = gatheringScope.fork(() -> fetchBody(documentId));
      var metadataTask = gatheringScope.fork(() -> fetchMetadata(documentId));

      gatheringScope.join();

      return analyzeContent(headerTask.get(), bodyTask.get(), metadataTask.get());
    } catch (StructuredTaskScope.FailedException e) {
      throw new RuntimeException("Failed to gather document content", e);
    }
  }
  ```

- 바깥 스코프가 하는 일은 넷이다 — 최상위 스코프를 열고, 머리말과 본문과 메타데이터를 서로 다른
  소스에서 가져오는 태스크를 동시에 띄우고, 그것이 모두 끝나기를 기다린 뒤, 필요한 내용이 다 갖춰진
  상태로 분석 단계로 넘어간다 (4장, pp.206–207).[^rahman2025]
- 안쪽 스코프는 `analyzeContent` 안에 있다. 분석 전용의 둘째 층 스코프를 열어 단어 세기와 감성
  분석과 요약 생성을 동시에 돌리고, 모두 끝나기를 기다린 뒤 최종 보고서를 만든다 (4장,
  p.207).[^rahman2025]
- 저자가 그린 위계는 두 층이다 — 문서 처리(1층) 아래에 머리말·본문·메타데이터 가져오기와 내용
  분석(2층)이 있고, 내용 분석 아래에 단어 세기·감성 분석·요약 생성(3층)이 있다 (4장,
  pp.207–208).[^rahman2025]

## 서술과 예제가 어긋나는 자리

- 이 절의 서술은 부모-자식 관계가 서는 조건을 **서브태스크가 자기 스코프를 만들 때**로 적는다 (4장,
  p.205).[^rahman2025]
- 그런데 실린 예제에서 안쪽 스코프를 여는 것은 서브태스크가 아니다. `analyzeContent`는
  `gatheringScope.join()`이 돌아온 **뒤에** 바깥 스코프의 소유자 스레드가 부르는 메서드이고, 그
  안에서 둘째 스코프가 열린다 (4장, pp.206–207).[^rahman2025]
- 이 KB는 어느 쪽도 고쳐 적지 않고 두 서술을 그대로 둔다. 서브태스크 안에서 스코프를 여는 형태의
  예제는 이 소스의 4장에 없다.

## 닫는 순서는 강제된다

- 중첩된 스코프가 모두 닫히기 전에 바깥 스코프의 `close()`가 불리면 `StructureViolationException`이
  던져진다. 그 규칙의 전문은
  [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md)에 있다.

## 이어지는 페이지

- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 닫는 순서 규칙과
  `StructureViolationException`
- [구조적 동시성의 원칙](../concepts/structured-concurrency-principle.md) — 이 위계가 구현하는
  언어 무관 규정
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — 스코프 하나
  안에서 벌어지는 일
- [구조가 드러나는 스레드 덤프](../concepts/structured-thread-dumps.md) — 이 위계가 실제로
  눈에 보이는 자리
- [구조적 스코프의 예외 처리](../concepts/exception-handling-in-structured-scopes.md) — 위로
  전파된 오류를 어디서 받을 것인가
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Nested Scopes"(pp.205–209).
    인용한 코드는 p.206의 `DocumentProcessor.processDocument`이고 조판 줄바꿈만 폈다.
    개념당 대표 코드 하나 규칙에 따라 남긴 것: 안쪽 스코프를 여는 `analyzeContent`(p.207),
    여섯 개의 흉내 메서드와 `DocumentReport` 레코드(p.208), `main`과 실행 출력(p.209).
    그림 4-3(p.206, 구조적 동시성에서 태스크가 이루는 위계 구조)은 미수록이다.
