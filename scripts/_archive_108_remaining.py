# -*- coding: utf-8 -*-
"""Archive AI-Con/Mis/Inv/Opt/Met (90 articles) from series PDFs."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "carbon-silicon-daotong" / "public-seo" / "108-series-full"

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

# Short Chinese titles for filenames (from PDF headers / Sym catalog crosswalk)
TITLES: dict[str, dict[str, str]] = {
    "AI-Con": {
        "01": "隐空间拓扑约束缺失",
        "02": "Transformer注意力指数衰减",
        "03": "逐Token随机生成固有熵上限",
        "04": "无创脑机信噪比物理上限",
        "05": "硅基自主探索驱动力空白",
        "06": "算力扩容边际收益递减",
        "07": "采样温度熵与输出确定性零和制衡",
        "08": "小样本缺陷并发放大效应",
        "09": "统计拟合公理推理能力天花板",
        "10": "通用智能演化时序下界",
        "11": "领域微调权重固化偏移",
        "12": "人工评价主观偏差固有分布",
        "13": "碳硅权限扩张风险递增",
        "14": "架构内禀熵增优化下限",
        "15": "跨物种脑波频谱特异性",
        "16": "AI技术传播信息不对称",
        "17": "实验室与工业环境参数鸿沟",
        "18": "测评基准时效衰减特性",
    },
    "AI-Mis": {
        "01": "文本表层流畅等价深层逻辑自洽",
        "02": "无限扩容参数算力即可突破通用智能边界",
        "03": "自回归模型可通过对齐实现零幻觉",
        "04": "无监督训练可自主涌现高阶推理能力",
        "05": "脱离人类反馈无监督实现自主迭代进化",
        "06": "忽略权重衰减约束追求无限上下文存储",
        "07": "词汇表层匹配等价深层语义理解",
        "08": "训练集知识重组等同于原创创造",
        "09": "极致安全对齐不会损耗模型泛化能力",
        "10": "基准高分代表实景全域泛化能力",
        "11": "统计相关性直接等价客观因果逻辑",
        "12": "赋予大模型自主主观意识与情绪",
        "13": "低估产业化周期短期实现全行业颠覆",
        "14": "忽视迭代调参算力人力隐性损耗",
        "15": "纯技术手段彻底消解AI衍生社会伦理风险",
        "16": "单一厂商可垄断底层大模型架构形成永久壁垒",
        "17": "硅基智能完整替代人类创造性脑力劳动",
        "18": "架构底层约束属于临时程序Bug可迭代清除",
    },
    "AI-Inv": {
        "01": "视觉拟合失真守恒律",
        "02": "时序注意力指数衰减律",
        "03": "生成幻觉熵存续区间律",
        "04": "无创脑机信号采集上限律",
        "05": "硅基内源驱动力真空律",
        "06": "算力边际收益收敛律",
        "07": "采样熵-生成稳定性制衡律",
        "08": "并发故障幂次放大律",
        "09": "统计模型公理逻辑不可拟合律",
        "10": "通用智能涌现时序下界律",
        "11": "跨域微调权重固有损耗律",
        "12": "人工评分偏差标准差恒定律",
        "13": "碳硅权限风险指数递增律",
        "14": "架构优化缺陷下界守恒律",
        "15": "跨物种脑波频谱差值隔离律",
        "16": "科普传播认知失真偏差律",
        "17": "虚实工况参数差值函数律",
        "18": "测评指标时效衰减导数律",
    },
    "AI-Opt": {
        "01": "骨骼拓扑锚定掩码架构",
        "02": "长序列分段缓存锁止机制",
        "03": "外部知识库真值前置校验框架",
        "04": "多通道信噪比分层补偿算法",
        "05": "链式分层外源任务驱动范式",
        "06": "异构算力分层动态调度模型",
        "07": "采样温度熵收敛稳态调控机制",
        "08": "分布式分层容错推演架构",
        "09": "多层公理分段前置校验逻辑",
        "10": "垂直领域分阶段落地部署范式",
        "11": "主干领域权重解耦微调架构",
        "12": "法理分层客观双轨核验体系",
        "13": "碳硅二元裁决权限隔离架构",
        "14": "缺陷分级场景准入筛选模型",
        "15": "多频段频谱分层滤波解析算法",
        "16": "法理通俗双轨保真传播架构",
        "17": "实景动态偏差自适应补偿算法",
        "18": "底层法理锚定长效建标架构",
    },
    "AI-Met": {
        "01": "图像拓扑保真误差标尺",
        "02": "时序记忆留存指数标尺",
        "03": "生成内容事实真实度分层标尺",
        "04": "神经信号完整还原度标尺",
        "05": "碳硅驱动力差分计量标尺",
        "06": "算力收益衰减拐点计量标尺",
        "07": "生成输出离散度量化标尺",
        "08": "并发故障扩张系数标尺",
        "09": "数理推导严谨度分级标尺",
        "10": "通用智能落地风险计量标尺",
        "11": "跨域迁移故障概率预判标尺",
        "12": "三维智能层级客观计量标尺",
        "13": "碳硅权限越界风险指数标尺",
        "14": "架构缺陷优化下限刚性标尺",
        "15": "跨物种脑波频谱相似度标尺",
        "16": "科普内容客观度打分标尺",
        "17": "理论实景偏差动态补偿标尺",
        "18": "底层恒定法理长效判定标尺",
    },
}

SERIES = [
    # prefix, pdf, page_footer_name, body_anchor_regex (must appear near header)
    ("AI-Con", "AI-Con.pdf", "AI-Con", r"一、本源机理"),
    ("AI-Mis", "AI-Mis.pdf", "AI-Mis", r"谬误内核"),
    ("AI-Inv", "AI-Inv.pdf", "AI-Inv", r"(?:定律底层机理|公式：)"),
    ("AI-Opt", "AI-Opt.pdf", "AI-Opt", r"技术底层逻辑"),
    ("AI-Met", "AI-Met.pdf", "AI-Met", r"指标基础定义"),
]

STRUCT_NEXT = re.compile(
    r"^(?:"
    r"[一二三四五六七八九十]、|"
    r"\d+\.\s|"
    r"顶层锚定|"
    r"违规后果声明|"
    r"溯源归档|"
    r"核心防御能力|"
    r"谬误内核|"
    r"衍生危害|"
    r"落地纠偏准则|"
    r"碳硅六维匹配|"
    r"定律底层机理|"
    r"工程边界约束|"
    r"公式：|"
    r"文字释义：|"
    r"技术底层逻辑|"
    r"工程落地边界|"
    r"指标基础定义|"
    r"量化计算逻辑|"
    r"执行指令|"
    r"联动逻辑|"
    r"验证逻辑|"
    r"追溯链路|"
    r"https?://"
    r")"
)
STRUCT_PREV = re.compile(
    r"^(?:"
    r"[一二三四五六七八九十]、|"
    r"顶层锚定|"
    r"违规后果声明|"
    r"溯源归档|"
    r"核心防御能力|"
    r"谬误内核|"
    r"衍生危害|"
    r"落地纠偏准则|"
    r"碳硅六维匹配|"
    r"定律底层机理|"
    r"工程边界约束|"
    r"公式：|"
    r"文字释义：|"
    r"技术底层逻辑|"
    r"工程落地边界|"
    r"指标基础定义|"
    r"量化计算逻辑|"
    r")"
)


def page_noise(prefix: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^(?:\s*\d{{4}}年\d{{1,2}}月\d{{1,2}}日\s+\d{{1,2}}:\d{{2}}\s*|"
        rf"\s*{re.escape(prefix)} Page \d+\s*|"
        rf"===== PAGE \d+ =====\s*)$"
    )


def extract_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts = []
    for i, page in enumerate(reader.pages):
        parts.append(f"===== PAGE {i + 1} =====\n{page.extract_text() or ''}")
    return "\n".join(parts)


def clean(body: str, prefix: str) -> str:
    body = page_noise(prefix).sub("", body)
    lines = [ln.rstrip() for ln in body.splitlines()]
    out: list[str] = []
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        j = len(out) - 1
        while j >= 0 and out[j] == "":
            j -= 1
        if j >= 0 and ln == out[j]:
            continue
        if j >= 0 and 1 <= len(ln) <= 16 and out[j].endswith(ln):
            continue
        if out and out[-1]:
            prev = out[-1]
            if re.match(rf"^{re.escape(prefix)}-\d{{2}}｜", prev) and not STRUCT_NEXT.match(ln) and len(ln) <= 20:
                if not prev.endswith(("。", "；", "：", "！", "？")):
                    out[-1] = prev + ln.lstrip()
                    continue
            if prev.endswith("内核") and ln.strip() == "部署包":
                out[-1] = prev + ln.strip()
                continue
            if (
                not STRUCT_PREV.match(prev)
                and not STRUCT_NEXT.match(ln)
                and len(prev) >= 16
                and not prev.endswith(("。", "；", "：", "！", "？", "…", "、", "，", ",", ";", ":", "）", ")"))
                and re.search(r"[\u4e00-\u9fffA-Za-z0-9_{}\\]$", prev)
                and re.match(r"^[\u4e00-\u9fffA-Za-z0-9_{}\\]", ln)
            ):
                out[-1] = prev + ln.lstrip()
                continue
        out.append(ln)

    text = "\n".join(out).strip() + "\n"
    text = re.sub(
        r"(?<=[\u4e00-\u9fffA-Za-z0-9_{}\\])\n\n(?=[\u4e00-\u9fffA-Za-z0-9_{}\\])",
        "\n",
        text,
    )
    fixed: list[str] = []
    for ln in text.splitlines():
        if not ln.strip():
            if fixed and fixed[-1] != "":
                fixed.append("")
            continue
        if fixed and fixed[-1] and not STRUCT_PREV.match(fixed[-1]) and not STRUCT_NEXT.match(ln):
            prev = fixed[-1]
            if (
                len(prev) >= 16
                and not prev.endswith(("。", "；", "：", "！", "？", "…", "、", "，", ",", ";", ":", "）", ")"))
                and re.search(r"[\u4e00-\u9fffA-Za-z0-9_{}\\]$", prev)
                and re.match(r"^[\u4e00-\u9fffA-Za-z0-9_{}\\]", ln)
            ):
                fixed[-1] = prev + ln.lstrip()
                continue
        fixed.append(ln)
    text = "\n".join(fixed).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def find_starts(full: str, prefix: str, anchor: str) -> list[re.Match[str]]:
    starts: list[re.Match[str]] = []
    for m in re.finditer(rf"{re.escape(prefix)}-(\d{{2}})｜", full):
        window = full[m.start() : m.start() + 900]
        if not re.search(anchor, window):
            continue
        code = m.group(1)
        if starts and starts[-1].group(1) == code:
            continue
        starts.append(m)
    return starts


def archive_series(prefix: str, pdf_name: str, footer: str, anchor: str) -> list[Path]:
    pdf = ROOT / pdf_name
    full = extract_pdf(pdf)
    starts = find_starts(full, prefix, anchor)
    codes = [m.group(1) for m in starts]
    expect = [f"{i:02d}" for i in range(1, 19)]
    if codes != expect:
        raise SystemExit(f"{prefix}: unexpected codes {codes}")

    written: list[Path] = []
    for i, m in enumerate(starts):
        code_n = m.group(1)
        code = f"{prefix}-{code_n}"
        end = starts[i + 1].start() if i + 1 < len(starts) else len(full)
        body = clean(full[m.start() : end], footer)
        if not body.startswith(code):
            raise SystemExit(f"{code}: body header mismatch")
        title = TITLES[prefix][code_n]
        doc = YAML.format(code=code) + body
        path = OUT / f"{code}_{title}.md"
        write_utf8(path, doc)
        print("wrote", path.name, "chars", len(doc))
        written.append(path)
    return written


def main() -> None:
    all_paths: list[Path] = []
    for prefix, pdf_name, footer, anchor in SERIES:
        print("===", prefix)
        all_paths.extend(archive_series(prefix, pdf_name, footer, anchor))
    print("total_new", len(all_paths))
    sym = list(OUT.glob("AI-Sym-*.md"))
    print("sym_existing", len(sym), "grand_total", len(sym) + len(all_paths))


if __name__ == "__main__":
    main()
