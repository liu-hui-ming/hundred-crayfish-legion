# -*- coding: utf-8
"""Probe public search for golden-24h WeChat/Zhihu URLs (read-only)."""
from __future__ import annotations

import re
import urllib.parse

from playwright.sync_api import sync_playwright

QUERIES = [
    "算力堆不出灵魂 碳硅道统 十维标尺 知乎",
    "算力堆不出灵魂 碳硅道统 公众号",
    "算力堆不出灵魂 黄清佳 知乎",
]


def extract(html: str) -> tuple[list[str], list[str]]:
    zh = re.findall(r"https://zhuanlan\.zhihu\.com/p/\d+", html)
    wx = re.findall(r"https://mp\.weixin\.qq\.com/s/[A-Za-z0-9_-]+", html)
    return list(dict.fromkeys(zh)), list(dict.fromkeys(wx))


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        for q in QUERIES:
            for engine, base in (
                ("bing", f"https://www.bing.com/search?q={urllib.parse.quote(q)}"),
                (
                    "sogou_wx",
                    "https://weixin.sogou.com/weixin?type=2&query="
                    + urllib.parse.quote(q),
                ),
            ):
                try:
                    page.goto(base, wait_until="domcontentloaded", timeout=90000)
                    page.wait_for_timeout(2500)
                    zh, wx = extract(page.content())
                    print(engine, q[:30], "zh", zh[:5], "wx", wx[:5])
                except Exception as exc:
                    print(engine, "ERR", exc)
        browser.close()


if __name__ == "__main__":
    main()
