"""Capture cneo snapshot with DNS override for www.cneo.com.cn."""
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://www.cneo.com.cn/detail102789.html"
OUT = Path("dossier/broadsword-100/snapshot/snapshot-cneo-v1.html")
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真", "碳硅道统")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--host-resolver-rules=MAP www.cneo.com.cn 120.26.85.122",
            "--ignore-certificate-errors",
        ],
    )
    page = browser.new_context(
        locale="zh-CN",
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    ).new_page()
    page.goto(URL, wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(15000)
    html = page.content()
    final = page.url
    browser.close()

print("final", final, "len", len(html), "hit", [m for m in MARKERS if m in html])
if not any(m in html for m in MARKERS):
    Path("_debug_cneo.html").write_text(html, encoding="utf-8")
    raise SystemExit(1)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
header = f"""<!-- broadsword-100 snapshot archive
 source-url: {URL}
 captured-at: {now}
 title: 碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径
 media: 企业观察网
 note: local archive snapshot (single-file HTML capture)
-->
"""
OUT.write_text(header + html, encoding="utf-8")
print("saved", OUT)
