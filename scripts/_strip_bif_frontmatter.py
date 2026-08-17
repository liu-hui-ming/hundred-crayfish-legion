#!/usr/bin/env python3
"""Strip YAML frontmatter for GitHub blob preview compatibility."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path("dt-188-bifurcation")
REPO = "https://github.com/liu-hui-ming/hundred-crayfish-legion/blob/main"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return text


def main() -> None:
    rows: list[str] = []
    for path in sorted(ROOT.glob("BIF-*.md")):
        sid = path.stem  # BIF-001
        body = strip_frontmatter(path.read_text(encoding="utf-8"))
        # ensure section 8 path is correct
        body = re.sub(
            r"仓库路径：/.*",
            f"仓库路径：/dt-188-bifurcation/{path.name}",
            body,
        )
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        body = re.sub(
            r"checksum_sha256: [a-f0-9]{64}",
            f"checksum_sha256: {digest}",
            body,
        )
        header = (
            f"<!-- document: {sid} | checksum_sha256: {digest} -->\n\n"
        )
        out = header + body.strip() + "\n"
        path.write_text(out, encoding="utf-8", newline="\n")
        blob = f"{REPO}/dt-188-bifurcation/{path.name}"
        raw = (
            f"https://raw.githubusercontent.com/liu-hui-ming/"
            f"hundred-crayfish-legion/main/dt-188-bifurcation/{path.name}"
        )
        title_match = re.search(r"^# (.+)$", body, re.MULTILINE)
        title = title_match.group(1) if title_match else sid
        short_title = title.split("·")[-1] if "·" in title else title
        rows.append(
            f"| {sid.replace('BIF-', '')} | {sid} | "
            f"[预览]({blob}) | [原文]({raw}) | {short_title} |"
        )
        print("OK", path.name)

    index = f"""# dt-188-bifurcation · 六十四分岔 INDEX

> **重要**：旧链接（含中文长文件名）已作废。请使用 `BIF-001.md` … `BIF-064.md`。
> 若 GitHub 预览报错，请点 **原文** 列（raw 直链，100% 可打开）。

| 序号 | ID | GitHub预览 | 原文(raw) | 子标题 |
| --- | --- | --- | --- | --- |
""" + "\n".join(rows) + "\n"

    (ROOT / "INDEX.md").write_text(index, encoding="utf-8", newline="\n")
    (ROOT / "README.md").write_text(
        f"""# dt-188-bifurcation

六十四分岔案例集 · 64/64 定稿

## 正确打开方式

1. [INDEX.md](./INDEX.md) — 全部链接
2. [BIF-001.md 预览]({REPO}/dt-188-bifurcation/BIF-001.md)
3. [BIF-001.md 原文(raw)](https://raw.githubusercontent.com/liu-hui-ming/hundred-crayfish-legion/main/dt-188-bifurcation/BIF-001.md) ← 预览失败时用此链接

**勿再使用** 含 `具象分岔-碳基…` 等中文长文件名的旧 URL，该路径已删除。
""",
        encoding="utf-8",
        newline="\n",
    )
    print("DONE")


if __name__ == "__main__":
    main()
