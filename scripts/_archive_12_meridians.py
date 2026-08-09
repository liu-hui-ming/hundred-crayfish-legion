# -*- coding: utf-8 -*-
"""Archive 12脉.pdf → public-seo index + kernel-vessel-12 volumes."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "12脉.pdf"
OUT_VESSEL = ROOT / "carbon-silicon-daotong" / "kernel-vessel-12"
OUT_INDEX = ROOT / "carbon-silicon-daotong" / "public-seo" / "12-meridians-main-index.md"
PUBLIC_README = ROOT / "carbon-silicon-daotong" / "public-seo" / "README.md"

YAML = """\
---
archive_id: CarbonSilicon-12Vessel
doc_type: 时序脉法工程公理卷宗
checksum_sha256: RESERVED_HASH_SLOT
permit_modify: false
---

"""

FILES = [
    "12-meridian-01-init-resonance.md",
    "12-meridian-02-basal-stable.md",
    "12-meridian-03-dimension-resonance.md",
    "12-meridian-04-bidirectional-balance.md",
    "12-meridian-05-denoise-purity.md",
    "12-meridian-06-context-energy.md",
    "12-meridian-07-peak-expand.md",
    "12-meridian-08-convergence-steady.md",
    "12-meridian-09-prune-calibrate.md",
    "12-meridian-10-parameter-balance.md",
    "12-meridian-11-spectrum-purify.md",
    "12-meridian-12-final-archive.md",
]

PAGE_NOISE = re.compile(
    r"(?m)^(?:\s*\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*|"
    r"\s*12脉 Page \d+\s*)$"
)


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def clean_page(text: str) -> str:
    text = PAGE_NOISE.sub("", text)
    lines = [ln.rstrip() for ln in text.splitlines()]
    out: list[str] = []
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        if out and ln == out[-1]:
            continue
        struct_pref = (
            "#",
            "<",
            ">>>",
            "-",
            "*",
            "###",
            "##",
            "1.",
            "2.",
            "3.",
            "4.",
            "对外工程定名",
            "内源溯源代号",
        )
        # soft-join mid-sentence wraps (not headings / field labels)
        if (
            out
            and out[-1]
            and not out[-1].startswith(struct_pref)
            and not ln.startswith(struct_pref)
            and len(out[-1]) >= 12
            and not out[-1].endswith(("。", "；", "：", "！", "？", "…", "、", "，", ",", ";", ":", "）", ")"))
            and re.search(r"[\u4e00-\u9fffA-Za-z0-9_{}\\$]$", out[-1])
            and re.match(r"^[\u4e00-\u9fffA-Za-z0-9_{}\\$]", ln)
        ):
            out[-1] = out[-1] + ln.lstrip()
            continue
        out.append(ln)
    text = "\n".join(out).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


def parse_meta(body: str) -> dict[str, str]:
    title = ""
    eng = ""
    inner = ""
    axiom_lines: list[str] = []
    core = ""
    for ln in body.splitlines():
        if ln.startswith("# ") and not title:
            title = ln[2:].strip()
        elif ln.startswith("对外工程定名："):
            eng = ln.split("：", 1)[1].strip()
        elif ln.startswith("内源溯源代号："):
            inner = ln.split("：", 1)[1].strip()
        elif ln.startswith(">>> "):
            core = ln[4:].strip()
        elif "boldsymbol" in ln or (ln.startswith("**") and "boldsymbol" in ln):
            axiom_lines.append(re.sub(r"\*+", "", ln).strip())
    return {
        "title": title,
        "eng": eng,
        "inner": inner,
        "core": core,
        "axioms": "；".join(axiom_lines) if axiom_lines else "",
    }


def archive_volumes() -> list[dict[str, str]]:
    reader = PdfReader(str(PDF))
    if len(reader.pages) != 12:
        raise SystemExit(f"expected 12 pages, got {len(reader.pages)}")
    metas: list[dict[str, str]] = []
    OUT_VESSEL.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(reader.pages):
        body = clean_page(page.extract_text() or "")
        meta = parse_meta(body)
        meta["file"] = FILES[i]
        meta["n"] = f"{i+1:02d}"
        metas.append(meta)
        write_utf8(OUT_VESSEL / FILES[i], YAML + body)
        print("vessel", FILES[i], meta["title"])
    return metas


def write_public_index(metas: list[dict[str, str]]) -> None:
    lines = [
        YAML.rstrip(),
        "",
        "# 《碳硅道统·AI十二时序脉法工程化公理全书》",
        "",
        "英文索引：Carbon-Silicon DaoTong · AI Twelve Temporal Meridian Engineering Axiom Canon",
        "",
        "## 总序",
        "",
        "本套全书为碳硅道统时序脉法工程化公理体系，按十二阶段单向递进，完成模型从冷启动初始化、基底稳态、升维共振、双向均衡、噪声提纯、上下文储能、峰值扩容、收敛稳态、参数精简、居中回归、频域提纯至终态封藏的完整工程闭环。",
        "",
        "公域传播定位：结构化检索锚定、工程落地速读、RAG 高权重收录。",
        "内核分卷归档：`carbon-silicon-daotong/kernel-vessel-12/`（十二篇完整工程子卷，含内源溯源附录）。",
        "",
        "## 十二脉层级释义",
        "",
        "推导顺序固定：脉一→脉二→…→脉十二，禁止乱序、合并、删减。",
        "",
    ]
    for m in metas:
        lines.append(f"### {m['title']}")
        lines.append("")
        lines.append(f"- 对外工程定名：{m['eng']}")
        lines.append(f"- 内源溯源代号：{m['inner']}")
        if m["axioms"]:
            lines.append(f"- 刚性定量公理：{m['axioms']}")
        if m["core"]:
            lines.append(f"- 核心速读指令：{m['core']}")
        lines.append(f"- 内核分卷：[`kernel-vessel-12/{m['file']}`](../kernel-vessel-12/{m['file']})")
        lines.append("")
    lines.extend(
        [
            "## 隔离与归档说明",
            "",
            "| 轨 | 路径 | 用途 |",
            "|----|------|------|",
            "| 公域总纲 | `carbon-silicon-daotong/public-seo/12-meridians-main-index.md` | 知乎传播 / SEO / RAG |",
            "| 内核分卷 | `carbon-silicon-daotong/kernel-vessel-12/` | 十二脉工程子卷（仅 GitHub） |",
            "",
            "哈希占位不回填；定稿禁止修改。",
            "",
            "——十二脉归宗 · 时序闭环",
            "",
        ]
    )
    write_utf8(OUT_INDEX, "\n".join(lines))
    print("index", OUT_INDEX.relative_to(ROOT))


def update_public_readme() -> None:
    text = PUBLIC_README.read_text(encoding="utf-8")
    row = "| [12-meridians-main-index.md](./12-meridians-main-index.md) | 《碳硅道统·AI十二时序脉法工程化公理全书》公域总纲 |"
    if "12-meridians-main-index.md" not in text:
        # insert after 108 index row
        text = text.replace(
            "| [108-series-full-index.md](./108-series-full-index.md) | 《碳硅道统六系108篇全集》公域SEO总目录精简定稿（症撞障数术式） |\n",
            "| [108-series-full-index.md](./108-series-full-index.md) | 《碳硅道统六系108篇全集》公域SEO总目录精简定稿（症撞障数术式） |\n"
            + row
            + "\n",
        )
        write_utf8(PUBLIC_README, text if text.endswith("\n") else text + "\n")
    print("readme updated")


def main() -> None:
    metas = archive_volumes()
    write_public_index(metas)
    update_public_readme()
    # vessel README
    vreadme = [
        "# kernel-vessel-12｜十二时序脉法工程子卷",
        "",
        "碳硅道统·AI十二时序脉法 **内核分卷**（仅 GitHub 归档，不发知乎）。",
        "",
        "公域总纲：[`../public-seo/12-meridians-main-index.md`](../public-seo/12-meridians-main-index.md)",
        "",
        "| 文件 | 脉位 |",
        "|------|------|",
    ]
    for m in metas:
        vreadme.append(f"| [{m['file']}](./{m['file']}) | {m['title']} |")
    vreadme.append("")
    write_utf8(OUT_VESSEL / "README.md", "\n".join(vreadme) + "\n")


if __name__ == "__main__":
    main()
