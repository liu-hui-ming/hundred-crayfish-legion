#!/usr/bin/env python3
"""Import 64.pdf content into dt-188-bifurcation case files."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path("dt-188-bifurcation")
PDF = Path("64.pdf")

CASE_START = re.compile(r"(BIF-\d{3}\s+[^\n]+)\n1\.\s*分岔核心诱因")

SECTION_HEADERS = [
    ("1.", "分岔核心诱因"),
    ("2.", "双路线具象落地路径"),
    ("3.", "碳硅联动十方万象分析"),
    ("4.", "认知盲区延伸推演"),
    ("5.", "落地优化解决方案"),
    ("6.", "拓扑与数理约束校验"),
    ("7.", "合规与伦理边界标注"),
    ("8.", "归档溯源哈希锚点"),
]


def slug_for_filename(title: str) -> str:
    return title.replace("/", "·")


def extract_pdf_text() -> str:
    reader = PdfReader(str(PDF))
    parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = re.sub(
            r"\n\s*\d{4}年\d+月\d+日.*?\n\s*64 Page \d+\s*",
            "",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(r"\n\s*64 Page \d+\s*", "", text)
        parts.append(text)
    return "\n".join(parts)


def split_cases(full: str) -> list[tuple[str, str, str]]:
    matches = list(CASE_START.finditer(full))
    cases: list[tuple[str, str, str]] = []
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        bif_id, title = header.split(" ", 1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full)
        body = full[start:end].strip()
        # drop duplicate header line
        body = re.sub(r"^" + re.escape(header) + r"\s*\n?", "", body).strip()
        cases.append((bif_id, title.strip(), body))
    return cases


def body_to_markdown(body: str) -> str:
    """Convert numbered sections to markdown ## headers."""
    out = body.strip()
    for num, name in SECTION_HEADERS:
        marker = f"{num} {name}"
        out = out.replace(marker, f"\n\n## {marker}\n", 1)
    return out.strip()


def find_target_file(bif_id: str, title: str) -> Path:
    slug = slug_for_filename(title)
    exact = ROOT / f"{bif_id}-具象分岔-{slug}.md"
    if exact.exists():
        return exact
    # fallback glob
    hits = sorted(ROOT.glob(f"{bif_id}-具象分岔-*.md"))
    if len(hits) == 1:
        return hits[0]
    raise FileNotFoundError(f"No target for {bif_id} {title}")


def build_document(bif_id: str, title: str, body_md: str) -> str:
    seq = int(bif_id.split("-")[1])
    full_title = f"碳硅道统·六十四分岔象·{bif_id}·{title}"
    slug = slug_for_filename(title)
    rel_path = f"dt-188-bifurcation/{bif_id}-具象分岔-{slug}.md"

    anchor_block = f"""卷宗归属：DT-188 六十四分岔推演层
仓库路径：/{rel_path}
体系溯源：碳硅道统·九元伦理量子·算力红线公律
全局索引编号：{bif_id}
版本封存标记：V1.0 基础定型版
checksum_sha256: [RESERVED_HASH_SLOT]"""

    if "## 8. 归档溯源哈希锚点" in body_md:
        body_md = re.sub(
            r"## 8\. 归档溯源哈希锚点\n.*",
            "## 8. 归档溯源哈希锚点\n\n" + anchor_block,
            body_md,
            flags=re.DOTALL,
        )
    else:
        body_md += "\n\n## 8. 归档溯源哈希锚点\n\n" + anchor_block

    doc_id = f"CS-DT-BIF-{seq:03d}-v1.0.0-FINAL"
    front = f"""---
document_id: "{doc_id}"
series: "dt-188-bifurcation"
catalog: "dt-188-bifurcation"
parent_rules: "碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则.md"
bifurcation_id: {bif_id}
bifurcation_label: "【推演虚拟分岔】"
status: final
version: v1.0.0-FINAL
checksum_sha256: [RESERVED_HASH_SLOT]
author: "黄清佳"
---

# {full_title}

"""
    return front + body_md + "\n"


def seal_checksum(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text.replace("[RESERVED_HASH_SLOT]", digest)


def main() -> None:
    full = extract_pdf_text()
    cases = split_cases(full)
    if len(cases) != 64:
        raise SystemExit(f"Expected 64 cases, got {len(cases)}")

    for bif_id, title, body in cases:
        body_md = body_to_markdown(body)
        doc = seal_checksum(build_document(bif_id, title, body_md))
        target = find_target_file(bif_id, title)
        target.write_text(doc, encoding="utf-8")
        print(f"OK {bif_id} -> {target.name} ({len(doc)} bytes)")

    print("DONE 64/64")


if __name__ == "__main__":
    main()
