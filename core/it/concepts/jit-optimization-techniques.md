---
type: concept
title: JIT 컴파일러의 최적화 기법
description: 핫스팟의 JIT 컴파일러가 쓰는 최적화 기법 전체 목록과 그 아홉 갈래 분류, 최적화가 자바 소스가 아니라 중간 표현에 적용된다는 전제, 그리고 게터 호출 두 번짜리 코드가 인라인·중복 저장 제거·복사 전파·죽은 코드 제거를 차례로 거치며 문장이 사라져 가는 과정
generated: { by: "claude-opus-5", at: "2026-08-15T23:20:00Z" }
sources:
  - { id: zhou2024, resource: /it/sources/zhou2024.md }
---

# JIT 컴파일러의 최적화 기법

- [번역이 아니라 최적화가 승부처다](#번역이-아니라-최적화가-승부처다)
- [기법 목록 — 아홉 갈래](#기법-목록--아홉-갈래)
- [예제를 읽기 전의 전제](#예제를-읽기-전의-전제)
- [네 번의 최적화가 지나간 자리](#네-번의-최적화가-지나간-자리)
- [자세히 볼 네 가지](#자세히-볼-네-가지)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **JIT 컴파일러가 실제로 하는 최적화에는 무엇이 있고, 그것들이 코드를 어떻게
바꾸는가.**

## 번역이 아니라 최적화가 승부처다

- 컴파일러의 목표와 난점이 분리된다 — **컴파일러의 목표는 프로그램 코드를 기계어로 번역하는
  것이다. 하지만 기계어로 번역하는 일 자체는 어려운 주제가 아니다. 출력 코드가 얼마나 잘
  최적화되었느냐가 컴파일러의 우수성을 결정하는 핵심이다** (11장, p.549).[^zhou2024]

## 기법 목록 — 아홉 갈래

- 목록의 출처가 문서다 — **OpenJDK 공식 위키에는 핫스팟의 JIT 컴파일러가 이용하는 최적화 기법들이
  나열되어 있다** (11장, p.550).[^zhou2024] 저자의 관찰은 **전통적인 컴파일러에서 쓰는 최적화
  기법도 많으며, 자바 언어나 자바 가상 머신에서 실행되는 언어들에 대응하는 최적화도 많다**는
  것이다 (11장, p.550).

  | 유형 | 최적화 기법 |
  |---|---|
  | 컴파일러 전략 | 지연 컴파일(delayed compilation) · 계층형 컴파일(tiered compilation) · 온스택 치환 · 지연 재최적화(delayed reoptimization) · 프로그램 의존성 그래프 표현(program dependence graph representation) · 정적 단일 할당 표현(static single assignment representation) |
  | 성능 모니터링 기반 기법(profile-based technique) | 낙관적 널 단언(optimistic nullness assertion) · 낙관적 타입 단언(optimistic type assertion) · 낙관적 타입 강화(optimistic type strengthening) · 낙관적 배열 길이 강화(optimistic array length strengthening) · 닿지 않는 가지(브랜치) 치기(untaken branch pruning) · 낙관적 N-모픽 인라인(optimistic N-morphic inlining) · 분기 빈도 예측(branch frequency prediction) · 호출 빈도 예측(call frequency prediction) |
  | 증명 기반 기법(proof-based technique) | 정확한 타입 추론(exact type inference) · 메모리 값 추론(memory value inference) · 메모리 값 추적(memory value tracking) · 상수 접기(constant folding) · 재결합(reassociation) · 연산자 강도 감소(operator strength reduction) · 널 검사 제거(null check elimination) · 타입 검사 강도 감소(type test strength reduction) · 타입 검사 제거(type test elimination) · 대수식 단순화(algebraic simplification) · 공통 하위 표현식 제거(common subexpression elimination) |
  | 흐름 인지 재작성(flow-sensitive rewrite) | 조건부 상수 전파(conditional constant propagation) · 흐름 분석 기반 타입 범위 좁히기(flow-carried type narrowing) · 죽은 코드 제거(dead code elimination) |
  | 언어 특화 기법(language-specific technique) | 클래스 계층 구조 분석(class hierarchy analysis) · 가상화 제거(devirtualization) · 심벌 상수 전파(symbolic constant propagation) · 오토박싱 제거(autobox elimination) · 탈출 분석(escape analysis) · 락 생략(lock elision) · 락 범위 확대(lock coarsening) · 리플렉션 취소(de-reflection) |
  | 메모리 및 배치 변환(memory and placement transformation) | 표현식 끌어올리기(expression hoisting) · 표현식 끌어내리기(expression sinking) · 중복 저장 제거(redundant store elimination) · 인접한 저장 합치기(adjacent store fusion) · 병합 지점 분할(merge-point splitting) |
  | 루프 변환(loop transformation) | 순환문 풀기(loop unrolling) · 순환문 벗기기(loop peeling) · 안전 지점 제거(safepoint elimination) · 반복 범위 분할(iteration range splitting) · 범위 확인 제거(range check elimination) · 순환문 벡터화(loop vectorization) |
  | 전역 코드 형태 가공(global code shaping) | 인라인 · 전역 코드 이동 · 실행 빈도 기반 코드 재배치(heat-based code layout) · 스위치 밸런싱(switch balancing) |
  | 제어 흐름 그래프 변환(control flow graph transformation) | 지역 코드 스케줄링(local code scheduling) · 지역 코드 번들링(local code bundling) · 지연 슬롯 채우기(delay slot filling) · 그래프 채색 레지스터 할당(graph-coloring register allocation) · 선형 스캔 레지스터 할당(linear scan register allocation) · 복사 병합(copy coalescing) · 상수 분할(constant splitting) · 복사 제거(copy removal) · 주소 모드 매칭(address mode matching) · 명령어 핍홀(instruction peepholing) · 결정적 유한 상태 머신 기반 코드 생성(DFA-based code generator) |

- 목록의 길이에 대해 저자가 붙인 말이 있다 — **최적화 기법은 종류가 어마어마하고 이름만 보고 바로
  이해되는 기법은 많지 않다. 사실 대다수 최적화 기법은 구현하기는 어렵지만 이해하기는 어렵지 않은
  경우가 많다** (11장, p.551).[^zhou2024]

## 예제를 읽기 전의 전제

- 이하의 자바 코드는 설명용 표기일 뿐이다 — **JIT 컴파일러가 수행하는 최적화와 변환은 자바 소스
  코드에 직접 적용되는 게 아니라 네이티브 코드나 중간 표현에 적용됨을 잊지 말자. 이 책에서는
  설명을 쉽게 하기 위해 자바 언어의 구문을 사용했을 뿐이다** (11장, p.551).[^zhou2024] 그 중간
  표현이 무엇인지는
  [JIT 컴파일러의 컴파일 과정](../concepts/jit-compilation-process.md)에 있다.

## 네 번의 최적화가 지나간 자리

- 출발점은 게터를 두 번 부르는 코드다 (11장, p.552, 코드 11-4):[^zhou2024]

  ```java
  static class B {
      int value;

      final int get() {
          return value;
      }
  }

  public void foo() {
      y = b.get();
      // ...무언가 수행...
      z = b.get();
      sum = y + z;
  }
  ```

- ① 메서드 인라인이 가장 먼저 온다 — **메서드를 인라인하는 목적은 두 가지다. 첫 번째는 메서드
  버전 찾기나 스택 프레임 구축 등의 메서드 호출 비용을 없애는 것이고, 두 번째는 다른 최적화를
  적용하기 쉽도록 길을 미리 평탄하게 닦는 것이다. 메서드 인라인은 후속 최적화를 더 큰 규모로
  수행하기 쉽게 해 주어 더 나은 최종 결과를 낳는 밑거름 역할을 한다. 많은 컴파일러가 다양한
  최적화 중 인라인을 가장 먼저 수행하곤 하는 이유다** (11장, p.552).[^zhou2024] 결과는
  `y = b.value; … z = b.value; sum = y + z;`다 (코드 11-5).
- ② 중복 저장 제거 — **코드 중간의 주석 `// ...무언가 수행...` 부분에서 `b.value`의 값을
  변경하지 않는다고 가정하자. 그러면 다음 줄의 `z = b.value`를 `z = y`로 대체할 수 있다. 첫 문장
  `y = b.value`가 변수 `y`와 `b.value`가 같다고 확인해 주기 때문이다. 이런 식으로 중간에 `b`
  객체를 거쳐 변수에 접근하는 수고를 없앨 수 있다** (11장, pp.552–553).[^zhou2024]
  - 같은 변환에 이름이 둘 붙는다 — **`b.value`를 표현식으로 본다면 이 최적화는 공통 하위 표현식
    제거에 해당한다** (11장, p.553).
- ③ 복사 전파 — **이 프로그램에서는 논리적으로 변수 `y`와 완전히 같은 또 다른 변수 `z`를 사용할
  필요가 없다. `z` 대신 `y`를 써도 똑같다는 뜻이다** (11장, p.553).[^zhou2024] 결과는
  `y = y; sum = y + y;`다 (코드 11-7).
- ④ 죽은 코드 제거 — **죽은 코드란 실행되지 않을 코드일 수도 있고, 실행해도 의미가 전혀 없는
  코드일 수도 있다. 그래서 '죽은 코드'라는 직관적인 이름으로 불린다. 앞의 코드에서 `y = y`
  문장은 아무 의미가 없다** (11장, p.553).[^zhou2024] 남는 것은 이것뿐이다 (코드 11-8):

  ```java
  public void foo() {
      y = b.value;
      // ...무언가 수행...
      sum = y + y;
  }
  ```

- 결론이 등가성과 효율을 함께 말한다 — **지금까지 총 네 번의 최적화를 거친 코드 11-8은 아무런
  최적화도 하기 전인 코드 11-4와 완전히 같은 효과를 낸다. 하지만 많은 문장이 제거된 덕분에
  바이트코드와 기계어 명령어가 달라지고 실행 효율 측면에서도 차이가 클 것이다. 이러한 최적화를
  컴파일러에 구현해 넣기는 매우 복잡할 수 있지만, 다행히 동작을 이해하기는 프로그래밍
  초보자라도 그리 어렵지 않을 것이다** (11장, pp.553–554).[^zhou2024]

## 자세히 볼 네 가지

- 저자가 골라 낸 대표는 넷이고, 고른 기준이 각각 다르다 (11장, p.554):[^zhou2024]

  | 기법 | 저자가 붙인 자리 |
  |---|---|
  | 메서드 인라인 | **가장 중요한 최적화 기법** |
  | 탈출 분석 | **비교적 첨단 최적화 기법** |
  | 공통 하위 표현식 제거 | **고전적인 언어 독립적 최적화 기법** |
  | 배열 경계 검사 제거 | **고전적인 언어 특화 최적화 기법** |

## 이어지는 페이지

- [메서드 인라인](../concepts/method-inlining.md) — '최적화의 어머니'가 가상 메서드라는 벽을
  넘는 방법
- [JIT 컴파일러의 컴파일 과정](../concepts/jit-compilation-process.md) — 이 기법들이 걸리는
  중간 표현과 단계
- [자바의 AOT 컴파일](../concepts/aot-compilation-in-java.md) — 급진적 예측 최적화가 JIT에만
  허락되는 이유
- [javac의 컴파일 과정](../concepts/javac-compilation-process.md) — 같은 이름의 상수 접기가
  프런트엔드에도 있다는 사실
- [핫스팟 JIT 코드 들여다보기](../concepts/hotspot-jit-inspection-tools.md) — 이 최적화들이
  적용되는 순간을 IGV로 확인하는 쪽

[^zhou2024]: 저우즈밍 2024(한국어판), 11장 "백엔드 컴파일과 최적화" §11.4 도입(p.549)과
    §11.4.1(pp.550–554). 표는 원문 표 11-1(pp.550–551)을 그대로 옮긴 것이며, 원문이 출처로 든
    OpenJDK 위키 `PerformanceTacticIndex`(각주 20)와 예제 출처인 오라클 JRockit 문서(각주 21)는
    링크라 옮기지 않았다. 이 소스의 PDF는 OCR 텍스트라 영문 용어가 훼손되어 있어 널리 쓰이는
    표기로 복원했다 — `nullness`가 "n나Iness"로, `elimination`이 "이imination"으로, `value`가
    "val니e"로, `redundant`가 "red니ndant"로, `scheduling`이 "codesched니ing"으로, `peepholing`이
    "peeph이ing"으로, "주소 모드 매칭"이 "주소 모드 nH칭"으로 깨져 있었다. 코드 11-4~11-8도
    `b.get()`이 "b.getO"로, 변수 `z`가 "그"로 깨져 있어 본문 서술과 일치하는 쪽으로 복원했고,
    중간 단계인 코드 11-5·11-7은 한 줄만 바뀌므로 펜스 대신 본문에 인라인으로 적었다
