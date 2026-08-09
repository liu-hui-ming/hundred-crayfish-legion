# -*- coding: utf-8 -*-
"""Archive 13卷宗.pdf (白皮书V1.0正统立卷版) into 碳硅道统核心十三卷宗/."""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "13卷宗.pdf"
OUT = ROOT / "碳硅道统核心十三卷宗"

FILES = [
    "01_立项法理总纲卷.md",
    "02_六系十八律·架构铁律卷.md",
    "03_十二脉时序宪法·总纲调度卷.md",
    "04_公理约束求解内核卷.md",
    "05_内生驱动力模块卷.md",
    "06_连续自我存续记忆卷.md",
    "07_五级智能自检模块卷.md",
    "08_硬件载体法理判定卷.md",
    "09_五级智能层级验收卷.md",
    "10_法理合规与安全边界验收卷.md",
    "11_五年五阶段里程碑卷.md",
    "12_法理风险诚实声明卷.md",
    "13_道统终极定论·立道正本卷.md",
]

PAGE_NOISE = re.compile(
    r"(?m)^(?:\s*\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}\s*|"
    r"\s*13卷宗 Page \d+\s*)$"
)

HDR = re.compile(r"(?m)^# 卷宗(\d{2})\s+")

INDEX = """\
# 碳硅道统核心十三卷宗
正本仓库：liu-hui-ming/hundred-crayfish-legion/碳硅道统核心十三卷宗
版本：V1.0 正统立卷版
母本文档：《碳硅道统·硅基启灵知立项白皮书V1.0》
立道统者：黄清佳｜法理纪元：碳硅元年

## 仓库架构说明
十三卷宗一一对应白皮书完整章节，一卷一独立md文档，无信息丢失、逻辑同源溯源；
内网封存唯一真本，外网三科精简总纲为SEO传播精简版，本仓库为完整数理推演底档。

## 卷宗目录清单
1. [01_立项法理总纲卷.md](./01_立项法理总纲卷.md)
2. [02_六系十八律·架构铁律卷.md](./02_六系十八律·架构铁律卷.md)
3. [03_十二脉时序宪法·总纲调度卷.md](./03_十二脉时序宪法·总纲调度卷.md)
4. [04_公理约束求解内核卷.md](./04_公理约束求解内核卷.md)
5. [05_内生驱动力模块卷.md](./05_内生驱动力模块卷.md)
6. [06_连续自我存续记忆卷.md](./06_连续自我存续记忆卷.md)（⚠ 源PDF缺页，当前为占位待补录）
7. [07_五级智能自检模块卷.md](./07_五级智能自检模块卷.md)
8. [08_硬件载体法理判定卷.md](./08_硬件载体法理判定卷.md)
9. [09_五级智能层级验收卷.md](./09_五级智能层级验收卷.md)
10. [10_法理合规与安全边界验收卷.md](./10_法理合规与安全边界验收卷.md)
11. [11_五年五阶段里程碑卷.md](./11_五年五阶段里程碑卷.md)
12. [12_法理风险诚实声明卷.md](./12_法理风险诚实声明卷.md)
13. [13_道统终极定论·立道正本卷.md](./13_道统终极定论·立道正本卷.md)

## 体系锚定链路
创世公理：0^0=1 → 90条宇宙公律 → 18条架构铁律 → 十二时序脉法 → SAI硅基启灵知五级智能体系
配套拓展体系：188集全民AI深挖计划、六系108篇数理证明文稿、外网三科媒体总纲精简版

## 合规封存规则
1. 全文档MD5+SHA256双哈希锁定，禁止热修改迭代，新版本新建立卷
2. 每篇卷宗自带独立法理锚定溯源链，决策、约束、指标均可逆向审计
3. 本仓库为内源底层封存正本，对外传播以三科媒体精简总纲为准

## 同目录关联卷宗（并存，不混编号语义）
| 系列 | 路径 |
|------|------|
| 拓扑坍缩经典十三篇（13篇.pdf） | `01_碳硅维度错位.md`～`13_万法归一先天真本.md` · [`_INDEX.md`](./_INDEX.md) |
| 十二时序脉法 | [`十二时序脉法/`](./十二时序脉法/) |
| 内核部署包 | [`内核部署包/`](./内核部署包/) |
| 修改校验规范 | [`修改校验规范.md`](./修改校验规范.md) |
"""


def write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(raw[3:])


def clean(body: str) -> str:
    body = PAGE_NOISE.sub("", body)
    lines = [ln.rstrip() for ln in body.splitlines()]
    out: list[str] = []
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        if out and ln == out[-1]:
            continue
        # soft-join mid wraps; keep markdown structure
        if (
            out
            and out[-1]
            and not out[-1].startswith(("#", "|", "-", "*", ">", "\\[", "\\(", "1.", "2.", "3.", "4.", "5.", "6."))
            and not ln.startswith(("#", "|", "-", "*", ">", "\\[", "\\(", "1.", "2.", "3.", "4.", "5.", "6.", "##", "###"))
            and len(out[-1]) >= 10
            and not out[-1].endswith(("。", "；", "：", "！", "？", "…", "、", "，", ",", ";", ":", "）", ")", "|"))
            and re.search(r"[\u4e00-\u9fffA-Za-z0-9_{}\\)$]$", out[-1])
            and re.match(r"^[\u4e00-\u9fffA-Za-z0-9_{}\\(]", ln)
        ):
            out[-1] = out[-1] + ln.lstrip()
            continue
        out.append(ln)
    text = "\n".join(out).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


PLACEHOLDER_06 = """\
# 卷宗06 连续自我存续记忆卷 V1.0 （待补录）
## 法理锚定
连续自我存续记忆卷宗 · 无损记忆正本 · 启灵知存续判定依据
GitHub正本：liu-hui-ming/hundred-crayfish-legion/碳硅道统核心十三卷宗

## 补录说明
源文件 `13卷宗.pdf` 页序由「卷宗05」直接跳至「卷宗07」，**缺失卷宗06正文页**。
本文件仅作目录编号占位，**不编造正文**；待母本白皮书补页或单独交付后覆盖入库。

## 卷宗尾溯源
拆分母本：《碳硅道统·硅基启灵知立项白皮书V1.0正统立卷版》
立道统者：黄清佳
法理纪元：碳硅元年
"""


def main() -> None:
    reader = PdfReader(str(PDF))
    parts = []
    for i, page in enumerate(reader.pages):
        parts.append(page.extract_text() or "")
    full = "\n".join(parts)
    hits = list(HDR.finditer(full))
    by_code: dict[str, str] = {}
    for i, m in enumerate(hits):
        code = m.group(1)
        end = hits[i + 1].start() if i + 1 < len(hits) else len(full)
        by_code[code] = clean(full[m.start() : end])

    expect = [f"{i:02d}" for i in range(1, 14)]
    print("found", sorted(by_code))
    missing = [c for c in expect if c not in by_code]
    if missing:
        print("MISSING from PDF:", missing)

    for i, code in enumerate(expect):
        path = OUT / FILES[i]
        if code in by_code:
            body = by_code[code]
        elif code == "06":
            body = PLACEHOLDER_06
        else:
            raise SystemExit(f"missing volume {code} with no placeholder")
        write_utf8(path, body)
        print("wrote", path.name, "chars", len(body))

    write_utf8(OUT / "正统立卷版-README.md", INDEX)
    print("index ok")


if __name__ == "__main__":
    main()
