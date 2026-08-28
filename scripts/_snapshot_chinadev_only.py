"""Playwright stealth snapshot for chinadev article."""
from pathlib import Path
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

URL = "http://www.chinadevelopment.com.cn/zxsd/2026/0825/2011961.shtml"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-chinadev-v1.html")
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        locale="zh-CN",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(20000)
    html = page.content()
    text = page.inner_text("body")
    browser.close()

print("len", len(html), "text", len(text), "hit", [m for m in MARKERS if m in html or m in text])
if not any(m in html or m in text for m in MARKERS):
    Path("_debug_chinadev2.html").write_text(html, encoding="utf-8")
    raise SystemExit(1)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
header = f"""<!-- broadsword-100 snapshot archive
 source-url: shturl.cc/Ew36O15jVmVVDdSC7a6mA6WhRFR5xqmGUyXr4Bmqcx0wtWiGauD3k
 resolved-url: {URL}
 captured-at: {now}
 title: 碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径
 media: 中国发展网
 note: local archive snapshot (single-file HTML capture)
-->
"""
OUT.write_text(header + html, encoding="utf-8")
print("saved", OUT)
