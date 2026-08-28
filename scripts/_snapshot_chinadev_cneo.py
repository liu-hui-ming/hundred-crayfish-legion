"""Resolve and snapshot chinadev + cneo articles."""
from __future__ import annotations

import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真")
TITLE = "碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径"


def save(out: Path, url: str, media: str, html: str) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = f"""<!-- broadsword-100 snapshot archive
 source-url: {url}
 captured-at: {now}
 title: {TITLE}
 media: {media}
 note: local archive snapshot (single-file HTML capture)
-->
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + html, encoding="utf-8")


def fetch_chinadev() -> tuple[str, str]:
    search = "https://search.chinadevelopment.com.cn/index.php?q=%E7%A2%B3%E7%A1%85%E9%81%93%E7%BB%9F%E5%85%AD%E9%97%AE"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(locale="zh-CN").new_page()
        page.goto(search, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(3000)
        link = page.locator("a", has_text="碳硅道统六问").first
        href = link.get_attribute("href")
        if not href:
            raise RuntimeError("chinadev article link not found")
        if href.startswith("/"):
            href = "http://www.chinadevelopment.com.cn" + href
        page.goto(href, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)
        html = page.content()
        final = page.url
        browser.close()
    return final, html


def fetch_cneo_playwright() -> tuple[str, str]:
    short = "https://shturl.cc/Ew36O15jVmVVDdSC7a6mA6WhRFR5xqmGUyXr4Bmqcx0wtWiGauD3k"
    direct = "https://www.cneo.com.cn/detail102789.html"
    candidates = [short, direct, "http://www.cneo.com.cn/detail102789.html"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            locale="zh-CN",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
        )
        page = ctx.new_page()
        last_html = ""
        final_url = direct
        for url in candidates:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=90000)
                page.wait_for_timeout(12000)
                final_url = page.url
                last_html = page.content()
                if any(m in last_html for m in MARKERS):
                    browser.close()
                    return final_url, last_html
            except Exception as exc:
                print("cneo try fail", url, exc)
        browser.close()
    if any(m in last_html for m in MARKERS):
        return final_url, last_html
    raise RuntimeError("cneo article not captured")


def main() -> None:
    # chinadev via search resolve
    chinadev_url, chinadev_html = fetch_chinadev()
    print("chinadev url", chinadev_url, "len", len(chinadev_html))
    if not any(m in chinadev_html for m in MARKERS):
        Path("_debug_chinadev.html").write_text(chinadev_html, encoding="utf-8")
        raise RuntimeError("chinadev markers missing")
    save(
        Path("dossier/broadsword-100/snapshot/snapshot-chinadev-v1.html"),
        "shturl.cc/Ew36O15jVmVVDdSC7a6mA6WhRFR5xqmGUyXr4Bmqcx0wtWiGauD3k",
        "中国发展网",
        chinadev_html,
    )
    print("saved snapshot-chinadev-v1.html", len(chinadev_html))

    # cneo
    try:
        cneo_url, cneo_html = fetch_cneo_playwright()
        save(
            Path("dossier/broadsword-100/snapshot/snapshot-cneo-v1.html"),
            "https://www.cneo.com.cn/detail102789.html",
            "企业观察网",
            cneo_html,
        )
        print("saved snapshot-cneo-v1.html", len(cneo_html))
    except Exception as exc:
        print("cneo fallback:", exc)
        # fallback: use gqyc subdomain search or HTTP resolve tricks
        import subprocess

        for ip in ("39.105.31.60", "47.92.121.139"):
            cmd = [
                "curl.exe", "-sL", "-m", "45",
                "--resolve", f"www.cneo.com.cn:443:{ip}",
                "https://www.cneo.com.cn/detail102789.html",
            ]
            out = subprocess.check_output(cmd)
            text = out.decode("utf-8", errors="replace")
            if any(m in text for m in MARKERS):
                save(
                    Path("dossier/broadsword-100/snapshot/snapshot-cneo-v1.html"),
                    "https://www.cneo.com.cn/detail102789.html",
                    "企业观察网",
                    text,
                )
                print("saved snapshot-cneo-v1.html via resolve", ip, len(text))
                return
        raise


if __name__ == "__main__":
    main()
