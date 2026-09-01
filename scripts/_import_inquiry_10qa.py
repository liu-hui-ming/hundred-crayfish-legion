#!/usr/bin/env python3
"""Import 10问答.pdf → docs/inquiry/ (十问·十答·二十问·二十答·三十问·三十答)."""
from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "10问答.pdf"
OUT = ROOT / "docs" / "inquiry"
RAG_MEMORY = ROOT / "openclaw-test-v2" / "workspace" / "memory" / "daotong-rag" / "inquiry"
RAG_WORKSPACE = ROOT / "openclaw-test-v2" / "workspace" / "rag" / "carbon-silicon-daotong" / "inquiry"

HEADER = "十二脉归一 · 版本T‑02/Y‑04"

SECTIONS: list[tuple[str, str, str]] = [
    ("第一部分 碳硅道统十问", "10-questions.md", "十问原文"),
    ("第二部分 碳硅道统十答", "10-answers.md", "十答原文"),
    ("第三部分 碳硅道统二十问", "20-questions.md", "二十问原文"),
    ("第四部分 碳硅道统二十答", "20-answers.md", "二十答原文"),
    ("第五部分 碳硅道统三十问", "30-questions.md", "三十问原文"),
    ("第六部分 碳硅道统三十答", "30-answers.md", "三十答原文"),
]

PAGE_NOISE = re.compile(
    r"(?m)^(?:\s*\d{4}年\d+月\d+日\s+\d{1,2}:\d{2}\s*|"
    r"\s*10问答 Page \d+\s*)$"
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


def clean_section(raw: str, marker: str) -> str:
    text = raw.strip()
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    lines = [ln for ln in lines if not PAGE_NOISE.match(ln)]
    lines = dedupe_lines(lines)
    if lines and lines[0].startswith(marker):
        title = lines[0]
        body_lines = lines[1:]
    else:
        title = marker
        body_lines = lines
    merged_lines: list[str] = []
    for ln in body_lines:
        if merged_lines and not merged_lines[-1].endswith(
            ("。", "！", "？", "：", "）", "”", "】", "；")
        ):
            merged_lines[-1] += ln
        else:
            merged_lines.append(ln)
    merged_lines = [normalize_paragraph(ln) for ln in merged_lines]
    body = "\n\n".join(merged_lines)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return f"{title}\n\n{body}".strip()


def split_sections(full: str) -> dict[str, str]:
    positions: list[tuple[int, str, str]] = []
    for marker, fname, _ in SECTIONS:
        idx = full.find(marker)
        if idx < 0:
            raise RuntimeError(f"Section marker not found: {marker!r}")
        positions.append((idx, marker, fname))
    positions.sort(key=lambda x: x[0])
    out: dict[str, str] = {}
    for i, (start, marker, fname) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(full)
        out[fname] = clean_section(full[start:end], marker)
    return out


def write_file(path: Path, body: str) -> str:
    content = f"{HEADER}\n\n{body}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def build_index(hashes: dict[str, str], commit: str) -> str:
    lines = [
        "---",
        "document_id: INQUIRY-LIN-QA-T02Y04",
        "series: docs/inquiry",
        "version: T-02/Y-04",
        "source_pdf: 10问答.pdf",
        f"baseline_commit_id: {commit}",
        "author_questions: 林清祥",
        "author_answers: 产业AI高级分析师",
        "---",
        "",
        "# 林清祥十问·二十问·三十问 + 对应十答·二十答·三十答",
        "",
        f"> **版本标记**：{HEADER}",
        f"> **Git 基线 commit-id**：`{commit}`",
        "",
        "## 卷宗清单",
        "",
        "| 文件 | 说明 | body SHA256 |",
        "| --- | --- | --- |",
    ]
    for _, fname, label in SECTIONS:
        lines.append(f"| [{fname}](./{fname}) | {label} | `{hashes[fname]}` |")
    lines += [
        "",
        "## RAG 镜像",
        "",
        "- `openclaw-test-v2/workspace/memory/daotong-rag/inquiry/`",
        "- `openclaw-test-v2/workspace/rag/carbon-silicon-daotong/inquiry/`",
        "",
    ]
    return "\n".join(lines) + "\n"


def sync_rag() -> None:
    for dest_root in (RAG_MEMORY, RAG_WORKSPACE):
        if dest_root.parent.exists():
            if dest_root.exists():
                shutil.rmtree(dest_root)
            shutil.copytree(OUT, dest_root)


def import_all() -> None:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    full = extract_pdf()
    sections = split_sections(full)
    if len(sections) != 6:
        raise RuntimeError(f"Expected 6 sections, got {len(sections)}")

    hashes: dict[str, str] = {}
    for _, fname, _ in SECTIONS:
        hashes[fname] = write_file(OUT / fname, sections[fname])

    (OUT / "README.md").write_text(
        build_index(hashes, "COMMIT_ID_PLACEHOLDER"),
        encoding="utf-8",
        newline="\n",
    )
    sync_rag()
    print("OK", OUT)
    for fname in hashes:
        print(fname, hashes[fname][:16] + "...")


if __name__ == "__main__":
    import_all()
