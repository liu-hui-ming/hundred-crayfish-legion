#!/usr/bin/env python3
"""Generate dt-188-bifurcation scaffold (64 cases + INDEX)."""
from __future__ import annotations

from pathlib import Path

CASES = [
    "碳基个体决策算力阈值分岔",
    "硅基大模型上下文窗口坍缩分岔",
    "碳化硅功率器件高温工况性能分岔",
    "通用AI行业落地成本收益分岔",
    "人类原生认知与AI模拟认知逻辑分岔",
    "分布式算力集群负载调度分岔",
    "星际深空通信时延约束推演分岔",
    "能源电力碳化硅替代硅基路线分岔",
    "公有云/私有AI私有化部署路径分岔",
    "碳硅伦理量子善恶判定边界分岔",
    "制造业产线AI改造轻重投入分岔",
    "大模型微调全参数/低秩优化分岔",
    "城市电网碳化硅储能拓扑结构分岔",
    "人脑记忆存储与向量数据库存储分岔",
    "开源大模型闭源商用化合规分岔",
    "车载功率半导体三代材料迭代分岔",
    "短期AI红利与长期文明熵增分岔",
    "本地端侧算力与云端中心算力分岔",
    "碳中和产业短期补贴/长效技术分岔",
    "人类自主创造与AI辅助创作权属分岔",
    "大模型幻觉成因数据层/算法层分岔",
    "光伏逆变器碳化硅集成方案分岔",
    "通用人工智能专用人工智能演化分岔",
    "算力基础设施国产替代引进路线分岔",
    "碳基生物生存能耗硅基硬件功耗分岔",
    "行业垂直模型通用基座适配改造分岔",
    "高压输电设备碳化硅器件封装分岔",
    "信息加密经典算法抗量子算法分岔",
    "AI监管事前准入事后追责治理分岔",
    "电池快充碳化硅驱动电路设计分岔",
    "人脑直觉推理AI逻辑推导路径分岔",
    "算力租赁自建算力资本投入分岔",
    "工业机器人伺服碳化硅驱动方案分岔",
    "数据私有留存数据共享训练权益分岔",
    "短期算力扩张长期贝肯斯坦上限约束分岔",
    "储能变流器单管碳化硅模组架构分岔",
    "人类价值判断AI数值量化评判分岔",
    "大模型蒸馏轻量化无损有损方案分岔",
    "航空机载碳化硅高温耐受工艺分岔",
    "开放数据训练闭环私有数据集分岔",
    "短期经济收益长期文明存续取舍分岔",
    "充电桩高低压碳化硅拓扑拓扑分岔",
    "碳硅融合共生对立对抗发展路线分岔",
    "多模态大模型文本图像音频融合分岔",
    "海上风电变流器碳化硅国产化分岔",
    "人类手工生产全自动AI产线替代分岔",
    "算力冷却液冷风冷散热方案成本分岔",
    "大模型安全对齐前置训练后置微调分岔",
    "轨道交通牵引碳化硅功率单元分岔",
    "区域算力中心跨省调度资源分配分岔",
    "生物碳基进化硅基人工迭代演化分岔",
    "AI原生工具原生软件重构迭代分岔",
    "户用光伏微型逆变器碳化硅集成分岔",
    "全球算力分配区域自主可控路线分岔",
    "短期技术跃进长期熵守恒约束分岔",
    "大模型本地离线在线运行模式分岔",
    "储能系统交直流碳化硅转换拓扑分岔",
    "人类主观体验AI模拟感官数据分岔",
    "芯片制造28nm/6nm碳化硅制程分岔",
    "行业AI标准化定制化开发路线分岔",
    "近地航天设备碳化硅抗辐照工艺分岔",
    "数据脱敏完全匿名可控脱敏方案分岔",
    "碳硅道统短期落地长期星际布局分岔",
    "六十四分岔总集合拓扑亏格推演边界分岔",
]

ROOT = Path("dt-188-bifurcation")
MAIN = Path("dt-188-main")


def slug_for_filename(title: str) -> str:
    return title.replace("/", "·")


def template(seq: int, title: str) -> tuple[str, str]:
    sid = f"BIF-{seq:03d}"
    slug = slug_for_filename(title)
    fname = f"{sid}-具象分岔-{slug}.md"
    full_title = f"碳硅道统·六十四分岔象·{sid}·{title}"
    content = f"""---
document_id: CS-DT-BIF-{seq:03d}-SCAFFOLD-v0.1.0
series: dt-188-bifurcation
catalog: dt-188-bifurcation
parent_rules: 碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则.md
bifurcation_id: {sid}
status: scaffold
version: v0.1.0-scaffold
author: 黄清佳
---

# {full_title}

## 1. 分岔核心诱因

## 2. 双路线具象落地路径

## 3. 碳硅联动十方万象分析

## 4. 认知盲区延伸推演

## 5. 落地优化解决方案

## 6. 拓扑与数理约束校验

## 7. 合规与伦理边界标注

## 8. 归档溯源哈希锚点

"""
    return fname, content


def main() -> None:
    ROOT.mkdir(exist_ok=True)
    MAIN.mkdir(exist_ok=True)

    index_lines = [
        "---",
        "document_id: CS-DT-188-BIFURCATION-INDEX-v0.1.0",
        "series: dt-188-bifurcation",
        "catalog: dt-188-bifurcation",
        "version: v0.1.0-scaffold",
        "author: 黄清佳",
        "---",
        "",
        "# dt-188-bifurcation · INDEX",
        "",
        "六十四分岔具象案例集检索索引。一条案例对应一个独立 `.md` 文件，禁止合并长文档。",
        "",
        "依赖总规则：[`六十四分岔象推演规则.md`](../碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则.md)",
        "",
        "| 序号 | BIF ID | 文件 | 子标题 |",
        "| --- | --- | --- | --- |",
    ]

    for i, title in enumerate(CASES, 1):
        fname, content = template(i, title)
        (ROOT / fname).write_text(content, encoding="utf-8")
        sid = f"BIF-{i:03d}"
        index_lines.append(f"| {i:03d} | {sid} | [`{fname}`](./{fname}) | {title} |")

    (ROOT / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    (ROOT / "README.md").write_text(
        """---
document_id: CS-DT-188-BIFURCATION-README-v0.1.0
series: dt-188-bifurcation
catalog: dt-188-bifurcation
version: v0.1.0-scaffold
author: 黄清佳
---

# dt-188-bifurcation · 具象分岔案例集

六十四分岔象具象案例独立归档区。检索入口：[`INDEX.md`](./INDEX.md)

## 命名规则

`BIF-NNN-具象分岔-【子标题唯一标识】.md` · NNN = 001–064

文件名中 `/` 以 `·` 替代（Windows 路径兼容），子标题正文保留原符号。

## 状态

当前全部为 scaffold 空白模板，待逐条填充推演正文。
""",
        encoding="utf-8",
    )

    (MAIN / "README.md").write_text(
        """---
document_id: CS-DT-188-MAIN-README-v0.1.0
series: dt-188-main
catalog: dt-188-main
version: v0.1.0-scaffold
author: 黄清佳
---

# dt-188-main · 主卷宗总纲文档区

本目录存放六十四分岔推演体系**总纲级**文档，与具象案例集物理隔离。

| 文档 | 说明 |
| --- | --- |
| [`六十四分岔象推演规则.md`](../碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则.md) | 推演总规则 V1.0（内核典藏卷 canonical） |

## 隔离规范

- 总纲文档 → `dt-188-main/` 或 `碳硅道统核心十三卷宗/内核典藏卷/`
- 具象分岔案例 → `dt-188-bifurcation/`（001–064 独立单文件）
- 禁止跨目录混存、禁止单文档堆砌多条案例
""",
        encoding="utf-8",
    )

    print(f"OK: {len(CASES)} cases + INDEX + READMEs")


if __name__ == "__main__":
    main()
