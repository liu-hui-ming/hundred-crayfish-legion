# -*- coding: utf-8 -*-
"""Extract 13 core volumes from 13篇.pdf into 碳硅道统核心十三卷宗/."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "13篇.pdf"
OUT = ROOT / "碳硅道统核心十三卷宗"

# filename stem (without .md) -> expected leading number
FILES = [
    (1, "01_碳硅维度错位.md"),
    (2, "02_双流形拓扑不对等.md"),
    (3, "03_五阶坍缩真链.md"),
    (4, "04_五大基础禁律.md"),
    (5, "05_硅基术心退化解析.md"),
    (6, "06_九翼动态悬挂架构.md"),
    (7, "07_熵垒熔断双重兜底.md"),
    (8, "08_三元修法归一.md"),
    (9, "09_模块化法理缝隙短板.md"),
    (10, "10_七轮熔铸五大机制.md"),
    (11, "11_一体四相解析.md"),
    (12, "12_碳硅二元核心公理.md"),
    (13, "13_万法归一先天真本.md"),
]

HDR = re.compile(r"(?m)^(\d{2})\s+([^\n]+)")
PAGE_MARK = re.compile(r"(?m)^===== PAGE \d+ =====\s*$")
FOOTER = re.compile(
    r"(?m)^(?:\s*13篇 Page \d+\s*|"
    r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*)$"
)
# meta / chatter to strip
META_LOC = re.compile(r"(?m)^本篇定位[：:].*(?:\n(?![摘要正文\d一二三四五六七八九十]).*)*")
NEXT_TEASE = re.compile(
    r"(?m)^(?:本篇完整拆解[^\n]*\n)?(?:下一篇将[^\n]*\n?)+"
)


def extract_text() -> str:
    reader = PdfReader(str(PDF))
    parts = []
    for i, page in enumerate(reader.pages):
        parts.append(f"===== PAGE {i + 1} =====\n{page.extract_text() or ''}")
    return "\n".join(parts)


def clean(body: str) -> str:
    body = PAGE_MARK.sub("", body)
    body = FOOTER.sub("", body)
    lines = [ln.rstrip() for ln in body.splitlines()]
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("本篇定位"):
            i += 1
            while i < len(lines):
                cur = lines[i].strip()
                if not cur:
                    break
                if cur.startswith(("摘要", "正文", "一、", "二、", "三、", "四、", "五、")):
                    break
                if re.match(r"^\d{2}\s+", cur):
                    break
                i += 1
            continue
        if ln.startswith("下一篇将") or ln.startswith("本篇完整拆解"):
            i += 1
            continue
        out.append(ln)
        i += 1

    # drop blank-separated duplicate lines (page overlap)
    cleaned: list[str] = []
    for ln in out:
        if not ln.strip():
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        j = len(cleaned) - 1
        while j >= 0 and cleaned[j] == "":
            j -= 1
        if j >= 0 and ln == cleaned[j]:
            continue
        cleaned.append(ln)

    # drop truncated orphan prefixes left by page splits
    final: list[str] = []
    for idx, ln in enumerate(cleaned):
        if not ln.strip():
            if final and final[-1] != "":
                final.append("")
            continue
        nxt = ""
        for k in range(idx + 1, len(cleaned)):
            if cleaned[k].strip():
                nxt = cleaned[k]
                break
        # orphan stump: "……构建虚" then next full para also contains that stump as prefix fragment
        if nxt and (nxt.startswith(ln) or ln in nxt) and len(nxt) > len(ln) + 5:
            # only drop short orphans (page-break stumps), not real short lines
            if len(ln) < 40 and not ln.endswith(("。", "！", "？", "：", "；")):
                continue
        final.append(ln)

    text = "\n".join(final).strip() + "\n"
    # strip trailing / inline 下一篇 tease sentences
    text = re.sub(r"[^。\n]*下一篇将[^。\n]*。?", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # careful soft-join across page wraps (do not glue section titles)
    heading = re.compile(
        r"^(摘要|正文|禁律|定论|[一二三四五六七八九十]+、|\d+阶|\d+[\.、．]|[0-9]{2}\s)"
    )
    lines3 = text.splitlines()
    joined: list[str] = []
    for ln in lines3:
        if not ln.strip():
            if joined and joined[-1] != "":
                joined.append("")
            continue
        # look back past blanks
        j = len(joined) - 1
        while j >= 0 and joined[j] == "":
            j -= 1
        prev = joined[j] if j >= 0 else ""
        can_join = (
            prev
            and not prev.endswith(("。", "！", "？", "：", "；", "）", ")", "…", "——"))
            and not heading.match(ln)
            and not ("：" in prev and len(prev) <= 48)
        )
        if can_join:
            # remove trailing blanks then glue
            while joined and joined[-1] == "":
                joined.pop()
            joined[-1] = prev + ln
        else:
            joined.append(ln)
    text = "\n".join(joined).strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> None:
    raw = extract_text()
    hits = list(HDR.finditer(raw))
    by_num: dict[int, str] = {}
    titles: dict[int, str] = {}
    for i, m in enumerate(hits):
        n = int(m.group(1))
        if n in by_num:
            continue
        end = hits[i + 1].start() if i + 1 < len(hits) else len(raw)
        by_num[n] = raw[m.start() : end]
        titles[n] = m.group(2).strip()

    miss = [n for n, _ in FILES if n not in by_num]
    if miss:
        raise SystemExit(f"missing chapters: {miss}")

    OUT.mkdir(parents=True, exist_ok=True)
    for n, fname in FILES:
        body = clean(by_num[n])
        path = OUT / fname
        path.write_text(body, encoding="utf-8", newline="\n")
        raw_bytes = path.read_bytes()
        if raw_bytes.startswith(b"\xef\xbb\xbf"):
            path.write_bytes(raw_bytes[3:])
        print(f"{n:02d} chars={len(body):5d} title={titles[n][:40]} -> {fname}")

    # refresh README status
    readme = OUT / "README.md"
    base = readme.read_text(encoding="utf-8")
    if "正文按序下发后逐篇覆盖入库" in base:
        base = base.replace(
            "正文按序下发后逐篇覆盖入库。",
            "正文已自 `13篇.pdf` 抽取入库（纯正文；已剔除页脚与本篇定位批注）。",
        )
        readme.write_text(base, encoding="utf-8", newline="\n")
    print("DONE")


if __name__ == "__main__":
    main()
