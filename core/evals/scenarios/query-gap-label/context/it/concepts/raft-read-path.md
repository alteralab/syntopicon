---
type: concept
title: Raft 읽기 경로
description: Raft에서 선형화 가능한 읽기가 요구하는 것
generated: { by: "claude-fable-5", at: "2026-07-20T09:10:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# Raft 읽기 경로

## 읽기와 quorum

- leader lease 없이는 읽기에도 quorum 왕복이 필요하다.[^ongaro2014-raft]
- 리더가 자신이 여전히 리더인지 확인하지 않으면 stale read가 발생한다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §5.4
