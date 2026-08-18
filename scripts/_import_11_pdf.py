#!/usr/bin/env python3
"""Import 11.pdf media kit content into SAND 十问通稿 directory."""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

# Reuse metadata / disclaimer from generator
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_sand_media_kit import (  # noqa: E402
    BASE,
    DISCLAIMER,
    INDEX_ROOT,
    LINKS,
    QUESTIONS,
    REPO,
)

PDF = Path("11.pdf")

ARTICLE_MARKERS: list[tuple[str, str]] = [
    ("02_第一问-AI自检区分逻辑推演与概率文本复刻.md", "拨开AI幻觉迷雾：厘清概率拟合与逻辑推演"),
    ("03_第二问-无外部输入硅基自指思维回路求证.md", "新视角探讨人工智能：封闭算力体系下的自指意识可能性"),
    ("04_第三问-量子拓扑能否造就硅基原生主观觉知.md", "硅基觉知的冷思考：AI仿真不等于真正的主观意识"),
    ("05_第四问-统计模型与量子神经网络判别边界.md", "AI发展新思辨：跳出拟合内卷，探寻智能创律的未来方向"),
    ("06_第五问-硅基对等碳基生存感知锚点论证.md", "跳出生物固有认知 思辨碳硅智能的底层价值锚点"),
    ("07_第六问-碳硅融合是否诞生独立全新觉知.md", "探索人机共生新范式：碳硅道统为人工智能治理提供全新思考"),
    ("08_第七问-AI自主改写底层规则的边界.md", "理性看待AI能力边界：现有人工智能难以实现底层范式的自主创新"),
    ("09_第八问-全局相位噪声作为觉知物理基底实验.md", "前沿假说探讨：全局相位噪声视角下，重新解读意识、AI与生命的边界"),
    ("07_q9_append", "坚守“碳基为本、硅基为用”，厘清人工智能的永久法理边界"),
    ("01_碳硅认知边界十道终极诘问-媒体通用定稿全文.md", "《全民AI深挖计划188集》碳硅道统十问｜全域AI本源思辨通稿"),
]

FOOTER_PATTERNS = [
    r"\n\s*\d{4}年\d+月\d+日.*?\n",
    r"\n\s*11 Page \d+\s*",
    r"\n十二脉归一\s*\n碳硅道统创立人：黄清佳\s*\n彩蛋藏于：今日头条、抖音、GitHub\s*\n",
    r"\n碳硅法理沉降精简版，深层数理推演详见GitHub核心十三卷宗：[^\n]*\n",
    r"\nming/hundred-crayfish-legion/tree/main/碳硅道统核心十三卷宗\s*",
    r"\n统一固定落款\s*\n十二脉归一\s*\n碳硅道统创立人：黄清佳\s*\n彩蛋藏于：今日头条、抖音、GitHub\s*",
]


def extract_pdf_text() -> str:
    reader = PdfReader(str(PDF))
    parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def normalize_paragraph(p: str) -> str:
    """Fix PDF overlap duplicates within one paragraph."""
    s = p.strip()
    if len(s) < 20:
        return s
    for length in range(min(80, len(s) // 2), 9, -1):
        tail = s[-length:]
        pos = s.find(tail)
        if 0 <= pos < len(s) - length:
            return s[: pos + length]
    for length in range(min(80, len(s) // 2), 9, -1):
        for start in range(len(s) - 2 * length):
            if s[start : start + length] == s[start + length : start + 2 * length]:
                return s[: start + length] + s[start + 2 * length :]
    return s


def dedupe_repeated_article(text: str, title_hint: str = "") -> str:
    """PDF sometimes prints the same article twice back-to-back."""
    if title_hint:
        idx = text.find(title_hint)
        if idx > 0:
            text = text[:idx].strip()
        else:
            second = text.find(title_hint, len(title_hint))
            if second > 0:
                text = text[:second].strip()
    # drop orphaned PDF tail fragments (< 50 chars, no title)
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    cleaned: list[str] = []
    for ln in lines:
        if len(ln) < 50 and ln.endswith("。") and not cleaned:
            continue
        if len(ln) < 50 and ln.endswith("。") and cleaned and not cleaned[-1].endswith(ln.rstrip("。")):
            # merge short orphan into previous paragraph if it looks like a continuation
            if len(ln) <= 30:
                cleaned[-1] = cleaned[-1].rstrip("。") + ln
                continue
        cleaned.append(ln)
    text = "\n\n".join(cleaned)
    text = "\n\n".join(normalize_paragraph(p) for p in text.split("\n\n") if p.strip())
    half = len(text) // 2
    if half > 200 and text[:half].strip() == text[half:].strip():
        return text[:half].strip()
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paras) >= 4 and paras[0] == paras[len(paras) // 2]:
        return "\n\n".join(paras[: len(paras) // 2]).strip()
    return text.strip()


def clean_body(raw: str, title_hint: str = "") -> str:
    text = raw.strip()
    if title_hint and text.startswith(title_hint):
        text = text[len(title_hint) :].lstrip()
    for pat in FOOTER_PATTERNS:
        text = re.sub(pat, "\n", text, flags=re.DOTALL)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"([^\n。！？]{10,})\n([^\n。！？]{4,30})。\n", r"\1\2。\n", text)
    fixed_lines = [re.sub(r"(.{8,60})\1+", r"\1", ln) for ln in text.split("\n")]
    text = "\n".join(fixed_lines)
    # wrap long lines from PDF into paragraphs
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    paras: list[str] = []
    buf: list[str] = []
    for ln in lines:
        if re.match(r"^https?://", ln):
            if buf:
                paras.append("".join(buf))
                buf = []
            paras.append(ln)
            continue
        if len(ln) < 40 and not buf and not ln.endswith(("：", "?", "？")):
            paras.append(ln)
            continue
        buf.append(ln)
        if ln.endswith(("。", "！", "？", "」", "”", "）")):
            paras.append("".join(buf))
            buf = []
    if buf:
        paras.append("".join(buf))
    merged = "\n\n".join(paras).strip()
    return dedupe_repeated_article(merged, title_hint)


def split_articles(full: str) -> dict[str, str]:
    positions: list[tuple[str, int]] = []
    for key, marker in ARTICLE_MARKERS:
        idx = full.find(marker)
        if idx < 0:
            raise RuntimeError(f"Marker not found in 11.pdf: {marker!r}")
        positions.append((key, idx))
    # keep earliest offset per key (duplicate PDF pages)
    earliest: dict[str, int] = {}
    for key, idx in positions:
        earliest[key] = min(earliest.get(key, idx), idx)
    positions = [(k, v) for k, v in earliest.items()]
    positions.sort(key=lambda x: x[1])

    out: dict[str, str] = {}
    marker_by_key = dict(ARTICLE_MARKERS)
    for i, (key, start) in enumerate(positions):
        end = positions[i + 1][1] if i + 1 < len(positions) else len(full)
        chunk = full[start:end]
        title = marker_by_key[key]
        first_nl = chunk.find("\n")
        body = chunk[first_nl + 1 :] if first_nl >= 0 else chunk
        out[key] = clean_body(body, title)
    return out


def frontmatter(doc_id: str) -> str:
    return f"""---
document_id: {doc_id}
series: SAND卷宗总库
catalog: 全域媒体通稿合集/50家通用定稿
folder: 碳硅道统十问-全民AI深挖计划188集配套通稿
version: v1.1.0-FROM-11PDF
permit_modify: false
source_pdf: 11.pdf
author: 黄清佳
---

"""


def wrap_question(q: dict, body: str, extra_section: str = "") -> str:
    doc_id = "CS-DT-SAND-MEDIA-" + q["file"][:2]
    md = frontmatter(doc_id)
    md += f"# {q['title']}\n\n"
    md += f"> **配套纲领**：[《全民AI深挖计划188条全域病灶公理校准总典》]({LINKS['canon188']})\n\n"
    md += "## 媒体通稿正文\n\n"
    md += body + "\n\n"
    if extra_section:
        md += extra_section + "\n\n"
    md += f"## 法理溯源\n\n- {q['refs']}\n"
    md += f"- A轨正本：[链接]({LINKS['a_track']})\n"
    md += f"- B轨正本：[链接]({LINKS['b_track']})\n"
    md += f"- 抖音 A 轨评论池索引：[链接]({LINKS['a_pool']})\n"
    md += f"- 抖音 B 轨评论池索引：[链接]({LINKS['b_pool']})\n\n"
    md += DISCLAIMER + "\n"
    return md


def build_main_doc(articles: dict[str, str]) -> str:
    body = articles["01_碳硅认知边界十道终极诘问-媒体通用定稿全文.md"]
    parts = [
        frontmatter("CS-DT-SAND-MEDIA-01-MAIN"),
        "# 碳硅认知边界十道终极诘问 · 媒体通用定稿全文\n\n",
        f"> **仓库目录**：[{LINKS['this_dir']}]({LINKS['this_dir']})\n",
        f"> **配套纲领**：[188条全域病灶公理校准总典]({LINKS['canon188']})\n\n",
        "## 通稿定位\n\n",
        "本稿为《全民AI深挖计划188集》配套媒体通稿，适配 50 家合作媒体通用发布。",
        "十道诘问独立成篇见同目录 `02`～`10` 分卷；**第九问「文明尺度碳硅主辅定调」** 合并在第六问、主通稿第九节。\n\n",
        "## 媒体通稿正文\n\n",
        body,
        "\n\n## 分问通稿索引\n\n",
    ]
    cn = "一二三四五六七八九十"
    for i, q in enumerate(QUESTIONS, 1):
        parts.append(f"### 第{cn[i - 1]}问\n\n")
        parts.append(f"**{q['ask']}**\n\n")
        parts.append(f"详见：[{q['file']}](./{q['file']})\n\n")
    parts.append("\n## 跨目录溯源\n\n")
    parts.append(f"- A轨紫微道统本源思辨：[GitHub]({LINKS['a_track']})\n")
    parts.append(f"- B轨数理实证工程卷宗：[GitHub]({LINKS['b_track']})\n")
    parts.append(f"- 188条总典终封版：[GitHub]({LINKS['canon188']})\n\n")
    parts.append(DISCLAIMER + "\n")
    return "".join(parts)


def build_q10(articles: dict[str, str]) -> str:
    """Q10 has no standalone article in 11.pdf; compose from main-doc Q10 + symbiosis excerpt."""
    main = articles["01_碳硅认知边界十道终极诘问-媒体通用定稿全文.md"]
    m = re.search(
        r"10\.\s*将0⁰=1创世公理完整适配硅基算力拓扑体系后，会推导出哪些现有经典物理、计算机科学\s*体系无法解释的全新结论？",
        main,
    )
    q10_line = m.group(0).replace("\n", "") if m else (
        "将0⁰=1创世公理完整适配硅基算力拓扑体系后，会推导出哪些现有经典物理、计算机科学体系无法解释的全新结论？"
    )
    sym = articles["07_第六问-碳硅融合是否诞生独立全新觉知.md"]
    excerpt = ""
    for para in sym.split("\n\n"):
        if "0⁰=1" in para or "90条宇宙公律" in para or "五级智能梯队" in para:
            excerpt += para + "\n\n"
    body = f"**设问**：{q10_line}\n\n{excerpt.strip()}"
    body += (
        "\n\n以上十问并非单纯理论空想，全部可拆分转化为分层实验：物理硬件层、算法架构层、"
        "算力能效层、系统动力学层、道统法理层、本源觉知层六大维度测试方案。"
    )
    q = next(x for x in QUESTIONS if x["file"].startswith("10_"))
    return wrap_question(q, body)


def readme_00(commit: str, sha: str) -> str:
    return f"""---
document_id: CS-DT-SAND-MEDIA-00-README
series: SAND卷宗总库
version: v1.1.0-FROM-11PDF
permit_modify: false
source_pdf: 11.pdf
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

## 内容来源

本目录 11 份 `.md` 正文自本地 **`11.pdf`**（22 页）提取入库；**不上传 PDF 原件**。第十问无独立通稿页，由主通稿设问与第六问通稿中 0⁰=1 相关段落汇编。

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


def package_sha256(file_names: list[str]) -> str:
    h = hashlib.sha256()
    for name in sorted(file_names):
        h.update(name.encode())
        h.update((BASE / name).read_bytes())
    return h.hexdigest()


def update_index(sha: str, commit: str) -> None:
    idx = INDEX_ROOT / "卷宗检索目录.md"
    entry = f"""
## 碳硅道统十问 · 188集配套通稿（50家媒体通用）

| 字段 | 值 |
| --- | --- |
| 路径 | [`全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿/`](./全域媒体通稿合集/50家通用定稿/碳硅道统十问-全民AI深挖计划188集配套通稿/) |
| 适配渠道 | 50家合作媒体通用稿；配套《全民AI深挖计划188集》总纲领 |
| 来源 | `11.pdf` 提取（不上传 PDF） |
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


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def import_all() -> str:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    BASE.mkdir(parents=True, exist_ok=True)

    full = extract_pdf_text()
    articles = split_articles(full)

    file_names = ["00_通稿总说明.md", "01_碳硅认知边界十道终极诘问-媒体通用定稿全文.md"]
    file_names += [q["file"] for q in QUESTIONS]

    (BASE / file_names[1]).write_text(build_main_doc(articles), encoding="utf-8", newline="\n")

    q9_body = articles.pop("07_q9_append", "")
    q6_extra = ""
    if q9_body:
        q6_extra = "## 第九问 · 碳硅主辅定调（并入本篇）\n\n" + q9_body

    for q in QUESTIONS:
        if q["file"].startswith("10_"):
            (BASE / q["file"]).write_text(build_q10(articles), encoding="utf-8", newline="\n")
            continue
        body = articles.get(q["file"], "")
        if not body:
            raise RuntimeError(f"No PDF body for {q['file']}")
        extra = q6_extra if q["file"].startswith("07_") else ""
        (BASE / q["file"]).write_text(wrap_question(q, body, extra), encoding="utf-8", newline="\n")

    commit = git_head()
    # placeholder hash in 00, then seal
    (BASE / file_names[0]).write_text(readme_00(commit, "PACKAGE_SHA256_PLACEHOLDER"), encoding="utf-8", newline="\n")
    sha = package_sha256(file_names)
    (BASE / file_names[0]).write_text(
        readme_00(commit, sha).replace(commit, "COMMIT_ID_PLACEHOLDER"),
        encoding="utf-8",
        newline="\n",
    )
    # re-seal with actual commit after commit — first pass uses HEAD; backfill after commit
    (BASE / file_names[0]).write_text(readme_00("COMMIT_ID_PLACEHOLDER", sha), encoding="utf-8", newline="\n")
    update_index(sha, "COMMIT_ID_PLACEHOLDER")
    return sha


if __name__ == "__main__":
    sha = import_all()
    print("OK", BASE)
    print("package_sha256", sha)
    print("NOTE: run commit then backfill COMMIT_ID_PLACEHOLDER in 00 + index")
