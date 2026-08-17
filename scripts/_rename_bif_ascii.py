#!/usr/bin/env python3
"""Rename bifurcation files to ASCII BIF-NNN.md for GitHub web compatibility."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path("dt-188-bifurcation")

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
    "充电桩高低压碳化硅拓扑分岔",
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

REPO = "https://github.com/liu-hui-ming/hundred-crayfish-legion/blob/main"
RULES_URL = (
    f"{REPO}/"
    "碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则.md"
)


def slug_for_filename(title: str) -> str:
    return title.replace("/", "·")


def find_legacy(seq: int) -> Path | None:
    sid = f"BIF-{seq:03d}"
    title = CASES[seq - 1]
    slug = slug_for_filename(title)
    candidates = [
        ROOT / f"{sid}.md",
        ROOT / f"{sid}-具象分岔-{slug}.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    hits = sorted(ROOT.glob(f"{sid}-具象分岔-*.md"))
    return hits[0] if len(hits) == 1 else None


def reseal(text: str) -> str:
    text = re.sub(
        r"checksum_sha256: [a-f0-9]{64}",
        "checksum_sha256: [RESERVED_HASH_SLOT]",
        text,
    )
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text.replace("[RESERVED_HASH_SLOT]", digest)


def main() -> None:
    index_rows: list[str] = []
    for seq, title in enumerate(CASES, 1):
        sid = f"BIF-{seq:03d}"
        target = ROOT / f"{sid}.md"
        legacy = find_legacy(seq)
        if legacy is None:
            raise SystemExit(f"missing source for {sid}")
        text = legacy.read_text(encoding="utf-8")
        rel = f"dt-188-bifurcation/{sid}.md"
        text = re.sub(
            r"仓库路径：/.*",
            f"仓库路径：/{rel}",
            text,
        )
        text = reseal(text)
        target.write_text(text, encoding="utf-8", newline="\n")
        if legacy != target and legacy.exists():
            legacy.unlink()
        blob = f"{REPO}/dt-188-bifurcation/{sid}.md"
        index_rows.append(
            f"| {seq:03d} | {sid} | [{sid}.md](./{sid}.md) | "
            f"[GitHub]({blob}) | {title} |"
        )
        print("OK", sid)

    index = f"""---
document_id: CS-DT-188-BIFURCATION-INDEX-v1.0.1-FINAL
series: dt-188-bifurcation
catalog: dt-188-bifurcation
version: v1.0.1-FINAL
author: 黄清佳
---

# dt-188-bifurcation · INDEX

六十四分岔具象案例集（64/64）。文件名采用 ASCII 短名 `BIF-NNN.md`，子标题见下表。

总规则：[六十四分岔象推演规则.md]({RULES_URL})

| 序号 | BIF ID | 本地文件 | GitHub | 子标题 |
| --- | --- | --- | --- | --- |
""" + "\n".join(index_rows) + "\n"

    (ROOT / "INDEX.md").write_text(index, encoding="utf-8", newline="\n")

    readme = f"""# dt-188-bifurcation · 六十四分岔案例集

- 检索索引：[INDEX.md](./INDEX.md)
- 总规则：[六十四分岔象推演规则.md]({RULES_URL})

## 打开方式

GitHub 网页请直接点 **INDEX.md** 中的链接，文件名均为 `BIF-001.md` … `BIF-064.md`（ASCII 短名，避免中文长路径导致页面报错）。

示例：[BIF-001.md](./BIF-001.md)
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print("DONE index+readme")


if __name__ == "__main__":
    main()
