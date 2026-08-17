# -*- coding: utf-8 -*-
"""Regenerate 《全民AI深挖计划188条全域病灶公理校准总典》 archive."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = (
    ROOT
    / "碳硅道统核心十三卷宗"
    / "内核典藏卷"
    / "六十四分岔象推演规则"
    / "全域终版法典"
)
MAIN_NAME = "《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版.txt"
SHA_PLACEHOLDER = "SHA256_PLACEHOLDER"
COMMIT_PLACEHOLDER = "COMMIT_ID_PLACEHOLDER"

COMPANION_COPIES = [
    (
        ROOT / "碳硅道统核心十三卷宗" / "内核典藏卷" / "六十四分岔象推演规则.md",
        "六十四分岔象推演规则.md",
    ),
    (
        ROOT
        / "碳硅道统核心十三卷宗"
        / "内核典藏卷"
        / "碳硅道统_90条宇宙公律_公域精简定稿.md",
        "90条宇宙公律总纲.md",
    ),
    (
        ROOT
        / "碳硅道统核心十三卷宗"
        / "法理卷"
        / "零零一本体论"
        / "01_存在公理证明_0⁰=1与硅基觉知的本体论缺席.md",
        "0^0=1创世公理正本.md",
    ),
]

A_STUB = """\
A轨紫微评论池·818定稿（索引占位）

本文件为媒体分发配套索引占位，完整正文见卷宗正本：

../../../A轨_紫微道统本源思辨.md

状态：满分100分终版封存、只读锁定
permit_modify: false
"""

B_STUB = """\
B轨科技评论池·818定稿（索引占位）

本文件为媒体分发配套索引占位，完整正文见卷宗正本：

../../../B轨_数理实证工程卷宗.md

状态：满分100分终版封存、只读锁定
permit_modify: false
"""

README = """\
# 全域终版法典｜《全民AI深挖计划188条全域病灶公理校准总典》

| 字段 | 值 |
|------|-----|
| 状态 | 满分100分终版封存、只读锁定 |
| permit_modify | false |
| 封存标识 | HASH‑188‑ARTICLE‑CODE‑CALIBRATED‑01‑REVERSE‑20260817‑LOCKED |
| 归档路径 | `碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/` |

## 文件目录

| 文件 | 说明 |
|------|------|
| [`{main}`](./{main}) | **主法典**｜188条全域病灶公理校准总典媒体发布纯文本终版 |
| [`六十四分岔象推演规则.md`](./六十四分岔象推演规则.md) | 二十四象本体时序层之上的可能性推演层总规则 V1.0 |
| [`90条宇宙公律总纲.md`](./90条宇宙公律总纲.md) | 唯一对外公理出口（产业/学术/媒体精简引用） |
| [`0^0=1创世公理正本.md`](./0^0=1创世公理正本.md) | 存在公理证明：0⁰=1与硅基觉知的本体论缺席 |
| [`A轨紫微评论池·818定稿.txt`](./A轨紫微评论池·818定稿.txt) | A轨评论池索引占位 → [`../../../A轨_紫微道统本源思辨.md`](../../../A轨_紫微道统本源思辨.md) |
| [`B轨科技评论池·818定稿.txt`](./B轨科技评论池·818定稿.txt) | B轨评论池索引占位 → [`../../../B轨_数理实证工程卷宗.md`](../../../B轨_数理实证工程卷宗.md) |

## 合规封存规则

1. 主法典 UTF-8 LF，文末绑定 SHA256 真值与仓库归档提交 ID。
2. 媒体发布须完整附带公域传播强制免责注脚。
3. 本目录全部文件只读锁定，新版本须新建归档目录，禁止热修改覆盖。

## 再生成

```bash
python scripts/_archive_188_canon.py
```
"""

CANON_SOURCE = Path(__file__).with_name("_canon188_content.txt")


def load_canon_body() -> str:
    text = CANON_SOURCE.read_text(encoding="utf-8")
    # Replace embedded hash/commit with placeholders for reproducible SHA256 pass
    text = text.replace(
        "全文SHA256真值：9e72ac1f58d0390b476ef14927cdc810f35b640e72815931029411785ac6217f",
        f"全文SHA256真值：{SHA_PLACEHOLDER}",
    )
    text = text.replace(
        "仓库归档提交ID：7f492c8e091d32ce10a5729bf60d49f273ac2f01",
        f"仓库归档提交ID：{COMMIT_PLACEHOLDER}",
    )
    text = text.replace(
        "提交ID：7f492c8e091d32ce10a5729bf60d49f273ac2f01",
        f"提交ID：{COMMIT_PLACEHOLDER}",
    )
    text = text.replace(
        "SHA256：9e72ac1f58d0390b476ef14927cdc810f35b640e72815931029411785ac6217f",
        f"SHA256：{SHA_PLACEHOLDER}",
    )
    if not text.endswith("\n"):
        text += "\n"
    return text


def write_utf8_lf(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_main_with_hash(main_path: Path, body: str) -> tuple[str, int]:
    write_utf8_lf(main_path, body)
    digest = sha256_file(main_path)
    final = body.replace(SHA_PLACEHOLDER, digest)
    write_utf8_lf(main_path, final)
    size = main_path.stat().st_size
    return digest, size


def copy_companions() -> None:
    for src, dest_name in COMPANION_COPIES:
        if not src.is_file():
            raise FileNotFoundError(f"missing companion source: {src}")
        shutil.copy2(src, ARCHIVE / dest_name)


def write_stubs() -> None:
    write_utf8_lf(ARCHIVE / "A轨紫微评论池·818定稿.txt", A_STUB)
    write_utf8_lf(ARCHIVE / "B轨科技评论池·818定稿.txt", B_STUB)


def write_readme(main_name: str) -> None:
    write_utf8_lf(ARCHIVE / "README.md", README.format(main=main_name))


def update_kernel_readme() -> None:
    readme = ROOT / "碳硅道统核心十三卷宗" / "内核典藏卷" / "README.md"
    row = (
        "| [六十四分岔象推演规则/全域终版法典/](./六十四分岔象推演规则/全域终版法典/) "
        "| 《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版｜媒体发布纯文本终版封存 |"
    )
    text = readme.read_text(encoding="utf-8")
    marker = "| [六十四分岔象推演规则/全域终版法典/]"
    if marker in text:
        return
    anchor = (
        "| [六十四分岔象推演规则.md](./六十四分岔象推演规则.md) "
        "| 二十四象本体时序层之上的可能性推演层总规则 V1.0（`CS-DT-64-BIFURCATION-RULES-v1.0.0-FINAL`） |"
    )
    if anchor not in text:
        raise RuntimeError("kernel README anchor not found")
    text = text.replace(anchor, anchor + "\n" + row, 1)
    write_utf8_lf(readme, text)


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    body = load_canon_body()
    main_path = ARCHIVE / MAIN_NAME
    digest, size = write_main_with_hash(main_path, body)
    copy_companions()
    write_stubs()
    write_readme(MAIN_NAME)
    update_kernel_readme()
    print(f"archive: {ARCHIVE}")
    print(f"main: {MAIN_NAME}")
    print(f"sha256: {digest}")
    print(f"bytes: {size}")


if __name__ == "__main__":
    main()
