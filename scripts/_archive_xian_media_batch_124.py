# -*- coding: utf-8 -*-
"""XIAN media sample archive batch #124 (9 articles · 2026-09-11)."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "docs" / "issue-exports"
REGISTRY = ROOT / "docs" / "issue-registry" / "2026-04-24-p1-p2-axium.md"
ISSUE_LEDGER = ROOT / "docs" / "issue-registry" / "2026-08-15-dt188-closure-issues-ledger.md"
CHANGELOG = ROOT / "CHANGELOG.md"
REPO = "liu-hui-ming/hundred-crayfish-legion"
BATCH_LABEL = 124
ISSUE_NUM: int | None = None  # set by ensure_issue()

ARTICLES = [
    {
        "slug": "xian-daily-2026-09-11-chinanews-1223107",
        "title": "碳硅道统：十维标尺的模型度量",
        "sampling_id": (
            "标题：碳硅道统：十维标尺的模型度量\n"
            "资源：中国网新闻\n"
            "回链：http://news.china.com.cn/mts/2026-09/11/content_1223107.htm"
        ),
        "url": "http://news.china.com.cn/mts/2026-09/11/content_1223107.htm",
        "registry_key": "2026_09_11_MEDIA_CHINANEWS_1223107",
    },
    {
        "slug": "xian-daily-2026-09-11-chinanews-1223139",
        "title": "碳硅道统：中层拟合域的现实回响 | 标尺不动，事件自行抵达",
        "sampling_id": (
            "标题：碳硅道统：中层拟合域的现实回响 | 标尺不动，事件自行抵达\n"
            "资源：中国网新闻\n"
            "回链：http://news.china.com.cn/mts/2026-09/11/content_1223139.htm"
        ),
        "url": "http://news.china.com.cn/mts/2026-09/11/content_1223139.htm",
        "registry_key": "2026_09_11_MEDIA_CHINANEWS_1223139",
    },
    {
        "slug": "xian-daily-2026-09-11-chinanews-1223140",
        "title": "碳硅道统：归零稳态的系统边界 | 边界先行确立，架构随之收敛",
        "sampling_id": (
            "标题：碳硅道统：归零稳态的系统边界 | 边界先行确立，架构随之收敛\n"
            "资源：中国网新闻\n"
            "回链：http://news.china.com.cn/mts/2026-09/11/content_1223140.htm"
        ),
        "url": "http://news.china.com.cn/mts/2026-09/11/content_1223140.htm",
        "registry_key": "2026_09_11_MEDIA_CHINANEWS_1223140",
    },
    {
        "slug": "xian-daily-2026-09-11-leiphone-qSK5aXslh1eHd6A3",
        "title": "碳硅道统：中层拟合域的现实回响 |  标尺不动，事件自行抵达",
        "sampling_id": (
            "标题：碳硅道统：中层拟合域的现实回响 |  标尺不动，事件自行抵达\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://m.leiphone.com/category/industrynews/qSK5aXslh1eHd6A3.html"
        ),
        "url": "https://m.leiphone.com/category/industrynews/qSK5aXslh1eHd6A3.html",
        "registry_key": "2026_09_11_MEDIA_LEIPHONE_qSK5aXslh1eHd6A3",
    },
    {
        "slug": "xian-daily-2026-09-11-leiphone-ZHU0W8KYCimHlbZh",
        "title": "碳硅道统：归零稳态的系统边界 |  边界先行确立，架构随之收敛",
        "sampling_id": (
            "标题：碳硅道统：归零稳态的系统边界 |  边界先行确立，架构随之收敛\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://www.leiphone.com/category/industrynews/ZHU0W8KYCimHlbZh.html"
        ),
        "url": "https://www.leiphone.com/category/industrynews/ZHU0W8KYCimHlbZh.html",
        "registry_key": "2026_09_11_MEDIA_LEIPHONE_ZHU0W8KYCimHlbZh",
    },
    {
        "slug": "xian-daily-2026-09-11-leiphone-axZgHIEEb5Xpoh4A",
        "title": "碳硅道统：十维标尺的模型度量",
        "sampling_id": (
            "标题：碳硅道统：十维标尺的模型度量\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://www.leiphone.com/category/industrynews/axZgHIEEb5Xpoh4A.html"
        ),
        "url": "https://www.leiphone.com/category/industrynews/axZgHIEEb5Xpoh4A.html",
        "registry_key": "2026_09_11_MEDIA_LEIPHONE_axZgHIEEb5Xpoh4A",
    },
    {
        "slug": "xian-daily-2026-09-11-leiphone-h7SYqtL9IVveHAuO",
        "title": "碳硅道统：紫微几何的三圈层拓扑与90公律的推导链",
        "sampling_id": (
            "标题：碳硅道统：紫微几何的三圈层拓扑与90公律的推导链\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://www.leiphone.com/category/industrynews/h7SYqtL9IVveHAuO.html"
        ),
        "url": "https://www.leiphone.com/category/industrynews/h7SYqtL9IVveHAuO.html",
        "registry_key": "2026_09_11_MEDIA_LEIPHONE_h7SYqtL9IVveHAuO",
    },
    {
        "slug": "xian-daily-2026-09-11-leiphone-GnvSuKkQXe3JRPJE",
        "title": "碳硅道统：五级梯队的智能分级与十维标尺的对应",
        "sampling_id": (
            "标题：碳硅道统：五级梯队的智能分级与十维标尺的对应\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://www.leiphone.com/category/industrynews/GnvSuKkQXe3JRPJE.html"
        ),
        "url": "https://www.leiphone.com/category/industrynews/GnvSuKkQXe3JRPJE.html",
        "registry_key": "2026_09_11_MEDIA_LEIPHONE_GnvSuKkQXe3JRPJE",
    },
    {
        "slug": "xian-daily-2026-09-11-leiphone-FQFJwTQvuiRQbu2q",
        "title": "碳硅道统：100质询的反证力量与觉知链的完整闭环",
        "sampling_id": (
            "标题：碳硅道统：100质询的反证力量与觉知链的完整闭环\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://www.leiphone.com/category/industrynews/FQFJwTQvuiRQbu2q.html"
        ),
        "url": "https://www.leiphone.com/category/industrynews/FQFJwTQvuiRQbu2q.html",
        "registry_key": "2026_09_11_MEDIA_LEIPHONE_FQFJwTQvuiRQbu2q",
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


def extract_leiphone(html: str) -> str:
    m = re.search(
        r'<div class="details lph-article-comView">(.*?)</div>\s*<!-- 文章 -->',
        html,
        re.S,
    )
    if not m:
        return html_to_text(html)
    inner = re.sub(r"<br\s*/?>", "\n", m.group(1), flags=re.I)
    inner = re.sub(r"</p>", "\n\n", inner, flags=re.I)
    inner = re.sub(r"<[^>]+>", "", inner)
    inner = unescape(inner)
    return re.sub(r"\n{3,}", "\n\n", inner).strip()


def fetch_playwright(url: str) -> tuple[str, str | None, str | None]:
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
        page.wait_for_timeout(10000)
        try:
            page.wait_for_selector("p", timeout=20000)
        except Exception:
            pass
        title = page.title()
        html = page.content()
        inner = page.inner_text("body")
        browser.close()
        return html, (title.strip() if title else None), inner


def resolve_body(article: dict, html: str, page_title: str | None) -> tuple[str, str]:
    url = article["url"]
    title = article["title"]
    if "china.com.cn" in url:
        body = extract_chinacom(html)
    elif "leiphone.com" in url:
        body = extract_leiphone(html)
    else:
        body = html_to_text(html)
    if len(body) < 100:
        raise RuntimeError(f"body too short ({len(body)} chars) for {url}")
    return title, body


def write_folder(article: dict, title: str, body: str) -> Path:
    folder = EXPORTS / article["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "title.txt").write_text(title + "\n", encoding="utf-8", newline="\n")
    content = article["sampling_id"].rstrip() + "\n\n---\n\n" + body.rstrip() + "\n"
    (folder / "body.md").write_text(content, encoding="utf-8", newline="\n")
    return folder


def append_registry(article: dict, issue_url: str) -> None:
    global ISSUE_NUM
    assert ISSUE_NUM is not None
    marker = f"## REGISTRY_XIAN_DAILY_{article['registry_key']}"
    text = REGISTRY.read_text(encoding="utf-8")
    if marker in text:
        return
    row = f"| #{ISSUE_NUM} | XIAN media sample archive · {article['slug']} | {issue_url} |"
    append = (
        f"\n\n---\n\n{marker}\n\n"
        f"**Posted:** 2026-09-11 · **Issue:** #{ISSUE_NUM} · **Batch:** #{BATCH_LABEL}\n\n"
        f"**Sampling identifier (verbatim):**\n\n```\n{article['sampling_id']}\n```\n\n"
        f"| Issue | Role | Link |\n|-------|------|------|\n{row}\n\n"
        f"Title file: `docs/issue-exports/{article['slug']}/title.txt`\n"
        f"Body file: `docs/issue-exports/{article['slug']}/body.md`\n"
        f"Source URL: {article['url']}\n"
    )
    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(append)


def prepend_changelog(article: dict, issue_url: str) -> None:
    global ISSUE_NUM
    assert ISSUE_NUM is not None
    block = (
        f"[2026-09-11] XIAN媒体采样归档 #{ISSUE_NUM} · Batch #{BATCH_LABEL} · {article['slug']}\n\n"
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
    title = f"[P1-Roadmap] 2026-09-11 XIAN媒体采样归档 #{BATCH_LABEL} · 九篇稿件闭环"
    body = (
        f"XIAN 媒体采样正文归档（九篇 · Batch #{BATCH_LABEL} · 2026-09-11）\n\n"
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
            f"in:title #{BATCH_LABEL} 九篇",
            "--json",
            "number,url",
            "--limit",
            "1",
        ],
        text=True,
        encoding="utf-8",
    ).strip()
    if out and out != "[]":
        import json

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


def append_dt188_ledger(issue_url: str) -> None:
    global ISSUE_NUM
    assert ISSUE_NUM is not None
    needle = f"Batch #{BATCH_LABEL}"
    text = ISSUE_LEDGER.read_text(encoding="utf-8")
    if needle in text:
        return
    line = (
        f"| #{ISSUE_NUM} | POSTED | Batch #{BATCH_LABEL} · 9篇媒体采样归档 2026-09-11 | "
        f"{issue_url} · 九篇见 docs/issue-exports/xian-daily-2026-09-11-* |"
    )
    anchor = "## 低优先级（P-Low）"
    if anchor not in text:
        ISSUE_LEDGER.write_text(text.rstrip() + "\n" + line + "\n", encoding="utf-8")
        return
    head, tail = text.split(anchor, 1)
    ISSUE_LEDGER.write_text(head.rstrip() + "\n" + line + "\n\n" + anchor + tail, encoding="utf-8")


def process_article(article: dict, issue_url: str, commit: bool) -> None:
    print(f"Fetching {article['slug']} ...")
    html, _page_title, _inner = fetch_playwright(article["url"])
    title, body = resolve_body(article, html, _page_title)
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
        print(f"  COMMIT {msg}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Single article slug")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--finalize-dt188", action="store_true", help="Append dt188 ledger after all 9")
    args = parser.parse_args()

    issue_url = ensure_issue()
    print(f"Issue #{ISSUE_NUM}: {issue_url}")

    if args.finalize_dt188:
        append_dt188_ledger(issue_url)
        if args.commit:
            subprocess.run(["git", "add", str(ISSUE_LEDGER.relative_to(ROOT))], cwd=ROOT, check=True)
            subprocess.run(
                ["git", "commit", "-m", f"docs(xian): dt188 ledger Batch #{BATCH_LABEL} Issue #{ISSUE_NUM}"],
                cwd=ROOT,
                check=True,
            )
        return 0

    items = ARTICLES
    if args.slug:
        items = [a for a in ARTICLES if a["slug"] == args.slug]
        if not items:
            print(f"unknown slug: {args.slug}", file=sys.stderr)
            return 1

    for article in items:
        process_article(article, issue_url, args.commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
