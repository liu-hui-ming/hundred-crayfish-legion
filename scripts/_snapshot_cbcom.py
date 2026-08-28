"""Capture cb.com.cn article bypassing bot challenge."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "http://www.cb.com.cn/index/show/gd/cv/cv1362586161496"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-cbcom-v1.html")
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真", "碳硅道统")


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            locale="zh-CN",
            viewport={"width": 1366, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        ctx.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(30000)
        try:
            page.wait_for_function(
                "document.body && document.body.innerText.length > 800",
                timeout=90000,
            )
        except Exception:
            pass
        text = page.inner_text("body")
        html = page.content()
        browser.close()

    if not any(m in text or m in html for m in MARKERS):
        print("ERROR: markers missing", len(text), text[:300])
        return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = f"""<!-- broadsword-100 snapshot archive
 source-url: {URL}
 captured-at: {now}
 title: 碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径
 media: 中国经营网
 note: local archive snapshot (single-file HTML capture)
-->
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + html, encoding="utf-8")
    print(f"saved {OUT} bytes={len(html)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
