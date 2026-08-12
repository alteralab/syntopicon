---
type: concept
title: 카프카 JVM과 운영체제 모니터링
description: 브로커 지표만으로는 모자란 자리에서 무엇을 보는가 — G1 가비지 컬렉션 빈 둘과 거기서 읽는 세 속성, JVM이 알려 주는 파일 디스크립터 두 값, 그리고 운영체제에서 직접 재는 CPU 부하 평균과 여덟 갈래 사용률, 메모리와 스왑, 디스크 공간과 아이노드와 입출력 통계, 유입보다 훨씬 커지는 유출 네트워크 트래픽
generated: { by: "claude-opus-5", at: "2026-08-12T23:30:00Z" }
status: draft
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 JVM과 운영체제 모니터링

- [왜 브로커 밖까지 보는가](#왜-브로커-밖까지-보는가)
- [가비지 컬렉션](#가비지-컬렉션)
- [JVM이 알려 주는 운영체제 정보](#jvm이-알려-주는-운영체제-정보)
- [운영체제에서 직접 재는 것](#운영체제에서-직접-재는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **브로커가 주는 지표만으로는 모자랄 때, JVM과 운영체제에서 무엇을 어떤
이름으로 읽는가.**

이 페이지는 값을 **어떻게 맞추는가**가 아니라 그 값이 지금 어떤지를 **어떻게 보는가**를
다룬다. 맞추는 쪽 — `vm.swappiness`, 파일 디스크립터 계산, 파일시스템, 네트워크 커널
매개변수, G1GC 옵션 — 은 [카프카 프로덕션 튜닝](../concepts/kafka-production-tuning.md)에
있다.

## 왜 브로커 밖까지 보는가

- **카프카 브로커가 제공하는 지표에 더해, 모든 서버에 대한 표준적인 측정값 묶음과 자바 가상
  머신(Java Virtual Machine, JVM) 자체를 모니터링해야 한다** (13장, p.366).[^shapira2021]
- 그것이 주는 것이 둘이다 (13장, p.366):[^shapira2021]
  - **브로커의 성능을 떨어뜨릴 상황 — 예컨대 가비지 컬렉션 활동의 증가 — 을 경보로 알려
    준다.**
  - **브로커의 하류(downstream) 지표가 왜 변했는지에 대한 통찰을 준다.**

## 가비지 컬렉션

- **JVM에서 모니터링해야 할 결정적인 것은 가비지 컬렉션(garbage collection, GC)의
  상태**다 (13장, p.366).[^shapira2021]
- **이 정보를 위해 보아야 하는 구체적인 빈(bean)은 쓰고 있는 자바 런타임
  환경(Java Runtime Environment, JRE)과 실제로 쓰이는 GC 설정에 따라 달라진다** (13장,
  p.366).[^shapira2021]

  | Name | JMX MBean |
  |---|---|
  | Full GC cycles | `java.lang:type=GarbageCollector,name=G1 Old Generation` |
  | Young GC cycles | `java.lang:type=GarbageCollector,name=G1 Young Generation` |

  (13장, p.366, 표 13-18)[^shapira2021]

  - 버전 조건: 위 빈 이름은 **오라클 자바 1.8 JRE에서 G1 가비지 컬렉션을 돌릴 때**의
    것이다 (13장, p.366).[^shapira2021] 다른 JRE나 다른 컬렉터를 쓰면 빈이 달라진다 —
    책은 그 경우의 이름을 주지 않는다.
- 낱말 하나를 먼저 정리해 둔다 — **GC의 의미론(semantics)에서 "Old"와 "Full"은 같은
  것**이다 (13장, p.366).[^shapira2021] 세대 구분 자체가 무엇인지는
  [세대별 수집](../concepts/generational-collection.md)에 있다.
- 두 지표 각각에서 볼 속성은 둘이다 (13장, p.366):[^shapira2021]
  - **`CollectionCount`는 JVM이 시작된 이후 그 유형(Full 또는 Young)의 GC 주기 수**다.
  - **`CollectionTime`은 JVM이 시작된 이후 그 유형의 GC 주기에 쓴 시간을 밀리초로 나타낸
    것**이다.
  - **둘 다 카운터이므로 지표 시스템이 단위 시간당 GC 주기 수와 GC에 쓴 시간의 절대값을
    말해 주는 데 쓸 수 있고**, **GC 주기당 평균 시간을 내는 데도 쓸 수 있지만 평상시 운영에서는
    덜 유용하다.**
- 세 번째 속성이 마지막 한 주기를 보여 준다 — **각 지표에는 `LastGcInfo` 속성도 있다.
  다섯 필드로 이뤄진 복합 값이며 그 빈이 서술하는 GC 유형의 마지막 주기에 대한 정보를
  준다** (13장, pp.366–367).[^shapira2021]
  - **볼 값은 `duration`** 이다 — **마지막 GC 주기가 밀리초로 얼마나 걸렸는지를 알려
    준다.** **나머지(`GcThreadCount`·`id`·`startTime`·`endTime`)는 정보성이고 그리 유용하지
    않다** (13장, p.367).[^shapira2021]
  - 한계도 함께 적혀 있다 — **이 속성으로 모든 GC 주기의 시간을 볼 수는 없다. 특히 young
    GC 주기는 자주 일어나기 때문**이다 (13장, p.367).[^shapira2021]

## JVM이 알려 주는 운영체제 정보

- **JVM은 `java.lang:type=OperatingSystem` 빈을 통해 운영체제에 대한 정보를 얼마간 줄 수
  있다. 그러나 이 정보는 제한적이고 브로커를 돌리는 시스템에 대해 알아야 할 모든 것을
  나타내지는 않는다** (13장, p.367).[^shapira2021]
- 여기서 건질 만한 속성은 둘뿐이며, 고르는 기준이 **운영체제 쪽에서 수집하기 어렵다는
  것**이다 (13장, p.367):[^shapira2021]
  - **`MaxFileDescriptorCount`는 JVM이 열 수 있도록 허용된 파일 디스크립터(file
    descriptor, FD)의 최대 개수**를 알려 준다.
  - **`OpenFileDescriptorCount`는 현재 열려 있는 FD 수**를 알려 준다.
- 이 값이 왜 위험 신호가 되는지 — **모든 로그 세그먼트와 모든 네트워크 연결마다 FD가
  열리므로 빠르게 쌓인다.** **네트워크 연결을 제대로 닫지 못하는 문제가 생기면 브로커가
  허용된 FD 개수를 급격히 소진할 수 있다** (13장, p.367).[^shapira2021] 로그 세그먼트가
  어떻게 파일로 놓이는지는
  [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.

## 운영체제에서 직접 재는 것

- **JVM은 자기가 돌고 있는 시스템에 대해 우리가 알아야 할 모든 정보를 줄 수 없다. 그래서
  브로커뿐 아니라 운영체제 자체에서도 지표를 수집해야 한다** (13장, p.367).[^shapira2021]
- **대부분의 모니터링 시스템은 우리가 관심을 가질 수 있는 것보다 더 많은 운영체제 정보를
  수집해 주는 에이전트를 제공**하며, **꼭 지켜봐야 할 주요 영역은 CPU 사용, 메모리 사용,
  디스크 사용, 디스크 I/O, 네트워크 사용**이다 (13장, p.367).[^shapira2021]

### CPU

- **CPU 이용률에 대해서는 최소한 시스템 부하 평균(system load average)을 보아야 한다.
  프로세서들의 상대적 이용률을 가리키는 숫자 하나를 준다** (13장, p.367).[^shapira2021]
- **여기에 더해 유형별로 쪼갠 CPU 사용 백분율을 잡아 두는 것도 유용할 수 있다.** 수집
  방법과 운영체제에 따라 **아래 중 일부 또는 전부**를 얻는다 (13장, pp.367–368, 약어는
  원문 표기):[^shapira2021]

  | 약어 | 무엇 |
  |---|---|
  | `us` | 사용자 공간에서 쓴 시간 |
  | `sy` | 커널 공간에서 쓴 시간 |
  | `ni` | 낮은 우선순위 프로세스에 쓴 시간 |
  | `id` | 유휴 시간 |
  | `wa` | (디스크) 대기에 쓴 시간 |
  | `hi` | 하드웨어 인터럽트 처리에 쓴 시간 |
  | `si` | 소프트웨어 인터럽트 처리에 쓴 시간 |
  | `st` | 하이퍼바이저를 기다린 시간 |

- 부하 평균이 무엇을 세는지는 오해가 잦은 자리라 책이 상자를 따로 뒀다 (13장,
  p.368):[^shapira2021]

  > While many know that system load is a measure of CPU usage on a system, most people
  > misunderstand how it is measured. The load average is a count of the number of processes
  > that are runnable and are waiting for a processor to execute on. Linux also includes
  > threads that are in an uninterruptable sleep state, such as waiting for the disk. The load
  > is presented as three numbers, which is the count averaged over the last minute,
  > 5 minutes, and 15 minutes. In a single CPU system, a value of 1 would mean the system is
  > 100% loaded, with a thread always waiting to execute. This means that on a multiple CPU
  > system, the load average number that indicates 100% is equal to the number of CPUs in the
  > system. For example, if there are 24 processors in the system, 100% would be a load
  > average of 24.

- **카프카 브로커는 요청 처리에 상당한 처리 자원을 쓴다. 그래서 카프카를 모니터링할 때 CPU
  이용률을 추적하는 것이 중요**하다 (13장, p.368).[^shapira2021] 요청 처리가 실제로
  무엇을 하는 경로인지는
  [카프카 요청 처리](../concepts/kafka-request-processing.md)에 있다.

### 메모리와 스왑

- **브로커 자체에 대해서는 메모리 추적이 덜 중요하다 — 카프카는 보통 상대적으로 작은 JVM 힙
  크기로 돌기 때문**이다. **압축 기능을 위해 힙 밖에서 적은 양의 메모리를 쓰지만 시스템
  메모리의 대부분은 캐시용으로 남겨진다** (13장, p.368).[^shapira2021]
- 그래도 두 가지는 본다 (13장, p.368):[^shapira2021]
  - **다른 애플리케이션이 브로커의 몫을 침범하지 않도록 메모리 이용률을 추적**한다.
  - **전체 스왑 메모리와 여유 스왑 메모리 양을 모니터링해 스왑 메모리가 쓰이지 않고 있음을
    확인**한다.

### 디스크

- **카프카에 관한 한 디스크가 단연 가장 중요한 서브시스템**이다. **모든 메시지가 디스크에
  영속화되므로 카프카의 성능은 디스크의 성능에 크게 의존한다** (13장,
  p.368).[^shapira2021]
- **디스크 공간과 아이노드(inode) 사용량을 둘 다 모니터링하는 것이 중요하다** — **공간이
  바닥나지 않음을 보장해야 하기 때문**이며 **카프카 데이터가 저장되는 파티션에서 특히
  그렇다** (13장, p.368).[^shapira2021]
  - 아이노드가 무엇인지도 원문이 괄호로 정의한다 — **유닉스 파일시스템의 파일·디렉터리
    메타데이터 객체** (13장, p.368).[^shapira2021]
- **디스크 I/O 통계도 모니터링할 필요가 있다 — 디스크가 효율적으로 쓰이고 있는지를 알려 주기
  때문**이다. **적어도 카프카 데이터가 저장되는 디스크에 대해서는 초당 읽기·쓰기, 평균
  읽기·쓰기 큐 크기, 평균 대기 시간, 디스크 이용률(%)을 모니터링**한다 (13장,
  p.369).[^shapira2021] 이 값들이 고장 쪽으로 기울 때 어떻게 읽는지는
  [카프카 클러스터 문제 진단](../concepts/kafka-cluster-problem-diagnosis.md)에 있다.

### 네트워크

- 마지막은 네트워크 이용률이며 **단순히 유입·유출 네트워크 트래픽의 양이고 보통 초당 비트로
  보고된다** (13장, p.369).[^shapira2021]
- 문턱값을 정할 때 반드시 감안할 셈이 있다 — **카프카 브로커로 들어오는 모든 비트는 컨슈머를
  빼고도 토픽의 복제 팩터와 같은 수의 비트로 나간다.** **컨슈머 수에 따라 유출 네트워크
  트래픽은 유입 트래픽보다 자릿수 하나만큼(an order of magnitude) 커지기 쉽다.** **경보
  문턱을 정할 때 이 점을 염두에 두어야 한다** (13장, p.369).[^shapira2021]
  - 브로커 쪽에서 같은 값을 재는 지표는 `BytesInPerSec`·`BytesOutPerSec`이고 거기서도 유출에
    레플리카 트래픽이 섞인다 —
    [카프카 브로커 지표](../concepts/kafka-broker-metrics.md)에 있다.

## 이어지는 페이지

- [카프카 프로덕션 튜닝](../concepts/kafka-production-tuning.md) — 여기서 읽는 값들을 미리
  맞추는 쪽. 스와핑, 파일 디스크립터, 파일시스템, 네트워크 커널, G1GC 옵션
- [카프카 클러스터 문제 진단](../concepts/kafka-cluster-problem-diagnosis.md) — 호스트
  수준 문제로 좁혀졌을 때 이 지표들을 들고 하는 일
- [카프카 브로커 지표](../concepts/kafka-broker-metrics.md) — 브로커 자신이 주는 쪽
- [카프카 지표의 기초](../concepts/kafka-metrics-basics.md) — JVM 빈에 무엇으로 붙어서
  읽는지
- [클래식 가비지 컬렉터](../concepts/hotspot-classic-collectors.md) — 여기서 개수와 시간만
  읽는 G1이 실제로 무엇을 하는지
- [세대별 수집](../concepts/generational-collection.md) — Young과 Old가 갈리는 이유
- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 파일 디스크립터를 쌓는
  로그 세그먼트 쪽

[^shapira2021]: Shapira et al. 2021, 13장 "Monitoring Kafka" §"JVM Monitoring"·§"OS Monitoring"(pp.366–369) — 인용 블록은 p.368 "What Is System Load?" 상자 원문. 표 13-18의 빈 이름과 CPU 백분율 약어는 원문 표기 그대로다
