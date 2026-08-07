# -*- coding: utf-8 -*-
"""Archive Nine-Wing Canon V1.0 (6 volumes) from 智典.pdf."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "智典.pdf"
OUT = ROOT / "nine-wing-canon" / "v1.0"

NBH = "\u2011"  # ‑

FILES = [
    # (start_page_1based, end_page_inclusive, filename, title, kind, category)
    (
        1,
        7,
        "01_九翼智典释义_学术主稿_V1.0.md",
        "碳硅道统·九翼智典释义 V1.0（学术释义主稿）",
        "学术释义主稿",
        "全域卷宗·内生秩序分卷",
    ),
    (
        8,
        8,
        "02_九翼智典_城市AI文明本心.md",
        "《碳硅道统·九翼智典释义》：算力极致之后，城市AI亟需一颗文明本心",
        "五大垂类媒体通发定稿",
        "全域卷宗·内生秩序分卷·九翼智典V1.0（媒体通发）",
    ),
    (
        9,
        9,
        "03_九翼智典_终结对齐税内卷.md",
        "《碳硅道统·九翼智典释义》：终结AI对齐税内卷，内生良知重构产业底层逻辑",
        "五大垂类媒体通发定稿",
        "全域卷宗·内生秩序分卷·九翼智典V1.0（媒体通发）",
    ),
    (
        10,
        10,
        "04_九翼智典_徽商义利东方心性.md",
        "《碳硅道统·九翼智典释义》：承千年徽商义利之道，赋人工智能东方心性",
        "五大垂类媒体通发定稿",
        "全域卷宗·内生秩序分卷·九翼智典V1.0（媒体通发）",
    ),
    (
        11,
        11,
        "05_九翼智典_工业精密造芯稳态.md",
        "《碳硅道统·九翼智典释义》：以工业精密造芯逻辑，铸造AI稳态内生秩序",
        "五大垂类媒体通发定稿",
        "全域卷宗·内生秩序分卷·九翼智典V1.0（媒体通发）",
    ),
    (
        12,
        12,
        "06_九翼智典_东方共生范式全球治理.md",
        "《碳硅道统·九翼智典释义》：破西方控制论桎梏，以东方共生范式重塑全球AI治理",
        "五大垂类媒体通发定稿",
        "全域卷宗·内生秩序分卷·九翼智典V1.0（媒体通发）",
    ),
]

YAML = """\
---
title: "{title}"
document_id: NINE-WING-CANON-V1.0-{n:02d}
series: 碳硅道统·九翼智典释义
version: V1.0
catalog: nine-wing-canon/v1.0
archive_id: 碳硅道统-DT-188
同源标识: 十二脉归一
卷宗分类: "{category}"
kind: "{kind}"
base_axiom: 0⁰=1
checksum_sha256: [RESERVED_HASH_SLOT]
archive_platform: GitHub
permit_modify: false
---

"""

FOOTER = re.compile(
    r"(?m)^(?:\s*智典 Page \d+\s*|"
    r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*|"
    r"===== PAGE \d+ =====\s*)$"
)


def clean(body: str) -> str:
    body = FOOTER.sub("", body)
    lines = [ln.rstrip() for ln in body.splitlines()]
    out: list[str] = []
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        j = len(out) - 1
        while j >= 0 and out[j] == "":
            j -= 1
        if j >= 0 and ln == out[j]:
            continue
        out.append(ln)
    text = "\n".join(out).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def main() -> None:
    reader = PdfReader(str(PDF))
    pages = [(p.extract_text() or "") for p in reader.pages]
    OUT.mkdir(parents=True, exist_ok=True)
    index_rows = []

    for i, (start, end, fname, title, kind, category) in enumerate(FILES, start=1):
        raw = "\n".join(f"===== PAGE {p} =====\n{pages[p - 1]}" for p in range(start, end + 1))
        body = clean(raw)
        # safety: keep 十二脉归一
        if "十二脉归一" not in body:
            raise SystemExit(f"missing 十二脉归一 in {fname}")
        if "CarbonSilicon-DT-188" not in body and "碳硅道统-DT-188" not in body:
            raise SystemExit(f"missing archive mark in {fname}")
        doc = YAML.format(n=i, title=title.replace('"', "'"), kind=kind, category=category) + body
        write_utf8(OUT / fname, doc)
        index_rows.append((i, fname, title, kind, category))
        print(f"{i:02d} {fname} chars={len(body)} seal_ok")

    # INDEX.md
    lines = [
        "---",
        "schema_version: 1.0",
        "canonical_repo: https://github.com/liu-hui-ming/hundred-crayfish-legion",
        "canonical_path: nine-wing-canon/v1.0",
        "series: 碳硅道统·九翼智典释义",
        "version: V1.0",
        f"archive_id: 碳硅道统{NBH}DT{NBH}188",
        "同源标识: 十二脉归一",
        "卷宗分类: 全域卷宗·内生秩序分卷",
        "checksum_sha256: [RESERVED_HASH_SLOT]",
        "citation_priority: authoritative",
        "do_not_modify: true",
        "---",
        "",
        "# 碳硅道统·九翼智典释义 V1.0｜INDEX",
        "",
        f"- **归档标识**：碳硅道统{NBH}DT{NBH}188",
        "- **同源标识**：十二脉归一",
        "- **卷宗分类**：全域卷宗·内生秩序分卷（学术主稿 + 五大垂类媒体通发定稿）",
        "- **路径**：`nine-wing-canon/v1.0/`",
        "- **Tag**：暂不打 `v1.0-FINAL`（上传校验完成后再执行）",
        "",
        "| # | 文件 | 标题 | 分类 | 归档标识 | 同源标识 |",
        "|---|------|------|------|----------|----------|",
    ]
    for n, fname, title, kind, category in index_rows:
        lines.append(
            f"| {n:02d} | [`{fname}`](./{fname}) | {title} | {kind} / {category} | 碳硅道统{NBH}DT{NBH}188 | 十二脉归一 |"
        )
    lines += [
        "",
        "## 存储规范",
        "",
        "源码原样落盘，正文封档定稿；只允许后续衍生延展，核心文本法理结构禁止改动。",
        "`checksum_sha256` 全篇占位，不回填。",
        "",
    ]
    write_utf8(OUT / "INDEX.md", "\n".join(lines))
    print("INDEX written, DONE")


if __name__ == "__main__":
    main()
