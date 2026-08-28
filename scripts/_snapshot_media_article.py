"""Save single-file HTML snapshots for media ledger articles."""
from __future__ import annotations

import argparse
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

TITLE = "碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径"
MARKERS = ("碳硅道统六问", "六大工程卡点", "物理仿真")


def fetch_http(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read()
        charset = "utf-8"
        ct = resp.headers.get("Content-Type", "")
        if "charset=" in ct.lower():
            charset = ct.lower().split("charset=")[-1].split(";")[0].strip()
        try:
            return raw.decode(charset, errors="replace")
        except LookupError:
            return raw.decode("utf-8", errors="replace")


def fetch_playwright(url: str) -> str:
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
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(6000)
        for marker in MARKERS:
            try:
                page.wait_for_selector(f"text={marker}", timeout=15000)
                break
            except Exception:
                continue
        html = page.content()
        browser.close()
        return html


def has_content(html: str) -> bool:
    return any(m in html for m in MARKERS)


def save_snapshot(url: str, out: Path, media: str) -> None:
    html = fetch_http(url)
    if not has_content(html):
        html = fetch_playwright(url)
    if not has_content(html):
        raise RuntimeError(f"article markers not found for {url}")

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
    print(f"OK {out.name} bytes={len(html)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("out")
    parser.add_argument("media")
    args = parser.parse_args()
    try:
        save_snapshot(args.url, Path(args.out), args.media)
        return 0
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
