# -*- coding: utf-8 -*-
"""Extract NOTE 001-120 from 1-120.pdf into SPINOFF-DEBATE-PAPERS/ as NOTE-DEBATE-*.md."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "1-120.pdf"
CACHE = ROOT / "_extract_debate" / "full.txt"
OUT = ROOT / "SPINOFF-DEBATE-PAPERS"
START_N, END_N = 1, 120

YAML = """\
---
title: NOTE-DEBATE-{n:03d} {title}
series: 碳硅天鉴·边界论战支线
catalog: SPINOFF-DEBATE-PAPERS
chain: 思辨→辩驳→证伪→归一
base_axiom: 0⁰=1
version: v1.0.0-FINAL
checksum_sha256: [RESERVED_HASH_SLOT]
archive_platform: GitHub
release_date: 2026-08-05
permit_modify: false
---

"""

# PDF mixes NOTE-DEBATE-NNN｜ (early) and NOTE-NNN｜ (later)
HDR = re.compile(r"(?m)^NOTE-(?:DEBATE-)?(\d{1,3})｜([^\n]*)")
PAGE_FOOTER = re.compile(
    r"(?m)^(?:\s*1-120 Page \d+\s*|"
    r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*|"
    r"===== PAGE \d+ =====\s*)$"
)


def extract_pdf_text() -> str:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    if CACHE.exists() and CACHE.stat().st_mtime >= PDF.stat().st_mtime:
        return CACHE.read_text(encoding="utf-8")
    reader = PdfReader(str(PDF))
    parts: list[str] = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        parts.append(f"===== PAGE {i + 1} =====\n{t}")
    text = "\n".join(parts)
    CACHE.write_text(text, encoding="utf-8")
    return text


def clean(s: str) -> str:
    s = PAGE_FOOTER.sub("", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    lines = [ln.rstrip() for ln in s.splitlines()]
    out: list[str] = []
    for line in lines:
        if not line.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(line)
    dedup: list[str] = []
    for line in out:
        if dedup and line == dedup[-1] and line.strip():
            continue
        dedup.append(line)
    return "\n".join(dedup).strip() + "\n"


def main() -> None:
    text = extract_pdf_text()
    hits = [(int(m.group(1)), m.start(), m.group(2).strip()) for m in HDR.finditer(text)]
    starts: dict[int, int] = {}
    ends: dict[int, int] = {}
    titles: dict[int, str] = {}
    for i, (n, start, title) in enumerate(hits):
        if n < START_N or n > END_N:
            continue
        end = hits[i + 1][1] if i + 1 < len(hits) else len(text)
        if n in starts:
            continue
        starts[n] = start
        ends[n] = end
        titles[n] = title

    miss = [i for i in range(START_N, END_N + 1) if i not in starts]
    if miss:
        raise SystemExit(f"missing notes: {miss}")

    for p in OUT.glob("NOTE-DEBATE-*.md"):
        p.unlink()

    OUT.mkdir(parents=True, exist_ok=True)
    written: list[tuple[int, str, str]] = []
    for n in range(START_N, END_N + 1):
        title = titles[n]
        body = clean(text[starts[n] : ends[n]])
        doc = YAML.format(n=n, title=title) + body
        fname = f"NOTE-DEBATE-{n:03d}｜{title}.md"
        for ch in '<>:"/\\|?*':
            fname = fname.replace(ch, "＿")
        path = OUT / fname
        path.write_text(doc, encoding="utf-8", newline="\n")
        # ensure no BOM
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            path.write_bytes(raw[3:])
        written.append((n, title, path.name))
        print(f"{n:03d} chars={len(body):5d} {path.name[:70]}")

    # index sidecar for README rebuild
    idx = OUT / "_titles.tsv"
    idx.write_text(
        "\n".join(f"{n:03d}\t{title}\t{name}" for n, title, name in written) + "\n",
        encoding="utf-8",
    )
    print(f"DONE count={len(written)}")


if __name__ == "__main__":
    main()
