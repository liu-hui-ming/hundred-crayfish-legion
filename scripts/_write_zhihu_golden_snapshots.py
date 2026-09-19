# -*- coding: utf-8 -*-
"""One-off: write Zhihu golden-24h snapshots when automated fetch is blocked."""
from __future__ import annotations

import html as htmlmod
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "dossier/broadsword-100/snapshot"
MD = ROOT / "dossier/broadsword-100/sync/golden-24h-cyzone843850-wechat-zhihu.md"
URL = "https://zhuanlan.zhihu.com/p/2074620442539733631"


def body_from_md() -> str:
    lines: list[str] = []
    for line in MD.read_text(encoding="utf-8").splitlines():
        if line.startswith("#基线") or line.startswith("#母基线") or line.startswith("#版本"):
            continue
        lines.append(line)
    paras = [p.strip() for p in "\n".join(lines).split("\n\n") if p.strip()]
    return "".join(f"<p>{htmlmod.escape(p)}</p>\n" for p in paras)


def write_snapshot(fname: str, note: str, inner: str) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = (
        "<!DOCTYPE html>\n"
        '<html lang="zh-CN">\n'
        "<head><meta charset=\"utf-8\"/>"
        "<title>算力堆不出\"灵魂\"：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板</title></head>\n"
        "<body>\n"
        f"<!-- broadsword-100 snapshot archive\n"
        f" source-url: {URL}\n"
        f" captured-at: {now}\n"
        f" note: {note}\n"
        f"-->\n"
        "<h1>算力堆不出\"灵魂\"：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板</h1>\n"
        f"{inner}\n"
        "</body></html>\n"
    )
    out = SNAP / fname
    out.write_text(doc, encoding="utf-8", newline="\n")
    print(out.name, out.stat().st_size)


def main() -> None:
    inner = body_from_md()
    write_snapshot(
        "snapshot-zhihu-cyzone843850-v1.html",
        "golden-24h sync backfill; Zhihu HTTP fetch blocked; body aligned to sync md + user URL",
        inner,
    )
    write_snapshot(
        "snapshot-zhihu-36kr-v2-sync-v1.html",
        "golden-24h 36kr v2 ledger row; same published URL; body from cyzone843850 sync md",
        inner,
    )


if __name__ == "__main__":
    main()
