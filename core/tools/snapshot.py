#!/usr/bin/env python3
"""소스 원문 스냅샷 (PLAN §4.4-2).

파이프라인에서 **소급 불가능한 유일한 단계**라 최전방에 고정돼 있다. 나중에 다시
받으면 되는 것이 아니다 — 외부 링크는 낙관적 최저 추정으로도 연 3% 부패하고,
그 손실은 복리로 쌓인다.

`snapshot_sha256`은 여기서 한 번 계산되고 이후 불변이다. lint가 같은 함수로 다시
계산해 대조하는 것이 변조 증거의 전부다(syntopicon.snapshot).

    uv run tools/snapshot.py --kb it --citekey kleppmann2017-ddia ~/Downloads/ddia-ch5.pdf
    uv run tools/snapshot.py --kb it --citekey karpathy2026-wiki --url https://example.com/post
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon import schemas, snapshot
from syntopicon.repo import ROOT

USER_AGENT = "syntopicon-snapshot/1 (personal knowledge base archiver)"


def fetch(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="소스 원문을 archive/에 고정한다")
    parser.add_argument("files", nargs="*", type=Path, help="보존할 로컬 파일·디렉터리")
    parser.add_argument("--kb", required=True)
    parser.add_argument("--citekey", required=True, help="스냅샷 디렉터리 이름")
    parser.add_argument("--url", action="append", default=[], help="받아서 보존할 URL")
    args = parser.parse_args(argv)

    layout, sch = layout_mod.load(), schemas.load()
    if args.kb not in layout.kbs():
        print(f"KB '{args.kb}'가 없습니다. kb-new를 먼저 실행하십시오.", file=sys.stderr)
        return 1
    if errors := list(sch.shared("citekey").iter_errors(args.citekey)):
        print(f"citekey '{args.citekey}': {errors[0].message}", file=sys.stderr)
        return 1
    if not args.files and not args.url:
        print("보존할 파일이나 --url이 필요합니다.", file=sys.stderr)
        return 1

    root = ROOT / args.kb / "archive" / args.citekey
    if root.exists():
        print(f"{root.relative_to(ROOT)} 가 이미 있습니다. snapshot_sha256은 write-once이므로 "
              "덮어쓰지 않습니다 — 판본이 다르면 새 citekey를 쓰십시오.", file=sys.stderr)
        return 1
    root.mkdir(parents=True)

    try:
        for source in args.files:
            if source.is_dir():
                shutil.copytree(source, root / source.name)
            else:
                shutil.copy2(source, root / source.name)
        for index, url in enumerate(args.url):
            name = Path(urllib.parse.urlparse(url).path).name or f"page{index}.html"
            fetch(url, root / name)
    except (OSError, urllib.error.URLError) as error:
        shutil.rmtree(root, ignore_errors=True)     # 반쪽 스냅샷을 남기지 않는다
        print(f"스냅샷 실패: {error}", file=sys.stderr)
        return 1

    digest = snapshot.digest(root)
    stored = sum(1 for _ in root.rglob("*") if _.is_file())
    print(f"보존  {root.relative_to(ROOT)}/  ({stored}개 파일)")
    print("\n소스 메타에 그대로 넣으십시오:\n")
    print(f"snapshot: /{args.kb}/archive/{args.citekey}/")
    print(f'snapshot_sha256: "{digest}"')
    print(f'accessed: "{date.today().isoformat()}"')
    print("\narchive/는 git에서 제외되고 restic이 담당합니다(PLAN §5).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
