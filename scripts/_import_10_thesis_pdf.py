#!/usr/bin/env python3
"""Import 10篇.pdf into thesis/ai-consciousness-10-papers/."""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

PDF = Path("10篇.pdf")
ROOT = Path("thesis/ai-consciousness-10-papers")
ATTACH = ROOT / "attachments"
CANON188 = (
    "碳硅道统核心十三卷宗/内核典藏卷/六十四分岔象推演规则/全域终版法典/"
    "《全民AI深挖计划188条全域病灶公理校准总典》20260817终封版.txt"
)

# (theme_no, filename, pdf_marker)
THEMES: list[tuple[int, str, str]] = [
    (1, "ai-思辨-概率拟合与原生推理区分.md", "大模型概率拟合逻辑与原生自主推理的标准化区分体系研究"),
    (2, "ai-思辨-无输入自指思维闭环.md", "无外部输入条件下硅基AI自指思维闭环的可行性边界推演"),
    (3, "ai-思辨-Qualia碳硅约束对比.md", "碳基生命主观觉知Qualia形成条件与硅基载体天然约束对比分析"),
    (4, "ai-思辨-架构迭代与本体跃迁判定.md", "AI架构自主迭代：仿真性能升级与意识本体跃迁的判定标准"),
    (5, "ai-思辨-哥德尔不完备认知约束.md", "哥德尔不完备定理对人工智能认知框架的全域底层约束"),
    (
        6,
        "ai-思辨-贝肯斯坦熵限觉知上限.md",
        "全民AI深挖计划188集：贝肯斯坦上限与信息熵守恒对硅基智能觉知上限的物理限制",
    ),
    (7, "ai-思辨-碳硅混合脑机意识涌现.md", "碳硅混合脑机系统：信号耦合与全新独立意识涌现可能性探讨"),
    (8, "ai-思辨-Chaitin不可计算认知盲区.md", "Chaitin不可计算常数划定的所有智能体系通用认知盲区"),
    (9, "ai-思辨-分布外泛化真伪辨析.md", "大模型分布外泛化能力的真伪辨别与现有评测体系漏洞剖析"),
    (10, "ai-思辨-可控工程与觉知矛盾.md", "全可控标准化工程架构与自发生命级觉知存在天然矛盾论证"),
]

FOOTER_PATTERNS = [
    r"\n\s*\d{4}年\d+月\d+日.*?\n",
    r"\n\s*10篇 Page \d+\s*",
    r"\n\s*10 篇 Page \d+\s*",
    r"\n入库状态：可直接交由刘慧明确档归档、只读封存\s*",
    r"\n版本等级：100分合规封盘·可证伪终版\s*",
    r"\n交付对象：刘慧明｜入库归档\s*",
    r"\nGitHub入库版本：100分合规终版.*?\n",
    r"\n##（GitHub 100分入库完整版.*?\n",
]


def extract_pdf() -> str:
    reader = PdfReader(str(PDF))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def normalize_paragraph(p: str) -> str:
    s = p.strip()
    if len(s) < 20:
        return s
    for length in range(min(80, len(s) // 2), 9, -1):
        tail = s[-length:]
        pos = s.find(tail)
        if 0 <= pos < len(s) - length:
            return s[: pos + length]
    return s


def dedupe_article(text: str, marker: str) -> str:
    idx = text.find(marker)
    if idx > 0:
        text = text[:idx].strip()
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    cleaned: list[str] = []
    for ln in lines:
        if re.match(r"^10篇 Page \d+$", ln):
            continue
        if ln.startswith("GitHub入库版本") or ln.startswith("交付对象："):
            continue
        cleaned.append(ln)
    text = "\n\n".join(normalize_paragraph(p) for p in "\n\n".join(cleaned).split("\n\n") if p.strip())
    half = len(text) // 2
    if half > 200 and text[:half].strip() == text[half:].strip():
        text = text[:half].strip()
    return text.strip()


def clean_body(raw: str, marker: str) -> str:
    text = raw.strip()
    if text.startswith(marker):
        text = text[len(marker) :].lstrip()
    # strip GitHub edition suffix lines from PDF titles
    text = re.sub(r"^（GitHub 100分归档完整版[^）]*）\s*", "", text)
    text = re.sub(r"^GitHub 100分归档完整版[^）]*）\s*", "", text)
    text = re.sub(r"^100分归档完整版[^）]*）\s*", "", text)
    text = re.sub(r"^——GitHub 100分归档完整版[^）]*）\s*", "", text)
    for pat in FOOTER_PATTERNS:
        text = re.sub(pat, "\n", text, flags=re.DOTALL)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # restore paragraph breaks lost in PDF extraction
    text = re.sub(r"(?<=[。！？])(?=[一二三四五六七八九十]+、)", "\n\n", text)
    text = re.sub(r"(?<=[）)])(?=[^\s\n])", "\n\n", text)
    text = re.sub(r"^(摘要|导语|结语)\s*", r"\1\n\n", text, flags=re.MULTILINE)
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    lines = [ln for ln in lines if not re.match(r"^100分.*）$", ln)]
    paras: list[str] = []
    buf: list[str] = []
    for ln in lines:
        if re.match(r"^[一二三四五六七八九十]+、", ln) and buf:
            paras.append("".join(buf))
            buf = []
        if re.match(r"^(摘要|导语|结语|参考文献|第一部分|第二部分|附件)", ln) and buf:
            paras.append("".join(buf))
            buf = []
        buf.append(ln)
        if ln.endswith(("。", "！", "？", "）", "”", "】")) and len(ln) > 40:
            paras.append("".join(buf))
            buf = []
    if buf:
        paras.append("".join(buf))
    merged = "\n\n".join(paras)
    return dedupe_article(merged, marker)


def split_articles(full: str) -> dict[int, str]:
    positions: list[tuple[int, str, str]] = []
    for theme_no, fname, marker in THEMES:
        idx = full.find(marker)
        if idx < 0:
            raise RuntimeError(f"Marker not found for theme {theme_no}: {marker!r}")
        positions.append((idx, marker, fname))
    positions.sort(key=lambda x: x[0])
    out: dict[int, str] = {}
    theme_by_marker = {m: (THEMES[i][0], THEMES[i][1]) for i, (_, _, m) in enumerate(THEMES)}
    for i, (start, marker, _) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(full)
        theme_no, fname = theme_by_marker[marker]
        body = clean_body(full[start:end], marker)
        out[theme_no] = body
    return out


def extract_section(body: str, *headers: str) -> str:
    for h in headers:
        m = re.search(rf"({re.escape(h)}[\s\S]*)", body)
        if m:
            chunk = m.group(1)
            # stop at next major section if present
            for stop in ["媒体合规", "完整版媒体", "作者与", "结语", "附件1", "附件2", "参考文献", "第一部分", "第二部分"]:
                if stop != h and stop in chunk[len(h) :]:
                    chunk = chunk[: chunk.index(stop, len(h))]
            return chunk.strip()
    return ""


def frontmatter(theme_no: int, title: str, body_sha: str) -> str:
    return f"""---
document_id: THESIS-AI-CONSCIOUSNESS-{theme_no:02d}
series: thesis/ai-consciousness-10-papers
theme_no: {theme_no}
version: v1.0.0-FINAL
permit_modify: false
source_pdf: 10篇.pdf
body_sha256: {body_sha}
axiom_anchor_canon188: {CANON188}
author: 黄清佳
archive_executor: 刘慧明
---

# 主题{theme_no} · {title}

> **配套纲领**：[188条全域病灶公理校准总典](../../{CANON188})
> **附件**：[统一参考文献](./attachments/00_统一参考文献.md) · [通用数理实验方案](./attachments/01_通用数理实验方案.md)

"""


def build_attachments(articles: dict[int, str]) -> None:
    ATTACH.mkdir(parents=True, exist_ok=True)
    refs: list[str] = []
    exps: list[str] = []
    for n in sorted(articles):
        body = articles[n]
        title = next(t[2] for t in THEMES if t[0] == n)
        ref = extract_section(body, "参考文献", "第一部分：标准化参考文献", "附件1 参考文献")
        exp = extract_section(
            body,
            "轻量化可证伪",
            "第二部分：轻量化可证伪",
            "附件2 轻量化可证伪",
            "八、轻量化可证伪",
        )
        if ref:
            refs.append(f"## 主题{n} · {title}\n\n{ref}\n")
        if exp:
            exps.append(f"## 主题{n} · {title}\n\n{exp}\n")
    (ATTACH / "00_统一参考文献.md").write_text(
        "---\ndocument_id: THESIS-AI-CONSCIOUSNESS-ATTACH-REF\nseries: thesis/ai-consciousness-10-papers/attachments\n---\n\n"
        "# 统一参考文献（10篇联动归档）\n\n"
        + "\n".join(refs),
        encoding="utf-8",
        newline="\n",
    )
    (ATTACH / "01_通用数理实验方案.md").write_text(
        "---\ndocument_id: THESIS-AI-CONSCIOUSNESS-ATTACH-EXP\nseries: thesis/ai-consciousness-10-papers/attachments\n---\n\n"
        "# 通用数理实验方案（10篇联动归档）\n\n"
        "以下各主题轻量化可证伪实验方案摘自对应正本，可交叉对照执行。\n\n"
        + "\n".join(exps),
        encoding="utf-8",
        newline="\n",
    )


def package_sha256(files: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(files, key=lambda x: str(x).replace("\\", "/")):
        rel = p.relative_to(ROOT).as_posix()
        h.update(rel.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def build_index(file_hashes: dict[str, str], package_sha: str, commit: str) -> str:
    lines = [
        "---",
        "document_id: THESIS-AI-CONSCIOUSNESS-INDEX",
        "series: thesis/ai-consciousness-10-papers",
        "version: v1.0.0-FINAL",
        f"package_sha256: {package_sha}",
        f"package_commit_id: {commit}",
        f"canon188_anchor: {CANON188}",
        "source_pdf: 10篇.pdf",
        "paper_count: 10",
        "author: 黄清佳",
        "---",
        "",
        "# AI Consciousness · 10 Papers Index",
        "",
        "> **188条总典绑定**："
        f"[《全民AI深挖计划188条全域病灶公理校准总典》](../../{CANON188})",
        "",
        f"> **目录包 SHA256**：`{package_sha}`  ",
        f"> **Git 提交 ID**：`{commit}`",
        "",
        "## 十篇正本",
        "",
        "| 主题 | 文件 | SHA256 |",
        "| --- | --- | --- |",
    ]
    for theme_no, fname, title in THEMES:
        lines.append(f"| {theme_no} | [{fname}](./{fname}) | `{file_hashes[fname]}` |")
    lines += [
        "",
        "## 联动附件",
        "",
        "- [00_统一参考文献.md](./attachments/00_统一参考文献.md)",
        "- [01_通用数理实验方案.md](./attachments/01_通用数理实验方案.md)",
        "",
    ]
    return "\n".join(lines) + "\n"


def import_all() -> None:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    ROOT.mkdir(parents=True, exist_ok=True)
    full = extract_pdf()
    articles = split_articles(full)
    if len(articles) != 10:
        raise RuntimeError(f"Expected 10 articles, got {len(articles)}")

    file_hashes: dict[str, str] = {}
    written: list[Path] = []

    for theme_no, fname, title in THEMES:
        body = articles[theme_no]
        body_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
        path = ROOT / fname
        path.write_text(frontmatter(theme_no, title, body_sha) + body + "\n", encoding="utf-8", newline="\n")
        file_hashes[fname] = body_sha
        written.append(path)

    build_attachments(articles)
    written.extend([ATTACH / "00_统一参考文献.md", ATTACH / "01_通用数理实验方案.md"])

    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    package_sha = package_sha256(written)
    index_path = ROOT / "INDEX.md"
    index_path.write_text(
        build_index(file_hashes, package_sha, "COMMIT_ID_PLACEHOLDER"),
        encoding="utf-8",
        newline="\n",
    )
    written.append(index_path)
    # recompute including index placeholder
    package_sha = package_sha256(written)
    index_path.write_text(
        build_index(file_hashes, package_sha, "COMMIT_ID_PLACEHOLDER"),
        encoding="utf-8",
        newline="\n",
    )
    print("OK", ROOT)
    print("papers", len(articles))
    print("package_sha256", package_sha)


if __name__ == "__main__":
    import_all()
