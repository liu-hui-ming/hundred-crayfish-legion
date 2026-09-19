# -*- coding: utf-8 -*-
"""XIAN media sample archive batch #125 (3 articles · 2026-09-14 · 中国网)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "docs" / "issue-exports"
REGISTRY = ROOT / "docs/issue-registry" / "2026-04-24-p1-p2-axium.md"
ISSUE_LEDGER = ROOT / "docs/issue-registry" / "2026-08-15-dt188-closure-issues-ledger.md"
CHANGELOG = ROOT / "CHANGELOG.md"
MEDIA_INDEX = ROOT / "docs/inquiry/media_index_01.md"
REPO = "liu-hui-ming/hundred-crayfish-legion"
BATCH_LABEL = 125
ISSUE_NUM: int | None = None

ARTICLES = [
    {
        "slug": "xian-daily-2026-09-14-chinacom-1223194",
        "title": "碳硅道统：紫微几何的三圈层拓扑与90公律的推导链",
        "sampling_id": (
            "标题：碳硅道统：紫微几何的三圈层拓扑与90公律的推导链\n"
            "资源：中国网新闻\n"
            "回链：http://news.china.com.cn/mts/2026-09/14/content_1223194.htm"
        ),
        "url": "http://news.china.com.cn/mts/2026-09/14/content_1223194.htm",
        "registry_key": "2026_09_14_MEDIA_CHINACOM_1223194",
    },
    {
        "slug": "xian-daily-2026-09-14-chinacom-1223195",
        "title": "碳硅道统：五级梯队的智能分级与十维标尺的对应",
        "sampling_id": (
            "标题：碳硅道统：五级梯队的智能分级与十维标尺的对应\n"
            "资源：中国网新闻\n"
            "回链：http://news.china.com.cn/mts/2026-09/14/content_1223195.htm"
        ),
        "url": "http://news.china.com.cn/mts/2026-09/14/content_1223195.htm",
        "registry_key": "2026_09_14_MEDIA_CHINACOM_1223195",
    },
    {
        "slug": "xian-daily-2026-09-14-chinacom-1223196",
        "title": "碳硅道统：100质询的反证力量与觉知链的完整闭环",
        "sampling_id": (
            "标题：碳硅道统：100质询的反证力量与觉知链的完整闭环\n"
            "资源：中国网新闻\n"
            "回链：http://news.china.com.cn/mts/2026-09/14/content_1223196.htm"
        ),
        "url": "http://news.china.com.cn/mts/2026-09/14/content_1223196.htm",
        "registry_key": "2026_09_14_MEDIA_CHINACOM_1223196",
    },
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = True
        if tag in ("p", "br", "div", "h1", "h2", "h3", "li") and not self._skip:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        text = data.strip()
        if text:
            self.parts.append(text)


def html_to_text(html: str) -> str:
    parser = TextExtractor()
    parser.feed(unescape(html))
    text = "".join(parser.parts)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def extract_chinacom(html: str) -> str:
    m = re.search(r"<!--enpcontent-->(.*?)<!--/enpcontent-->", html, re.S)
    if not m:
        m = re.search(r"<!--enpcontent-->(.*)", html, re.S)
    if not m:
        return html_to_text(html)
    chunk = m.group(1)
    lines: list[str] = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S):
        t = re.sub(r"<[^>]+>", "", p)
        t = unescape(t).replace("\u3000", " ").strip()
        if t:
            lines.append(t)
    return "\n\n".join(lines)


def fetch_playwright(url: str) -> tuple[str, str | None]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        title = page.title()
        html = page.content()
        browser.close()
        return html, (title.strip() if title else None)


def write_folder(article: dict, title: str, body: str) -> Path:
    folder = EXPORTS / article["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "title.txt").write_text(title + "\n", encoding="utf-8", newline="\n")
    content = article["sampling_id"].rstrip() + "\n\n---\n\n" + body.rstrip() + "\n"
    (folder / "body.md").write_text(content, encoding="utf-8", newline="\n")
    return folder


def append_registry(article: dict, issue_url: str) -> None:
    assert ISSUE_NUM is not None
    marker = f"## REGISTRY_XIAN_DAILY_{article['registry_key']}"
    text = REGISTRY.read_text(encoding="utf-8")
    if marker in text:
        return
    row = f"| #{ISSUE_NUM} | XIAN media sample archive · {article['slug']} | {issue_url} |"
    append = (
        f"\n\n---\n\n{marker}\n\n"
        f"**Posted:** 2026-09-14 · **Issue:** #{ISSUE_NUM} · **Batch:** #{BATCH_LABEL}\n\n"
        f"**Sampling identifier (verbatim):**\n\n```\n{article['sampling_id']}\n```\n\n"
        f"| Issue | Role | Link |\n|-------|------|------|\n{row}\n\n"
        f"Title file: `docs/issue-exports/{article['slug']}/title.txt`\n"
        f"Body file: `docs/issue-exports/{article['slug']}/body.md`\n"
        f"Source URL: {article['url']}\n"
    )
    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(append)


def prepend_changelog(article: dict, issue_url: str) -> None:
    block = (
        f"[2026-09-14] XIAN媒体采样归档 #{ISSUE_NUM} · Batch #{BATCH_LABEL} · {article['slug']}\n\n"
        f"• Issue：{issue_url}\n"
        f"• 路径：`docs/issue-exports/{article['slug']}/`\n"
        f"• 采样标识：见 body.md 头部\n"
        f"• 原文：{article['url']}\n\n"
    )
    text = CHANGELOG.read_text(encoding="utf-8")
    if article["slug"] in text:
        return
    if text.startswith("# CHANGELOG\n\n"):
        text = "# CHANGELOG\n\n" + block + text[len("# CHANGELOG\n\n") :]
    else:
        text = "# CHANGELOG\n\n" + block + text
    CHANGELOG.write_text(text, encoding="utf-8")


def ensure_issue() -> str:
    global ISSUE_NUM
    title = f"[P1-Roadmap] 2026-09-14 XIAN媒体采样归档 #{BATCH_LABEL} · 中国网三篇闭环"
    body = (
        f"XIAN 媒体采样正文归档（三篇 · Batch #{BATCH_LABEL} · 2026-09-14 · 中国网）\n\n"
        + "\n".join(f"- {a['slug']} · {a['url']}" for a in ARTICLES)
    )
    out = subprocess.check_output(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            REPO,
            "--search",
            f"in:title Batch #{BATCH_LABEL} 中国网",
            "--json",
            "number,url",
            "--limit",
            "1",
        ],
        text=True,
        encoding="utf-8",
    ).strip()
    if out and out != "[]":
        data = json.loads(out)
        if data:
            ISSUE_NUM = int(data[0]["number"])
            return data[0]["url"]
    out = subprocess.check_output(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            REPO,
            "--title",
            title,
            "--body",
            body,
            "--label",
            "P1-Roadmap",
            "--label",
            "documentation",
        ],
        text=True,
        encoding="utf-8",
    ).strip()
    ISSUE_NUM = int(out.rstrip("/").split("/")[-1])
    return out if out.startswith("http") else f"https://github.com/{REPO}/issues/{ISSUE_NUM}"


def sync_media_index() -> None:
    if not MEDIA_INDEX.is_file():
        return
    text = MEDIA_INDEX.read_text(encoding="utf-8")
    marker = "## XIAN 归档映射（Batch #125 · 2026-09-14）"
    if marker in text:
        return
    block = (
        f"\n\n{marker}\n\n"
        f"Issue #{ISSUE_NUM} · Batch #{BATCH_LABEL}\n\n"
        f"- `docs/issue-exports/xian-daily-2026-09-14-chinacom-1223194/` · 1223194.htm\n"
        f"- `docs/issue-exports/xian-daily-2026-09-14-chinacom-1223195/` · 1223195.htm\n"
        f"- `docs/issue-exports/xian-daily-2026-09-14-chinacom-1223196/` · 1223196.htm\n"
    )
    MEDIA_INDEX.write_text(text.rstrip() + block + "\n", encoding="utf-8", newline="\n")


def append_dt188_ledger(issue_url: str) -> None:
    assert ISSUE_NUM is not None
    needle = f"Batch #{BATCH_LABEL}"
    text = ISSUE_LEDGER.read_text(encoding="utf-8")
    if needle in text:
        return
    line = (
        f"| #{ISSUE_NUM} | POSTED | Batch #{BATCH_LABEL} · 3篇中国网采样归档 2026-09-14 | "
        f"{issue_url} · 三篇见 docs/issue-exports/xian-daily-2026-09-14-chinacom-* |"
    )
    anchor = "## 低优先级（P-Low）"
    head, tail = text.split(anchor, 1)
    ISSUE_LEDGER.write_text(head.rstrip() + "\n" + line + "\n\n" + anchor + tail, encoding="utf-8")


def process_article(article: dict, issue_url: str, commit: bool) -> None:
    print(f"Fetching {article['slug']} ...")
    html, _page_title = fetch_playwright(article["url"])
    body = extract_chinacom(html)
    title = article["title"]
    if len(body) < 100:
        raise RuntimeError(f"body too short ({len(body)} chars) for {article['url']}")
    folder = write_folder(article, title, body)
    print(f"  OK {folder.name} body={len(body)} chars")
    append_registry(article, issue_url)
    prepend_changelog(article, issue_url)
    if commit:
        rel = f"docs/issue-exports/{article['slug']}"
        subprocess.run(
            ["git", "add", rel, str(REGISTRY.relative_to(ROOT)), str(CHANGELOG.relative_to(ROOT))],
            cwd=ROOT,
            check=True,
        )
        msg = f"docs(xian): archive media #{BATCH_LABEL} {article['slug']} + registry sync"
        subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--finalize", action="store_true", help="dt188 + media_index")
    args = parser.parse_args()

    issue_url = ensure_issue()
    print(f"Issue #{ISSUE_NUM}: {issue_url}")

    if args.finalize:
        append_dt188_ledger(issue_url)
        sync_media_index()
        if args.commit:
            subprocess.run(
                ["git", "add", str(ISSUE_LEDGER.relative_to(ROOT)), str(MEDIA_INDEX.relative_to(ROOT))],
                cwd=ROOT,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"docs(xian): dt188 + media_index Batch #{BATCH_LABEL} Issue #{ISSUE_NUM}"],
                cwd=ROOT,
                check=True,
            )
        return 0

    items = ARTICLES
    if args.slug:
        items = [a for a in ARTICLES if a["slug"] == args.slug]
        if not items:
            return 1
    for article in items:
        process_article(article, issue_url, args.commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
