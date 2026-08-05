# 스킬 배포

이 디렉터리가 **정본**이다(커밋 대상). 클라이언트로의 배포는 **기기마다** 심링크로
하고, 저장소 안에 사본을 두지 않는다.

`.agents/`에 두는 이유는 크로스 클라이언트 관례이자, evals 러너가 스킬을 저장소 루트
상대 경로(`.agents/skills/<이름>`)로 참조하기 때문이다.

## 기기별 설치 (PLAN §5 복구 런북 ⑦)

```bash
for s in kb-query kb-ingest kb-lint kb-new; do
  ln -sfn "$PWD/.agents/skills/$s" "$HOME/.claude/skills/$s"
done
```

개인 스코프(`~/.claude/skills/`)라 **전 프로젝트에서** `/kb-query`가 뜬다. 같은 타깃은
한 번만 로드되므로 프로젝트 스코프와 겹쳐 둘 이유가 없다.

**심링크를 커밋하지 않는다** — Windows 클론이 깨진다. 홈 디렉터리 심링크는 무관하다.

## 사용자 레벨 훅

산문 지시의 준수는 보장되지 않으므로, 1줄 포인터를 `~/.claude/settings.json`의
`UserPromptSubmit` 훅으로 주입한다. 프로젝트 훅이 아니라 **사용자 레벨**인 이유는
타 프로젝트에서 KB를 조회하는 것이 기본 사용 방식이기 때문이다.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"syntopicon 개인 KB: ~/workspace/syntopicon. 지식 조회·저장은 /kb-query, 소스 반입은 /kb-ingest, 점검은 /kb-lint — 명시 호출이 기본.\""
          }
        ]
      }
    ]
  }
}
```

훅은 **보조 경로**다. 기본 워크플로는 명시 호출(`/kb-query`)이고, 암묵 발동에
의존하지 않는다 — 트리거율 최적화는 불채택이다(PLAN §6).

되돌리려면 `hooks.UserPromptSubmit`에서 그 항목만 지운다. 매 프롬프트마다 한 줄이
붙으므로, 부담스러우면 지워도 명시 호출은 그대로 동작한다.

## 검증

```bash
skills-ref validate .agents/skills/kb-query     # agentskills.io 공식 검증기
uv run pytest tools/tests/test_skills.py        # 구조 규약
```

## 평가

시나리오는 `evals/`에 있고 **스킬 본문보다 먼저** 쓰였다. 스킬을 고치면 해당
시나리오를 다시 돌린다(`evals/README.md`).
