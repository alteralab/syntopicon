#!/bin/sh
# README 다이어그램 렌더 — .mmd가 정본, SVG는 커밋되는 산출물.
# GitHub 내장 mermaid 대신 사전 렌더링을 쓰는 이유: 뷰어 컨트롤 제거 +
# 렌더러 버전·버그로부터 독립 (결정적 렌더). 수정 절차: .mmd 편집 → ./build.sh → 커밋.
cd "$(dirname "$0")" || exit 1
for f in *.mmd; do
  b="${f%.mmd}"
  npx -y @mermaid-js/mermaid-cli -q -b transparent -i "$f" -o "$b-light.svg" || exit 1
  npx -y @mermaid-js/mermaid-cli -q -b transparent -t dark -i "$f" -o "$b-dark.svg" || exit 1
done
