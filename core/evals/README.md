# 스킬 평가 시나리오

정본 도구는 **dbt skill-eval**, 커밋 `de682831d6736f9205c717c344d627abc21da255` 핀
(PLAN §4.6). 설치:

```
uv tool install "git+https://github.com/dbt-labs/dbt-agent-skills@de682831d6736f9205c717c344d627abc21da255#subdirectory=evals"
```

실행은 **저장소 루트에서** 한다 — `skill-sets.yaml`의 스킬 경로가 루트 상대다.

```
skill-eval run  -d evals                 # 실행당 실비용이 든다
skill-eval grade -d evals <run-id>
skill-eval report -d evals <run-id>
```

## 규약 (PLAN §4.6)

- **baseline arm 의무.** 모든 시나리오에 스킬 없는 `no-skills` 팔이 있다. 스킬이
  없을 때도 되는 일은 스킬의 공로가 아니다.
- **스킬당 ≥3 시나리오.**
- **evals를 스킬 본문보다 먼저 쓴다.** 무엇을 재는지 정하기 전에 쓴 스킬은
  자기가 잘하는 것만 재게 된다.
- **합격 숫자 게이트 없음, CI 게이트 없음.** 결론은 사람이 비교 리포트를 읽고 낸다.
  스킬을 고치면 해당 시나리오를 다시 돌린다.
- `runs/`는 gitignore 대상이다.

## 시나리오 구성

`scenarios/<이름>/`
- `prompt.txt` — 사용자 발화
- `scenario.md` — 배경 / 기대 결과 / 채점 기준
- `skill-sets.yaml` — 비교할 팔(baseline 포함)
- `context/` — 에이전트 작업 디렉터리로 복사되는 파일

`context/`의 KB는 시나리오마다 다르다. 재는 것이 다르면 픽스처도 달라야 하고,
공유 픽스처는 "이 시나리오가 무엇을 전제하는가"를 읽는 사람에게서 감춘다.
