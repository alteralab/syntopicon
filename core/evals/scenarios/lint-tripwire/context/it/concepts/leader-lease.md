---
type: concept
title: 리더 임차
description: 시계 가정으로 읽기 quorum을 생략하는 최적화
generated: { by: "claude-fable-5", at: "2026-07-20T09:12:00Z" }
contradicts: [lease-clock-risk]
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# 리더 임차

## 무엇을 교환하는가

- 임차(lease) 기간 동안 리더는 quorum 왕복 없이 읽기에 답한다.[^ongaro2014-raft]
- 대가는 시계 가정이다 — 드리프트 한계를 넘으면 안전성이 깨진다.[^ongaro2014-raft]
- #hypothesis 실무에서 드리프트로 인한 사고 사례는 드물게 보고된다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §6.4
