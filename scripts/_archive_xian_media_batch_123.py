# -*- coding: utf-8 -*-
"""Fetch media article text and scaffold XIAN #123 archive folders (7 articles)."""
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
ISSUE_NUM = 121  # GitHub assigned; user batch label #123 in sampling registry
BATCH_LABEL = 123

# ahnews.com.cn unreachable from archive env; body mirrors same-batch newfj syndication.
MIRROR_BODY_FROM: dict[str, str] = {
    "xian-daily-2026-09-10-ahnews-537412": "xian-daily-2026-09-10-newfj-115754",
    "xian-daily-2026-09-10-ahnews-537430": "xian-daily-2026-09-10-newfj-115755",
}

ARTICLES = [
    {
        "slug": "xian-daily-2026-09-10-chinanews-xj",
        "title": "碳硅道统：十维标尺的模型度量",
        "sampling_id": (
            "标题：碳硅道统：十维标尺的模型度量\n"
            "资源：中国新闻网新疆（全国）\n"
            "回链：http://www.xj.chinanews.com.cn/kejiao/2026-09-10/detail-ihfizwvu6757040.shtml"
        ),
        "url": "http://www.xj.chinanews.com.cn/kejiao/2026-09-10/detail-ihfizwvu6757040.shtml",
        "registry_key": "2026_09_10_MEDIA_CHINANEWS_XJ",
    },
    {
        "slug": "xian-daily-2026-09-10-leiphone",
        "title": "碳硅道统：中层拟合域的现实回响 |  标尺不动，事件自行抵达",
        "sampling_id": (
            "标题：碳硅道统：中层拟合域的现实回响 |  标尺不动，事件自行抵达\n"
            "媒体名称：雷峰网\n"
            "回链地址：https://m.leiphone.com/category/industrynews/qSK5aXslh1eHd6A3.html"
        ),
        "url": "https://m.leiphone.com/category/industrynews/qSK5aXslh1eHd6A3.html",
        "registry_key": "2026_09_10_MEDIA_LEIPHONE",
    },
    {
        "slug": "xian-daily-2026-09-10-hubeidaily",
        "title": None,
        "sampling_id": (
            "湖北日报客户端首发:https://news.hubeidaily.net/hbrbsharenew/news_detail/5/5958221/5376428/0"
            "?w=1789033579027&uik=bb7c872d&share_plat=android&sec=d40276b6&historyback=1"
        ),
        "url": (
            "https://news.hubeidaily.net/hbrbsharenew/news_detail/5/5958221/5376428/0"
            "?w=1789033579027&uik=bb7c872d&share_plat=android&sec=d40276b6&historyback=1"
        ),
        "registry_key": "2026_09_10_MEDIA_HUBEIDAILY",
    },
    {
        "slug": "xian-daily-2026-09-10-ahnews-537412",
        "title": "碳硅道统破局：算力堆不出真正智能，理性看待2026年AGI估值泡沫",
        "sampling_id": "12\t安徽日报客户端首发\thttps://web.ahnews.com.cn/news?id=537412",
        "url": "https://web.ahnews.com.cn/news?id=537412",
        "registry_key": "2026_09_10_MEDIA_AHNEWS_537412",
    },
    {
        "slug": "xian-daily-2026-09-10-newfj-115754",
        "title": "碳硅道统破局：算力堆不出真正智能，理性看待2026年AGI估值泡沫",
        "sampling_id": "13\t新福建网首发\thttp://www.newfj.com.cn/home/news/index/id/115754.html",
        "url": "http://www.newfj.com.cn/home/news/index/id/115754.html",
        "registry_key": "2026_09_10_MEDIA_NEWFJ_115754",
    },
    {
        "slug": "xian-daily-2026-09-10-ahnews-537430",
        "title": "碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径",
        "sampling_id": "12\t安徽日报客户端首发\thttps://web.ahnews.com.cn/news?id=537430",
        "url": "https://web.ahnews.com.cn/news?id=537430",
        "registry_key": "2026_09_10_MEDIA_AHNEWS_537430",
    },
    {
        "slug": "xian-daily-2026-09-10-newfj-115755",
        "title": "碳硅道统六问：物理仿真与大模型融合的六大工程卡点与破局路径",
        "sampling_id": "13\t新福建网首发\thttp://www.newfj.com.cn/home/news/index/id/115755.html",
        "url": "http://www.newfj.com.cn/home/news/index/id/115755.html",
        "registry_key": "2026_09_10_MEDIA_NEWFJ_115755",
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

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript"):
            self._skip = False
        if tag in ("p", "br", "div", "h1", "h2", "h3", "li") and not self._skip:
            self.parts.append("\n")

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
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_leiphone(html: str) -> str:
    m = re.search(r'<div class="details lph-article-comView">(.*?)</div>\s*<!-- 文章 -->', html, re.S)
    if not m:
        return html_to_text(html)
    inner = re.sub(r"<br\s*/?>", "\n", m.group(1), flags=re.I)
    inner = re.sub(r"</p>", "\n\n", inner, flags=re.I)
    inner = re.sub(r"<[^>]+>", "", inner)
    inner = unescape(inner)
    inner = re.sub(r"\n{3,}", "\n\n", inner)
    return inner.strip()


def extract_chinanews(html: str) -> str:
    m = re.search(r'<div class="left_zw">(.*)', html, re.S)
    if not m:
        return html_to_text(html)
    chunk = m.group(1)
    end = chunk.find("<!--正文end-->")
    if end > 0:
        chunk = chunk[:end]
    lines: list[str] = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S):
        t = re.sub(r"<[^>]+>", "", p)
        t = unescape(t).replace("\u3000", " ").strip()
        if t:
            lines.append(t)
    return "\n\n".join(lines)


def extract_hubeidaily(page_text: str) -> tuple[str, str]:
    lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
    skip = {
        "湖北日报客户端",
        "听新闻",
        "APP内打开",
        "打开",
        "还没有人评论过，快来抢首评吧！",
    }
    title = ""
    body_lines: list[str] = []
    for ln in lines:
        if ln in skip or ln.isdigit() and len(ln) <= 3:
            continue
        if ln == "评论":
            break
        if not title and "碳硅道统" in ln:
            title = ln
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}", ln):
            continue
        body_lines.append(ln)
    return title, "\n\n".join(body_lines)


def extract_newfj(page_text: str, fallback_title: str | None) -> tuple[str, str]:
    lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
    skip = {
        "新福建网",
        "网站首页",
        "登录",
        "注册",
        "手机版",
        "微信",
        "微博",
        "分享",
    }
    title = fallback_title or ""
    body_lines: list[str] = []
    started = False
    for ln in lines:
        if ln in skip:
            continue
        if not title and "碳硅道统" in ln:
            title = ln
            continue
        if title and re.match(r"^\d{4}-\d{2}-\d{2}", ln):
            continue
        if title and ln.startswith("来源"):
            continue
        if title:
            if ln.startswith("责任编辑") or ln in ("相关阅读", "上一篇", "下一篇"):
                break
            if len(ln) > 15 or started:
                started = True
                body_lines.append(ln)
    if not title:
        title = fallback_title or "UNKNOWN_TITLE"
    return title, "\n\n".join(body_lines)


def extract_generic_article(html: str) -> str:
    for pat in (
        r'<article[^>]*>(.*?)</article>',
        r'class="[^"]*article[^"]*content[^"]*"[^>]*>(.*?)</div>',
        r'class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ):
        m = re.search(pat, html, re.S | re.I)
        if m and len(m.group(1)) > 200:
            return html_to_text(m.group(1))
    return html_to_text(html)


def fetch_playwright(url: str) -> tuple[str, str | None, str | None]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
            extra_http_headers={"Referer": "http://www.newfj.com.cn/"},
        )
        page = context.new_page()
        if "newfj.com.cn" in url and "/home/news/" in url:
            page.goto("http://www.newfj.com.cn/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
        wait_until = "domcontentloaded" if "newfj.com.cn" in url else "domcontentloaded"
        page.goto(url, wait_until=wait_until, timeout=120000)
        page.wait_for_timeout(12000 if "newfj.com.cn" in url else 8000)
        try:
            page.wait_for_selector("p", timeout=20000)
        except Exception:
            pass
        title = page.title()
        html = page.content()
        inner = page.inner_text("body")
        browser.close()
        page_title = title.strip() if title else None
        return html, page_title, inner


class FetchBlocked(RuntimeError):
    pass


def fetch_article_content(article: dict) -> tuple[str, str]:
    url = article["url"]
    try:
        html, page_title, inner_text = fetch_playwright(url)
    except Exception as exc:
        mirror = MIRROR_BODY_FROM.get(article["slug"])
        if mirror:
            return load_mirrored_body(article, mirror)
        raise FetchBlocked(f"fetch failed for {url}: {exc}") from exc
    try:
        return resolve_body(article, html, page_title, inner_text)
    except RuntimeError:
        mirror = MIRROR_BODY_FROM.get(article["slug"])
        if mirror:
            return load_mirrored_body(article, mirror)
        raise


def load_mirrored_body(article: dict, mirror_slug: str) -> tuple[str, str]:
    mirror_body = EXPORTS / mirror_slug / "body.md"
    if not mirror_body.is_file():
        raise FetchBlocked(
            f"{article['slug']}: source URL unreachable; mirror {mirror_slug} not archived yet"
        )
    text = mirror_body.read_text(encoding="utf-8")
    if "\n---\n\n" not in text:
        raise FetchBlocked(f"mirror {mirror_slug} body.md missing separator")
    body = text.split("\n---\n\n", 1)[1].strip()
    title = article["title"] or (EXPORTS / mirror_slug / "title.txt").read_text(encoding="utf-8").strip()
    if len(body) < 100:
        raise FetchBlocked(f"mirror body too short for {article['slug']}")
    print(f"  MIRROR body from {mirror_slug} ({len(body)} chars)")
    return title, body


def load_body_from_file(path: Path, article: dict) -> tuple[str, str]:
    body = path.read_text(encoding="utf-8").strip()
    title = article["title"] or "UNKNOWN_TITLE"
    if len(body) < 100:
        raise RuntimeError(f"body file too short ({len(body)} chars)")
    return title, body


def resolve_body(article: dict, html: str, page_title: str | None, inner_text: str | None) -> tuple[str, str]:
    url = article["url"]
    title = article["title"] or page_title or "UNKNOWN_TITLE"
    if "chinanews.com.cn" in url:
        body = extract_chinanews(html)
    elif "leiphone.com" in url:
        body = extract_leiphone(html)
    elif "hubeidaily.net" in url and inner_text:
        t, body = extract_hubeidaily(inner_text)
        if t:
            title = t
    elif "newfj.com.cn" in url and inner_text:
        t, body = extract_newfj(inner_text, article["title"])
        if t:
            title = t
    else:
        body = extract_generic_article(html)
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
    marker = f"## REGISTRY_XIAN_DAILY_{article['registry_key']}"
    text = REGISTRY.read_text(encoding="utf-8")
    if marker in text:
        return
    row = (
        f"| #{ISSUE_NUM} | XIAN media sample archive · {article['slug']} | {issue_url} |"
    )
    append = (
        f"\n\n---\n\n{marker}\n\n"
        f"**Posted:** 2026-09-10 · **Issue:** #{ISSUE_NUM} · **Batch:** #123\n\n"
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
        f"[2026-09-10] XIAN媒体采样归档 #{ISSUE_NUM} · {article['slug']}\n\n"
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
    issue_url = f"https://github.com/{REPO}/issues/{ISSUE_NUM}"
    try:
        subprocess.run(
            ["gh", "issue", "view", str(ISSUE_NUM), "--repo", REPO],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return issue_url
    except subprocess.CalledProcessError:
        raise RuntimeError(f"GitHub issue #{ISSUE_NUM} not found; create it first")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Process single article slug")
    parser.add_argument("--fetch-only", action="store_true")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--body-from-file", type=Path, help="Use local body text when URL fetch blocked")
    args = parser.parse_args()

    items = ARTICLES
    if args.slug:
        items = [a for a in ARTICLES if a["slug"] == args.slug]
        if not items:
            print(f"unknown slug: {args.slug}", file=sys.stderr)
            return 1

    issue_url = ensure_issue()
    print(f"Issue: {issue_url}")

    for article in items:
        print(f"Fetching {article['slug']} ...")
        if args.body_from_file:
            title, body = load_body_from_file(args.body_from_file, article)
        else:
            title, body = fetch_article_content(article)
        folder = write_folder(article, title, body)
        print(f"  OK {folder} title={title[:40]}... body={len(body)} chars")

        if args.fetch_only:
            continue

        append_registry(article, issue_url)
        prepend_changelog(article, issue_url)

        if args.commit:
            rel = f"docs/issue-exports/{article['slug']}"
            subprocess.run(["git", "add", rel, str(REGISTRY.relative_to(ROOT)), str(CHANGELOG.relative_to(ROOT))], cwd=ROOT, check=True)
            msg = f"docs(xian): archive media #123 {article['slug']} + registry sync"
            subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True)
            print(f"  COMMIT {msg}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
