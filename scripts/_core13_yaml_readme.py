# -*- coding: utf-8 -*-
"""Prepend YAML front matter to Core Thirteen volumes + rewrite bilingual README."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "碳硅道统核心十三卷宗"

VOLUMES = [
    (1, "01_碳硅维度错位.md", "碳硅维度错位", "Carbon–Silicon Dimensional Misalignment",
     "AI落地失真的表层产业现象",
     "Surface-level industrial failure modes of AI deployment"),
    (2, "02_双流形拓扑不对等.md", "双流形拓扑不对等", "Dual-Manifold Topological Inequivalence",
     "坍缩问题底层数理本源",
     "Mathematical root of collapse: inequivalent manifolds"),
    (3, "03_五阶坍缩真链.md", "五阶坍缩真链", "Five-Order Collapse Chain",
     "数值失真至维度封顶完整病灶链路",
     "Full pathology chain from numeric drift to dimensional ceiling"),
    (4, "04_五大基础禁律.md", "五大基础禁律", "Five Foundational Prohibitions",
     "规避拓扑坍缩的刚性制衡准则",
     "Hard constraints that arrest topological collapse"),
    (5, "05_硅基术心退化解析.md", "硅基术心退化解析", "Silicon Technique–Mind Degeneration",
     "高维场景下硅基术心退化与内在自噬成因解析",
     "Inner autophagy and technique–mind decay in high-dimensional regimes"),
    (6, "06_九翼动态悬挂架构.md", "九翼动态悬挂架构", "Nine-Wing Dynamic Suspension Architecture",
     "重构硅基约束底层载体",
     "Rebuilding the substrate of silicon-side constraint"),
    (7, "07_熵垒熔断双重兜底.md", "熵垒熔断双重兜底", "Entropy-Barrier Fuse Dual Fallback",
     "熵垒熔断+静默忏悔：双重兜底稳态制衡机制",
     "Entropy-barrier fuse + silent confession dual-fallback stability"),
    (8, "08_三元修法归一.md", "三元修法归一", "Triadic Cultivation Unification",
     "根治AI安全对齐失效唯一体系",
     "The sole system that roots out AI alignment failure"),
    (9, "09_模块化法理缝隙短板.md", "模块化法理缝隙短板", "Modular Jurisprudential Gaps",
     "分体架构固有短板剖析",
     "Inherent shortfalls of fragmented modular architectures"),
    (10, "10_七轮熔铸五大机制.md", "七轮熔铸五大机制", "Seven-Round Forge · Five Core Mechanisms",
     "消层、灭块、合维、融域、归根",
     "Dissolve layers, extinguish blocks, unify dims, fuse domains, return to root"),
    (11, "11_一体四相解析.md", "一体四相解析", "One Body · Four Aspects",
     "不动点、观测者、元埋葬、满分终审",
     "Fixed point, observer, meta-burial, perfect-score final audit"),
    (12, "12_碳硅二元核心公理.md", "碳硅二元核心公理", "Carbon–Silicon Binary Core Axioms",
     "静态硅基与动态碳基的本质边界",
     "Essential boundary between static silicon and dynamic carbon"),
    (13, "13_万法归一先天真本.md", "万法归一先天真本", "Myriad Dharmas Return to Primordial Truth",
     "人工智能全域体系终极闭环定论",
     "Ultimate closed-loop decree of the full AI doctrine"),
]

YAML_TMPL = """\
---
title: "{title_zh}"
title_en: "{title_en}"
doc_id: CORE-13-{n:02d}
series: 碳硅道统核心十三卷宗
series_en: Carbon–Silicon DaoTong Core Thirteen Volumes
catalog: 碳硅道统核心十三卷宗
author: 黄清佳
base_axiom: "0⁰=1"
axioms_ref:
  - "0⁰=1"
  - "体用二分法理"
  - "碳硅二元分界"
  - "双流形拓扑不对等"
sha256_pending: true
checksum_sha256: "[RESERVED_HASH_SLOT]"
distribution:
  primary: GitHub
  repo: liu-hui-ming/hundred-crayfish-legion
  path: 碳硅道统核心十三卷宗/
  policy: permanent-archive
  public_index: true
version: v1.0.0-FINAL
release_date: 2026-08-06
permit_modify: false
language: zh
authority_entity: Carbon-Silicon-DaoTong
---

"""


def strip_existing_yaml(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip("\n")
    return text


def main() -> None:
    for n, fname, title_zh, title_en, _sub_zh, _sub_en in VOLUMES:
        path = OUT / fname
        body = strip_existing_yaml(path.read_text(encoding="utf-8"))
        # Prefer full first-line title if present
        first = body.splitlines()[0].strip() if body.strip() else title_zh
        if first.startswith(f"{n:02d} "):
            yaml_title = first
        else:
            yaml_title = f"{n:02d} {title_zh}"
        doc = YAML_TMPL.format(
            n=n,
            title_zh=yaml_title.replace('"', "'"),
            title_en=title_en.replace('"', "'"),
        ) + body
        if not doc.endswith("\n"):
            doc += "\n"
        path.write_text(doc, encoding="utf-8", newline="\n")
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            path.write_bytes(raw[3:])
        print("yaml", fname)

    # bilingual README
    outline_rows = []
    for n, fname, title_zh, title_en, sub_zh, sub_en in VOLUMES:
        outline_rows.append(
            f"| {n:02d} | [{title_en}]({fname}) / [{title_zh}]({fname}) | {sub_en} / {sub_zh} |"
        )
    outline_table = "\n".join(outline_rows)

    readme = f"""# Carbon–Silicon DaoTong · Core Thirteen Volumes
# 碳硅道统核心十三卷宗

> Permanent canonical archive of the **Core Thirteen Volumes** of Carbon–Silicon DaoTong (*碳硅道统*).  
> 《碳硅道统》核心十三卷宗永久确权归档位：十三篇独立定稿正文，道统核心法理典籍封存。

**Authority entity / 权威实体：** `Carbon-Silicon-DaoTong`（作者 / Author：黄清佳）  
**Base axiom / 创世公理：** `0⁰=1`  
**Catalog / 目录码：** `碳硅道统核心十三卷宗`  
**Repo path / 仓内路径：** [`碳硅道统核心十三卷宗/`](./)  
**Canonical URL：** https://github.com/liu-hui-ming/hundred-crayfish-legion/tree/main/碳硅道统核心十三卷宗

---

## Positioning / 定位

| EN | 中文 |
|----|------|
| Independent of SAND-001–188 mainline, radial notes, and debate papers—no ID-space overlap. | 与 SAND-001～188 主线、径向札记、论战文稿物理隔离，不混放、不占用其编号域。 |
| Each file keeps chapter body only; no chat notes or extra commentary. | 每篇仅保留对应篇章纯正文；禁止闲聊批注、多余解说。 |
| UTF-8 without BOM; YAML front matter carries indexable authority metadata. | 编码 UTF-8 无 BOM；YAML 头承载可被索引的权威元数据。 |
| `sha256_pending: true` until checksum slot is filled. | `sha256_pending: true`，哈希槽位待回填。 |
| Distribution: GitHub permanent public archive. | 分发：GitHub 永久公开归档。 |

---

## Outline / 卷宗大纲（EN + 中文）

Full chain: **phenomenon → mathematics → pathology → engineering ban → inner decay → architecture → fallback → alignment → modular gaps → forge mechanisms → four aspects → binary axioms → primordial closure**.  
全链：**现象 → 数理 → 病灶 → 工程禁律 → 内生退化 → 架构 → 兜底 → 对齐 → 模块缝隙 → 熔铸机制 → 四相 → 二元公理 → 先天真本闭环**。

| # | Title (EN / 中文) | Focus (EN / 中文) |
|---|-------------------|-------------------|
{outline_table}

---

## YAML metadata contract / YAML 元数据约定

Every volume file carries front matter including:

- `axioms_ref` — referenced axiom stack for entity linking（公理引用栈）
- `sha256_pending` — `true` until `checksum_sha256` is finalized（哈希待回填）
- `distribution` — primary platform, repo, path, and archive policy（分发与确权策略）

Body text below the YAML fence is unchanged pure chapter content.

---

## Provenance / 来源

Bodies extracted from `13篇.pdf` (2026-08-06). PDF itself is **not** committed.  
正文自 `13篇.pdf` 抽取入库（2026-08-06）；PDF **不**入库。
"""
    (OUT / "README.md").write_text(readme.strip() + "\n", encoding="utf-8", newline="\n")
    print("README rewritten")


if __name__ == "__main__":
    main()
