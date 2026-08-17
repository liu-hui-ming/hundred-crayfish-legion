#!/usr/bin/env python3
"""Fix bifurcation markdown: YAML quoting, paragraph reflow, reseal checksum."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path("dt-188-bifurcation")

CONTINUATION_START = re.compile(
    r"^(路线[AB]|方案\d+|盲区\d+|硅基延伸|具象表现|适用场景|算力消耗|核心临界|"
    r"\d+\.|#{1,3}\s|\*\*|[-*]|卷宗归属|仓库路径|体系溯源|全局索引|版本封存|checksum)"
)


def quote_yaml_value(value: str) -> str:
    if not value:
        return '""'
    if value.startswith('"') and value.endswith('"'):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def fix_frontmatter(fm: str) -> str:
    lines: list[str] = []
    quote_keys = {
        "parent_rules",
        "bifurcation_label",
        "author",
        "catalog",
        "series",
        "document_id",
        "source_pdf",
    }
    for line in fm.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            lines.append(line)
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if key in quote_keys and val and not (val.startswith('"') and val.endswith('"')):
            lines.append(f"{key}: {quote_yaml_value(val)}")
        else:
            lines.append(line)
    return "\n".join(lines)


def reflow_section(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    buf = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buf:
                out.append(buf)
                buf = ""
            out.append("")
            continue
        if not buf:
            buf = stripped
            continue
        if CONTINUATION_START.match(stripped):
            out.append(buf)
            buf = stripped
            continue
        if re.search(r"[。！？；：]$", buf) or re.search(r"[.!?;:]$", buf):
            out.append(buf)
            buf = stripped
        else:
            buf += stripped
    if buf:
        out.append(buf)
    return "\n".join(out)


def reflow_body(body: str) -> str:
    parts = re.split(r"(^## .+$)", body, flags=re.MULTILINE)
    if len(parts) == 1:
        return reflow_section(body)
    rebuilt: list[str] = []
    for i, part in enumerate(parts):
        if part.startswith("## "):
            rebuilt.append(part)
        else:
            rebuilt.append(reflow_section(part))
    return "".join(rebuilt).strip() + "\n"


def reseal(text: str) -> str:
    text = re.sub(r"checksum_sha256: [a-f0-9]{64}", "checksum_sha256: [RESERVED_HASH_SLOT]", text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text.replace("[RESERVED_HASH_SLOT]", digest)


def process_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return
    _, fm, body = raw.split("---", 2)
    fm = fix_frontmatter(fm.strip("\n"))
    body = body.lstrip("\n")
    body = reflow_body(body)
    doc = f"---\n{fm}\n---\n\n{body}"
    if not doc.endswith("\n"):
        doc += "\n"
    doc = reseal(doc)
    path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> None:
    files = sorted(ROOT.glob("BIF-*.md"))
    for p in files:
        process_file(p)
        print("fixed", p.name)
    print(f"DONE {len(files)} files")


if __name__ == "__main__":
    main()
