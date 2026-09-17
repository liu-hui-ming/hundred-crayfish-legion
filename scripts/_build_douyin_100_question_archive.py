#!/usr/bin/env python3
"""Build content/comment-pool/douyin-100-question-series from _tmp_100pdf.txt (100.pdf extract)."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "_tmp_100pdf.txt"
OUT = REPO / "content" / "comment-pool" / "douyin-100-question-series"
MAIN_MD = OUT / "carbon-silicon-100-questions-douyin.md"
PREFIX = "【碳硅道统】@抖音求真 @豆包"
SAMPLING_ID = "20260917-douyin-100-question-series-carbon-silicon"


def is_noise(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if re.match(r"^\d{4}年\d+月\d+日", s):
        return True
    if "Nouvelle section" in s:
        return True
    return False


def parse_entries(text: str) -> dict[int, list[str]]:
    lines = text.splitlines()
    entries: dict[int, list[str]] = {}
    i = 0
    while i < len(lines):
        raw = lines[i].strip()
        if not re.fullmatch(r"\d+", raw):
            i += 1
            continue
        num = int(raw)
        if num < 1 or num > 100:
            i += 1
            continue
        i += 1
        while i < len(lines) and is_noise(lines[i]):
            i += 1
        if i >= len(lines) or lines[i].strip() != PREFIX:
            continue
        i += 1
        subs: list[str] = []
        seen_sub: set[int] = set()
        while i < len(lines):
            if is_noise(lines[i]):
                i += 1
                continue
            peek = lines[i].strip()
            if peek == PREFIX:
                i += 1
                continue
            if re.fullmatch(r"\d+", peek):
                nxt = i + 1
                while nxt < len(lines) and is_noise(lines[nxt]):
                    nxt += 1
                if nxt < len(lines) and lines[nxt].strip() == PREFIX:
                    break
            m = re.match(r"^(\d+)\.\s", peek)
            if m:
                sub_n = int(m.group(1))
                if sub_n in seen_sub:
                    i += 1
                    continue
                seen_sub.add(sub_n)
                subs.append(lines[i].rstrip())
                i += 1
                if len(subs) >= 7 and sub_n == 6:
                    break
                continue
            i += 1
        if subs:
            entries[num] = subs
    return entries


def format_block(num: int, subs: list[str]) -> str:
    parts = [str(num), PREFIX, *subs]
    return "\n".join(parts)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_utf8_no_bom(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"missing source: {SRC}")
    text = SRC.read_text(encoding="utf-8")
    entries = parse_entries(text)
    missing = [n for n in range(1, 101) if n not in entries]
    if missing:
        raise SystemExit(f"missing entries: {missing[:20]}... total {len(missing)}")
    bad = [n for n, subs in entries.items() if len(subs) != 7]
    if bad:
        raise SystemExit(f"bad sub counts: {[(n, len(entries[n])) for n in sorted(bad)[:10]]}")

    blocks = [format_block(n, entries[n]) for n in range(1, 101)]
    main_body = "\n".join(blocks) + "\n"
    write_utf8_no_bom(MAIN_MD, main_body)

    items_dir = OUT / "items"
    for n in range(1, 101):
        item_body = PREFIX + "\n" + "\n".join(entries[n]) + "\n"
        write_utf8_no_bom(items_dir / f"q-{n:03d}.md", item_body)

    md_hash = sha256_file(MAIN_MD)
    manifest = {
        "schema": "content/comment-pool/douyin-100-question-series/manifest.v1",
        "document_title": "碳硅道统 抖音100条链式质询评论集",
        "material_type": "抖音舆论质询文案",
        "total_entries": 100,
        "sampling_id": SAMPLING_ID,
        "source_pdf": "100.pdf",
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tags": [
            "carbon-silicon-doctrine",
            "comment",
            "red-blue-challenge",
            "douyin",
        ],
        "markdown": {
            "path": "carbon-silicon-100-questions-douyin.md",
            "sha256": md_hash,
        },
        "items_dir": "items/",
        "item_files": [f"q-{n:03d}.md" for n in range(1, 101)],
        "encoding": "UTF-8 without BOM",
        "remote_push": "frozen_until_explicit_instruction",
    }
    write_utf8_no_bom(
        OUT / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

    readme = f"""# 碳硅道统 · 抖音100条链式质询评论集

## 定位

红蓝对抗链式质询库，用于抖音评论投放。

## 目录

| 文件 | 说明 |
|------|------|
| [`carbon-silicon-100-questions-douyin.md`](carbon-silicon-100-questions-douyin.md) | 100条完整原文（序号 + 前缀 + 0–6 子问） |
| [`manifest.json`](manifest.json) | 元数据与主文档 SHA256 |
| [`items/`](items/) | 单条拆分 `q-001.md` … `q-100.md` |

## 标签

`carbon-silicon-doctrine`, `comment`, `red-blue-challenge`, `douyin`

## 校验

- 采样标识：`{SAMPLING_ID}`
- 主文档 SHA256：`{md_hash}`

## 分支管控

素材已提交本地分支；远端只读冻结，无明确推送指令不得同步远程。
"""
    write_utf8_no_bom(OUT / "README.md", readme)

    print(f"OK entries={len(entries)} main_sha256={md_hash}")
    print(f"OUT={OUT}")


if __name__ == "__main__":
    main()
