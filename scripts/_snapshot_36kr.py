"""Fetch 36kr article HTML via headless browser (anti-bot bypass)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://36kr.com/p/3948977352965248"
TITLE = "碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-36kr-v1.html")
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真")


def main() -> int:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        page = context.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(8000)
        for marker in MARKERS:
            try:
                page.wait_for_selector(f"text={marker}", timeout=20000)
                break
            except Exception:
                continue
        html = page.content()
        browser.close()

    if not any(m in html for m in MARKERS):
        print("ERROR: article body not found in rendered HTML", file=sys.stderr)
        print("len", len(html), file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = f"""<!-- broadsword-100 snapshot archive
 source-url: {URL}
 captured-at: {now}
 title: {TITLE}
 media: 36氪
 note: local archive snapshot (headless browser HTML capture)
-->
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + html, encoding="utf-8")
    print("saved", out_path, "bytes", len(html))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
