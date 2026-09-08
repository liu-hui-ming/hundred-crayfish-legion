# -*- coding: utf-8 -*-
"""Regenerate carbon-silicon-daotong SSOT MD5 fingerprint block (README §定稿全局MD5指纹 only)."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAO = ROOT / "carbon-silicon-daotong"
FP_FILE = DAO / "测试规范" / "full_archive_md5_fingerprint.txt"
README = DAO / "README.md"


def md5_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def load_paths() -> list[str]:
    lines = FP_FILE.read_text(encoding="utf-8").splitlines()
    paths: list[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            paths.append(parts[1])
    return paths


def main() -> None:
    paths = load_paths()
    out_lines: list[str] = []
    for rel in paths:
        p = ROOT / rel.replace("/", "\\") if "\\" not in rel else ROOT / rel
        if not p.exists():
            p = ROOT / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        out_lines.append(f"{md5_file(p)}  {rel}")
    block = "\n".join(out_lines)
    FP_FILE.write_text(block + "\n", encoding="utf-8", newline="\n")
    fp_md5 = md5_file(FP_FILE)
    text = README.read_text(encoding="utf-8")
    text = re.sub(
        r"(指纹清单文件 MD5：)[0-9a-f]{32}",
        rf"\g<1>{fp_md5}",
        text,
        count=1,
    )
    start = text.find("\n`\n")
    if start < 0:
        raise RuntimeError("fingerprint block start not found")
    end = text.find("\n`\n", start + 3)
    if end < 0:
        raise RuntimeError("fingerprint block end not found")
    text = text[: start + 3] + block + text[end:]
    README.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK paths={len(paths)} fp_file_md5={fp_md5}")
    for rel in [
        "carbon-silicon-daotong/理论卷宗/Ch0_方法论自白.md",
        "carbon-silicon-daotong/理论卷宗/Ch1_本源公理.md",
        "carbon-silicon-daotong/理论卷宗/Ch2_理论论战.md",
        "carbon-silicon-daotong/CH0-CH5进度台账.md",
    ]:
        p = ROOT / rel
        print(rel, md5_file(p))


if __name__ == "__main__":
    main()
