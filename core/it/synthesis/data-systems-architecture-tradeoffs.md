---
type: synthesis
title: 데이터 시스템 아키텍처 트레이드오프
description: 운영계와 분석계, 클라우드와 자체 호스팅, 분산과 단일 노드 사이의 선택을 모으는 허브
generated: { by: "human:me", at: "2026-08-10T21:00:00Z" }
---

# 데이터 시스템 아키텍처 트레이드오프

정답이 하나가 아닌 선택들을 모은다. 각 페이지가 한 축을 맡고, 그 축의
장단점과 언제 어느 쪽을 고르는지를 다룬다.

## 운영계와 분석계

- [EDW](../concepts/enterprise-data-warehouse.md) — 운영계와 분석계를 왜 가르며 어떤 아키텍처들이 그 요구를 감당했나
- [데이터 레이크](../concepts/data-lake.md) — 스키마를 강제하지 않는 분석 저장소와 원시 데이터 우선 원칙
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 무엇이 정본이고 무엇이 다시 만들 수 있는 사본인가

## 클라우드와 자체 호스팅

- [클라우드와 자체 호스팅](../concepts/cloud-versus-self-hosting.md) — 만들 것인가 살 것인가, 그리고 통제권을 잃는 대가
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 서비스 계층화, 저장과 연산의 분리, 멀티테넌시

## 분산과 단일 노드

- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 여러 기계로 갈 아홉 가지 이유와 가지 말아야 할 이유
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 서비스마다 자기 데이터베이스를 두는 이유와 그 대가
