---
type: paper-conference
title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
author:
  - { family: "Jimenez", given: "Carlos E." }
  - { family: "Yang", given: "John" }
  - { family: "Wettig", given: "Alexander" }
  - { family: "Yao", given: "Shunyu" }
  - { family: "Pei", given: "Kexin" }
  - { family: "Press", given: "Ofir" }
  - { family: "Narasimhan", given: "Karthik" }
issued: "2024"
event-title: "ICLR 2024"
number: "2310.06770"
version: "v3"
URL: "https://arxiv.org/abs/2310.06770"
snapshot: /it/archive/jimenez2024-swebench/
snapshot_sha256: "165c56eda49b8a8303f35fe3058f56caf481981e16da31241fcf80b544abf118"
accessed: "2026-08-22"
---

# jimenez2024-swebench

실제 GitHub 이슈와 그것을 닫은 병합 풀 리퀘스트에서 과제를 뽑아, 모델이 만든 패치를
그 저장소의 실제 테스트로 채점하는 벤치마크의 원전이다. 이 KB에서는 **한 벤치마크가
어떤 절차로 만들어져 표준이 되었는가**의 원전으로 쓰고, 같은 벤치마크의 파생판을 2026년에
철회한 [벤더 보고](openai2026-swebench-verified-retire.md)와 한 페이지에 묶는다.

## 게재 지위 — 심사 실증(peer-reviewed), 문면 근거

확보본 52쪽 전 쪽의 쪽머리가 `Published as a conference paper at ICLR 2024`다. 1쪽
좌측에 `arXiv:2310.06770v3 [cs.CL] 11 Nov 2024`가 인쇄돼 있다. 곧 **게재본 조판의 arXiv
사본**이고, 게재 지위의 근거는 레코드가 아니라 문면이다.

ICLR 프로시딩은 권·호·쪽수로 매기지 않는다. 이 KB의 쪽 표기는 **확보본 PDF의 쪽
번호(1~52)**이고, 논문 안 인쇄 쪽 번호와 일치한다.

## 인용 규칙

- **이 논문이 스스로 잰 값만 옮긴다.** 논문이 비교 대상으로 이름을 부르는 다른
  벤치마크(HumanEval 등)의 수치는 옮기지 않는다.
- **결과 수치에는 검색 설정을 반드시 붙인다.** 같은 모델의 % Resolved가 검색 설정마다
  다르다 — Claude 2는 BM25에서 `1.97`(Table 5, p.6), "oracle" 검색에서 `4.80`(Table 18,
  p.25), "oracle"-collapsed에서 `5.93`(Table 6, p.7)이다. 설정을 떼면 같은 값이 세 개가
  된다.
- **GPT-4의 값은 분모가 다르다.** 예산 제약으로 "Oracle"과 BM25 27k 설정에서 SWE-bench의
  **25% 무작위 부분집합**에만 평가됐다 (Table 7 주석, p.7; Table 18 주석, p.25).
- **`SWE-bench Verified`는 이 논문 밖이다.** 확보본 52쪽 전문에 `verified`라는 낱말이
  단 한 번 나오는데(p.2 `verified by running unit tests`) 데이터셋 이름이 아니다. 검증
  부분집합에 대한 서술은 전부 [철회문](openai2026-swebench-verified-retire.md) 경유다.

## 판본과 텍스트 레이어

텍스트 레이어 판정은 `text_based`(신뢰도 0.88, OCR 필요 0/52쪽)라 기계 추출로 읽었다.
다만 **표와 도판이 다단 조판이라 기본 추출에서 열 순서가 뒤섞인다** — Table 1·Table 5·
Table 18의 값은 `pdftotext -layout` 정렬본으로 대조해 옮겼다. 20쪽(Figure 8, 평가
파이프라인 도해)은 기본 추출이 `suspected_garbled_text` 판정을 받아 정렬본으로 읽었다.

## 이 확보본에 실재하는 결함

- **부록 A.7이 한 문장에서 끊겨 있다.** `SWE-bench Lite is a canonical subset for more
  efficient evaluation of languag models on the SWE-bench task. SWE-bench is`에서 절이
  끝나고 바로 부록 B가 시작한다(p.25). Lite의 필터 기준은 **게재본에 실려 있지 않다.**
- **본문 §2.4도 같은 자리에서 문장이 깨져 있다** — `The full filtering criteria and
  dataset information is included in SWE-bench Lite covers 11 of the original 12
  repositories`(p.4)로, 참조 대상이 빠진 채 두 문장이 이어 붙었다.
- **Claude 2의 BM25 % Resolved가 두 값이다.** 초록·§1·§5 산문은 `1.96%`, Table 2(13k
  칸)도 `1.96`인데 Table 5는 `1.97`이다 (pp.1, 2, 5, 6). 개념 페이지는 표 본체의
  `1.97`을 쓰고 산문 인용에서만 `1.96%`를 원문대로 남긴다.
- **§4.3의 모델 목록과 Table 5의 행이 어긋난다.** §4.3(p.5)은 ChatGPT-3.5·GPT-4·
  Claude 2·SWE-Llama만 세는데 Table 5(p.6)에는 Claude 3 Opus와 GPT-4-turbo 행이 있다.
  v3 개정에서 표만 갱신된 자국으로 보이나 논문이 그렇게 밝히지는 않는다 — 그래서
  **결과 표의 모델군은 2023년에서 2024년 초에 걸친다**고 읽어야 한다.

## 이 소스가 닿을 자리

- [벤치마크의 수명과 철회](../concepts/benchmark-lifespan-and-retirement.md) — 이 소스가
  세우는 페이지의 앞쪽 절반(표준이 된 경위)
