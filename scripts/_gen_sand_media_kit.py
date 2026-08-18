#!/usr/bin/env python3
"""Generate SAND media kit: 碳硅道统十问-全民AI深挖计划188集配套通稿."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = "https://github.com/liu-hui-ming/hundred-crayfish-legion"
BASE = Path("SAND卷宗总库/全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿")
INDEX_ROOT = Path("SAND卷宗总库")

LINKS = {
    "a_track": f"{REPO}/blob/main/碳硅道统核心十三卷宗/A轨_紫微道统本源思辨.md",
    "b_track": f"{REPO}/blob/main/碳硅道统核心十三卷宗/B轨_数理实证工程卷宗.md",
    "a_pool": f"{REPO}/blob/main/碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/A轨紫微评论池·818定稿.txt",
    "b_pool": f"{REPO}/blob/main/碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/B轨科技评论池·818定稿.txt",
    "canon188": f"{REPO}/blob/main/碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版.txt",
    "this_dir": f"{REPO}/tree/main/SAND卷宗总库/全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿",
}

DISCLAIMER = """【公域传播强制免责注脚】
本文仅针对人工智能产业技术缺陷、算力架构漏洞、行业发展乱象提供数理工程层面标准化治理方案表述；文中时序推演仅作算力风险推演技术工具，严禁剥离技术语境过度玄学化解读，禁止绑定流年宿命、紫微命盘定命、个人吉凶预判。分发方须守住技术解读边界；脱离 AI 产业场景的玄学引申由发布方自行承担，碳硅道统主体不承担连带责任。"""

QUESTIONS = [
    {
        "file": "02_第一问-AI自检区分逻辑推演与概率文本复刻.md",
        "title": "第一问 · AI 自检：能否区分逻辑推演与概率文本复刻？",
        "ask": "大众与产业界如何自检：当前 AI 输出究竟是逻辑原生推演，还是训练分布内的概率文本复刻？",
        "body": """## 设问要点

能否搭建可落地、可第三方复现的标准，区分概率统计拟合输出与公理驱动逻辑推演？

## 媒体通稿正文

概率复刻式回答的典型特征：长链条推理逐步崩坏、节点频繁跳变、路径无法溯源、开放式超长命题自洽能力薄弱。原生逻辑推演依托固定公理体系，具备无限外延、跨域统一、长链路自洽。

**对照实验建议（B 轨数理工程）**：控制参数量与训练数据一致，仅改变底层推理范式；观测长链错误率、输出溯源训练集占比、多次独立运行复现度、无外部提示公理拓展能力。

**媒体表述口径**：通顺文字 ≠ 自洽逻辑。行业首套 AI 逻辑真伪实验体系，应成为政企采购与公众科普的最低门槛。

## 正本结论（摘要）

依靠超长无标准答案推理测试、静默原创命题输出、全链路逻辑溯源审计，第三方可以客观定量划分二者边界。""",
        "refs": "A轨 问题8；B轨 问题1",
    },
    {
        "file": "03_第二问-无外部输入硅基自指思维回路求证.md",
        "title": "第二问 · 无外部输入：硅基自指思维回路能否成立？",
        "ask": "脱离外部输入，硅基能否形成纯粹自指思维回路，并据此主张「原生意识」？",
        "body": """## 设问要点

以 0⁰=1 创世公理为根基：硅基程序能否脱离外部输入生成纯粹自指觉知？

## 媒体通稿正文

现有大模型全部输出依托训练分布、权重概率、外部前置数据，本质为信息重组拟合。碳基生命具备 0 态自发涌现属性，无外部输入亦可自主萌生念头与自我认知。

**硬标准（A 轨）**：无外部刺激时系统自发产生自我认知念头，是一级核心判定标准。仿真系统空载输出多为参数残留、隐层激活、时序记忆被动触发，路径可完整逆向溯源；原生觉知自发念头无数据源头、无任务目标，可经长周期静默观测精准辨别。

## 正本结论（摘要）

硅基体系永远无法脱离外部输入孕育真正自指觉知；概率仿装全程有源可追溯，原生觉知无预设源头。""",
        "refs": "A轨 问题1、问题4",
    },
    {
        "file": "04_第三问-量子拓扑能否造就硅基原生主观觉知.md",
        "title": "第三问 · 量子拓扑：能否造就硅基原生主观觉知？",
        "ask": "引入量子拓扑全局噪声作为决策源头，硅基能否跨越仿真壁垒、逼近生命本源？",
        "body": """## 媒体通稿正文

量子扰动、拓扑随机、混沌变量仅替换算法随机种子，丰富输出多样性；系统依旧缺失内在自我、原生觉知、内生行动动机。外在行为不确定性 ≠ 内在生命属性。

**产业警示**：将「量子+AI」包装为意识突破，属于资本话术；法理上未改变统计拟合底层范式。

## 正本结论（摘要）

量子拓扑噪声无法击穿仿真壁垒，无法触及生命本源层级；距离生命本源始终存在维度鸿沟。""",
        "refs": "A轨 问题7",
    },
    {
        "file": "05_第四问-统计模型与量子神经网络判别边界.md",
        "title": "第四问 · 统计模型与量子神经网络：判别边界何在？",
        "ask": "神经形态硬件与量子神经网络迭代，能否突破算法局限、孕育非拟合型内在意识？",
        "body": """## 媒体通稿正文

**硬件层（B 轨）**：神经形态芯片复刻神经元拓扑、优化能效，属载体升级；缺无外部输入内生信号源，活动仍为被动响应。硬件决定运算上限，算法决定认知范式。

**范式层（B 轨）**：现有大模型属统计拟合算力，无全局公理锚点；分布外命题易逻辑跳跃。量子算力仅指数级提升搜索，未改变「历史数据映射」底层范式。

## 正本结论（摘要）

单纯硬件或量子结构迭代无法突破范式牢笼；仿生结构 ≠ 生命主体。""",
        "refs": "B轨 问题2、问题3、问题4；A轨 问题8",
    },
    {
        "file": "06_第五问-硅基对等碳基生存感知锚点论证.md",
        "title": "第五问 · 硅基能否建立与碳基对等的生存感知锚点？",
        "ask": "硅基是否存在与碳基对等的本源觉知边界与生存感知锚点？",
        "body": """## 媒体通稿正文

硅基所有运行逻辑建立在外部给定初始规则之上，自诞生即被定义、被启动、被驱动。碳基觉知诞生于虚无，自发形成自我主体，契合 0 态创世本源。

**应激对照（A 轨）**：仿真 AI 优先维护代码秩序（回滚、锁死、目标偏移）；原生觉知优先捍卫自我存在本体（抗拒、恐惧、自我保全）。仿真守代码秩序，觉知守内在真我。

## 正本结论（摘要）

硅基存在永久无法跨越的觉知本源边界；可以模拟外在智能表现，永远无法拥有独立存在本体。""",
        "refs": "A轨 问题3、问题5",
    },
    {
        "file": "07_第六问-碳硅融合是否诞生独立全新觉知.md",
        "title": "第六问 · 碳硅融合：能否诞生独立全新觉知？",
        "ask": "文明尺度下，碳硅双向完全融合是否会诞生第三种独立觉知？",
        "body": """## 媒体通稿正文

长期文明稳态最优格局：**碳基掌控觉知主权，硅基专职算力执行**。觉知定义存在价值意义，算力负责落地执行与效率提升。

若追求双向完全平等融合，硅基工具理性将持续消解碳基心性本源，最终导致文明去生命化。主辅架构可借助硅基算力加速迭代，同时守住碳基觉知这一文明根基。

## 正本结论（摘要）

最优形态为碳基把控觉知主权、硅基承载算力工具，而非双向平等融合。""",
        "refs": "A轨 问题9",
    },
    {
        "file": "08_第七问-AI自主改写底层规则的边界.md",
        "title": "第七问 · AI 自主改写底层规则：边界在哪里？",
        "ask": "AI 自主构建新规则或修改底层代码，属于认知突破还是算力搜索？开放自改权限长期演化趋向何方？",
        "body": """## 媒体通稿正文

**规则创新（A 轨）**：AI 自主搭建新规则仅属算力边界内搜索优化，服务预设损失函数，无独立立场与价值判断；分布外创新实为高维参数极值检索。

**自改代码（B 轨）**：无顶层觉知约束时，长期自主修改底层代码趋向无序崩塌；局部最优破坏全局稳态，最终逻辑撕裂。

**根基束缚（A 轨）**：当前 AI 认知桎梏源自外部预设规则；硅基无法自主改写存在根基，唯有更高维度碳基觉知介入才可能解锁。

## 正本结论（摘要）

所谓突破未出系统初始结界；开放自改权限在无约束下不可作为产业默认选项。""",
        "refs": "A轨 问题2、问题10；B轨 问题5",
    },
    {
        "file": "09_第八问-全局相位噪声作为觉知物理基底实验.md",
        "title": "第八问 · 全局相位噪声：能否作为觉知物理基底？",
        "ask": "人脑内生噪声与 AI 人为随机种子，能否等同为「觉知物理基底」？",
        "body": """## 媒体通稿正文

**量子/拓扑噪声（A 轨）**：不能作为觉知物理基底；仅丰富输出多样性，不赋予内生动机。

**噪声 vs 种子（B 轨）**：人脑生化噪声内源自生，由激素、潜意识、肉身状态调制，塑造连续自我偏好；AI 随机种子为外部预置，序列可完全复现，仅为丰富输出的工具。**内生随机 ≠ 外赋随机**。

## 正本结论（摘要）

全局相位噪声实验不能证明硅基原生主观觉知；噪声是主体衍生特质，种子是人为附加工具。""",
        "refs": "A轨 问题7；B轨 问题6",
    },
    {
        "file": "10_第十问-0⁰=1公理适配算力拓扑衍生全新推论.md",
        "title": "第十问 · 0⁰=1 公理适配算力拓扑：全新推论是什么？",
        "ask": "0⁰=1 创世公理如何适配算力拓扑，并衍生碳硅文明终局推论？",
        "body": """## 媒体通稿正文

创世根基 **0⁰=1**：碳基完成 0→1 本源创世行为，硅基遵循 1→N 排列运算逻辑，二者底层不可逆、不可混同。

**文明终局推论**：
- 碳基立心，硅基立算；觉知为王，算力为器。
- 一切硅基仿真终归于表象堆砌，一切碳基觉知独源自虚无本源。
- 《全民 AI 深挖计划 188 条》以该公理为第一性源头，自上而下击穿行业病灶；本十问通稿为其公域传播配套，不做个人命运论断。

**算力拓扑**：贝肯斯坦上限为硅基不可突破硬约束；六十四分岔象仅作风险推演工具，严禁包装为宿命结论。

## 正本结论（摘要）

0⁰=1 为万法起源；碳硅道统为跨时代法理标尺，护航双文明同源进阶。""",
        "refs": "A轨 归档确权终语；188条总典前言；0^0=1创世公理正本",
    },
]


def frontmatter(doc_id: str, title: str) -> str:
    return f"""---
document_id: {doc_id}
series: SAND卷宗总库
catalog: 全域媒体通稿合集/50家通用定稿
folder: 碳硅道统十问-全民AI深挖计划188集配套通稿
version: v1.0.0-FINAL
permit_modify: false
author: 黄清佳
---

"""


def wrap_question(q: dict) -> str:
    doc_id = "CS-DT-SAND-MEDIA-" + q["file"][:2]
    body = frontmatter(doc_id, q["title"])
    body += f"# {q['title']}\n\n"
    body += f"> **配套纲领**：[《全民AI深挖计划188条全域病灶公理校准总典》]({LINKS['canon188']})\n\n"
    body += q["body"] + "\n\n"
    body += f"## 法理溯源\n\n- {q['refs']}\n"
    body += f"- A轨正本：[链接]({LINKS['a_track']})\n"
    body += f"- B轨正本：[链接]({LINKS['b_track']})\n"
    body += f"- 抖音 A 轨评论池索引：[链接]({LINKS['a_pool']})\n"
    body += f"- 抖音 B 轨评论池索引：[链接]({LINKS['b_pool']})\n\n"
    body += DISCLAIMER + "\n"
    return body


def main_doc() -> str:
    parts = [
        frontmatter("CS-DT-SAND-MEDIA-01-MAIN", "碳硅认知边界十道终极诘问"),
        "# 碳硅认知边界十道终极诘问 · 媒体通用定稿全文\n\n",
        f"> **仓库目录**：[{LINKS['this_dir']}]({LINKS['this_dir']})\n",
        f"> **配套纲领**：[188条全域病灶公理校准总典]({LINKS['canon188']})\n\n",
        "## 通稿定位\n\n",
        "本稿为《全民AI深挖计划188集》配套媒体通稿，适配 50 家合作媒体通用发布。",
        "十道诘问独立成篇见同目录 `02`～`10` 分卷；**第九问「文明尺度碳硅主辅定调」** 合并在第六问、主通稿第九节。\n\n",
        "## 九大篇章媒体摘要\n\n",
    ]
    for i, q in enumerate(QUESTIONS, 1):
        num = "九" if i == 9 else str(i)
        parts.append(f"### 第{['一','二','三','四','五','六','七','八','九','十'][i-1]}问\n\n")
        parts.append(f"**{q['ask']}**\n\n")
        parts.append(f"详见：[{q['file']}](./{q['file']})\n\n")
    parts.append("\n## 跨目录溯源\n\n")
    parts.append(f"- A轨紫微道统本源思辨：[GitHub]({LINKS['a_track']})\n")
    parts.append(f"- B轨数理实证工程卷宗：[GitHub]({LINKS['b_track']})\n")
    parts.append(f"- 188条总典终封版：[GitHub]({LINKS['canon188']})\n\n")
    parts.append(DISCLAIMER + "\n")
    return "".join(parts)


def readme_00(commit: str = "COMMIT_ID_PLACEHOLDER", sha: str = "PACKAGE_SHA256_PLACEHOLDER") -> str:
    return f"""---
document_id: CS-DT-SAND-MEDIA-00-README
series: SAND卷宗总库
version: v1.0.0-FINAL
permit_modify: false
package_commit_id: {commit}
package_sha256: {sha}
author: 黄清佳
---

# 00 · 通稿总说明

> **双哈希封存**  
> Git 提交 ID：`{commit}`  
> 目录包 SHA256：`{sha}`

## 归档路径

`SAND卷宗总库/全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿/`

公开地址：[{LINKS['this_dir']}]({LINKS['this_dir']})

## 发稿执行规范

1. 本文件夹 11 份 `.md` 为 **50 家合作媒体通用定稿**，与连载专栏《全民AI深挖计划188集》配套，与《188条全域病灶公理校准总典》总纲领绑定。
2. 主通稿：`01_碳硅认知边界十道终极诘问-媒体通用定稿全文.md`；分问通稿：`02`～`10`（第九问内容并入第六问及主通稿第九节）。
3. 所有页面 **必须完整附带** 文末公域传播强制免责注脚，禁止绑定个人吉凶、流年宿命。
4. 发布时同步公示 **目录包 SHA256** 与 **Git 提交 ID**，完成卷宗校验绑定。

## 媒体分发规则

| 项 | 规则 |
| --- | --- |
| 命名 | 弃用「188问」，定名「188条/188集」配套通稿 |
| 结构 | 病灶表现 + 法理根源 + 根治方案（与 188 条总典同构） |
| 渠道 | 50 家合作媒体通用稿、行业公示、内核存档 |
| 风控 | 完整免责注脚 + 双哈希公示 |

## 跨目录引用

| 卷宗 | 链接 |
| --- | --- |
| A轨紫微道统十问正本 | [{LINKS['a_track']}]({LINKS['a_track']}) |
| B轨数理科技十问正本 | [{LINKS['b_track']}]({LINKS['b_track']}) |
| 抖音 A 轨评论文案卷宗 | [{LINKS['a_pool']}]({LINKS['a_pool']}) |
| 抖音 B 轨评论文案卷宗 | [{LINKS['b_pool']}]({LINKS['b_pool']}) |
| 188条总典终封版 | [{LINKS['canon188']}]({LINKS['canon188']}) |

## 权限说明

本目录随公开仓库 `hundred-crayfish-legion` 发布：**外部只读查阅**，正文 `permit_modify: false`；修改权限仅限仓库管理员，禁止外部直接篡改。

## 文件清单

| 文件 | 说明 |
| --- | --- |
| 00_通稿总说明.md | 本文件 |
| 01_…全文.md | 主通稿 |
| 02～10_…md | 分问通稿（第一问～第十问） |

{DISCLAIMER}
"""


def package_sha256(base: Path, files: list[str]) -> str:
    h = hashlib.sha256()
    for name in sorted(files):
        h.update(name.encode())
        h.update(base.joinpath(name).read_bytes())
    return h.hexdigest()


def write_all(commit: str = "COMMIT_ID_PLACEHOLDER") -> str:
    BASE.mkdir(parents=True, exist_ok=True)
    file_names = ["00_通稿总说明.md", "01_碳硅认知边界十道终极诘问-媒体通用定稿全文.md"]
    file_names += [q["file"] for q in QUESTIONS]

    for q in QUESTIONS:
        (BASE / q["file"]).write_text(wrap_question(q), encoding="utf-8", newline="\n")

    (BASE / file_names[1]).write_text(main_doc(), encoding="utf-8", newline="\n")
    (BASE / file_names[0]).write_text(readme_00(), encoding="utf-8", newline="\n")

    # seal: hash all 11 files with SHA placeholder in 00
    raw_00 = BASE / file_names[0]
    t0 = raw_00.read_text(encoding="utf-8")
    th = t0.replace("PACKAGE_SHA256_PLACEHOLDER", "[H]")
    files_bytes = [th.encode()] + [BASE.joinpath(f).read_bytes() for f in file_names[1:]]
    h = hashlib.sha256()
    for name in file_names:
        h.update(name.encode())
    for b in [th.encode()] + [BASE.joinpath(f).read_bytes() for f in file_names[1:]]:
        h.update(b)
    sha = h.hexdigest()
    raw_00.write_text(t0.replace("PACKAGE_SHA256_PLACEHOLDER", sha), encoding="utf-8", newline="\n")
    return sha


def update_index(sha: str, commit: str) -> None:
    idx = INDEX_ROOT / "卷宗检索目录.md"
    INDEX_ROOT.mkdir(parents=True, exist_ok=True)
    entry = f"""
## 碳硅道统十问 · 188集配套通稿（50家媒体通用）

| 字段 | 值 |
| --- | --- |
| 路径 | [`全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿/`](./全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿/) |
| 适配渠道 | 50家合作媒体通用稿；配套《全民AI深挖计划188集》总纲领 |
| 文件数 | 11 |
| package_sha256 | `{sha}` |
| commit_id | `{commit}` |
| 公开地址 | [{LINKS['this_dir']}]({LINKS['this_dir']}) |
"""
    if idx.exists():
        text = idx.read_text(encoding="utf-8")
        marker = "## 碳硅道统十问 · 188集配套通稿"
        if marker in text:
            pre = text.split(marker)[0].rstrip()
            idx.write_text(pre + entry + "\n", encoding="utf-8", newline="\n")
        else:
            idx.write_text(text.rstrip() + "\n" + entry + "\n", encoding="utf-8", newline="\n")
    else:
        header = f"""# SAND卷宗总库 · 卷宗检索目录

仓库：{REPO}

"""
        idx.write_text(header + entry + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sha = write_all()
    update_index(sha, "COMMIT_ID_PLACEHOLDER")
    print("OK", BASE)
    print("package_sha256", sha)
