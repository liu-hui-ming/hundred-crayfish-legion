# -*- coding: utf-8 -*-
"""Archive AI-Sym-01~18 from AI-Sym.pdf into public-seo/108-series-full/."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "AI-Sym.pdf"
OUT = ROOT / "carbon-silicon-daotong" / "public-seo" / "108-series-full"

TITLES = {
    "01": "生成视觉人体拓扑畸变",
    "02": "长文本代码变量漂移",
    "03": "大模型数理符号失准",
    "04": "超长上下文时序记忆衰减",
    "05": "学术引文幻觉",
    "06": "多轮对话指令权重衰减",
    "07": "古文翻译深层语义偏移",
    "08": "地理场景生成逻辑紊乱",
    "09": "细粒度视觉识别类别混淆",
    "10": "迭代训练性能震荡退化",
    "11": "任务对话业务闭环断裂",
    "12": "多模态图文字符乱码",
    "13": "复杂自然意图识别失效",
    "14": "AGI落地指标预期落差",
    "15": "模型原生知识缺失依赖标注",
    "16": "自回归生成固有事实熵",
    "17": "增量学习灾难性遗忘",
    "18": "多模态虚实工况性能割裂",
}

YAML = """\
---
archive_id: CarbonSilicon-108-Full
doc_type: 公域法理沉降精简定稿
series_type: 六系108篇全集
anchor_code: {code}
checksum_sha256: RESERVED_HASH_SLOT
permit_modify: false
---

"""

PAGE_NOISE = re.compile(
    r"(?m)^(?:\s*\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*|"
    r"\s*AI-Sym Page \d+\s*|"
    r"===== PAGE \d+ =====\s*)$"
)

# Do not soft-join onto these (new structural / block starts)
STRUCT_NEXT = re.compile(
    r"^(?:"
    r"[一二三四五六七八九十]、|"
    r"\d+\.\s|"
    r"顶层锚定|"
    r"违规后果声明|"
    r"溯源归档|"
    r"核心防御能力|"
    r"AI-Sym-\d{2}｜|"
    r"执行指令|"
    r"联动逻辑|"
    r"验证逻辑|"
    r"追溯链路|"
    r"https?://"
    r")"
)
# Do not soft-join from these short labels (keep as standalone heads)
STRUCT_PREV = re.compile(
    r"^(?:"
    r"[一二三四五六七八九十]、|"
    r"顶层锚定|"
    r"违规后果声明|"
    r"溯源归档|"
    r"核心防御能力|"
    r")"
)


def extract_body_pages() -> str:
    reader = PdfReader(str(PDF))
    parts: list[str] = []
    for i, page in enumerate(reader.pages):
        if i + 1 < 10:
            continue
        parts.append(f"===== PAGE {i + 1} =====\n{page.extract_text() or ''}")
    return "\n".join(parts)


def clean(body: str) -> str:
    """Strip PDF chrome only; keep body wording intact (no semantic rewrite)."""
    body = PAGE_NOISE.sub("", body)
    lines = [ln.rstrip() for ln in body.splitlines()]
    out: list[str] = []

    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue

        # Drop exact consecutive duplicates (page overlap)
        j = len(out) - 1
        while j >= 0 and out[j] == "":
            j -= 1
        if j >= 0 and ln == out[j]:
            continue

        # Drop short suffix overlap fragment from page carry
        if j >= 0 and 1 <= len(ln) <= 16 and out[j].endswith(ln):
            continue

        # Soft-join ONLY when previous line is clearly mid-wrap (not a structure line)
        # and current continues the same sentence (common PDF line-break artifact).
        if out and out[-1]:
            prev = out[-1]
            # Title line wrap: AI-Sym-XX｜....错 \\n 位
            if re.match(r"^AI-Sym-\d{2}｜", prev) and not STRUCT_NEXT.match(ln) and len(ln) <= 12:
                if not prev.endswith(("。", "；", "：", "！", "？")):
                    out[-1] = prev + ln.lstrip()
                    continue
            # URL / path wrap: ...内核 \\n 部署包
            if prev.endswith("内核") and ln.strip() == "部署包":
                out[-1] = prev + ln.strip()
                continue
            if (
                not STRUCT_PREV.match(prev)
                and not STRUCT_NEXT.match(ln)
                and len(prev) >= 16
                and not prev.endswith(
                    ("。", "；", "：", "！", "？", "…", "、", "，", ",", ";", ":", "）", ")")
                )
                and re.search(r"[\u4e00-\u9fffA-Za-z0-9_{}\\]$", prev)
                and re.match(r"^[\u4e00-\u9fffA-Za-z0-9_{}\\]", ln)
            ):
                out[-1] = prev + ln.lstrip()
                continue

        out.append(ln)

    text = "\n".join(out).strip() + "\n"
    # Heal page-break blank between mid-sentence wraps: ...多指\\n\\n样本修复...
    text = re.sub(
        r"(?<=[\u4e00-\u9fffA-Za-z0-9_{}\\])\n\n(?=[\u4e00-\u9fffA-Za-z0-9_{}\\])",
        "\n",
        text,
    )
    # Second pass soft-join remaining mid-sentence newlines
    fixed_lines: list[str] = []
    for ln in text.splitlines():
        if not ln.strip():
            if fixed_lines and fixed_lines[-1] != "":
                fixed_lines.append("")
            continue
        if fixed_lines and fixed_lines[-1] and not STRUCT_PREV.match(fixed_lines[-1]) and not STRUCT_NEXT.match(ln):
            prev = fixed_lines[-1]
            if (
                len(prev) >= 16
                and not prev.endswith(("。", "；", "：", "！", "？", "…", "、", "，", ",", ";", ":", "）", ")"))
                and re.search(r"[\u4e00-\u9fffA-Za-z0-9_{}\\]$", prev)
                and re.match(r"^[\u4e00-\u9fffA-Za-z0-9_{}\\]", ln)
            ):
                fixed_lines[-1] = prev + ln.lstrip()
                continue
        fixed_lines.append(ln)
    text = "\n".join(fixed_lines).strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def main() -> None:
    raw = extract_body_pages()
    starts = list(re.finditer(r"(AI-Sym-(\d{2})｜)", raw))
    filtered = []
    for m in starts:
        window = raw[m.start() : m.start() + 500]
        if "一、现象具象表征" in window:
            filtered.append(m)
    starts = filtered
    codes = [m.group(2) for m in starts]
    print("found", codes)
    if codes != [f"{i:02d}" for i in range(1, 19)]:
        raise SystemExit(f"unexpected codes: {codes}")

    required_heads = [
        "一、现象具象表征",
        "二、故障直观影响",
        "三、故障浅层诱因",
        "四、临时应急兜底手段",
        "五、六维法理闭环注解",
        "六、CI流水线拦截指令集",
        "七、裸金属物理定律级免疫系统",
        "违规后果声明",
        "溯源归档",
    ]

    for i, m in enumerate(starts):
        code_n = m.group(2)
        code = f"AI-Sym-{code_n}"
        end = starts[i + 1].start() if i + 1 < len(starts) else len(raw)
        body = clean(raw[m.start() : end])
        miss = [h for h in required_heads if h not in body]
        if miss:
            raise SystemExit(f"{code} missing sections: {miss}")
        # Guard against header-body glue bugs
        if re.search(r"三、故障浅层诱因[\u4e00-\u9fff]", body):
            raise SystemExit(f"{code}: section header glued to body")
        if re.search(r"违规后果声明[\u4e00-\u9fff]", body):
            raise SystemExit(f"{code}: 违规后果声明 glued")
        if re.search(r"溯源归档[\u4e00-\u9fff]", body):
            raise SystemExit(f"{code}: 溯源归档 glued")
        doc = YAML.format(code=code) + body
        fname = f"{code}_{TITLES[code_n]}.md"
        write_utf8(OUT / fname, doc)
        print("wrote", fname, "chars", len(doc))


if __name__ == "__main__":
    main()
