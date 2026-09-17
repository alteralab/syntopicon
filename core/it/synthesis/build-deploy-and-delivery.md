---
type: synthesis
title: 빌드와 배포와 전달
description: 쪼갠 서비스들의 소스 코드와 빌드를 저장소 하나에 둘 것인가 서비스마다 둘 것인가와 그 선택이 독립 배포 가능성에 거는 조항, 그 배치가 촉발하는 지속적 통합과 전달의 세 물음과 아티팩트를 한 번만 만든다는 조항, 나른 것을 실제로 놓을 때 지키는 격리 실행과 자동화 집중과 코드형 인프라와 무중단 배포와 원하는 상태 관리, 무엇 위에 놓는가의 사다리인 물리 기계부터 가상 기계와 컨테이너와 PaaS와 FaaS까지와 여러 기계에 걸쳐 돌리는 컨테이너 오케스트레이션 층, 그리고 그렇게 놓은 것을 프로덕션에서 시험한다는 것의 규정과 안전하게 만드는 조건을 모으는 허브
generated: { by: "claude-opus-5", at: "2026-09-17T01:20:00Z" }
---

# 빌드와 배포와 전달

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **소스에서 프로덕션까지 한 줄로 이어지는 경로**가
사는 자리다. 경로의 순서대로 놓았다 — 소스를 어디에 두는가에서 시작해 무엇으로 통합하고 무엇을
지키며 놓고 무엇 위에 놓는가를 지나 놓은 뒤에 무엇을 확인하는가로 끝난다. 부모 허브는
[소프트웨어 아키텍처](software-architecture.md)다.

여기 없는 것: 놓인 것이 프로덕션에서 **무엇을 하고 있는지 알아내는 일**과 **얼마나 잘 버티는가**는
[비기능 요건](nonfunctional-requirements.md)이 갖는다.

## 소스와 빌드

- [마이크로서비스 소스와 빌드의 배치](../concepts/microservice-source-layout.md) — 쪼갠
  서비스들의 소스 코드와 빌드를 저장소 하나에 둘 것인가 서비스마다 둘 것인가, 그리고 그 선택이
  독립 배포 가능성에 거는 조항
- [버전 관리](../concepts/version-control-practice.md) — 그 저장소를 다루는 실천 층. **정본
  자리는 [실용주의 프로그래머](pragmatic-programmer.md) 축의
  [기본 도구와 편집증적 방어](pragmatic-basic-tools-and-paranoia.md)다**

## 통합과 파이프라인

- [지속적 통합과 지속적 전달](../concepts/continuous-integration-and-delivery.md) — 그 배치가
  촉발하는 통합과 파이프라인. 도구를 들여놓은 것과 실천하는 것을 가르는 세 물음, 아티팩트를
  한 번만 만든다는 조항

## 놓을 때 지키는 것

- [마이크로서비스 배포의 다섯 원칙](../concepts/microservice-deployment-principles.md) — 그
  파이프라인이 실어 나른 것을 실제로 놓을 때 지키는 조문 다섯. 격리 실행, 자동화 집중, 코드형
  인프라, 무중단 배포, 원하는 상태 관리

## 무엇 위에 놓는가

- [마이크로서비스 배포 선택지](../concepts/microservice-deployment-options.md) — 그 조문으로
  재는 수단의 사다리. 물리 기계부터 가상 기계와 컨테이너와 PaaS와 FaaS까지, 그리고 FaaS가
  마이크로서비스를 논리 개념으로 바꾸는 자리
- [컨테이너 오케스트레이션과 쿠버네티스](../concepts/container-orchestration-and-kubernetes.md) —
  컨테이너를 여러 기계에 걸쳐 돌리는 층이 떠맡는 일과 쿠버네티스의 핵심 개념, 그리고 들일
  것인가의 판단

## 놓은 뒤에 확인하는 것

- [프로덕션에서의 테스트](../concepts/testing-in-production.md) — 그렇게 놓은 것을 프로덕션에서
  시험한다는 것. 이미 하면서 테스트라 부르지 않던 넷과 그것을 안전하게 만드는 조건, 그리고
  테스트를 더 쌓는 노력과 빨리 고치는 능력 사이의 저울. 같은 페이지가
  [비기능 요건](nonfunctional-requirements.md)의 신뢰성 절에도 걸려 있는데, 그쪽이 보는 것은
  실패 확률을 0으로 내릴 수 없다는 전제이고 여기서 보는 것은 **파이프라인의 마지막 칸**이다

## 이웃 허브

- [소프트웨어 아키텍처](software-architecture.md) — 부모 허브
- [마이크로서비스 경계와 통신](microservice-boundaries-and-communication.md) — 여기서 나르는
  단위의 경계를 정하는 쪽
- [비기능 요건](nonfunctional-requirements.md) — 놓인 것을 관측하고 버티게 하는 쪽
- [테스트 스위트의 운영](test-suite-operations.md) — 파이프라인 안쪽의 테스트 배합과 크기
- [테스팅에서 자동화의 경계](automation-boundary-in-testing.md) — 무엇을 기계에 맡길 수
  있는가의 어휘가 프로덕션 확인과 만나는 자리
- [실용주의 프로그래머](pragmatic-programmer.md) — 같은 자동화 요구의 개별 개발자 실천 층
