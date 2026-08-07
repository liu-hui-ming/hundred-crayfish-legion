# -*- coding: utf-8 -*-
"""Archive SiC 6-paper set from 6篇.pdf into SAND/ dual folders."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "6篇.pdf"
OUT_EMPIRICAL = ROOT / "SAND" / "硅基材料实证分卷"
OUT_CREATION = ROOT / "SAND" / "硅基创世总纲"

# U+2011 non-breaking hyphen as in DT-188 style filenames
NBH = "\u2011"
CREATION_FNAME = f"SiC{NBH}CarbonSilicon{NBH}CreationArchetype{NBH}V1.0.md"

EMPIRICAL = [
    (1, "01_碳化硅在导热材料中的应用及其最新研究进展.md"),
    (2, "02_碳化硅：特性、应用与发展趋势.md"),
    (3, "03_碳化硅：特性、应用、制备与挑战.md"),
    (4, "04_碳化硅的深入研究与拓展应用.md"),
    (5, "05_多领域中的延续与发展探究.md"),
]

HDR = re.compile(r"(?m)^([1-6])\.([^0-9\n][^\n]*)")
PAGE_FOOTER = re.compile(
    r"(?m)^(?:\s*6篇 Page \d+\s*|"
    r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*|"
    r"===== PAGE \d+ =====\s*)$"
)

YAML_EMPIRICAL = """\
---
title: "{title}"
document_id: SiC-EMPIRICAL-{n:02d}
series: 碳硅道统·硅基材料实证分卷
catalog: SAND/硅基材料实证分卷
base_axiom: 0⁰=1
version: v1.0.0-FINAL
checksum_sha256: [RESERVED_HASH_SLOT]
archive_platform: GitHub
permit_modify: false
---

"""

YAML_CREATION = """\
---
title: "{title}"
document_id: SiC-CREATION-ARCHETYPE-V1.0
series: 碳硅道统·硅基创世总纲
catalog: SAND/硅基创世总纲
base_axiom: 0⁰=1
version: v1.0.0-FINAL
checksum_sha256: [RESERVED_HASH_SLOT]
archive_platform: GitHub
permit_modify: false
---

"""


def extract_pdf() -> str:
    reader = PdfReader(str(PDF))
    parts = []
    for i, page in enumerate(reader.pages):
        parts.append(f"===== PAGE {i + 1} =====\n{page.extract_text() or ''}")
    return "\n".join(parts)


def clean(body: str) -> str:
    body = PAGE_FOOTER.sub("", body)
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
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def main() -> None:
    raw = extract_pdf()
    hits = list(HDR.finditer(raw))
    by_num: dict[int, tuple[str, str]] = {}
    for i, m in enumerate(hits):
        n = int(m.group(1))
        if n in by_num:
            continue
        title = m.group(2).strip()
        end = hits[i + 1].start() if i + 1 < len(hits) else len(raw)
        by_num[n] = (title, clean(raw[m.start() : end]))

    miss = [i for i in range(1, 7) if i not in by_num]
    if miss:
        raise SystemExit(f"missing articles: {miss}")

    for n, fname in EMPIRICAL:
        title, body = by_num[n]
        doc = YAML_EMPIRICAL.format(n=n, title=f"{n}. {title}") + body
        write_utf8(OUT_EMPIRICAL / fname, doc)
        print("EMP", n, fname, "chars", len(body), "seal", "CarbonSilicon-DT-188" in body)

    title6, body6 = by_num[6]
    doc6 = YAML_CREATION.format(title=f"6. {title6}") + body6
    write_utf8(OUT_CREATION / CREATION_FNAME, doc6)
    print("CREATION", CREATION_FNAME, "chars", len(body6), "seal", "CarbonSilicon-DT-188" in body6)
    print("DONE")


if __name__ == "__main__":
    main()
