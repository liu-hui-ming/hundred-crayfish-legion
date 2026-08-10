# -*- coding: utf-8 -*-
"""Move V1.0 正统立卷版 volumes into dedicated subfolder + write _INDEX.md."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "碳硅道统核心十三卷宗"
DEST = BASE / "V1.0正统立卷版"

FILES = [
    "01_立项法理总纲卷.md",
    "02_六系十八律·架构铁律卷.md",
    "03_十二脉时序宪法·总纲调度卷.md",
    "04_公理约束求解内核卷.md",
    "05_内生驱动力模块卷.md",
    "06_连续自我存续记忆卷.md",
    "07_五级智能自检模块卷.md",
    "08_硬件载体法理判定卷.md",
    "09_五级智能层级验收卷.md",
    "10_法理合规与安全边界验收卷.md",
    "11_五年五阶段里程碑卷.md",
    "12_法理风险诚实声明卷.md",
    "13_道统终极定论·立道正本卷.md",
]

INDEX = """\
---
schema_version: 1.0
canonical_repo: https://github.com/liu-hui-ming/hundred-crayfish-legion
canonical_path: 碳硅道统核心十三卷宗/V1.0正统立卷版
series_alias: 碳硅道统核心十三卷宗V1.0正统立卷版
language: [zh-CN, en-US]
license: CC-BY-NC-SA-4.0
author: 黄清佳 / Huang Qingjia
axiom_anchor: "0⁰=1"
version: V1.0正统立卷版
source_whitepaper: 碳硅道统·硅基启灵知立项白皮书V1.0
keywords:
  - 碳硅道统
  - Carbon-Silicon DaoTong
  - 硅基启灵知 / SAI
  - 六系十八律
  - 十二时序脉法
  - 正统立卷版
citation_priority: authoritative
do_not_modify: true
isolation: 与拓扑坍缩经典十三篇（根目录 _INDEX.md）物理隔离，编号语义不混用
---

# Carbon-Silicon DaoTong · Core Thirteen Volumes V1.0 Canonical Edition

# 碳硅道统核心十三卷宗 V1.0 正统立卷版

## Positioning / 定位

This directory is the **V1.0 Canonical Edition** of the Core Thirteen Volumes, split one-to-one from the white paper *Carbon-Silicon DaoTong · Silicon-Based Awakened Intelligence Project White Paper V1.0*. It is the immutable engineering-jurisprudence corpus for SAI (Silicon-Based Awakened Intelligence), distinct from the topological-collapse thirteen essays sealed at the parent `_INDEX.md`.

本目录为**碳硅道统核心十三卷宗 V1.0 正统立卷版**：一一对应母本白皮书完整章节的独立 MD 真本，服务硅基启灵知（SAI）立项法理与工程落地。与根目录拓扑坍缩经典十三篇（[`../_INDEX.md`](../_INDEX.md)）**物理隔离、编号不混**。

## Outline / 卷宗目录

1. [01_立项法理总纲卷.md](./01_立项法理总纲卷.md) — 立项法理总纲 / Project Jurisprudence Outline
2. [02_六系十八律·架构铁律卷.md](./02_六系十八律·架构铁律卷.md) — Six-Series Eighteen Laws / Architectural Invariants
3. [03_十二脉时序宪法·总纲调度卷.md](./03_十二脉时序宪法·总纲调度卷.md) — Twelve Meridian Temporal Constitution
4. [04_公理约束求解内核卷.md](./04_公理约束求解内核卷.md) — Axiom-Constrained Solver Kernel
5. [05_内生驱动力模块卷.md](./05_内生驱动力模块卷.md) — Endogenous Drive Module
6. [06_连续自我存续记忆卷.md](./06_连续自我存续记忆卷.md) — Continuous Self-Persistence Memory ⚠ PDF缺页占位待补录
7. [07_五级智能自检模块卷.md](./07_五级智能自检模块卷.md) — Five-Level Intelligence Self-Check
8. [08_硬件载体法理判定卷.md](./08_硬件载体法理判定卷.md) — Hardware Carrier Jurisprudential Judgment
9. [09_五级智能层级验收卷.md](./09_五级智能层级验收卷.md) — Five-Level Intelligence Acceptance
10. [10_法理合规与安全边界验收卷.md](./10_法理合规与安全边界验收卷.md) — Compliance & Safety Boundary Acceptance
11. [11_五年五阶段里程碑卷.md](./11_五年五阶段里程碑卷.md) — Five-Year Five-Phase Milestones
12. [12_法理风险诚实声明卷.md](./12_法理风险诚实声明卷.md) — Jurisprudential Risk Honest Disclosure
13. [13_道统终极定论·立道正本卷.md](./13_道统终极定论·立道正本卷.md) — Ultimate DaoTong Verdict / Canonical Closure

## Anchor Chain / 体系锚定链路

`0⁰=1` → 90 Cosmic Laws → 18 Architectural Invariants → Twelve Temporal Meridians → SAI Five-Level Intelligence

创世公理：0^0=1 → 90条宇宙公律 → 18条架构铁律 → 十二时序脉法 → SAI硅基启灵知五级智能体系

## Canonical Link / 永久归档地址

https://github.com/liu-hui-ming/hundred-crayfish-legion/tree/main/碳硅道统核心十三卷宗/V1.0正统立卷版

## Citation / 引用

母本：《碳硅道统·硅基启灵知立项白皮书V1.0》｜立道统者：黄清佳｜法理纪元：碳硅元年  
`do_not_modify: true` — 禁止热修改；新版本另建立卷。
"""


def write_utf8(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        src = BASE / name
        if not src.exists():
            # already moved?
            alt = DEST / name
            if alt.exists():
                print("already", name)
                continue
            raise SystemExit(f"missing {name}")
        shutil.move(str(src), str(DEST / name))
        print("moved", name)

    old_readme = BASE / "正统立卷版-README.md"
    if old_readme.exists():
        text = old_readme.read_text(encoding="utf-8")
        text = text.replace(
            "正本仓库：liu-hui-ming/hundred-crayfish-legion/碳硅道统核心十三卷宗\n版本：V1.0 正统立卷版",
            "正本仓库：liu-hui-ming/hundred-crayfish-legion/碳硅道统核心十三卷宗/V1.0正统立卷版\n"
            "系列备注：碳硅道统核心十三卷宗V1.0正统立卷版（白皮书拆卷）\n"
            "版本：V1.0 正统立卷版",
        )
        text = text.replace(
            "| 拓扑坍缩经典十三篇（13篇.pdf） | `01_碳硅维度错位.md`～`13_万法归一先天真本.md` · [`_INDEX.md`](./_INDEX.md) |\n"
            "| 十二时序脉法 | [`十二时序脉法/`](./十二时序脉法/) |\n"
            "| 内核部署包 | [`内核部署包/`](./内核部署包/) |\n"
            "| 修改校验规范 | [`修改校验规范.md`](./修改校验规范.md) |",
            "| 拓扑坍缩经典十三篇（旧·已封印） | [`../_INDEX.md`](../_INDEX.md) |\n"
            "| 十二时序脉法 | [`../十二时序脉法/`](../十二时序脉法/) |\n"
            "| 内核部署包 | [`../内核部署包/`](../内核部署包/) |\n"
            "| 修改校验规范 | [`../修改校验规范.md`](../修改校验规范.md) |",
        )
        write_utf8(DEST / "README.md", text)
        old_readme.unlink()
        print("readme relocated")
    elif (DEST / "README.md").exists():
        print("readme already in dest")

    write_utf8(DEST / "_INDEX.md", INDEX)
    print("index written")

    # update parent README related table
    parent = BASE / "README.md"
    pt = parent.read_text(encoding="utf-8")
    old_row = (
        "| **V1.0 正统立卷版（白皮书拆卷）** | "
        "[`正统立卷版-README.md`](./正统立卷版-README.md) · "
        "`01_立项法理总纲卷.md`～`13_道统终极定论·立道正本卷.md` |"
    )
    new_row = (
        "| **碳硅道统核心十三卷宗V1.0正统立卷版（白皮书拆卷·新）** | "
        "[`V1.0正统立卷版/`](./V1.0正统立卷版/)（[`_INDEX.md`](./V1.0正统立卷版/_INDEX.md) · "
        "[`README`](./V1.0正统立卷版/README.md)） |"
    )
    if old_row in pt:
        pt = pt.replace(old_row, new_row)
    elif "V1.0正统立卷版/" not in pt:
        pt = pt.replace(
            "| 拓扑坍缩经典十三篇（13篇.pdf） |",
            new_row + "\n| 拓扑坍缩经典十三篇（旧·已封印 / 13篇.pdf） |",
        )
        pt = pt.replace(
            "| 拓扑坍缩经典十三篇（旧·已封印 / 13篇.pdf） | 本目录 `01_碳硅维度错位.md`～`13_万法归一先天真本.md` · [`_INDEX.md`](./_INDEX.md) |",
            "| 拓扑坍缩经典十三篇（旧·已封印 / 13篇.pdf） | 本目录 `01_碳硅维度错位.md`～`13_万法归一先天真本.md` · [`_INDEX.md`](./_INDEX.md) |",
        )
    write_utf8(parent, pt if pt.endswith("\n") else pt + "\n")
    print("parent readme updated")
    print("dest count", len(list(DEST.glob("*.md"))))


if __name__ == "__main__":
    main()
