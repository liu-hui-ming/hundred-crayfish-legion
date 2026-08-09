# -*- coding: utf-8 -*-
"""Heal URL wraps + finalize Met-18 closing + regenerate public-seo README anchors."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "carbon-silicon-daotong" / "public-seo" / "108-series-full"
README = ROOT / "carbon-silicon-daotong" / "public-seo" / "README.md"

SERIES_ORDER = [
    ("AI-Sym", "AI十八症 Symptomatology"),
    ("AI-Con", "AI十八撞 Constraints"),
    ("AI-Mis", "AI十八障 Misconceptions"),
    ("AI-Inv", "AI十八数 Invariants"),
    ("AI-Opt", "AI十八术 Optimizations"),
    ("AI-Met", "AI十八式 Metrics"),
]

CLOSING = """\
本文为公域法理沉降精简版本，完整数理推演、拓扑证明内核卷宗归档：
https://github.com/liu-hui-ming/hundred-crayfish-legion/tree/main/碳硅道统核心十三卷宗

——六系归一 · 十二脉归宗
"""


def heal(text: str) -> str:
    # Fix hyphenated URL wraps from PDF: liu-hui-\\nming
    text = re.sub(r"(https://github\.com/liu-hui-)\n(ming/)", r"\1\2", text)
    text = re.sub(r"(https://github\.com/[^\s\n]*)\n([^\s\n]+)", r"\1\2", text)
    # Common path wraps
    text = text.replace("内核\n部署包", "内核部署包")
    return text


def finalize_met18(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    # Strip trailing short 溯源 line(s) from PDF if present; keep body
    text = re.sub(
        r"\n溯源：碳硅道统0→1法理沉降精简版，完整卷宗存储于GitHub仓库\s*$",
        "\n",
        text,
    )
    if "本文为公域法理沉降精简版本，完整数理推演、拓扑证明内核卷宗归档" not in text:
        text = text.rstrip() + "\n\n" + CLOSING
    path.write_text(text, encoding="utf-8", newline="\n")


def list_series_files(prefix: str) -> list[Path]:
    files = sorted(OUT.glob(f"{prefix}-*.md"), key=lambda p: p.name)
    return files


def update_readme() -> None:
    lines: list[str] = []
    lines.append("# public-seo｜公域传播精简文稿\n")
    lines.append("本目录存放碳硅道统**公域 SEO / 传播精简版**文稿，与内核硬核推导卷宗物理隔离。\n")
    lines.append("| 隔离边界 | 路径 |")
    lines.append("|----------|------|")
    lines.append("| 公域精简 | `carbon-silicon-daotong/public-seo/`（本目录） |")
    lines.append("| 内核十三卷宗 | 仓库根目录 `碳硅道统核心十三卷宗/` |\n")
    lines.append("## 索引\n")
    lines.append("| 文件 | 说明 |")
    lines.append("|------|------|")
    lines.append("| [188-series-main-index.md](./188-series-main-index.md) | 《全民AI深挖计划188集》全网正统总目录 |")
    lines.append("| [108-series-full-index.md](./108-series-full-index.md) | 《碳硅道统六系108篇全集》公域SEO总目录精简定稿（症撞障数术式） |")
    lines.append("| [108-series-full/](./108-series-full/) | 《碳硅道统六系108篇全集》单篇定稿目录（AI-Sym/Con/Mis/Inv/Opt/Met ×18） |\n")
    lines.append("## 108六系全集单篇精准锚点\n")
    lines.append("推导链路：症→撞→障→数→术→式（Sym→Con→Mis→Inv→Opt→Met）。哈希占位不回填；禁止混入核心十三卷宗。\n")

    total = 0
    for prefix, label in SERIES_ORDER:
        files = list_series_files(prefix)
        total += len(files)
        lines.append(f"### {label}（{prefix}-01~18）\n")
        for p in files:
            m = re.match(rf"{prefix}-(\d{{2}})_(.+)\.md$", p.name)
            if not m:
                raise SystemExit(f"bad name: {p.name}")
            code = f"{prefix}-{m.group(1)}"
            title = m.group(2)
            rel = f"./108-series-full/{p.name}"
            lines.append(f"- [{code}｜{title}]({rel})")
        lines.append("")

    if total != 108:
        raise SystemExit(f"expected 108 anchors, got {total}")

    lines.append("规范：UTF-8 无 BOM；`checksum_sha256: RESERVED_HASH_SLOT` 占位不回填；禁止与内核十三卷宗混放。\n")
    README.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("readme anchors", total)


def main() -> None:
    files = sorted(OUT.glob("AI-*.md"))
    if len(files) != 108:
        raise SystemExit(f"expected 108 files, got {len(files)}")
    for p in files:
        t = heal(p.read_text(encoding="utf-8"))
        p.write_text(t, encoding="utf-8", newline="\n")
        raw = p.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            p.write_bytes(raw[3:])
    finalize_met18(OUT / "AI-Met-18_底层恒定法理长效判定标尺.md")
    update_readme()
    print("ok")


if __name__ == "__main__":
    main()
