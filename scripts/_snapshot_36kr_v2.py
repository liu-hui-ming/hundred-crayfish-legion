"""Fetch 36kr article snapshot-36kr-v2 (十维标尺姊妹篇)."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://36kr.com/p/3957153109622150"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-36kr-v2.html")
TITLE = "算力堆不出“灵魂”：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板"
MARKERS = ("算力堆不出", "十维标尺", "AGI", "碳硅道统")


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(
            locale="zh-CN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        ).new_page()
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
        print("ERROR markers missing", len(html))
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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + html, encoding="utf-8")
    print("saved", OUT, "bytes", len(html))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
