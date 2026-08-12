---
type: synthesis
title: 카프카 보안
description: 클라이언트와 브로커 사이의 인증, 주체가 할 수 있는 일을 정하는 인가, 전송과 저장의 암호화, 그리고 카프카 밖의 주키퍼와 플랫폼까지 — 배포를 잠그는 선택들의 진입점
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
---

# 카프카 보안

무엇을 지켜야 하는지의 목록에서 시작해, 리스너에 무엇을 걸지 고르고, 인증·인가·암호화를
차례로 채운 뒤, 카프카 밖으로 나간다. 보안은 컴포넌트가 아니라 시스템 전체의 속성이라는
전제가 이 순서를 만든다.

## 무엇을 지키는가

- [카프카 보안 모델](../concepts/kafka-security-model.md) — 보안 절차 다섯, 예시 데이터
  흐름의 여섯 단계, 안전한 배포가 보장해야 하는 일곱 가지

## 인증

- [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md) — 리스너마다 고르는 네
  프로토콜과 인증이 만들어 내는 KafkaPrincipal
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — 키스토어와 트러스트스토어,
  호스트명 검증, 인증서를 만드는 흐름, 성능 대가
- [카프카 SASL 인증](../concepts/kafka-sasl-authentication.md) — 챌린지·응답 뼈대, JAAS
  설정과 접두어, 콜백 핸들러 세 종류
- [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md) — GSSAPI·PLAIN·SCRAM·
  OAUTHBEARER의 설정과 각각의 위험
- [카프카 위임 토큰](../concepts/kafka-delegation-tokens.md) — 키스토어·키탭을 배포하지 않고
  워커에 인증을 나눠 주는 기제
- [카프카 재인증과 무중단 보안 갱신](../concepts/kafka-reauthentication.md) — 인증이 한 번만
  일어난다는 사실이 만드는 구멍과 롤링 갱신 순서

## 인가와 감사

- [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md) — ACL 바인딩 일곱 항목,
  판정 규칙, ACL과 카프카 요청의 대응표, 감사 로그

## 암호화

- [카프카 암호화](../concepts/kafka-encryption.md) — 전송 계층이 덮지 못하는 자리와 종단 간
  암호화, 키 교체와 메시지 키의 해시 등가성

## 카프카 밖

- [주키퍼 보안](../concepts/kafka-zookeeper-security.md) — SCRAM 자격 증명과 ACL이 저장되는
  곳을 잠그는 법 (Kafka 3.9 이하)
- [카프카 플랫폼 보안](../concepts/kafka-platform-security.md) — 위협 모델, 자격 증명 파일의
  권한, 설정 파일의 비밀번호를 밖으로 빼기

## 닿는 페이지

- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 보안 절차 다섯 중 이 축이
  3장으로 넘긴 하나
- [미러메이커](../concepts/kafka-mirrormaker.md) — 데이터센터 간 트래픽에 이 선택들이 실제로
  요구되는 사례
- [데이터 파이프라인 고려사항](../concepts/kafka-data-pipeline-considerations.md) — 파이프라인
  관점에서 던지는 보안 질문 다섯

## 이어지는 허브

- [카프카](kafka-basics.md) — 이 허브의 상위
- [카프카 설치와 운영](kafka-operations.md) — 리스너·설정·튜닝이 사는 곳
- [카프카 내부 구조](kafka-internals.md) — 인가가 걸리는 요청 처리와 메타데이터
