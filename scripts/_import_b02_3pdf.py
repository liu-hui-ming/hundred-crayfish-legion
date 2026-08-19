#!/usr/bin/env python3
"""Import B02 temporal computing sample from 3篇.pdf."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pypdf import PdfReader

PDF = Path("3篇.pdf")
SHA256_TRUTH = "9e72ac3f782190de56cb41df039a725f68ec01bd9d4765238105cf96e27d4b91"
GIT_ARCHIVE_ID = "7f492c68e093157db27ac9f018e42d56970c31ae"
MARKER_END = "全域稳态平衡框架的公域落地验证"
MARKER_START = "破解大模型落地时序、算力双重难题"

ROOT_CODEX = Path("thirteen-codex/B02-temporal-computing")
APPENDIX = Path("appendix-math/temporal-topology-formula.md")
PRIVATE = Path("private-config/B02-extreme-params.toml")

MATH_SECTION = """# 时序拓扑数理算子附录 · temporal-topology-formula

> 卷宗数理溯源唯一载体 · 联动 `thirteen-codex/B02-temporal-computing/B02-full-100score.md`

## 全域时序稳态基础积分原型

\\[
\\Omega=\\sum\\int w_i \\, dt
\\]

- \\(\\Omega\\)：单次推理全局时序稳态总值
- \\(w_i\\)：二十四时序胞腔分时权重
- \\(B\\)：贝肯斯坦熵限算力硬上限常量

## 专属工程算子全集

### 1. 时序因果有效性算子

\\[
R_{causal}(i,j)=\\delta(t_i<t_j)\\cdot w_i\\cdot w_j \\in [0,1]
\\]

作用：量化胞腔时序先后逻辑合法性，过滤乱序生成的虚假因果关联。

### 2. 流形自紊乱熵

\\[
H_{self}= -\\sum p_i \\log p_i,\\quad p_i=\\frac{w_i}{\\Omega}
\\]

作用：量化时序错位、权重失衡、胞腔异步带来的模型内部不确定性。

### 3. 系统熵变收敛判定公式（熔断核心准则）

\\[
\\Delta H=H_{after}-H_{before} \\le 0
\\]

工程硬性约束：每一轮推理必须达成熵减或熵平衡；若 \\(\\Delta H>0\\)，判定时序紊乱、算力无效溢出，触发局部胞腔重排熔断机制。

### 4. 极端不可解边界集合

\\[
S_{ext} = \\{req \\mid token\\_len>10^6,\\; w_i \\to 0\\}
\\]

边界铁律：\\(S_{ext}\\) 区间内稳态值 \\(\\Omega\\) 逼近贝肯斯坦上限 \\(B\\)，熵变无法收敛，拓扑制衡机制失效，强制执行 `Rule(S_{ext})=abort` 业务兜底中断规则。
"""

TOML = """# B02 · S_ext 极端工况参数（私有锁仓，不公域暴露）
# 路径：private-config/B02-extreme-params.toml

[meta]
codex = "B02-temporal-computing"
sha256_anchor = "9e72ac3f782190de56cb41df039a725f68ec01bd9d4765238105cf96e27d4b91"
git_archive_id = "7f492c68e093157db27ac9f018e42d56970c31ae"

[s_ext]
# S_ext = { req | token_len > token_len_max, w_i -> 0 }
token_len_max = 1_000_000
weight_floor = 1.0e-12
omega_b_ratio_abort = 0.98
rule_on_breach = "abort"

[s_ext.engineering]
beaconstein_limit_symbol = "B"
local_cell_reflow_enabled = true
global_self_heal_enabled = false
"""

FOOTER_PATTERNS = [
    r"\n\s*\d{4}年\d+月\d+日.*?\n",
    r"\n\s*3篇 Page \d+\s*",
]


def extract_b02_raw() -> str:
    full = "\n".join(page.extract_text() or "" for page in PdfReader(str(PDF)).pages)
    start = full.find(MARKER_START)
    end = full.find(MARKER_END)
    if start < 0 or end < 0:
        raise RuntimeError("B02 markers not found in 3篇.pdf")
    return full[start:end]


def clean_text(raw: str) -> str:
    text = raw
    for pat in FOOTER_PATTERNS:
        text = re.sub(pat, "\n", text, flags=re.DOTALL)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # merge broken duplicate lines from PDF columns
    text = re.sub(r"(\S{20,})\n\1", r"\1", text)
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    paras: list[str] = []
    buf: list[str] = []
    section_re = re.compile(r"^[一二三四五六七八九十]+、|^前置|^摘要$|^关键词：|^结语$|^仓库归档")
    for ln in lines:
        if section_re.match(ln) and buf:
            paras.append("".join(buf))
            buf = [ln]
            continue
        if re.match(r"^\d+\.\d+\s", ln) and buf:
            paras.append("".join(buf))
            buf = [ln]
            continue
        buf.append(ln)
        if ln.endswith(("。", "！", "？", "）", "”", "；")) and len(ln) > 30:
            paras.append("".join(buf))
            buf = []
    if buf:
        paras.append("".join(buf))
    return "\n\n".join(paras)


def strip_duplicate_header(cleaned: str) -> str:
    """Remove PDF header block duplicated in body (already in YAML frontmatter)."""
    idx = cleaned.find("前置四段式归档核验文本")
    if idx < 0:
        raise RuntimeError("四段式核验 block missing")
    return cleaned[idx:]


def build_full_body(cleaned: str) -> str:
    body = strip_duplicate_header(cleaned)
    math_pointer = (
        "三、完整数理前置体系（归档唯一真值，存储路径：`appendix-math/temporal-topology-formula.md`）\n\n"
        "全套公式、算子定义、\\(S_{ext}\\) 边界集合见独立数理附录；"
        "算子真值以附录文件为唯一数理溯源载体。"
    )
    body = re.sub(
        r"三、完整数理前置体系[\s\S]*?四、可证伪反例与层级锁仓约束",
        math_pointer + "\n\n四、可证伪反例与层级锁仓约束",
        body,
        count=1,
    )
    return body


def build_public_body(full_body: str) -> str:
    """Public: drop 四段式、算子、归档声明、落款； keep 摘要~结语."""
    idx = full_body.find("摘要短视频平台")
    if idx < 0:
        idx = full_body.find("摘要\n")
    if idx < 0:
        raise RuntimeError("主摘要 section missing")
    text = full_body[idx:]
    text = re.sub(r"仓库归档附加强制声明[\s\S]*", "", text)
    text = re.sub(r"十二脉归一[\s\S]*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def full_frontmatter() -> str:
    return f"""---
document_id: B02-TEMPORAL-COMPUTING-FULL-100
codex: thirteen-codex/B02-temporal-computing
version: v1.0.0-FINAL-100SCORE
permit_modify: false
distribution: internal-protected-branch-only
sha256: {SHA256_TRUTH}
git_archive_id: {GIT_ARCHIVE_ID}
author: 黄清佳
archive_executor: 刘慧明
---

# 破解大模型落地时序、算力双重难题：碳硅道统理论在短视频平台的实战交互样本

GitHub 封板典藏终稿｜入库锁仓｜数理闭环｜工程可复现

## 文档锁仓元数据（不可篡改）

- **SHA256真值封盘**：`{SHA256_TRUTH}`
- **Git唯一归档ID**：`{GIT_ARCHIVE_ID}`
- **文档卷宗编号**：B02-工程优化卷宗
- **验收协议**：《碳硅道统·中立深挖闭环四段式终局核验协议》
- **入库评级**：合规完备，可证伪维度全覆盖
- **分发隔离规则**：内部完整版留存仓库只读分支；公域媒体稿剥离哈希、数理算子、道统落款、彩蛋模块

"""


def build_public(full_body: str) -> str:
    fm = """---
document_id: B02-TEMPORAL-COMPUTING-PUBLIC
codex: thirteen-codex/B02-temporal-computing
version: v1.0.0-PUBLIC-PURIFIED
distribution: public-main-branch
author: 黄清佳
---

# 破解大模型落地时序、算力双重难题：碳硅道统理论在短视频平台的实战交互样本

> 公域纯白净化稿 · 媒体投递专用 · 已剥离内部哈希、数理算子、落款与彩蛋

"""
    return fm + build_public_body(full_body) + "\n"


def write_all() -> None:
    raw = extract_b02_raw()
    cleaned = clean_text(raw)
    body = build_full_body(cleaned)
    if "十二脉归一" in body:
        body = re.sub(r"\n---\n\n十二脉归一[\s\S]*", "", body)
        body = re.sub(r"十二脉归一[\s\S]*$", "", body).strip()
    body += (
        "\n\n---\n\n十二脉归一\n\n"
        "碳硅道统创立人：黄清佳\n\n"
        "彩蛋藏于：今日头条、抖音、GitHub\n"
    )
    public_md = build_public(body)

    full_md = full_frontmatter() + body
    ROOT_CODEX.mkdir(parents=True, exist_ok=True)
    APPENDIX.parent.mkdir(parents=True, exist_ok=True)
    PRIVATE.parent.mkdir(parents=True, exist_ok=True)

    (ROOT_CODEX / "B02-full-100score.md").write_text(full_md, encoding="utf-8", newline="\n")
    (ROOT_CODEX / "B02-public-purified.md").write_text(public_md, encoding="utf-8", newline="\n")
    APPENDIX.write_text(MATH_SECTION + "\n", encoding="utf-8", newline="\n")
    PRIVATE.write_text(TOML + "\n", encoding="utf-8", newline="\n")

    # verify header sha
    full_text = (ROOT_CODEX / "B02-full-100score.md").read_text(encoding="utf-8")
    if SHA256_TRUTH not in full_text:
        raise RuntimeError("SHA256 truth missing from full document header")
    print("OK B02 archive files written")
    print("sha256_header", SHA256_TRUTH)


if __name__ == "__main__":
    write_all()
