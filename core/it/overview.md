---
type: guide
title: "IT 지식"
description: "서적·논문·기술 문서에서 축적한 IT 개념"
generated: { by: "tools/kb-new", at: "2026-08-05T02:09:19Z" }
---

# IT 지식

서적·논문·기술 문서에서 축적한 IT 개념

## Hubs

<!-- 허브(synthesis) 링크 + 한 줄 설명, 10–30개. 포인터만 — 본문 발췌·수치 복제
     금지(진입점 부패 벡터, PLAN §3). **상위 축만 나열한다** — 자식 허브는 부모 허브
     본문이 안내한다(2026-08-16 재편: 39개가 상한을 넘어 부모-전용으로 접음).
     갱신 후보는 kb-lint의 링크 차수 대조가 낸다. -->

- [데이터 웨어하우스 모델링](synthesis/data-warehouse-modeling.md) — DW 축의 부모 허브: 차원 모델링·Data Vault·운영과 프로세스
- [카프카](synthesis/kafka-basics.md) — 스트리밍 축의 부모 허브: 내부 구조·클라이언트·운영·신뢰성·파이프라인·보안·모니터링·스트림 처리
- [데이터 엔지니어링 수명 주기](synthesis/data-engineering-lifecycle.md) — 생성부터 서빙까지의 단계와 저류
- [데이터 엔지니어링 디자인 패턴](synthesis/data-engineering-design-patterns.md) — 원리 서술 위에 얹힌 이름 층: 반입·멱등성·품질·보안·관측 패턴 카탈로그
- [배치 처리](synthesis/batch-processing.md) — 유한한 입력을 통째로 읽어 출력을 다시 만드는 쪽: 저장·오케스트레이션·연산
- [스트림 처리](synthesis/stream-processing.md) — 끝나지 않는 입력의 처리: 브로커·시간·상태·이중성
- [데이터플로 아키텍처](synthesis/dataflow-architecture.md) — 데이터 통합·언번들드 DB·쓰기 경로와 읽기 경로·종단 간 논증
- [데이터 시스템 아키텍처 트레이드오프](synthesis/data-systems-architecture-tradeoffs.md) — 운영/분석·클라우드·분산 선택 축과 사업·사용자의 요구
- [데이터 메시 원칙](synthesis/data-mesh-principles.md) — 데이터 메시 축의 부모 허브: 네 원칙과 논증, 논리 아키텍처·프로덕트 설계·실행과 조직으로 이어짐
- [비기능 요건](synthesis/nonfunctional-requirements.md) — 성능·신뢰성·확장성·유지보수성을 정의하는 어휘
- [데이터 모델과 질의 언어](synthesis/data-models-and-query-languages.md) — 관계형·문서·그래프·이벤트·데이터프레임과 그 질의 언어들
- [저장 엔진](synthesis/storage-engines.md) — 디스크에 데이터를 놓는 구조, B-트리 대 LSM, 분석용 열 저장과 색인들
- [인코딩과 진화](synthesis/encoding-and-evolution.md) — 데이터를 바이트로 바꾸는 형식과 버전을 넘어 살아남는 방법
- [분산 시스템 기초](synthesis/distributed-systems-basics.md) — 통신·시간·장애의 가정과 그 위의 실패 감지·리더 선출
- [분산 합의](synthesis/distributed-consensus.md) — 서버 여럿을 하나처럼 굴게 만드는 문제와 Raft·Paxos 계열의 해법
- [데이터 복제](synthesis/data-replication.md) — 리더 하나·여럿·없음의 세 갈래와 각각이 낳는 문제
- [레플리카 일관성](synthesis/replica-consistency.md) — 사본이 여럿일 때의 가시성 계약과 수렴 장치
- [데이터 샤딩](synthesis/data-sharding.md) — 데이터셋을 노드로 쪼개는 기준·쏠림·라우팅·색인
- [데이터베이스 트랜잭션](synthesis/database-transactions.md) — ACID·격리 수준·직렬성 구현·분산 원자적 커밋
- [실용주의 프로그래머](synthesis/pragmatic-programmer.md) — 소프트웨어 실천 축의 부모 허브: 철학·도구·유연성·코딩·프로젝트 다섯 갈래
- [자바 기술 시스템](synthesis/java-technology-system.md) — JVM 축의 부모 허브: 메모리·도구·클래스 파일과 로딩·컴파일·동시성
- [파운데이션 모델과 AI 엔지니어링](synthesis/foundation-models-and-ai-engineering.md) — LLM 축의 부모 허브: 모델 계보·스택과 아홉 자식 축(평가·프롬프트·RAG·에이전트·파인 튜닝·데이터셋·추론 서빙·아키텍처·피드백)
- [복잡성과 모듈 설계](synthesis/complexity-and-modular-design.md) — 코드 품질 축의 부모 허브: 복잡성의 정의와 증상, 모듈 설계 처방과 두 형제 축(문서화와 코드 명료함·복잡성 잣대의 적용)
- [리팩터링과 코드 냄새](synthesis/refactoring-and-code-smells.md) — 같은 축의 이행 절차 쪽: 행동 보존 소단계의 정의와 리듬, 언제 하는가의 계기, 냄새 어휘, 담보가 되는 테스트, 막는 것들
- [클린 코드](synthesis/clean-code.md) — 같은 축의 **논쟁 중인 소스**(Martin 2008): 규칙 목록과 그 지위, 삼급 경사로 읽는 법, 이 KB의 `contradicts` 셋 중 둘이 나온 자리
- [도메인 모델과 애플리케이션 계층](synthesis/domain-model-and-application-layers.md) — 같은 축의 파이썬 구체화: 의존 역전과 그 위의 네 패턴(리포지터리·서비스 레이어·작업 단위·애그리게이트), 테스트 층 선택, 부트스트랩
- [도메인 주도 설계](synthesis/domain-driven-design.md) — 같은 축의 모델 쪽 원전(Evans 2003): 이름의 정본을 모델에 두는 유비쿼터스 언어, 모델과 코드의 결속, 이름에 개념까지 담고 사실은 담지 않는다는 경계, 그리고 모델이 통하는 범위를 긋는 경계 컨텍스트
- [POSIX 셸 명령 언어](synthesis/posix-shell-command-language.md) — 셸 스크립트의 실패를 규범으로 설명하는 축: 인용·확장 순서·필드 분리와 종료 상태·오류의 귀결·실행 환경
- [테스트 오라클 문제](synthesis/test-oracle-problem.md) — 무엇이 옳은 동작인지를 무엇이 답하는가: 오라클 정보의 네 출처와 통과가 증명하지 못하는 것, 형식 명세가 없을 때 기대를 구하는 세 자리, 기대값을 기계가 지을 때 결함이 몰리는 층
- [파이썬 데이터 모델과 프로토콜](synthesis/python-data-model-and-protocols.md) — 같은 축의 파이썬 관용 참조이자 그 다섯 갈래의 부모 허브: 특수 메서드라는 바닥, 데이터 클래스 빌더 셋과 그것이 냄새가 되는 경계, 인터페이스를 규정하는 네 방식, 그리고 형제 축 넷(함수를 객체로·상속 기제·제어 흐름 기제·클래스 메타프로그래밍)

## Tools

- 검색: `qmd query <질의> -c it` / 형태소 레그 `tools/ksearch`
- 저장: `/kb-ingest --kb it` — inbox/ 경유
- 점검: `tools/lint --kb it`
