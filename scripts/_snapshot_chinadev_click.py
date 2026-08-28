"""Click-through chinadev search result and save snapshot."""
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

SEARCH = "https://search.chinadevelopment.com.cn/index.php?q=%E7%A2%B3%E7%A1%85%E9%81%93%E7%BB%9F%E5%85%AD%E9%97%AE"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-chinadev-v1.html")
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(locale="zh-CN").new_page()
    page.goto(SEARCH, wait_until="networkidle", timeout=120000)
    with page.expect_navigation(timeout=120000):
        page.locator("a", has_text="碳硅道统六问").first.click()
    page.wait_for_timeout(15000)
    page.wait_for_function("() => document.body && document.body.innerText.length > 500", timeout=90000)
    html = page.content()
    final = page.url
    browser.close()

print("final", final, "len", len(html), "hit", [m for m in MARKERS if m in html])
if not any(m in html for m in MARKERS):
    OUT.with_name("_debug_chinadev3.html").write_text(html, encoding="utf-8")
    raise SystemExit(1)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
header = f"""<!-- broadsword-100 snapshot archive
 source-url: shturl.cc/Ew36O15jVmVVDdSC7a6mA6WhRFR5xqmGUyXr4Bmqcx0wtWiGauD3k
 resolved-url: {final}
 captured-at: {now}
 title: 碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径
 media: 中国发展网
 note: local archive snapshot (single-file HTML capture)
-->
"""
OUT.write_text(header + html, encoding="utf-8")
print("saved", OUT)
