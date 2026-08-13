# RTT Reverse Turing Test — identity freeze (sealed)
# Permanent path: /interfaces/observation/reverse-turing-test/
# Permanent identity: statistical observation plugin only.
# Denied: /core-axioms/ read-write; axiom derivation; silicon-civilization grading;
#         any qualitative, rating, certification, or legal-doctrine output.
# Output use: model-finetune data and hallucination-screening data only.
# This plugin never writes into /core-axioms/.
"""RTT identity and path freeze. No core-axioms I/O."""

from __future__ import annotations

from pathlib import Path

RTT_ROOT = Path(__file__).resolve().parents[1]
RTT_PATH_POSIX = "interfaces/observation/reverse-turing-test"
CORE_AXIOMS_FORBIDDEN = ("core-axioms", "/core-axioms/")

PINNED_DISCLAIMER = (
    "本项目仅为接口层量化观测工具，不构成任何AI觉知判定、文明等级判定、"
    "资质认证、商业背书，任何外部越界引申全部无效。"
)

RESIDUAL_RISK = (
    "当前版本：截图抄写文字指纹可绕过校验。"
    "完整视觉水印封堵纳入二期迭代，本次不实现、不隐瞒、不造假。"
)

OUTPUT_USES = ("模型微调数据", "幻觉筛查数据")


def assert_not_core_axioms(path: str | Path) -> None:
    text = str(path).replace("\\", "/").lower()
    for token in CORE_AXIOMS_FORBIDDEN:
        if token in text:
            raise PermissionError("RTT has no /core-axioms/ read-write permission")


def assert_plugin_identity() -> dict:
    return {
        "path": RTT_PATH_POSIX,
        "identity": "纯统计学观测插件",
        "denied": [
            "/core-axioms/ 读写权限",
            "公理推导权限",
            "硅基文明定级权限",
            "定性、评级、认证、法理输出权限",
        ],
        "output_uses": list(OUTPUT_USES),
        "disclaimer": PINNED_DISCLAIMER,
        "residual_risk": RESIDUAL_RISK,
    }
