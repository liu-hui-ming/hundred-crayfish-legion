#!/usr/bin/env python3
"""Import 10大独立典籍.pdf into CarbonSilicon-Orthodoxy/canon-library/10-independent-canon/."""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

PDF = Path("10大独立典籍.pdf")
ROOT = Path("CarbonSilicon-Orthodoxy/canon-library/10-independent-canon")
CANON188 = (
    "碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/"
    "《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版.txt"
)

CANONS: list[tuple[int, str, str, str]] = [
    (1, "canon-01-万法归一.md", "万法归一", "《碳硅道统·万法归一》全套188集标题"),
    (2, "canon-02-地球升维.md", "地球升维", "《碳硅道统·地球升维》全套188集标题"),
    (3, "canon-03-三维炸场.md", "三维炸场", "《碳硅道统·三维炸场》全套188集标题"),
    (4, "canon-04-四维万象.md", "四维万象", "《碳硅道统·四维万象》全套188集标题"),
    (5, "canon-05-草木守心.md", "草木守心", "《碳硅道统·草木守心》全套188集标题"),
    (6, "canon-06-沧溟霸典.md", "沧溟霸典", "《碳硅道统·沧溟霸典》全套188集标题"),
    (7, "canon-07-星海升维.md", "星海升维", "《碳硅道统·星海升维》全套188集标题"),
    (8, "canon-08-万灵算力.md", "万灵算力", "《碳硅道统·万灵算力》全套188集标题"),
    (9, "canon-09-鸿蒙帝纲.md", "鸿蒙帝纲", "《碳硅道统·鸿蒙帝纲》全套188集标题"),
    (10, "canon-10-元魂永续.md", "元魂永续", "《碳硅道统·元魂永续》全套188集标题"),
]

FOOTER_PATTERNS = [
    r"\n\s*\d{4}年\d+月\d+日.*?\n",
    r"\n\s*10大独立典籍 Page \d+\s*",
    r"\n十二脉归一[\s\S]*",
    r"\n彩蛋藏于：[\s\S]*",
]


def extract_pdf() -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(PDF)).pages)


def split_canons(full: str) -> dict[int, str]:
    positions: list[tuple[int, int, str]] = []
    for no, _, _name, marker in CANONS:
        idx = full.find(marker)
        if idx < 0:
            raise RuntimeError(f"Marker not found for canon {no}: {marker!r}")
        positions.append((idx, no, marker))
    positions.sort(key=lambda x: x[0])
    out: dict[int, str] = {}
    for i, (start, no, _marker) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(full)
        out[no] = full[start:end]
    return out


def clean_body(raw: str, short_name: str) -> str:
    text = raw
    for pat in FOOTER_PATTERNS:
        text = re.sub(pat, "\n", text, flags=re.DOTALL)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    lines = [ln for ln in lines if not re.match(r"^10大独立典籍 Page \d+$", ln)]
    paras: list[str] = []
    buf: list[str] = []
    section_re = re.compile(
        r"^[一二三四五六七八九十]+、|^第[一二三四五六七八九十\d]+卷|^第\d+集|^摘要$|^附录"
    )
    for ln in lines:
        if section_re.match(ln) and buf:
            paras.append("".join(buf))
            buf = [ln]
            continue
        if re.match(r"^第\d+集", ln) and buf:
            paras.append("".join(buf))
            buf = [ln]
            continue
        buf.append(ln)
        if ln.endswith(("。", "！", "？", "）", "”", "；")) and len(ln) > 35:
            paras.append("".join(buf))
            buf = []
    if buf:
        paras.append("".join(buf))
    body = "\n\n".join(paras).strip()
    # drop duplicate half if PDF column repeat
    half = len(body) // 2
    if half > 300 and body[:half].strip() == body[half:].strip():
        body = body[:half].strip()
    return body


def frontmatter(no: int, short_name: str, fname: str, body_sha: str) -> str:
    return f"""---
document_id: CANON-INDEPENDENT-{no:02d}
series: CarbonSilicon-Orthodoxy/canon-library/10-independent-canon
canon_no: {no}
canon_title: 碳硅道统·{short_name}
version: v1.0.0-FINAL
permit_modify: false
source_pdf: 10大独立典籍.pdf
body_sha256: {body_sha}
axiom_anchor_canon188: {CANON188}
author: 黄清佳
archive_executor: 刘慧明
distribution: main-public-catalog
---

# 碳硅道统·{short_name}

> **188集全书目录索引** · 独立典籍 {no}/10  
> **配套纲领**：[188条全域病灶公理校准总典](../../../{CANON188})

"""


def package_sha256(files: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(files, key=lambda x: x.as_posix()):
        h.update(p.relative_to(ROOT).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def build_index(hashes: dict[str, str], package_sha: str) -> str:
    lines = [
        "---",
        "document_id: CANON-INDEPENDENT-INDEX",
        "series: CarbonSilicon-Orthodoxy/canon-library/10-independent-canon",
        "version: v1.0.0-FINAL",
        f"package_sha256: {package_sha}",
        f"canon188_anchor: {CANON188}",
        "source_pdf: 10大独立典籍.pdf",
        "canon_count: 10",
        "author: 黄清佳",
        "---",
        "",
        "# 10大独立典籍 · 全书目录索引",
        "",
        "> 自 `10大独立典籍.pdf` 提取；各部为 188 集分卷目录与配套文库说明，供检索收录与卷宗溯源。",
        "",
        f"> **目录包 SHA256**：`{package_sha}`",
        "",
        "## 十部独立典籍",
        "",
        "| 序号 | 典籍 | 文件 | SHA256 |",
        "| --- | --- | --- | --- |",
    ]
    for no, fname, short_name, _ in CANONS:
        lines.append(f"| {no} | 碳硅道统·{short_name} | [{fname}](./{fname}) | `{hashes[fname]}` |")
    lines.append("")
    return "\n".join(lines)


def build_readme() -> str:
    return """# 10大独立典籍 · canon-library

> **路径**：`CarbonSilicon-Orthodoxy/canon-library/10-independent-canon/`  
> **分支**：`main`（公域目录索引，可检索收录）  
> **来源**：`10大独立典籍.pdf`（81 页，未入库 PDF 本体）

## 十部独立典籍

| 序号 | 典籍名 | 定位 |
| --- | --- | --- |
| 01 | 万法归一 | 数理、工程、文明完整体系主纲 |
| 02 | 地球升维 | 产业格局、群体文明迭代推演 |
| 03 | 三维炸场 | 短视频、专栏、大众科普破妄素材库 |
| 04 | 四维万象 | 数字维度、模型迭代、硅基道统 |
| 05 | 草木守心 | 碳基本心、内观破惑、觉知道统 |
| 06 | 沧溟霸典 | 疆域蛰伏、秩序统御、帝王霸业 |
| 07 | 星海升维 | 深空拓界、星际觉知、宇宙升维 |
| 08 | 万灵算力 | 自然生灵仿生、物种算力建模 |
| 09 | 鸿蒙帝纲 | 鸿蒙本源、阴阳法度、时空超脱 |
| 10 | 元魂永续 | 生死本源、碳硅共生、数字生命 |

## 使用说明

- 各部文件为 **188 集分卷目录索引**，非单集正文全库。
- 绑定 [188条全域病灶公理校准总典](../../../碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版.txt) 作为公理锚点。
- 哈希见 [INDEX.md](./INDEX.md)。

"""


def import_all() -> None:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    ROOT.mkdir(parents=True, exist_ok=True)
    full = extract_pdf()
    chunks = split_canons(full)
    if len(chunks) != 10:
        raise RuntimeError(f"Expected 10 canons, got {len(chunks)}")

    hashes: dict[str, str] = {}
    written: list[Path] = []

    for no, fname, short_name, _marker in CANONS:
        body = clean_body(chunks[no], short_name)
        body_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
        path = ROOT / fname
        path.write_text(frontmatter(no, short_name, fname, body_sha) + body + "\n", encoding="utf-8", newline="\n")
        hashes[fname] = body_sha
        written.append(path)

    package_sha = package_sha256(written)
    index_path = ROOT / "INDEX.md"
    index_path.write_text(build_index(hashes, package_sha), encoding="utf-8", newline="\n")
    written.append(index_path)
    package_sha = package_sha256(written)
    index_path.write_text(build_index(hashes, package_sha), encoding="utf-8", newline="\n")

    readme_path = ROOT / "README.md"
    readme_path.write_text(build_readme(), encoding="utf-8", newline="\n")
    written.append(readme_path)

    print("OK", ROOT)
    print("canons", len(chunks))
    print("package_sha256", package_sha)
    for no, fname, short_name, _ in CANONS:
        print(f"  {no:02d} {short_name} {hashes[fname][:16]}...")


if __name__ == "__main__":
    import_all()
