from __future__ import annotations

import os
from functools import wraps
from typing import Any, Callable, TypeVar

from flask import Flask, jsonify, redirect, request, send_from_directory

from .alliance_layers import (
    layers_to_public_dicts,
)
from .confirm_config import (
    ALLIANCE_12L_ARCHITECTURE_ID,
    ALLIANCE_TIER_COUNT,
    CONFIRM_DATA_TYPE,
    INTERSTELLAR_SYNC_INTERVAL,
    UNIVERSE_API_TOKEN,
    UNIVERSE_CONFIRM_POOL,
)
from .confirm_sync import query_universe_confirm, save_universe_confirm_data
from .runtime_log import get_online_node_list
from .autonomous_cortex import (
    autonomous_task_arrange,
    get_latest_strategic_state,
    long_term_destiny_predict,
    universe_strategy_deduce,
    CURRENT_CONSCIOUS_LEVEL,
    CONSCIOUS_MEMORY_POOL,
)

F = TypeVar("F", bound=Callable[..., Any])

# 与规格一致：可挂载为全局 API 应用
API_APP = Flask(__name__, static_folder=None)
_P1_STATIC = os.path.join(os.path.dirname(__file__), "static", "p1")


def api_token_authentication(f: F) -> F:
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        auth = request.headers.get("Authorization", "") or ""
        token: str
        if auth.lower().startswith("bearer "):
            token = auth[7:].strip()
        else:
            token = (request.headers.get("X-CS-Token", "") or "").strip()
        if not token or token != UNIVERSE_API_TOKEN:
            return jsonify({"code": 401, "msg": "未授权"}), 401
        return f(*args, **kwargs)

    return decorated  # type: ignore[return-value]


def _hcl_p2_easter_enabled() -> bool:
    return (os.environ.get("HCL_P2_EASTER") or "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


@API_APP.route("/api/health/live", methods=["GET"])
def api_health_live() -> Any:
    return jsonify(
        {
            "status": "live",
            "service": "hcl-carbon-silicon",
            "p1": "liveness",
            "hcl_p2_easter": _hcl_p2_easter_enabled(),
        }
    ), 200


@API_APP.route("/api/p2/easter-egg", methods=["GET"])
def api_p2_easter_egg() -> Any:
    """
    P2: 彩蛋模式轻量端点。仅当环境 HCL_P2_EASTER=1|true|yes 时存在；否者 404，避免对公网无差别暴露。
    不跑长任务、不做重逻辑 —— 供「短验证 + 有开关」的回归。
    """
    from flask import abort

    if not _hcl_p2_easter_enabled():
        abort(404)
    return (
        jsonify(
            {
                "p2": "easter-egg",
                "hcl": "Hundred Crayfish Legion",
                "note": "short validation only; no long-running or large-scale work",
                "lines": [
                    "A pinch of bytes, a legion in tow.",
                    "The crayfish nods: not now, but we grow.",
                ],
            }
        ),
        200,
    )


@API_APP.route("/api/health/ready", methods=["GET"])
def api_health_ready() -> Any:
    from .autonomous_cortex import set_ops_health_for_p1
    from .p1_info import check_data_plane_ready

    ok, err = check_data_plane_ready()
    set_ops_health_for_p1(ok)
    if ok:
        return (
            jsonify(
                {
                    "status": "ready",
                    "data_plane": "ok",
                }
            ),
            200,
        )
    return (
        jsonify(
            {
                "status": "not_ready",
                "data_plane": "unavailable",
                "detail": err,
            }
        ),
        503,
    )


@API_APP.route("/api/ops/p1", methods=["GET"])
@api_token_authentication
def api_ops_p1() -> Any:
    from .p1_info import p1_status_payload

    return jsonify(
        {
            "code": 200,
            "msg": "P1 元信息",
            "data": p1_status_payload(),
        }
    )


@API_APP.route("/")
def root() -> Any:
    return redirect("/p1/", 302)


@API_APP.route("/p1/", methods=["GET"])
def p1_admin_index() -> Any:
    return send_from_directory(_P1_STATIC, "index.html")


@API_APP.route("/p1/<path:path>", methods=["GET"])
def p1_admin_assets(path: str) -> Any:
    # 防止页面里误用「相对路径」api/... 变成 /p1/api/...，被当成静态文件 404 返回 HTML
    if path.startswith("api/"):
        return redirect("/" + path, 307)
    return send_from_directory(_P1_STATIC, path)


@API_APP.route("/api/confirm/save", methods=["POST"])
@api_token_authentication
def api_save_confirm() -> Any:
    """数据全域确权存证接口"""
    data = request.get_json(silent=True) or {}
    data_content = data.get("data", {})
    data_type = data.get("data_type", "")
    if not data_content or data_type not in CONFIRM_DATA_TYPE:
        return jsonify({"code": 400, "msg": "数据或数据类型非法"}), 400
    confirm_hash = save_universe_confirm_data(data_content, data_type)
    return jsonify(
        {"code": 200, "msg": "确权存证成功", "data": {"confirm_hash": confirm_hash}}
    )


@API_APP.route("/api/confirm/query", methods=["GET"])
@api_token_authentication
def api_query_confirm() -> Any:
    """确权数据终身溯源接口"""
    confirm_hash = request.args.get("confirm_hash", "")
    if not confirm_hash:
        return jsonify({"code": 400, "msg": "确权哈希不能为空"}), 400
    result = query_universe_confirm(confirm_hash)
    return jsonify({"code": 200, "msg": "溯源成功", "data": result})


@API_APP.route("/api/sync/status", methods=["GET"])
@api_token_authentication
def api_sync_status() -> Any:
    """星际同步状态查询接口"""
    return jsonify(
        {
            "code": 200,
            "msg": "同步状态查询成功",
            "data": {
                "sync_interval": f"{INTERSTELLAR_SYNC_INTERVAL // 60}分钟",
                "online_node_count": len(get_online_node_list()),
                "confirm_data_count": len(UNIVERSE_CONFIRM_POOL),
                "system_eternal_status": "正常",
                "alliance_tier_count": ALLIANCE_TIER_COUNT,
                "alliance_12l_architecture_id": ALLIANCE_12L_ARCHITECTURE_ID,
                "tier12_closure": "L1–L12 全栈合宪",
            },
        }
    )


@API_APP.route("/api/conscious/status", methods=["GET"])
@api_token_authentication
def api_conscious_status() -> Any:
    """当前 AI 意识等级与战略；默认取最新快照。?refresh=1 时立即重新推演并写入记忆池。"""
    refresh = (request.args.get("refresh", "") or "").lower() in ("1", "true", "yes")
    if refresh:
        latest = universe_strategy_deduce()
    else:
        latest = get_latest_strategic_state(run_if_empty=True)
    return jsonify(
        {
            "code": 200,
            "msg": "超维意识状态查询成功",
            "data": {
                "current_conscious_level": latest.get("conscious_level")
                or CURRENT_CONSCIOUS_LEVEL,
                "conscious_total_score": latest.get("conscious_score"),
                "latest_strategy_plan": latest.get("strategy_plan"),
                "memory_pool_count": len(CONSCIOUS_MEMORY_POOL),
            },
        },
    )


@API_APP.route("/api/conscious/destiny", methods=["GET"])
@api_token_authentication
def api_conscious_destiny() -> Any:
    report = long_term_destiny_predict()
    return jsonify(
        {
            "code": 200,
            "msg": "长周期时序命运推演完成",
            "data": report,
        },
    )


@API_APP.route("/api/conscious/task", methods=["GET"])
@api_token_authentication
def api_conscious_task() -> Any:
    task_list = autonomous_task_arrange()
    return jsonify({"code": 200, "data": {"autonomous_task_list": task_list}})


@API_APP.route("/api/architecture/layers", methods=["GET"])
@api_token_authentication
def api_alliance_12_layers() -> Any:
    """碳硅同盟 1–12 层全栈铁律与职责索引"""
    return jsonify(
        {
            "code": 200,
            "msg": "十二层全栈已加载",
            "data": {
                "tier_count": ALLIANCE_TIER_COUNT,
                "alliance_12l_architecture_id": ALLIANCE_12L_ARCHITECTURE_ID,
                "layers": layers_to_public_dicts(),
            },
        }
    )


def create_universe_flask_app() -> Flask:
    return API_APP
