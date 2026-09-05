---
type: concept
title: 재귀 감지와 평탄화 트랜잭션
description: 스코프 값을 숨은 매개변수 말고 다른 쓰임으로 돌리는 두 자리 — isBound로 재진입을 감지하고 리바인딩으로 재귀 깊이 카운터를 모형화하는 템플릿 처리기, 그리고 이미 열린 트랜잭션이 있으면 새로 열지 않고 합류하는 평탄화 트랜잭션
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 재귀 감지와 평탄화 트랜잭션

- [버전 조건](#버전-조건)
- [숨은 매개변수 말고 또 무엇에 쓰는가](#숨은-매개변수-말고-또-무엇에-쓰는가)
- [재귀 감지와 깊이 카운터](#재귀-감지와-깊이-카운터)
- [예제가 보호 장치를 발동시키지 못하는 자리](#예제가-보호-장치를-발동시키지-못하는-자리)
- [평탄화 트랜잭션](#평탄화-트랜잭션)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프 값을 문맥 전달 말고 어디에 더 쓰는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상에서 정식 API다. JDK 21부터 24까지는 미리 보기(preview) 기능이라
> 컴파일과 실행에 `--enable-preview`가 필요하다 (5장, pp.217·226).[^rahman2025] 만료일은 달지
> 않는다 — 정식 API라 다음 릴리스를 재심 시점으로 잡을 근거가 없다.

## 숨은 매개변수 말고 또 무엇에 쓰는가

- 저자가 절을 열며 범위를 넓힌다 — 스코프 값은 오늘 스레드 로컬 변수가 쓰이는 많은 상황에서
  쓸모 있고 더 나은 선택일 가능성이 높으며, 숨은 메서드 매개변수 노릇을 넘어 특히 유용한 영역이
  몇 있다 (5장 §"Migrating to Scoped Values", p.237).[^rahman2025]
- 첫째로 드는 것이 재귀 감지다 — 프레임워크가 재진입 가능하지 않거나 재귀를 어떤 식으로든
  제한해야 해서 재귀를 감지하고 싶을 때가 있고, 스코프 값이 그것을 감지하고 다루는 방법을 준다
  (5장, p.237).[^rahman2025]

## 재귀 감지와 깊이 카운터

- 방법이 둘로 갈린다 (5장, p.237).[^rahman2025]
  - 평소처럼 `ScopedValue.run()`으로 설정해 두고, 호출 스택 깊은 곳에서 `ScopedValue.isBound()`를
    불러 현재 스레드에 바인딩이 있는지 검사한다. 있으면 이미 그 안에 있다는 뜻이다.
  - 더 정교하게는, 되풀이해 리바인딩함으로써 스코프 값이 재귀 카운터를 모형화하게 할 수 있다.
- 저자가 드는 실물은 중첩 템플릿을 다루는 문서 처리 시스템이다. 재귀 제한이 없으면 순환 참조를 가진
  악의적으로 만들어진 템플릿이 애플리케이션을 무너뜨릴 수 있다 (5장, p.237).[^rahman2025]
- 바깥 진입점이 바인딩의 유무로 갈린다 (5장, p.237).[^rahman2025]

  ```java
  public class TemplateProcessor {
      private static final ScopedValue<Integer> RECURSION_DEPTH = ScopedValue.newInstance();
      private static final int MAX_NESTING_LEVEL = 50;

      public String processTemplate(String template) {
          if (!RECURSION_DEPTH.isBound()) {
              return ScopedValue.where(RECURSION_DEPTH, 0)
                                .call(() -> processTemplateInternal(template));
          } else {
              return processTemplateInternal(template);
          }
      }
  }
  ```

- 안쪽 메서드가 카운터를 올린다 — 현재 깊이를 `get()`으로 읽어 `MAX_NESTING_LEVEL`과 견주고,
  중첩된 내용을 처리할 때는 `currentDepth + 1`로 리바인딩한 스코프 안에서 자기 자신을 다시 부른다
  (5장, p.238).[^rahman2025]
- 저자가 예제에 붙인 주석 넷 가운데 뒤의 둘이 이 구조의 요점이다 — 스코프 값이 되풀이해
  리바인딩되면서 재귀 카운터를 모형화하고, 그 메서드가 반환하면 이전 깊이 값이 자동으로 복원된다
  (5장, p.238).[^rahman2025] 되돌림이 자동이라는 것은
  [중첩 스코프에서의 리바인딩](../concepts/scoped-value-rebinding.md)의 성질 그대로다.
- 저자가 주석 하나에 스스로 단서를 단다 — 본문은 `ScopedValue.run()`으로 평소처럼 설정한다고
  적지만, 실린 코드는 `where()`와 `call()`을 쓴다. 그 둘이 현대 API라는 사실이 주석 안에
  괄호로 적혀 있다 (5장, p.238).[^rahman2025]

## 예제가 보호 장치를 발동시키지 못하는 자리

- 저자는 `main` 메서드를 소개하며 단순한 템플릿부터 재귀 보호 장치를 발동시키는 깊이 중첩된 것까지
  여러 쓰임을 보여 준다고 적는다 (5장, p.239).[^rahman2025]
- 그런데 실린 실행 결과는 예외를 내지 않는다. 셋째 예제가 `Level 0`부터 `Level 9`까지 이어진 뒤
  `level10.tpl`의 내용으로 정상 종료한다 (5장, p.240).[^rahman2025]
- 이유는 예제 자신에게 있다. 템플릿을 읽어 오는 흉내 메서드가 `level` 번호가 10보다 작을 때만
  다음 단계를 이어 붙이므로, 재귀 깊이가 `MAX_NESTING_LEVEL`인 50에 닿을 길이 없다 (5장,
  p.239).[^rahman2025]
- #hypothesis 소개 문장과 실행 결과가 어긋나는 이 자리는 예제의 상수 둘(멈춤 지점 10과 상한 50)이
  서로 맞춰지지 않은 결과로 보인다. 저자는 이 어긋남을 언급하지 않으므로 단정하지 않는다.
  카운터가 실제로 상한에 닿는 모습은 이 장에 실려 있지 않다.

## 평탄화 트랜잭션

- 둘째 쓰임은 재귀 감지의 다른 얼굴이다 — 평탄화 트랜잭션(flattened transactions)에서는 진행 중인
  트랜잭션이 있는 동안 시작된 트랜잭션이 가장 바깥 트랜잭션의 일부가 된다 (5장,
  p.240).[^rahman2025]
- 예제가 그 판정을 `isBound()` 하나로 한다. 바깥 트랜잭션을 만들어 스코프 값에 묶고, 중첩된
  연산은 이미 묶인 트랜잭션이 있는지 검사해 있으면 그것에 합류하고 없을 때만 새 트랜잭션을 연다
  (5장, pp.240–241).[^rahman2025]
- 저자가 이 패턴에서 짚는 것 넷 가운데 마지막이 결론이다 — 모든 연산이 같은 트랜잭션 문맥에
  참여하게 된다 (5장, p.241).[^rahman2025]
- 얻는 것이 둘이다 — 중첩된 것까지 모든 연산이 하나의 포괄적 트랜잭션의 일부가 되므로 관리가
  단순해지고 데이터 일관성이 지켜진다 (5장, p.241).[^rahman2025]
- 실행 결과가 그것을 그대로 보인다. 바깥 트랜잭션이 시작되고, 중첩된 연산이 새로 열지 않고
  그것에 합류하며, 데이터베이스 연산도 같은 트랜잭션에서 실행되고, 바깥 것이 커밋된다 (5장,
  p.241).[^rahman2025]

## 이어지는 페이지

- [중첩 스코프에서의 리바인딩](../concepts/scoped-value-rebinding.md) — 깊이 카운터가 기대는 성질
- [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md) — `isBound()`가 무엇을 답하는가
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — `call()`이 값을 돌려주는
  자리
- [ThreadLocal에서 스코프 값으로 옮기기](../concepts/migrating-from-thread-local-to-scoped-values.md) — 이
  쓰임들이 실려 있는 절의 나머지
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — 재진입 코드가 무엇이고
  왜 그 자체로 스레드 안전한가
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Migrating to Scoped Values"의 앞부분
    (pp.237–241). 개념당 대표 코드 하나 규칙에 따라 `TemplateProcessor`의 진입점만 실었고,
    `processTemplateInternal` 전문(p.238), 흉내 메서드 `loadTemplate`(p.239), 세 시나리오를
    도는 `main`(p.239), 그 실행 출력(p.240), `FlattenedTransactionExample` 전문(pp.240–241)과
    그 출력(p.241)은 미수록이다 — 각 예제가 보이는 결말은 본문에 옮겼다.
