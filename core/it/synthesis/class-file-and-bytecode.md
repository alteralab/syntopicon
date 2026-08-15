---
type: synthesis
title: 클래스 파일과 바이트코드
description: 자바 가상 머신이 유일하게 의존하는 바이너리 형식의 진입점 — 형식의 뼈대와 매직 넘버·버전 번호, 상수 풀, 필드·메서드 테이블, 속성 테이블과 그 안의 Code 속성, 그리고 그 위에 실리는 바이트코드 명령어 집합
generated: { by: "claude-opus-5", at: "2026-08-15T13:00:00Z" }
---

# 클래스 파일과 바이트코드

**이름의 범위가 곧 이 허브의 범위다.** 여기는 컴파일 결과물의 **저장 형식**, 그 안에 실리는
**명령어 집합**, 그 명령어를 돌리는 **실행 엔진**, 그리고 그 결과물을 만들어 내는 **프런트엔드
컴파일러**가 산다. 그 파일을 읽어 들이는
절차(클래스 로딩)는 형제 허브 [클래스 로딩](class-loading.md)이 다룬다. 가상 머신 자체와 그 판올림은
[자바 기술 시스템](java-technology-system.md)이, 실행 중 메모리는
[JVM 자동 메모리 관리](jvm-memory-management.md)가 담당한다.

읽는 순서가 있다. 이 형식이 무엇을 위한 것인지를 먼저 보고, 파일의 뼈대에서 시작해 항목을
하나씩 열어 간 뒤, 마지막이 명령어 집합이다.

## 무엇을 위한 형식인가

- [가상 머신의 플랫폼 독립과 언어 독립](../concepts/jvm-language-independence.md) — 바이트코드가
  플랫폼 독립성을 담는 자리, 명세를 언어와 가상 머신으로 나눈 설계, 형식만 정하고 구현은 열어
  두는 원칙

## 파일의 뼈대

- [클래스 파일 형식](../concepts/class-file-format.md) — 구분 기호 없는 빅 엔디언 이진 스트림,
  부호 없는 숫자와 테이블, `ClassFile` 구조의 순서, `0xCAFEBABE`와 버전 번호가 정하는 호환 범위

## 항목 하나씩

- [클래스 파일의 상수 풀](../concepts/class-file-constant-pool.md) — 17가지 상수 타입, 1부터
  세는 인덱스, 링크 단계가 없다는 사실이 남긴 심벌 참조
- [클래스 파일의 필드와 메서드 기술](../concepts/class-file-fields-and-methods.md) — 접근
  플래그, 상속 관계를 정하는 세 인덱스, 구조가 같은 두 테이블, 서술자 문법
- [클래스 파일의 속성 테이블](../concepts/class-file-attributes.md) — 형식이 20년 넘게 추가만으로
  확장되어 온 통로와 지금 거기 실린 30개 속성
- [클래스 파일의 Code 속성](../concepts/class-file-code-attribute.md) — 메서드 본문이 사는 자리,
  스택 깊이와 변수 슬롯, 예외 테이블

## 그 위에 실리는 것

- [바이트코드 명령어 집합](../concepts/jvm-bytecode-instruction-set.md) — 1바이트 연산 코드가
  만든 제약과 아홉 가지 명령어 범주

## 그것을 돌리는 쪽

- [런타임 스택 프레임 구조](../concepts/stack-frame-structure.md) — 메서드 하나가 쓰는 지역 변수
  테이블과 피연산자 스택, 변수 슬롯 재사용이 가비지 컬렉션에 남기는 흔적, 동적 링크와 반환 주소
- [메서드 호출과 디스패치](../concepts/method-invocation-and-dispatch.md) — 어느 버전의 메서드를
  부를지 정하는 절차, 비가상 메서드와 호출 명령어 다섯 개, 정적·동적 디스패치, 가상 메서드 테이블
- [메서드 핸들과 invokedynamic](../concepts/method-handles-and-invokedynamic.md) — 디스패치
  로직을 사용자 코드로 넘기는 다섯 번째 호출 명령어와 메서드 핸들
- [스택 기반 바이트코드 해석 실행 엔진](../concepts/stack-based-interpreter.md) — 스택 기반 명령어
  집합의 맞교환과 명령어를 하나씩 따라간 실행 과정

## 그것을 만들어 내는 쪽

- [javac의 컴파일 과정](../concepts/javac-compilation-process.md) — 프런트엔드 컴파일러가 거치는
  준비 하나와 처리 셋, 애너테이션 처리 라운드, 상수 접기, `<init>`·`<clinit>`가 만들어지는 자리
- [자바의 편의 문법 해체](../concepts/java-syntactic-sugar.md) — 순회 루프 한 줄에 겹친 다섯 가지
  문법이 제거되면 나오는 코드, 오토박싱의 함정, `if` 상수 조건으로 하는 조건부 컴파일
- [제네릭과 타입 소거](../concepts/java-generics-and-type-erasure.md) — 바이너리 하위 호환성이
  강제한 소거 방식, 원시 타입과 형 변환 코드 삽입, `Signature` 속성이 남겨 둔 것

## 경계에 있는 페이지

- [온디스크 파일 형식](../concepts/on-disk-file-format.md) — 매직 넘버·버저닝·바이트 순서·가변
  길이 데이터라는 같은 문제를 저장 엔진 쪽에서 푸는 방식
- [그랄VM과 네이티브 이미지](../concepts/graalvm-and-native-image.md) — 이 형식의 언어 독립성을
  제품으로 만든 쪽
- [핫스팟 JIT 코드 들여다보기](../concepts/hotspot-jit-inspection-tools.md) — 바이트코드가
  네이티브 코드로 바뀐 뒤를 되돌려 읽는 도구
- [런타임 데이터 영역과 메모리 오버플로](../concepts/jvm-runtime-data-areas.md) — 상수 풀과 스택
  프레임이 실행 중 올라가는 자리

## 이어지는 허브

- [자바 기술 시스템](java-technology-system.md) — 이 형식을 읽는 가상 머신과 JDK 자체
- [JVM 자동 메모리 관리](jvm-memory-management.md) — 이 명령어들이 실행될 때의 메모리
- [JVM 모니터링과 문제 해결 도구](jvm-troubleshooting-tools.md) — javap를 포함한 JDK 도구들
