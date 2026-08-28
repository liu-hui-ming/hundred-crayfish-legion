"""Capture chinadev via search href then direct navigation."""
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

SEARCH = "https://search.chinadevelopment.com.cn/index.php?q=%E7%A2%B3%E7%A1%85%E9%81%93%E7%BB%9F%E5%85%AD%E9%97%AE"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-chinadev-v1.html")
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真")
RESOLVED = "http://www.chinadevelopment.com.cn/zxsd/2026/0825/2011961.shtml"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--host-resolver-rules=MAP www.chinadevelopment.com.cn 203.207.196.66"],
    )
    ctx = browser.new_context(locale="zh-CN")
    page = ctx.new_page()
    page.goto(SEARCH, wait_until="networkidle", timeout=120000)
    href = page.locator("a", has_text="碳硅道统六问").first.get_attribute("href")
    if href and href.startswith("/"):
        href = "http://www.chinadevelopment.com.cn" + href
    target = href or RESOLVED
    print("target", target)
    page.goto(target, wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(20000)
    try:
        page.wait_for_function("() => document.body && document.body.innerText.length > 800", timeout=60000)
    except Exception:
        pass
    html = page.content()
    final = page.url
    browser.close()

print("final", final, "len", len(html), "hit", [m for m in MARKERS if m in html])
if not any(m in html for m in MARKERS):
    Path("_debug_chinadev4.html").write_text(html, encoding="utf-8")
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
