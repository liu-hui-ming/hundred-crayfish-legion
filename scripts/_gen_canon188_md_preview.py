#!/usr/bin/env python3
"""Generate md preview copy from 188 canon txt (txt unchanged)."""
from __future__ import annotations

import hashlib
from pathlib import Path

TXT = Path(
    "碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/"
    "《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版.txt"
)
MD = TXT.with_suffix(".md")


def main() -> None:
    body_bytes = TXT.read_bytes()
    sha = hashlib.sha256(body_bytes).hexdigest()
    text = body_bytes.decode("utf-8")
    frontmatter = "\n".join(
        [
            "---",
            "document_id: CS-DT-CANON-188-PREVIEW-MD",
            "series: 内核典藏卷/全域终版法典",
            "format: github-preview-copy",
            f"source_txt: {TXT.name}",
            f"source_txt_sha256: {sha}",
            "version: 20260817-FINAL",
            "permit_modify: false",
            "author: 黄清佳",
            "license: CC-BY-NC-SA-4.0",
            'axiom_anchor: "0⁰=1"',
            "note: 本文件为 GitHub 网页预览副本；抗篡改真值正本为同目录 .txt，正文与 txt 逐字一致。",
            "---",
            "",
        ]
    )
    MD.write_text(frontmatter + text, encoding="utf-8", newline="\n")
    print("OK", MD)
    print("source_txt_sha256", sha)


if __name__ == "__main__":
    main()
