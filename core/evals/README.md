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

## 격리 규약 (2026-08-06 첫 실행에서 실측된 오염의 대응)

- **`.env`에 `HOME=/private/tmp/skill-eval-home`** (빈 디렉터리, 없으면 mkdir).
  하네스는 CLAUDE_CONFIG_DIR만 격리하고 HOME은 실기기 그대로라, 에이전트가
  `find ~`로 실저장소·실스킬을 찾아 읽는 이탈이 3개 팔에서 실측됐다.
- **픽스처가 실저장소의 사본임을 자기 표지하면 안 된다.** 낯익은 구조 + "아직
  없다" 라우터를 본 에이전트는 "낡은 사본, 진본을 찾자"고 추론했다(new-first-kb
  양팔 0점의 실제 기전). 주변이 비어 있는 이유를 서사로 설명하라 — 행동 지시가
  아니라 환경 설명("새 노트북에 방금 클론했다")이라 eval을 오염시키지 않는다.
- **프롬프트가 가리키는 산출물은 실재해야 한다.** "방금 정리한 내용"은 새 세션에
  존재하지 않는다 — `context/notes.md`로 두고 프롬프트가 파일을 가리키게 한다.
- **kb-query 시나리오의 프롬프트는 `/kb-query`로 시작한다** — 운영 기본이 명시
  호출이므로, 자동 발동 여부는 재는 대상이 아니다.
