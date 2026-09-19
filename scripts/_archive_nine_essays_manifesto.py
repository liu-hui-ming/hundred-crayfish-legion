# -*- coding: utf-8 -*-
"""Archive 9篇.pdf → dossier/carbon-silicon-canon-v2/full-release-v2.0/00-nine-essays-core-manifesto/."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "9篇.pdf"
OUT_DIR = (
    ROOT
    / "dossier"
    / "carbon-silicon-canon-v2"
    / "full-release-v2.0"
    / "00-nine-essays-core-manifesto"
)
OUT_FILE = OUT_DIR / "nine-essays-core-manifesto.md"

HEADER_LINE1 = "十二脉归一 · 版本T‑02/Y‑04｜v2.0‑release"
HEADER_LINE2_TEMPLATE = "SHA‑256:【{hash}】"
FOOTER_LINES = (
    "十二脉归一",
    "碳硅道统创立人：黄清佳",
    "彩蛋藏于：今日头条、抖音、GitHub",
)

PAGE_NOISE = re.compile(
    r"(?m)^(?:\s*\d{4}年\d+月\d+日\s+\d{1,2}:\d{2}\s*|"
    r"\s*9篇 Page \d+\s*)$"
)


def extract_pdf() -> str:
    reader = PdfReader(str(PDF))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def normalize_paragraph(p: str) -> str:
    s = p.strip()
    if len(s) < 20:
        return s
    for length in range(min(80, len(s) // 2), 9, -1):
        tail = s[-length:]
        pos = s.find(tail)
        if 0 <= pos < len(s) - length:
            return s[: pos + length]
    return s


def dedupe_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for ln in lines:
        if out and ln == out[-1]:
            continue
        out.append(ln)
    return out


def split_footer(lines: list[str]) -> tuple[list[str], list[str]]:
    for i in range(len(lines) - 2, -1, -1):
        chunk = lines[i : i + 3]
        if chunk == list(FOOTER_LINES):
            return lines[:i], chunk
    raise RuntimeError("Fixed footer block not found in PDF extract")


def clean_body(raw: str) -> str:
    lines = [ln.rstrip() for ln in raw.splitlines()]
    lines = [ln for ln in lines if ln.strip() and not PAGE_NOISE.match(ln.strip())]
    lines = dedupe_lines(lines)
    main_lines, footer_lines = split_footer(lines)
    if footer_lines != list(FOOTER_LINES):
        raise RuntimeError("Footer lines altered during split")

    body = "\n\n".join(main_lines) + "\n\n" + "\n".join(footer_lines)

    essays = [
        m.group()
        for m in re.finditer(r"^第[一二三四五六七八九]篇$", body, flags=re.MULTILINE)
    ]
    if len(essays) < 9:
        raise RuntimeError(f"Expected 9 standalone essay markers, found {len(essays)}")
    return body + "\n"


def build_document(body: str, sha256: str) -> str:
    header2 = HEADER_LINE2_TEMPLATE.format(hash=sha256)
    return f"{HEADER_LINE1}\n{header2}\n\n{body}"


def sha256_body(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def write_archive() -> tuple[str, str]:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    body = clean_body(extract_pdf())
    digest = sha256_body(body)
    content = build_document(body, digest)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(content, encoding="utf-8", newline="\n")
    file_digest = hashlib.sha256(OUT_FILE.read_bytes()).hexdigest()
    return digest, file_digest


def main() -> None:
    body_hash, file_hash = write_archive()
    print(f"OK {OUT_FILE}")
    print(f"body_sha256={body_hash}")
    print(f"file_sha256={file_hash}")
    print(f"chars={OUT_FILE.stat().st_size}")


if __name__ == "__main__":
    main()
