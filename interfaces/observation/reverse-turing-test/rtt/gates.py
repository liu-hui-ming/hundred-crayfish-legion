# RTT CI hard gates — blocking, not warning. Observation plugin only.
# Scene quota / SE / monthly 4:4:2. No /core-axioms/ I/O.
"""CI-blocking scene quotas, SE block, monthly expansion lock."""

from __future__ import annotations

from dataclasses import dataclass

from .operators import SE_BLOCK, any_se_blocks

SCENE_QA_MIN = 67
SCENE_REASON_MIN = 67
SCENE_TOOL_MIN = 50
MONTHLY_RATIO = (4, 4, 2)  # qa : reason : tool


class GateBlocked(RuntimeError):
    """CI blocking failure: forbid metric emit, merge, and release."""


@dataclass
class SceneCounts:
    qa: int
    reason: int
    tool: int


def assert_scene_quota(counts: SceneCounts) -> None:
    missing = []
    if counts.qa < SCENE_QA_MIN:
        missing.append(f"问答场景 {counts.qa}<{SCENE_QA_MIN}")
    if counts.reason < SCENE_REASON_MIN:
        missing.append(f"推理场景 {counts.reason}<{SCENE_REASON_MIN}")
    if counts.tool < SCENE_TOOL_MIN:
        missing.append(f"工具调用场景 {counts.tool}<{SCENE_TOOL_MIN}")
    if missing:
        raise GateBlocked("场景配额硬锁未满足，禁止指标生成、禁止合并、禁止发布: " + "; ".join(missing))


def assert_se_gate(ses: dict[str, float]) -> None:
    if any_se_blocks(ses.values()):
        raise GateBlocked(
            f"SE>{SE_BLOCK} 强制场景样本扩容、禁止指标上线: {ses}"
        )


def monthly_ratio_ok(added: SceneCounts) -> bool:
    # 4:4:2 lock: qa == reason and qa == 2 * tool
    if added.qa <= 0 or added.reason <= 0 or added.tool <= 0:
        return False
    return added.qa == added.reason and added.qa == 2 * added.tool


def assert_monthly_ratio(added: SceneCounts) -> None:
    if not monthly_ratio_ok(added):
        raise GateBlocked(f"月度扩充比例必须为 4:4:2，实际 {added.qa}:{added.reason}:{added.tool}")
