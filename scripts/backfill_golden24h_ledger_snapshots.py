# -*- coding: utf-8
"""Backfill golden-24h WeChat/Zhihu URLs into broadsword-media-ledger + HTML snapshots.

Reads four URLs from dossier/broadsword-100/sync/golden-24h-published-urls.json
Refuses empty or non-matching domains. Verifies page mentions 算力堆不出 or 碳硅道统.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
URLS_JSON = ROOT / "dossier/broadsword-100/sync/golden-24h-published-urls.json"
LEDGER = ROOT / "dossier/broadsword-100/broadsword-media-ledger.md"
SNAP_DIR = ROOT / "dossier/broadsword-100/snapshot"
RELEASE = ROOT / "dossier/broadsword-100/sync/RELEASE-CHAIN-BACKFILL-20260905.md"
CHANGELOG = ROOT / "CHANGELOG.md"
ISSUE_LEDGER = ROOT / "docs/issue-registry/2026-08-15-dt188-closure-issues-ledger.md"

TITLE_NEEDLE = "算力堆不出"
ALT_NEEDLE = "碳硅道统"

SNAPSHOTS = {
    "cyzone843850_wechat": "snapshot-wechat-cyzone843850-v1.html",
    "cyzone843850_zhihu": "snapshot-zhihu-cyzone843850-v1.html",
    "kr36_v2_wechat": "snapshot-wechat-36kr-v2-sync-v1.html",
    "kr36_v2_zhihu": "snapshot-zhihu-36kr-v2-sync-v1.html",
}

LEDGER_PLACEHOLDERS = [
    (
        "|算力堆不出\"灵魂\"：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板|碳硅道统公众号|全文同步|【待发布后补链】|待发布||黄金24小时同步；注明首发于创业邦|【待补充】|",
        "cyzone843850_wechat",
    ),
    (
        "|算力堆不出\"灵魂\"：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板|知乎|全文同步|【待发布后补链】|待发布||黄金24小时同步；注明首发于创业邦|【待补充】|",
        "cyzone843850_zhihu",
    ),
    (
        "|算力堆不出\"灵魂\"：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板|碳硅道统公众号（36kr v2 同步）|全文同步|【待发布后补链】|待发布||黄金24h；注明首发于36kr；稿见 sync/golden-24h-36kr-v2-wechat-zhihu.md|【待补充】|",
        "kr36_v2_wechat",
    ),
    (
        "|算力堆不出\"灵魂\"：用碳硅道统十维标尺，戳破AGI估值泡沫与算力天花板|知乎（36kr v2 同步）|全文同步|【待发布后补链】|待发布||黄金24h；注明首发于36kr|【待补充】|",
        "kr36_v2_zhihu",
    ),
]


def load_urls() -> dict[str, str]:
    data = json.loads(URLS_JSON.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for key in SNAPSHOTS:
        val = (data.get(key) or "").strip()
        if not val:
            raise SystemExit(f"Missing URL for {key} in {URLS_JSON}")
        out[key] = val
    return out


def validate_url(url: str) -> None:
    if "mp.weixin.qq.com/s/" not in url and "zhihu.com/p/" not in url and "zhuanlan.zhihu.com/p/" not in url:
        raise SystemExit(f"Refusing non WeChat/Zhihu URL: {url}")


def fetch_html(url: str) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://www.zhihu.com/" if "zhihu.com" in url else "",
        },
    )
    try:
        with urlopen(req, timeout=60) as resp:
            if resp.status != 200:
                raise SystemExit(f"HTTP {resp.status} for {url}")
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        if "zhihu.com" not in url:
            raise
        print(f"  urllib failed for {url} ({exc}); trying Playwright…")
        return fetch_html_playwright(url)


def fetch_html_playwright(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Zhihu fetch blocked; install playwright: pip install playwright") from exc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4000)
        html = page.content()
        browser.close()
    if "40362" in html or "暂时限制本次访问" in html:
        raise SystemExit(f"Zhihu anti-bot blocked snapshot fetch: {url}")
    return html


def verify_content(html: str, url: str) -> None:
    if TITLE_NEEDLE not in html and ALT_NEEDLE not in html:
        raise SystemExit(f"Page content does not match expected article markers: {url}")


def write_snapshot(url: str, fname: str, html: str) -> Path:
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    out = SNAP_DIR / fname
    header = (
        f"<!-- broadsword-100 snapshot archive\n"
        f" source-url: {url}\n"
        f" captured-at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f" note: golden-24h sync backfill\n"
        f"-->\n"
    )
    out.write_text(header + html, encoding="utf-8", newline="\n")
    return out


def patch_ledger(urls: dict[str, str]) -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for old_line, key in LEDGER_PLACEHOLDERS:
        if old_line not in text:
            raise SystemExit(f"Ledger row not found (already backfilled?): {key}")
        url = urls[key]
        snap = SNAPSHOTS[key]
        parts = old_line.split("|")
        # columns: title|platform|type|url|status|time|note|snapshot
        parts[4] = url
        parts[5] = "已发布"
        parts[8] = snap
        new_line = "|".join(parts)
        text = text.replace(old_line, new_line, 1)
    # progress table
    text = text.replace(
        "| 创业邦 843850 | https://www.cyzone.cn/article/843850.html | ✅ 已上线（复核通过） | ⏳ 待人工发布 → `golden-24h-cyzone843850-wechat-zhihu.md` |",
        "| 创业邦 843850 | https://www.cyzone.cn/article/843850.html | ✅ 已上线（复核通过） | ✅ 同步链已回填（见 ledger 公众号/知乎行） |",
    )
    text = text.replace(
        "| 36kr v2 | https://36kr.com/p/3957153109622150 | ✅ 已上线（台账+快照） | ⏳ 待人工发布 → `golden-24h-36kr-v2-wechat-zhihu.md` |",
        "| 36kr v2 | https://36kr.com/p/3957153109622150 | ✅ 已上线（台账+快照） | ✅ 同步链已回填（见 ledger 公众号/知乎行） |",
    )
    LEDGER.write_text(text, encoding="utf-8", newline="\n")


def sync_dt188_golden24h_backfill() -> None:
    needle = "golden-24h 四条同步链已回填"
    text = ISSUE_LEDGER.read_text(encoding="utf-8")
    if needle in text:
        return
    line = (
        "| — | POSTED | broadsword-100 golden-24h 四条同步链回填 | "
        "`dossier/broadsword-100/broadsword-media-ledger.md` · 见 CHANGELOG golden-24h 四条 |"
    )
    note = (
        "\n\n**golden-24h 四条同步链已回填（台账行，非 Issue 编号）：** "
        "创业邦/36kr v2 公众号+知乎 · `sync/golden-24h-published-urls.json` · snapshot 四文件\n"
    )
    anchor = "## 低优先级（P-Low）"
    head, tail = text.split(anchor, 1)
    ISSUE_LEDGER.write_text(head.rstrip() + "\n" + line + note + "\n" + anchor + tail, encoding="utf-8")


def prepend_changelog() -> None:
    block = (
        "[2026-09-15] broadsword-100 golden-24h 四条同步链回填\n\n"
        "• ledger：`dossier/broadsword-100/broadsword-media-ledger.md`\n"
        "• 快照：`dossier/broadsword-100/snapshot/snapshot-wechat-cyzone843850-v1.html` 等 4 文件\n"
        "• URL 源：`sync/golden-24h-published-urls.json`（真实链接，禁止手工捏造）\n\n"
    )
    text = CHANGELOG.read_text(encoding="utf-8")
    if "golden-24h 四条同步链回填" in text:
        return
    if text.startswith("# CHANGELOG\n\n"):
        text = "# CHANGELOG\n\n" + block + text[len("# CHANGELOG\n\n") :]
    CHANGELOG.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--skip-fetch", action="store_true", help="Only patch ledger (dangerous)")
    args = parser.parse_args()

    urls = load_urls()
    for key, url in urls.items():
        validate_url(url)
        print(f"OK domain {key}: {url}")

    if not args.skip_fetch:
        for key, url in urls.items():
            html = fetch_html(url)
            verify_content(html, url)
            path = write_snapshot(url, SNAPSHOTS[key], html)
            print(f"  snapshot {path.name} ({len(html)} bytes)")

    patch_ledger(urls)
    sync_dt188_golden24h_backfill()
    prepend_changelog()
    print("Ledger updated.")

    if args.commit:
        rel = [
            "dossier/broadsword-100/broadsword-media-ledger.md",
            "dossier/broadsword-100/snapshot",
            "dossier/broadsword-100/sync/golden-24h-published-urls.json",
            "CHANGELOG.md",
            str(ISSUE_LEDGER.relative_to(ROOT)),
        ]
        subprocess.run(["git", "add", *rel], cwd=ROOT, check=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "broadsword-100: golden-24h WeChat/Zhihu URL backfill + snapshots",
                "-m",
                "Four verified mp.weixin.qq.com / zhihu.com links from golden-24h-published-urls.json.",
            ],
            cwd=ROOT,
            check=True,
        )
        print("Committed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
