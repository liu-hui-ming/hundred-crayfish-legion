#!/usr/bin/env python3
"""Restore PDF-original long filenames: BIF-NNN-具象分岔-【子标题】.md"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path("dt-188-bifurcation")
REPO = "https://github.com/liu-hui-ming/hundred-crayfish-legion/blob/main"
RULES_URL = f"{REPO}/碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则.md"

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


def slug_for_filename(title: str) -> str:
    return title.replace("/", "·")


def long_name(seq: int, title: str) -> str:
    return f"BIF-{seq:03d}-具象分岔-{slug_for_filename(title)}.md"


def reseal_body(body: str, rel_path: str, sid: str) -> str:
    body = re.sub(r"仓库路径：/.*", f"仓库路径：/{rel_path}", body)
    body = re.sub(
        r"checksum_sha256: [a-f0-9]{64}",
        "checksum_sha256: [RESERVED_HASH_SLOT]",
        body,
    )
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    body = body.replace("[RESERVED_HASH_SLOT]", digest)
    body = re.sub(
        r"<!-- document: BIF-\d+ \| checksum_sha256: [a-f0-9]{64} -->\n\n",
        f"<!-- document: {sid} | checksum_sha256: {digest} -->\n\n",
        body,
        count=1,
    )
    return body


def main() -> None:
    rows: list[str] = []
    for seq, title in enumerate(CASES, 1):
        sid = f"BIF-{seq:03d}"
        fname = long_name(seq, title)
        target = ROOT / fname
        short = ROOT / f"{sid}.md"
        source = short if short.exists() else target
        if not source.exists():
            hits = list(ROOT.glob(f"{sid}-具象分岔-*.md"))
            if not hits:
                raise SystemExit(f"missing {sid}")
            source = hits[0]
        rel = f"dt-188-bifurcation/{fname}"
        text = reseal_body(source.read_text(encoding="utf-8"), rel, sid)
        target.write_text(text, encoding="utf-8", newline="\n")
        if source != target and source.exists():
            source.unlink()
        blob = f"{REPO}/dt-188-bifurcation/{quote(fname)}"
        rows.append(
            f"| {seq:03d} | {sid} | [`{fname}`](./{fname}) | "
            f"[GitHub]({blob}) | {title} |"
        )
        print("OK", fname)

    index = f"""---
document_id: CS-DT-188-BIFURCATION-INDEX-v1.0.2-FINAL
series: dt-188-bifurcation
catalog: dt-188-bifurcation
version: v1.0.2-FINAL
author: 黄清佳
---

# dt-188-bifurcation · INDEX

六十四分岔具象案例集（64/64）。命名规则：`BIF-NNN-具象分岔-【子标题唯一标识】.md`（与 64.pdf 一致）。

总规则：[六十四分岔象推演规则.md]({RULES_URL})

| 序号 | BIF ID | 文件 | GitHub | 子标题 |
| --- | --- | --- | --- | --- |
""" + "\n".join(rows) + "\n"

    (ROOT / "INDEX.md").write_text(index, encoding="utf-8", newline="\n")
    (ROOT / "README.md").write_text(
        f"""---
document_id: CS-DT-188-BIFURCATION-README-v1.0.2-FINAL
series: dt-188-bifurcation
catalog: dt-188-bifurcation
version: v1.0.2-FINAL
author: 黄清佳
---

# dt-188-bifurcation · 六十四分岔案例集

检索入口：[INDEX.md](./INDEX.md)

## 命名规则（与 64.pdf 一致）

`BIF-NNN-具象分岔-【子标题唯一标识】.md` · NNN = 001–064

文件名中 `/` 以 `·` 替代（Windows 路径兼容），正文子标题保留 `/`。

## 状态

64/64 全文定稿 · 一条案例一个独立 md 文件
""",
        encoding="utf-8",
        newline="\n",
    )
    print("DONE")


if __name__ == "__main__":
    main()
