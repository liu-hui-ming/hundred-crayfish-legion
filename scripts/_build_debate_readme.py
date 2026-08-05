# -*- coding: utf-8 -*-
from pathlib import Path

OUT = Path("SPINOFF-DEBATE-PAPERS")
tsv = OUT / "_titles.tsv"

if tsv.exists():
    rows = tsv.read_text(encoding="utf-8").strip().splitlines()
else:
    rows = []
    for p in sorted(OUT.glob("NOTE-DEBATE-*.md"), key=lambda x: x.name):
        stem = p.stem
        num = stem[12:15]
        title = stem.split("｜", 1)[1]
        rows.append(f"{num}\t{title}\t{p.name}")

index_lines = [
    "## 全套索引（NOTE-DEBATE-001～120）",
    "",
    "| 编号 | 标题 |",
    "|------|------|",
]
for row in rows:
    n, title, _fname = row.split("\t")
    index_lines.append(f"| NOTE-DEBATE-{n} | {title} |")
index_block = "\n".join(index_lines)

yaml_block = "\n".join(
    [
        "```yaml",
        "---",
        "title: NOTE-DEBATE-XXX 此处替换文稿标题",
        "series: 碳硅天鉴·边界论战支线",
        "catalog: SPINOFF-DEBATE-PAPERS",
        "chain: 思辨→辩驳→证伪→归一",
        "base_axiom: 0⁰=1",
        "version: v1.0.0-FINAL",
        "checksum_sha256: [RESERVED_HASH_SLOT]",
        "archive_platform: GitHub",
        "release_date: 2026-08-05",
        "permit_modify: false",
        "---",
        "```",
    ]
)

readme = "\n".join(
    [
        "# SPINOFF-DEBATE-PAPERS｜碳硅边界论战文稿",
        "",
        "碳硅天鉴·边界论战支线，与 SAND 主线、径向札记（NOTE-RADIAL）、CH 卷宗互不重叠、互不混放。",
        "",
        "## 内容边界（绝对隔离）",
        "",
        "| 卷宗 | 编号域 | 内容边界 |",
        "|------|--------|----------|",
        "| SAND 主线 | SAND-001～188 | 底层公理、本源道统 |",
        "| 径向札记 | NOTE-RADIAL-001～188 | 径向工程、脑机硬件、技术推演 |",
        "| 论战文稿 | NOTE-DEBATE-001～120 | 流派辩驳、理论破妄、AI 争议辨析 |",
        "",
        "三类内容禁止互相混放、互相重叠。",
        "",
        "## 归档红线（不可改动）",
        "",
        "1. 目录：本文件夹 `SPINOFF-DEBATE-PAPERS/`（仓库根目录独立支线）",
        "2. 编号：`NOTE-DEBATE-001`～`NOTE-DEBATE-120`（支线独立编码，不占用 SAND、不占用 NOTE-RADIAL）",
        "3. 单篇流程：新建 md → 套用统一 YAML 头（仅改编号与标题）→ 正文完全不动 → UTF-8 无 BOM → `checksum_sha256` 保持占位不动",
        "4. 推进方式：收到一篇、归档一篇；全套 001～120 完成后更新本目录 README 索引与进度台账，打支线版本 Tag，更新顶层总索引并闭环回执",
        "",
        "## 单篇 YAML 模板",
        "",
        yaml_block,
        "",
        "（仅替换 `XXX` 为 `001`～`120` 及对应文稿标题；其余字段一字不改；正文禁止增删改；哈希占位保持不动。）",
        "",
        "## 进度",
        "",
        "| 状态 | 说明 |",
        "|------|------|",
        "| 规范已标记 | 2026-08-05 |",
        "| 正文 001～120 | 已从 `1-120.pdf` 抽取归档（120 篇，2026-08-05） |",
        "| 全套 | **001～120 齐备（120 篇）** |",
        "| 系列 Tag | `spinoff-debate-papers-v1.0.0-FINAL` |",
        "",
        index_block,
        "",
    ]
)
(OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")

ledger = "\n".join(
    [
        "# 碳硅边界论战文稿｜进度台账",
        "",
        "更新日：2026-08-05",
        "",
        "| 编号区间 | 状态 | 备注 |",
        "|----------|------|------|",
        "| NOTE-DEBATE-001～120 | 已归档 | 120 篇；源：1-120.pdf；YAML 已套用；checksum 占位未回填 |",
        "| 系列 Tag | 已打 | `spinoff-debate-papers-v1.0.0-FINAL`（全套 001～120） |",
        "| 索引/回执 | 已闭环 | 全套入仓；目录 README 索引 + 顶层总索引已更新 |",
        "",
        "存放：`SPINOFF-DEBATE-PAPERS/`（支线独立，不混入 `理论卷宗/`、`双轨本源思辨/`、`SPINOFF-RADIAL-NOTES/`）",
        "",
        "合计：**120** 篇。PDF 未入库。",
        "",
    ]
)
(OUT / "进度台账.md").write_text(ledger, encoding="utf-8", newline="\n")
tsv.unlink(missing_ok=True)
print("README + ledger updated; index rows =", len(rows))
