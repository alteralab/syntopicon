---
type: concept
title: OpenJDK 직접 빌드하기
description: 가상 머신 내부를 소스로 확인하려 할 때 필요한 준비 — 소스를 어디서 받고 어떤 하드웨어·툴체인·부트 JDK가 필요한지, configure가 받는 매개 변수로 무엇을 고를 수 있는지, make 타깃과 생성되는 디렉터리, 그리고 템플릿 인터프리터 때문에 중단점이 안 걸릴 때 쓰는 매개 변수
generated: { by: "claude-opus-5", at: "2026-08-15T12:00:00Z" }
sources:
  - { id: zhou2024, resource: /it/sources/zhou2024.md }
---

# OpenJDK 직접 빌드하기

- [왜 직접 빌드하는가](#왜-직접-빌드하는가)
- [소스와 시스템 요구 사항](#소스와-시스템-요구-사항)
- [툴체인과 부트 JDK](#툴체인과-부트-jdk)
- [configure가 고르게 해 주는 것](#configure가-고르게-해-주는-것)
- [make와 산출물](#make와-산출물)
- [통합 개발 환경에서 디버깅하기](#통합-개발-환경에서-디버깅하기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **핫스팟 소스를 실제로 컴파일하고 디버깅하려면 무엇을 준비하고 어떤 선택을
해야 하는가.**

## 왜 직접 빌드하는가

- **자바 가상 머신의 내부 구현 원리를 엿볼 수 있는 가장 직접적인 길은 바로 JDK를 직접
  컴파일하고 JDK 소스 코드를 읽고 분석하고 디버깅해 가며 자바 기술 시스템이 어떻게 동작하는지
  이해해 보는 것**이다 (1장, p.44).[^zhou2024]
- 실무적인 이유도 있다 — **자바 클래스 라이브러리의 저수준 메서드 다수는 네이티브 코드로
  작성되어 있다. 이런 메서드들의 동작을 이해하려고 하거나 JDK를 필요에 맞게 수정하거나 섬세하게
  최적화하려면 가상 머신 코드를 직접 컴파일하고 디버깅할 수 있어야 한다** (1장,
  p.44).[^zhou2024]

## 소스와 시스템 요구 사항

- 책이 고른 대상은 **OpenJDK 17** 이며, **자바 SE 참조 구현 페이지에서 'zip file' 링크로 전체
  소스를 받을 수 있다.** **받은 zip 파일의 크기는 164MB이며 압축을 풀면 약 582MB**다 (1장,
  pp.44–45).[^zhou2024]
- **JDK 16부터 소스 코드 저장소를 깃허브로 옮겨 관리하고 있다.** **깃허브에는 JDK 7부터 현재
  개발 중인 최신 버전까지 모든 코드가 담겨 있다** (1장, p.45).[^zhou2024]
- 플랫폼 권고 — **OpenJDK 빌드는 되도록이면 리눅스나 맥OS에서 진행하길 권한다. 툴체인과 필요한
  라이브러리를 준비하기가 윈도우보다 훨씬 쉽기 때문**이며, 책은 **우분투 22.04 LTS**에서
  진행한다. 더 자세한 안내는 **소스 코드에 포함된 `JDK_SRC_HOME/doc/building.html`** 이 정본
  이다 (1장, pp.45–46).[^zhou2024]
- **공식 문서에 따른 OpenJDK 컴파일의 최소 요구 사항**은 이렇다(x86 기준) (1장, p.46):[^zhou2024]
  - **CPU: 2~4코어**
  - **메모리: 2~4GB**(CPU 코어가 많을수록 메모리를 더 소비함)
  - **디스크 여유 공간: 6GB**
  - 디스크가 그만큼 필요한 이유 — **소스 코드 자체는 600MB가 채 안 되지만 컴파일 도중 수많은
    중간 파일이 만들어지고, 핫스팟 가상 머신은 최적화 수준(Product, FastDebug, SlowDebug)에 따라
    중간 파일을 반복해서 생성할 수도 있다** (1장, p.46).
- 32비트로 만들 때도 64비트 시스템에서 하라고 권한다 — **컴파일 과정에서 메모리를 많이
  사용하기 때문**이며(32비트 시스템은 메모리가 4GB로 제한), 32비트로 컴파일하려면
  `--with-target-bits=32`를 지정한다 (1장, p.46).[^zhou2024]
- 함정 하나가 따로 경고된다 — **컴파일을 한글이 포함된 디렉터리에서 수행하면 안 된다. JDK 소스
  코드는 물론 컴파일에 필요한 다른 프로젝트들의 파일 모두에 해당한다** (1장,
  p.46).[^zhou2024]

## 툴체인과 부트 JDK

- **맥OS의 경우 10.13(High Sierra) 이상을 권장하며, 최신 버전의 XCode와 XCode용 명령 줄
  도구(Command Line Tools)가 필요하다** — **이 개발자 도구에 OpenJDK를 컴파일할 Clang
  컴파일러와 Makefile에서 쓰는 기타 외부 도구들이 포함되어 있다** (1장, pp.46–47).[^zhou2024]
- **우분투에서는 GCC와 Clang 중 선택할 수 있다. GCC는 5.0 이상이 필요하며 권장 버전은 10.2다.
  Clang은 3.5 이상이 필요하다** (1장, p.47).[^zhou2024]
- 컴파일을 완료하려면 **다수의 서드 파티 라이브러리와 빌드 도구가 필요하다** — **Fontconfig(폰트
  설정), FreeType(폰트 렌더링), CUPS, X11(X 윈도 시스템), ALSA, libffi(포터블 외부 함수
  인터페이스(foreign function interface) 라이브러리), Autoconf(M4 매크로의 확장 패키지)** (1장,
  p.47).[^zhou2024] 우분투에서 미리 설치하는 명령은 이렇다.

  ```sh
  sudo apt-get install build-essential
  sudo apt-get install libfontconfig1-dev
  sudo apt-get install libfreetype6-dev
  sudo apt-get install libcups2-dev
  sudo apt-get install libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev
  sudo apt-get install libasound2-dev
  sudo apt-get install libffi-dev
  sudo apt-get install autoconf
  ```

- 자바로 자바를 컴파일해야 하므로 **부트 JDK**가 필요하다 — **JDK를 구성하는 요소 중 일부는
  C·C++로 작성되었지만 그보다 더 많은 코드가 자바 언어로 구현되었고, 이 자바 코드들을
  컴파일하려면 또 다른 JDK가 이미 설치되어 있어야 한다.** **부트 JDK는 설치하려는 JDK의 '직전
  메이저 버전'이 원칙이며 같은 메이저 버전도 가능하다** (1장, pp.47–48).[^zhou2024]

## configure가 고르게 해 주는 것

- **OpenJDK를 컴파일하는 목적은 단지 컴파일된 제품을 얻기 위해서만은 아닌 경우가 많다. 예컨대
  디버깅이나 사용자화 등을 위해서일 때도 많다. 따라서 OpenJDK가 제공하는 컴파일 매개 변수들을
  알아 두는 게 좋다** (1장, p.48).[^zhou2024]
- 자주 쓰는 매개 변수는 이렇다 (1장, pp.48–49):[^zhou2024]

  | 매개 변수 | 무엇을 정하는가 |
  |---|---|
  | `--with-debug-level=<레벨>` | 컴파일 레벨. `release`·`fastdebug`·`slowdebug`이며 **최적화를 덜 수행할수록 디버깅 정보를 많이 제공한다.** 기본값은 `release` |
  | `--enable-debug` | `--with-debug-level=fastdebug`와 같다 |
  | `--with-native-debug-symbols=<방식>` | 디버그 심벌 정보의 컴파일 방식. `none`·`internal`·`external`·`zipped` |
  | `--with-version-string=<string>` | 컴파일된 JDK 버전. `java -version` 출력값이며 `--with-version-<부분>=<값>` 형태로 세분화 가능 |
  | `--with-jvm-variants=<변형>[,…]` | 핫스팟을 특별한 모드로 컴파일한다. `server`·`client`·`minimal`·`core`·`zero`·`custom` |
  | `--with-jvm-features=<기능>[,…]` | `custom` 가상 머신용 기능 목록. `--with-jvm-variants=custom`일 때 다양한 기능을 동시에 명시할 수 있다 |
  | `--with-target-bits=<비트>` | 32비트로 컴파일할지 64비트로 컴파일할지 |
  | `--with-<라이브러리>=<경로>` | 의존 패키지 경로. 여러 버전의 부트 JDK나 의존 패키지가 설치되어 있을 때 정확한 대상을 지정 |
  | `--with-extra-<플래그 종류>=<플래그들>` | 추가 컴파일 매개 변수. `cflags`·`cxxflags`·`ldflags` |
  | `--with-conf-name=<이름>` | 컴파일 설정 이름. 기본값은 `linux-x86_64-server-release` 형태로 자동 생성된다 |

  - **전체 목록은 `bash configure --help` 명령으로 확인할 수 있다** (1장, p.49).
- **`configure` 명령은 의존성 검사, 매개 변수 설정, 결과를 담을 디렉터리 구조 생성 등 다양한
  역할을 수행**하며, 성공하면 **컴파일 설정 이름, 디버그 레벨, 자바 가상 머신의 모드와 기능
  목록, 사용한 컴파일러 버전 등**을 담은 요약이 출력된다 (1장, pp.49–50).[^zhou2024] 그 요약의
  기능 목록이 [핫스팟의 모듈화](../concepts/hotspot-modularity-and-interfaces.md)가 말한 '골라
  담기'의 실물이다.

  ```text
  Configuration summary:
  * Name:           linux-x86_64-server-fastdebug
  * Debug level:    fastdebug
  * HS debug level: fastdebug
  * JVM variants:   server
  * JVM features:   server: 'cds compiler1 compiler2 epsilongc g1gc jfr
      jni-check jvmci jvmti management nmt parallelgc serialgc services
      shenandoahgc vm-structs zgc'
  ```

## make와 산출물

- 서버용 FastDebug 빌드를 만들고 JDK 이미지 전체를 컴파일하는 명령은 이렇다 (1장,
  pp.49–51):[^zhou2024]

  ```sh
  bash configure --enable-debug --with-jvm-variants=server
  make
  make images
  ```

  - **`make`는 JDK를 본격 빌드하는 단계로, 컴퓨터 성능에 따라 10분 이상 걸릴 수 있다** (1장,
    p.50).
  - **`images`란 `product-images`의 줄임말로, JDK 이미지 전체를 컴파일하는 타깃**이다 (1장,
    p.51).
  - 다른 타깃도 있다 — **`hotspot`(핫스팟만), `hotspot-<variant>`(지정한 모드의 핫스팟만),
    `docs-image`, `test-image`, `all-images`(product·docs·test를 차례로), `bootcycle-images`(JDK를
    두 번 컴파일하여 첫 번째 결과를 두 번째의 부트 JDK로 이용), `clean`, `dist-clean`** (1장,
    p.51).
  - 재설정 시 주의 — **디렉터리 구조가 성공적으로 만들어진 이후 다시 컴파일하거나 설정을
    변경하려면 `make clean`과 `make dist-clean` 명령을 차례로 실행해 미리 청소를 해 두어야
    한다** (1장, p.51).
- 산출물의 위치가 정해져 있다 — **컴파일이 완료되면 `JDK_SRC_HOME/build/<설정이름>/` 밑에
  `buildtools/`(컴파일 과정에서 쓰이는 도구), `hotspot/`(핫스팟이 컴파일하는 중간 파일),
  `images/`, `jdk/`(컴파일이 완료된 JDK), `support/`, `test-results/`, `configure-support/`,
  `make-support/`, `test-support/` 디렉터리들이 만들어진다** (1장, pp.50–51).[^zhou2024]
  - **`JDK_SRC_HOME/build/<설정이름>/jdk/` 디렉터리의 파일들을 `JAVA_HOME` 디렉터리에 복사하면
    완전한 JDK로 이용할 수 있다** (1장, p.51).
  - **OpenJDK 17 전체를 처음 컴파일하는 데는 상당한 시간이 소요되지만, 파일 몇 개만 수정해 다시
    빌드하면 증분 컴파일이 이루어져 몇 초면 끝날 것이다** (1장, p.51).

## 통합 개발 환경에서 디버깅하기

- **핫스팟 가상 머신을 디버깅용으로, 즉 최적화를 해제하고 심벌 정보를 포함하여 빌드한 결과는
  명령 줄에서 GDB로 곧바로 디버깅할 수 있다.** 책은 그 대신 **젯브레인즈의 CLion**에서 소스를
  임포트해 디버깅하는 방법을 설명한다 (1장, p.52).[^zhou2024]
  - **OpenJDK 자체는 통합 개발 환경용 프로젝트 설정을 따로 제공하지 않지만**, **코드 수정이나
    재컴파일 없이 CLion으로 소스 코드를 읽고 추적해 볼 수는 있다** — 실행 파일로 방금 빌드한
    `JDK_SRC_HOME/build/<설정이름>/jdk/bin/java`를 지정하면 된다 (1장, pp.53–54).
- 자바 코드를 추적하려 할 때 걸리는 벽이 하나 있다 — **핫스팟이 운영 체제 위에서 바이트코드를
  실행할 때 템플릿 인터프리터를 사용하기 때문**이며, **이 인터프리터는 JIT 컴파일러와 똑같이
  최종 실행 코드를 런타임에 생성하기 때문에 소스 코드에서 중단점을 직접 설정할 수 없다** (1장,
  pp.54–55).[^zhou2024]
  - 그래서 핫스팟이 따로 제공하는 것이 `-XX:+TraceBytecodes -XX:StopInterpreterAt=<n>`이며,
    **일련번호 `<n>`에 해당하는 바이트코드 명령을 만나면 프로그램 실행에 끼어들어
    중단점(breakpoint)을 추가하는 기능**을 한다 (1장, p.55).
- 진입점도 명시되어 있다 — **핫스팟 가상 머신을 실행하는 진입점은
  `JDK_SRC_HOME/src/java.base/share/native/libjli/java.c` 파일에 정의된 `JavaMain()` 함수**다
  (1장, p.55).[^zhou2024]

## 이어지는 페이지

- [핫스팟의 모듈화와 확장 인터페이스](../concepts/hotspot-modularity-and-interfaces.md) —
  여기서 고르는 기능 목록이 왜 고를 수 있게 되었는지
- [핫스팟 JIT 코드 들여다보기](../concepts/hotspot-jit-inspection-tools.md) — 빌드한 가상
  머신에서 JIT 결과를 직접 확인하는 도구
- [JHSDB와 서비스 에이전트](../concepts/jhsdb-serviceability-agent.md) — 소스를 빌드하지 않고도
  실행 중인 가상 머신 내부를 보는 쪽
- [JDK 판올림의 역사](../concepts/jdk-release-history.md) — 소스 저장소가 깃허브로 옮겨 간 시점

[^zhou2024]: 저우즈밍 2024(한국어판), 1장 "자바 기술 시스템 소개" §1.6 "실전: 내 손으로 빌드하는
    JDK"(pp.44–55). 명령 펜스는 원문 예제에서 셸 프롬프트(`$ `)를 제거하고 지면 폭 때문에 접힌
    줄을 한 줄로 되돌린 것이며, `text` 펜스는 `configure` 출력 예시의 발췌다
