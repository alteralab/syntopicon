---
type: concept
title: jaotc로 미리 컴파일해 보기
description: JDK 9에 들어왔다 16에서 빠진 AOT 컴파일 도구를 손으로 확인하는 절차 — 클래스 하나를 정적 링크 라이브러리로 만들어 실행하는 최소 예제, java.base 모듈을 통째로 사전 컴파일할 때 필요한 제외 목록과 가비지 컬렉터 제약, 그리고 5분에 353MB라는 실측치와 PrintAOT로 확인하는 적용 범위
generated: { by: "claude-opus-5", at: "2026-08-15T23:10:00Z" }
sources:
  - { id: zhou2024, resource: /it/sources/zhou2024.md }
---

# jaotc로 미리 컴파일해 보기

- [무엇이었고 왜 사라졌는가](#무엇이었고-왜-사라졌는가)
- [그랄 컴파일러의 AOT와 다른 점](#그랄-컴파일러의-aot와-다른-점)
- [최소 예제 — 클래스 하나](#최소-예제--클래스-하나)
- [java-base 모듈을 통째로](#java-base-모듈을-통째로)
- [가비지 컬렉터 제약](#가비지-컬렉터-제약)
- [실측 결과](#실측-결과)
- [무엇이 사전 컴파일되었는지 확인하기](#무엇이-사전-컴파일되었는지-확인하기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **JIT가 런타임에 할 일을 미리 해 두는 방식을 실제로 돌려 보면 무엇이
필요하고 무엇이 남는가.**

## 버전 조건

> **버전 조건**: JDK 9 이상 JDK 15 이하 — jaotc가 표준 JDK에 실려 있던 구간이다. **표준
> JDK에서는 16 버전부터 jaotc 제공을 중단했다** (11장, p.549).[^zhou2024] 이 페이지의 실습
> 수치는 **LTS 버전인 OpenJDK 11**에서 나온 것이다 (11장, p.545, 각주 18).

## 무엇이었고 왜 사라졌는가

- 도입 목적과 제약이 한 문단에 있다 — **JDK 9는 클래스 파일과 모듈의 AOT 컴파일을 지원하는
  도구인 jaotc를 도입했다. jaotc는 프로그램 구동과 예열 시간을 줄여 최대 성능을 빨리 끌어낸다.
  하지만 이 기능은 특정 하드웨어에서 특정 가상 머신 매개 변수를 설정해 사용해야 한다. 다른
  제약도 너무 많기 때문에 잘 이해하고 활용하는 개발자가 많지 않았다. 사실 너무 적어서 관련
  코드와 도구를 그랄VM 쪽으로 넘기고 JDK 16부터는 표준 JDK에서 제거했다** (11장,
  p.545).[^zhou2024] 근거 문서는 **JEP 410: Remove the Experimental AOT and JIT Compiler**다
  (11장, p.545, 각주 18).

## 그랄 컴파일러의 AOT와 다른 점

- 같은 AOT라도 결과물의 실행 조건이 다르다 — **그랄VM에 포함된 그랄 컴파일러와 jaotc는 목적과
  사용법에서 차이가 있다. jaotc는 코드 일부를 네이티브로 미리 컴파일해 두지만, 여전히 자바 가상
  머신에서 구동되는 것을 가정한다. 반면 그랄 컴파일러의 AOT는 가상 머신 없이 실행되는 네이티브
  이미지를 생성한다** (11장, pp.545–546).[^zhou2024] 그쪽은
  [그랄VM과 네이티브 이미지](../concepts/graalvm-and-native-image.md)에 있다.

## 최소 예제 — 클래스 하나

- 절차는 컴파일·라이브러리 생성·확인·실행 넷이다 (11장, p.546):[^zhou2024]

  ```sh
  javac HelloWorld.java
  java HelloWorld
  # Hello World!

  jaotc --output libHelloWorld.so HelloWorld.class

  ldd libHelloWorld.so     # statically linked
  nm  libHelloWorld.so     # HelloWorld.<init>()V 와 HelloWorld.main([Ljava/lang/String;)V 가 보인다

  java -XX:+UnlockExperimentalVMOptions -XX:AOTLibrary=./libHelloWorld.so HelloWorld
  # Hello World!
  ```

  - 확인 명령이 무엇을 말해 주는지가 적혀 있다 — **리눅스의 `ldd` 명령을 사용하여 이것이 정적 링크
    라이브러리인지 확인하고, `nm` 명령으로 생성자와 `main()` 메서드가 제대로 포함되어 있는지
    확인할 수 있다** (11장, p.546).
  - 실행 매개 변수 하나가 잠금 해제용이다 — **`-XX:+UnlockExperimentalVMOptions` 매개 변수는
    실험 버전 기능을 활용할 수 있게 해 준다** (11장, p.546).

## java-base 모듈을 통째로

- 최소 예제로는 의미가 없다 — **`HelloWorld` 정도로는 AOT 컴파일의 효과를 체감할 수 없으니 좀
  더 실용적인 작업을 해 보자** (11장, p.547).[^zhou2024]
- 통째로 컴파일하려면 예외 목록이 필요하다 — **`java.base`에는 엄청난 양의 코드가 들어 있다. 그중
  대부분은 jaotc의 AOT 컴파일을 지원하지만 컴파일 오류를 일으키는 메서드가 몇 개 있다. 다행히
  문제가 되는 메서드들을 파일로 작성해 한 번에 건네줄 수 있다** (11장, p.547).[^zhou2024]
  제외 목록(코드 11-3)은 네 부류를 주석으로 구분한다 — `java.lang.StackOverflowError`를 내는
  `sun.util.resources`의 `getContents()` 계열, **Trampoline must not be defined by the bootstrap
  classloader** 오류를 내는 `sun.reflect.misc.Trampoline`, JVM 단언(assert)에 걸리는
  `com.sun.crypto.provider`·`sun.security.ssl`·`sun.net.RegisteredDomain` 계열, 그리고 너무 커서
  빠지는 `jdk.internal.module.SystemModules.descriptors()` (11장, p.547).
- 실제 명령은 이렇다 (11장, p.547):[^zhou2024]

  ```sh
  jaotc -J-XX:+UseCompressedOops -J-XX:+UseG1GC -J-Xmx4g --compile-for-tiered --info \
        --compile-commands java.base-list.txt --output libjava.base-coop.so --module java.base
  ```

  - 가상 머신 매개 변수를 넘기는 통로가 따로 있다 — **`-J` 매개 변수는 가상 머신에 전달할 매개
    변수 정보를 jaotc에 알려 주는 역할이다. 이 정보는 컴파일된 정적 링크 라이브러리에 기록되어
    라이브러리를 이용하는 가상 머신에까지 전달된다** (11장, pp.547–548).

## 가비지 컬렉터 제약

- 컴파일러 계보가 그대로 제약이 된다 — **jaotc는 그랄 컴파일러를 기초로 개발되었기 때문에 그랄
  컴파일러를 지원하지 않는 ZGC와 셰넌도어 가비지 컬렉터는 당연히 jaotc에서 사용할 수 없다.
  그래서 JDK 11의 jaotc는 G1과 패러렐(PS+PS 올드), 2개의 가비지 컬렉터만 지원한다** (11장,
  p.548).[^zhou2024] 컬렉터별 성격은
  [핫스팟의 고전 가비지 컬렉터](../concepts/hotspot-classic-collectors.md)에 있다.

## 실측 결과

- 시간과 크기가 함께 기록되어 있다 (11장, p.548):[^zhou2024]

  ```text
  Compiling libjava.base-coop.so...
  6272 classes found (505 ms)
  56501 methods total, 50070 methods to compile (1265 ms)
  Compiling with 4 threads
  50070 methods compiled, 0 methods failed (277459 ms)
  Parsing compiled code (1343 ms)
  Processing metadata (14906 ms)
  Preparing stubs binary (1 ms)
  Preparing compiled binary (164 ms)
  Creating binary: libjava.base-coop.o (4178 ms)
  Creating shared library: libjava.base-coop.so (7035 ms)
  Total time: 312251 ms
  ```

  - 저자의 요약은 두 줄이다 — **JDK 11의 `java.base`를 컴파일하는 데는 몇 분 정도 걸릴 것이다.
    생성된 `libjava.base-coop.so` 라이브러리의 크기는 353MB다** (11장, p.548). 바이트
    팽창(byte bloat)이라는 AOT의 단점이 이 숫자로 나타난다.

## 무엇이 사전 컴파일되었는지 확인하기

- 링크는 쉼표로 여러 개를 건다 — **컴파일이 완료되면 사전 컴파일된 버전의 `java.base` 모듈을
  사용하여 자바 프로그램들을 실행할 수 있다. (…) `-XX:AOTLibrary` 매개 변수로 링크할
  라이브러리의 위치를 알려 주면 된다** (11장, p.548):[^zhou2024]

  ```sh
  java -XX:+UnlockExperimentalVMOptions -XX:+PrintAOT \
       -XX:AOTLibrary=./libjava.base-coop.so,./libHelloWorld.so HelloWorld
  ```

- 적용 범위는 매개 변수 하나로 드러난다 — **`-XX:+PrintAOT` 매개 변수로는 사전 컴파일된 버전을
  사용하는 메서드를 확인할 수 있다. 다음 출력 정보에서 알 수 있듯이 사전 컴파일된 `java.base`
  모듈을 사용하지 않으면 `HelloWorld`의 생성자와 `main()` 메서드만 사전 컴파일된 버전이다**
  (11장, p.548).[^zhou2024] 라이브러리를 함께 걸면 달라진다 — **`libjava.base-coop.so`를
  추가하면 표준 자바 SE API 거의 모두가 사전 컴파일된 버전을 이용한다.** 출력에는
  `java.lang.Object`의 `<clinit>()`·`finalize()`까지 `aot[1]` 표시와 함께 나온다 (11장, p.549).

## 이어지는 페이지

- [자바의 AOT 컴파일](../concepts/aot-compilation-in-java.md) — 이 실습이 속한 갈래와 그 장단점
- [그랄VM과 네이티브 이미지](../concepts/graalvm-and-native-image.md) — 이 코드와 도구가
  넘어간 곳
- [구동 시간 줄이기의 실전](../concepts/jvm-startup-time-optimization.md) — 사전 컴파일이 줄이려는
  그 시간
- [자바 모듈 시스템](../concepts/java-module-system.md) — 컴파일 단위가 된 `java.base`가 무엇인가
- [핫스팟의 고전 가비지 컬렉터](../concepts/hotspot-classic-collectors.md) — 함께 쓸 수 있는
  컬렉터가 둘로 좁혀지는 이유

[^zhou2024]: 저우즈밍 2024(한국어판), 11장 "백엔드 컴파일과 최적화" §11.3.2(pp.545–549).
    코드 11-3(`java.base-list.txt` 전문)은 OCR로 `exclude` 줄의 정규식 이스케이프와 클래스 이름이
    심하게 깨져(`sun.util.resources`가 "sun.util.reso나rces"·"sun.니til.resources"로,
    `exclude`가 "excl니de"로) 원형 복원이 불가능해 직인용하지 않고 주석이 가른 네 부류만 옮겼다.
    `-XX:+PrintAOT` 출력 두 벌(pp.548–549)도 열이 줄 단위로 흩어져 원형을 잃어 저자의 해설만
    옮겼다. jaotc 실행 로그는 훼손이 없어 그대로 실었다. 명령 펜스는 원문 예제에서 셸
    프롬프트(`$`)를 떼고 지면 폭 때문에 접힌 줄을 이어 붙인 것이며, 식별자는 본문 서술과 일치하는
    쪽으로 복원했다 — `-J-XX:+UseG1GC`가 "UseGlGC"로, `--compile-for-tiered`가
    "--compile-for-1iered"로, `--output`이 "--o나tput"으로, `ldd`가 "Idd"로, `HelloWorld`가
    "HelioWorld"·"HelloWorid"로, `G1`이 "이"로 깨져 있었다
