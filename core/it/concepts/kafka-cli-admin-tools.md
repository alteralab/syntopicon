---
type: concept
title: 카프카 명령줄 관리 도구
description: 카프카 배포판이 함께 주는 CLI 관리 도구를 쓰기 전에 성립하는 전제들 — 자바 클래스를 부르는 스크립트라는 실체와 그것이 못 하는 일, 기본 설정에서는 인증 없이 실행된다는 경고, 브로커와 버전을 맞춰야 하는 이유, 접속 문자열과 도구가 놓인 자리, 그리고 이 장이 이름만 대고 지나가는 나머지 도구들
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 명령줄 관리 도구

- [무엇을 주고 무엇을 안 주는가](#무엇을-주고-무엇을-안-주는가)
- [기본값에서는 아무나 쓸 수 있다](#기본값에서는-아무나-쓸-수-있다)
- [브로커와 버전을 맞춘다](#브로커와-버전을-맞춘다)
- [접속 문자열과 도구가 놓인 자리](#접속-문자열과-도구가-놓인-자리)
- [이름만 대고 지나가는 도구들](#이름만-대고-지나가는-도구들)
- [규모가 커지면 이 도구들로 부족해진다](#규모가-커지면-이-도구들로-부족해진다)
- [작업별로 어디를 볼 것인가](#작업별로-어디를-볼-것인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **카프카가 함께 주는 명령줄 도구는 실체가 무엇이고, 쓰기 전에 무엇을
확인해야 하는가.**

## 무엇을 주고 무엇을 안 주는가

- 클러스터를 운영하려면 토픽·설정 따위를 바꿀 추가 도구가 필요하고, 카프카는 그런 변경에
  쓰는 **명령줄 인터페이스(command-line interface, CLI) 유틸리티를 여럿 제공**한다. 책이
  그 실체를 한 문장으로 적어 뒀다 (12장, p.305):[^shapira2021]

  > The tools are implemented in Java classes, and a set of scripts are provided natively to
  > call those classes properly. While these tools provide basic functions, you may find they
  > are lacking for more complex operations or are unwieldy to use at larger scales.

- 그래서 이 장의 범위 자체가 좁다 — **아파치 카프카 오픈소스 프로젝트의 일부로 제공되는
  기본 도구만 다루고**, 코어 프로젝트 바깥에서 커뮤니티가 개발한 고급 도구는 아파치 카프카
  웹사이트로 넘긴다 (12장, p.305).[^shapira2021]

## 기본값에서는 아무나 쓸 수 있다

- 이 장이 첫 쪽에서 경고 상자로 세운 전제다. 인가를 구현해 놓고도 기본 설정이 그것을 걸지
  않는다는 것이 요점이라 원문 그대로 옮긴다 (12장, p.305):[^shapira2021]

  > While Apache Kafka implements authentication and authorization to control topic
  > operations, default configurations do not restrict the use of these tools. This means that
  > these CLI tools can be used without any authentication required, which will allow
  > operations such as topic changes to be executed with no security check or audit. Always
  > ensure that access to this tooling on your deployments is restricted to administrators only
  > to prevent unauthorized changes.

  - 즉 **이 도구에 대한 접근 통제는 카프카가 아니라 배포 환경이 지는 책임**이다. 인증과
    인가를 실제로 켜는 쪽은 [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md)에
    있다.

## 브로커와 버전을 맞춘다

- 두 번째 전제도 경고 상자다 — **도구가 브로커 버전에 의존하며, 그중에는 브로커에 붙는
  대신 주키퍼에 데이터를 쓰는 명령도 있다**는 것이 이유다 (12장, p.306):[^shapira2021]

  > For this reason, it is important to make sure the version of the tools that you are using
  > matches the version of the brokers in the cluster. The safest approach is to run the tools
  > on the Kafka brokers themselves, using the deployed version.

  - 버전 조건: 주키퍼에 직접 쓰는 명령이 남아 있는 것은 Kafka 3.9 이하다 — 4.0 이상에는
    주키퍼 자체가 없다([주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)). 버전을 맞추라는
    권고 자체는 그 뒤로도 유효하다.
- 콘솔 컨슈머에는 같은 경고가 한 번 더, 더 강한 말로 붙는다 — **클러스터와 같은 버전의
  컨슈머를 쓰는 것이 매우 중요하며, 옛 버전 콘솔 컨슈머는 클러스터나 주키퍼와 잘못된 방식으로
  상호작용해 클러스터를 망가뜨릴 수 있다** (12장, p.323).[^shapira2021] 그 도구는
  [콘솔 프로듀서와 콘솔 컨슈머](../concepts/kafka-console-producer-and-consumer.md)에 있다.

## 접속 문자열과 도구가 놓인 자리

- 붙는 방식은 도구마다 같다 — **클러스터 접속 문자열과 포트를 `--bootstrap-server` 옵션으로
  준다.** 책의 예제는 클러스터에 속한 호스트 한 대에서 도구를 돌린다고 가정하고
  `localhost:9092`를 쓴다 (12장, pp.305–306).[^shapira2021]
  - `--bootstrap-server`가 옛 `--zookeeper` 플래그를 대체한 경위는
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)에 있다.
- **이 장 전체에서 도구는 `/usr/local/kafka/bin/` 디렉터리에 있고**, 예제 명령은 사용자가 그
  디렉터리에 있거나 그것을 `$PATH`에 넣어 뒀다고 가정한다 (12장, p.306).[^shapira2021]

## 이름만 대고 지나가는 도구들

- 배포판에는 이 장이 깊이 다루지 않는 도구가 더 들어 있고, 자세한 것은 아파치 카프카
  웹사이트로 넘긴다 (12장, pp.334–335).[^shapira2021]
  - **클라이언트 ACL** — `kafka-acls.sh`는 **카프카 클라이언트의 접근 제어를 다루는 명령줄
    도구**로, **인가자(authorizer) 속성 전체 기능, 주체(principal)에 대한 거부·허용 설정,
    클러스터 단위와 토픽 단위 제한, 주키퍼 TLS 파일 설정 등**을 갖는다 (12장,
    p.335).[^shapira2021] 그 사용례는
    [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md)에 있다.
  - **경량 미러메이커** — `kafka-mirror-maker.sh` 스크립트를 데이터 미러링에 쓸 수 있고,
    복제의 자세한 이야기는 10장이 담당한다 (12장, p.335).[^shapira2021] 그쪽은
    [미러메이커](../concepts/kafka-mirrormaker.md)다.
  - **테스트 도구** — **`kafka-broker-api-versions.sh`는 한 카프카 버전에서 다른 버전으로
    업그레이드할 때 쓸 수 있는 API 요소의 버전 차이를 쉽게 식별하고 호환성 문제를 확인하게
    해 준다.** 그 밖에 **프로듀서·컨슈머 성능 테스트 스크립트, 주키퍼 관리용 스크립트들,
    그리고 벤치마크와 스트레스 테스트를 돌리도록 설계된 테스트 프레임워크 `trogdor.sh`**가
    있다 (12장, p.335).[^shapira2021]

## 규모가 커지면 이 도구들로 부족해진다

- 장을 닫으며 책이 스스로 한계를 적는다 (12장, p.337):[^shapira2021]

  > As you begin to scale your Kafka clusters larger, even the use of these tools may become
  > arduous and difficult to manage. It is highly recommended to engage with the open source
  > Kafka community and take advantage of the many other open source projects in the ecosystem
  > to help automate many of the tasks outlined in this chapter.

- 그 "다른 프로젝트"의 실물로 이 장이 두 번 드는 것이 **크루즈 컨트롤(Cruise Control)**이다 —
  한 번은 리더 균형을 상시 유지하는 용도이고 (12장, p.326),[^shapira2021] 한 번은 브로커에서
  리더십을 안전하게 걷어내는 **브로커 격하(broker demotion)** 기능이다 (12장,
  p.330).[^shapira2021] 둘 다
  [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md)의 맥락이다.
- 도구를 다 익혀도 남는 것이 있다 — **클러스터를 관리하는 데 필요한 도구에 익숙해졌더라도
  제대로 된 모니터링 없이는 여전히 불가능하며**, 그 이야기는 13장이 맡는다 (12장,
  p.337).[^shapira2021] 13장은 아직 이 KB에 반입돼 있지 않다.

## 작업별로 어디를 볼 것인가

- 이 장이 다루는 작업 대부분은 5장이 API로 다룬 것과 같은 작업이다 — **토픽 작업, 컨슈머 그룹,
  동적 설정 변경, 파티션 관리** (12장, pp.305–332).[^shapira2021] 그래서 이 KB는 CLI 절차를
  같은 작업의 API 페이지 안 "명령줄에서" 절에 두고, CLI에만 있는 작업(콘솔 도구, 로그 덤프와
  레플리카 검증, 안전하지 않은 작업)만 별도 페이지로 세웠다. 전체 목록은 허브
  [카프카 설치와 운영](../synthesis/kafka-operations.md)에 있다.

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 같은 작업을 코드에서 하는 쪽.
  이 도구들이 하던 일에 프로그램 API를 준 것이 그것이다
- [토픽 관리](../concepts/kafka-topic-administration.md) — `kafka-topics.sh`의 생성·조회·삭제와
  이름 규칙
- [설정 관리](../concepts/kafka-config-administration.md) — `kafka-configs.sh`의 엔티티 타입 넷과
  재정의 조회·삭제
- [컨슈머 그룹 관리](../concepts/kafka-consumer-group-administration.md) —
  `kafka-consumer-groups.sh`의 조회·삭제와 오프셋 내보내기·가져오기
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) —
  `kafka-leader-election.sh`와 `kafka-reassign-partitions.sh`
- [콘솔 프로듀서와 콘솔 컨슈머](../concepts/kafka-console-producer-and-consumer.md) — 손으로
  쓰고 읽어 보는 두 유틸리티
- [로그 세그먼트 덤프와 레플리카 검증](../concepts/kafka-log-dump-and-replica-verification.md) —
  디스크를 직접 여는 두 도구
- [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md) — 이 도구를 아무나 못 쓰게
  하려면 켜야 하는 것
- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 버전을 맞추라는 경고의 근거이자
  `--zookeeper`가 사라진 경위
- [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md) — 같은 장의 마지막 절.
  이 도구들이 안 해 주는 일을 손으로 할 때
- [미러메이커](../concepts/kafka-mirrormaker.md) — 이름만 나오는 `kafka-mirror-maker.sh`의 본문

[^shapira2021]: Shapira et al. 2021, 12장 "Administering Kafka" — 인용 블록은 pp.305·306·337 원문
