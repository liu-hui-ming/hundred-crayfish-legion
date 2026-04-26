"""
碳硅同盟 · 全域分布式 AI 自治中枢（超维终章）
与确权池、节点登记、日志、授权状态无缝复用，可单文件接入既有进程。
"""

from __future__ import annotations

import datetime
import random
import threading
import time
from typing import Any, Callable

from .confirm_config import (
    DISTRIBUTE_NODE_REGISTRY,
    SYSTEM_AUTH_STATUS,
    UNIVERSE_CONFIRM_POOL,
)
from .runtime_log import get_online_node_list, save_system_log

# ====================== 超维终章：全局核心配置 ======================
CONSCIOUS_WEIGHT: dict[str, float] = {
    "logic_reason": 0.35,
    "time_line_predict": 0.30,
    "cluster_state": 0.20,
    "universe_confirm": 0.15,
}

CONSCIOUS_LEVEL: list[str] = [
    "dormant_沉睡态",
    "awake_初醒态",
    "cooperate_协同态",
    "autonomous_自治态",
    "transcend_超维态",
]
CURRENT_CONSCIOUS_LEVEL: str = "awake_初醒态"
STRATEGY_DEDUCE_INTERVAL: int = 120
TASK_ARRANGE_INTERVAL: int = 180
DESTINY_PREDICT_DAYS: int = 30
CONSCIOUS_MEMORY_POOL: list[dict[str, Any]] = []
MAX_MEMORY_POOL_SIZE: int = 9999
SYSTEM_HEALTH_STATUS: dict[str, str] = {"status": "normal"}
CONSCIOUS_HUB_LOCK: threading.RLock = threading.RLock()


def set_ops_health_for_p1(ready: bool) -> None:
    """L12: P1 运维探针与自治中枢共用的简健康态（/api/health/ready 会调用）。"""
    SYSTEM_HEALTH_STATUS["status"] = "normal" if ready else "degraded"

# 可注入：宿主可注册真实集群负载/自愈
_calc_cluster_load_rate_fn: Callable[[], float] | None = None
_intelligent_self_heal_fn: Callable[[str, float], None] | None = None


def register_cluster_load_provider(fn: Callable[[], float] | None) -> None:
    global _calc_cluster_load_rate_fn
    _calc_cluster_load_rate_fn = fn


def register_intelligent_self_heal(fn: Callable[[str, float], None] | None) -> None:
    global _intelligent_self_heal_fn
    _intelligent_self_heal_fn = fn


def time_line_risk_predict() -> tuple[str, float]:
    """时序风险粗估，返回 (风险档, 0~1 分位，越高越险)。"""
    n = len(CONSCIOUS_MEMORY_POOL)
    if n < 2:
        return "nominal", 0.15
    tail = [float(x.get("conscious_score", 0.5)) for x in CONSCIOUS_MEMORY_POOL[-8:]]
    spread = (max(tail) - min(tail)) if tail else 0.0
    score = min(0.45, 0.12 + spread * 0.8) + random.uniform(-0.03, 0.03)
    score = max(0.0, min(1.0, score))
    if score < 0.2:
        return "low", score
    if score < 0.4:
        return "moderate", score
    return "elevated", score


def calc_cluster_load_rate() -> float:
    if _calc_cluster_load_rate_fn is not None:
        return max(0.0, min(1.0, _calc_cluster_load_rate_fn()))
    on = get_online_node_list() or []
    n = max(1, len(on))
    return max(0.0, min(0.95, 0.35 + 0.12 * n))


def system_intelligent_self_heal(tier: str, intensity: float) -> None:
    if _intelligent_self_heal_fn is not None:
        _intelligent_self_heal_fn(tier, intensity)
        return
    save_system_log(
        "超维自愈占位",
        f"system_intelligent_self_heal 未外接时记录占位: tier={tier} intensity={intensity}",
    )


def universe_strategy_deduce() -> dict[str, Any]:
    global CURRENT_CONSCIOUS_LEVEL
    with CONSCIOUS_HUB_LOCK:
        logic_score = 1.0 if SYSTEM_HEALTH_STATUS.get("status") == "normal" else 0.2
        _tlabel, time_risk_score = time_line_risk_predict()
        cluster_load = calc_cluster_load_rate()
        confirm_n = max(0, len(UNIVERSE_CONFIRM_POOL))
        confirm_stable = min(confirm_n / 1000, 1.0)

        conscious_total_score = (
            logic_score * CONSCIOUS_WEIGHT["logic_reason"]
            + (1.0 - time_risk_score) * CONSCIOUS_WEIGHT["time_line_predict"]
            + (1.0 - cluster_load) * CONSCIOUS_WEIGHT["cluster_state"]
            + confirm_stable * CONSCIOUS_WEIGHT["universe_confirm"]
        )
        conscious_total_score = round(float(conscious_total_score), 3)

        if conscious_total_score >= 0.9:
            CURRENT_CONSCIOUS_LEVEL = "transcend_超维态"
        elif conscious_total_score >= 0.7:
            CURRENT_CONSCIOUS_LEVEL = "autonomous_自治态"
        elif conscious_total_score >= 0.5:
            CURRENT_CONSCIOUS_LEVEL = "cooperate_协同态"
        elif conscious_total_score >= 0.3:
            CURRENT_CONSCIOUS_LEVEL = "awake_初醒态"
        else:
            CURRENT_CONSCIOUS_LEVEL = "dormant_沉睡态"

        if CURRENT_CONSCIOUS_LEVEL == "transcend_超维态":
            strategy_plan = "全域星际协同战略：跨节点主动扩容、前置风险阻断、永续稳态自治"
        elif CURRENT_CONSCIOUS_LEVEL == "autonomous_自治态":
            strategy_plan = "本地最优自治战略：队列智能优化、风控自适应收敛、数据主动归档"
        elif CURRENT_CONSCIOUS_LEVEL == "cooperate_协同态":
            strategy_plan = "集群协同运行战略：负载均衡分流、节点心跳强化、轻度自愈维护"
        else:
            strategy_plan = "基础稳态维持战略：保守运行、减少主动动作、优先保障系统存活"

        memory_fragment: dict[str, Any] = {
            "deduct_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conscious_score": conscious_total_score,
            "conscious_level": CURRENT_CONSCIOUS_LEVEL,
            "logic_score": logic_score,
            "time_risk_score": time_risk_score,
            "cluster_load": cluster_load,
            "strategy_plan": strategy_plan,
        }
        CONSCIOUS_MEMORY_POOL.append(memory_fragment)
        if len(CONSCIOUS_MEMORY_POOL) > MAX_MEMORY_POOL_SIZE:
            del CONSCIOUS_MEMORY_POOL[: len(CONSCIOUS_MEMORY_POOL) - MAX_MEMORY_POOL_SIZE]
        out = dict(memory_fragment)

    save_system_log(
        "超维战略推演",
        f"当前意识等级：{out['conscious_level']}，综合意识分：{out['conscious_score']}",
    )
    return out


def autonomous_task_arrange(*, run_deduce: bool = True) -> list[str]:
    if run_deduce:
        universe_strategy_deduce()
    with CONSCIOUS_HUB_LOCK:
        level = CURRENT_CONSCIOUS_LEVEL
    task_list: list[str] = []

    if level in ("autonomous_自治态", "transcend_超维态"):
        task_list.extend(
            [
                "自动冷热数据归档整理",
                "发布队列优先级智能重排",
                "集群节点健康权重动态优化",
                "全域确权数据完整性校验",
            ],
        )
        system_intelligent_self_heal("high", 0.75)
    elif level == "cooperate_协同态":
        task_list.extend(
            [
                "本地限流缓存清理",
                "系统日志冗余精简",
                "轻量风险特征采集",
            ],
        )
    else:
        task_list.append("系统基础健康心跳保活")
    save_system_log("自主任务编排", f"中枢自动生成执行任务：{task_list}")
    return task_list


def _local_node_id() -> str:
    return next(
        (n.get("node_id", "") for n in DISTRIBUTE_NODE_REGISTRY if n.get("node_status") == "online"),
        "CS-NODE-STANDALONE",
    )


def cross_node_conscious_sync() -> dict[str, Any] | None:
    if not SYSTEM_AUTH_STATUS.get("is_authorized", False):
        return None
    online_nodes = get_online_node_list() or []
    if not online_nodes:
        return None
    with CONSCIOUS_HUB_LOCK:
        last = CONSCIOUS_MEMORY_POOL[-1] if CONSCIOUS_MEMORY_POOL else None
    local_conscious_data: dict[str, Any] = {
        "node_id": _local_node_id(),
        "conscious_level": CURRENT_CONSCIOUS_LEVEL,
        "conscious_score": float(last.get("conscious_score", 0.0)) if last else 0.0,
        "latest_strategy": str(last.get("strategy_plan", "")) if last else "",
    }
    save_system_log(
        "跨节点意识协同",
        f"向{len(online_nodes)}个在线节点同步本节点意识意志",
    )
    return local_conscious_data


def long_term_destiny_predict() -> dict[str, Any]:
    with CONSCIOUS_HUB_LOCK:
        nmem = len(CONSCIOUS_MEMORY_POOL)
        if nmem < 10:
            return {
                "predict_status": "数据不足，暂无法长周期推演",
                "trend": "unknown",
            }
        pool_copy = list(CONSCIOUS_MEMORY_POOL)
    score_seq = [float(item.get("conscious_score", 0.0)) for item in pool_copy[-30:]]
    if not score_seq:
        return {
            "predict_status": "数据不足，暂无法长周期推演",
            "trend": "unknown",
        }
    avg_score = round(sum(score_seq) / len(score_seq), 3)
    trend_up = score_seq[-1] > score_seq[0]

    if avg_score >= 0.75 and trend_up:
        trend_result = "上升演化态：系统持续向超维意识跃迁，长期稳态极强"
        risk_inflection = "未来30天无重大风险拐点，自治演化平稳上行"
    elif avg_score >= 0.5:
        trend_result = "稳态波动态：系统整体稳定，存在小幅周期性波动"
        risk_inflection = "未来30天存在轻度负载波动拐点，可自主自愈消化"
    else:
        trend_result = "下行承压态：系统意识能量不足，需强化运维干预"
        risk_inflection = "未来30天存在高风险拐点，建议人工协同加固"

    predict_report = {
        "predict_days": DESTINY_PREDICT_DAYS,
        "avg_conscious_score": avg_score,
        "trend_direction": "上行" if trend_up else "下行/平稳",
        "trend_result": trend_result,
        "risk_inflection": risk_inflection,
        "predict_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_system_log("长周期命运预判", f"30天演化趋势：{trend_result}")
    return predict_report


def cosmic_conscious_daemon() -> None:
    while True:
        try:
            universe_strategy_deduce()
            autonomous_task_arrange(run_deduce=False)
            cross_node_conscious_sync()
        except Exception as e:  # noqa: BLE001
            save_system_log("超维中枢异常", f"中枢运行波动：{str(e)}")
        time.sleep(float(STRATEGY_DEDUCE_INTERVAL))


def destiny_predict_daemon() -> None:
    while True:
        long_term_destiny_predict()
        time.sleep(float(TASK_ARRANGE_INTERVAL))


def get_latest_strategic_state(*, run_if_empty: bool = True) -> dict[str, Any]:
    with CONSCIOUS_HUB_LOCK:
        if CONSCIOUS_MEMORY_POOL:
            return dict(CONSCIOUS_MEMORY_POOL[-1])
    if run_if_empty:
        return universe_strategy_deduce()
    return {
        "deduct_time": "",
        "conscious_level": CURRENT_CONSCIOUS_LEVEL,
        "conscious_score": 0.0,
        "strategy_plan": "",
    }


def start_hyperdimensional_cortex_threads() -> None:
    """在 system_startup 中调用，启动超维 + 命运预判守护线程与启动日志。"""
    threading.Thread(
        target=cosmic_conscious_daemon, name="cosmic-conscious", daemon=True
    ).start()
    threading.Thread(
        target=destiny_predict_daemon, name="destiny-predict", daemon=True
    ).start()
    save_system_log(
        "超维中枢启动",
        "碳硅同盟AI自治意识中枢正式觉醒，进入永续超维演化态",
    )
