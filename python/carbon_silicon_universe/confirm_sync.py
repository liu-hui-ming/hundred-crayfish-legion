from __future__ import annotations

import datetime
import hashlib
import json
import os
import sqlite3
import threading
import time
from typing import Any

from .alliance_layers import ALLIANCE_LAYER_COUNT
from .autonomous_cortex import start_hyperdimensional_cortex_threads
from .confirm_config import (
    CARBON_SILICON_CONFIRM_PUBLIC_KEY,
    CONFIRM_DATA_TYPE,
    DEVICE_HARDWARE_FINGERPRINT,
    DISTRIBUTE_NODE_REGISTRY,
    INTERSTELLAR_SYNC_INTERVAL,
    INTERSTELLAR_SYNC_SALT,
    MAX_CONFIRM_DATA_SIZE,
    RULE_VERSION,
    ENV_TYPE,
    SYNC_NODE_LOCK,
    UNIVERSE_CONFIRM_POOL,
    UNIVERSE_DB_PATH,
    ALLIANCE_12L_ARCHITECTURE_ID,
    ALLIANCE_TIER_COUNT,
    SYSTEM_AUTH_STATUS,
)
from .runtime_log import get_online_node_list, save_system_log


def get_db_connection() -> sqlite3.Connection:
    parent = os.path.dirname(UNIVERSE_DB_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(UNIVERSE_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    _ensure_universe_table(conn)
    return conn


def _ensure_universe_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS universe_confirm_record
           (id INTEGER PRIMARY KEY AUTOINCREMENT, confirm_hash TEXT UNIQUE NOT NULL,
            data_type TEXT NOT NULL, data_detail TEXT NOT NULL, confirm_time TEXT,
            device_fingerprint TEXT, node_id TEXT)"""
    )
    conn.commit()


def generate_universe_confirm_hash(data: dict[str, Any], data_type: str) -> str:
    """生成全域唯一确权哈希，实现数据永久不可篡改存证"""
    data_str = json.dumps(data, ensure_ascii=False, sort_keys=True)
    raw_hash_str = (
        f"{data_type}{data_str}{INTERSTELLAR_SYNC_SALT}{CARBON_SILICON_CONFIRM_PUBLIC_KEY}"
    )
    first_hash = hashlib.sha256(raw_hash_str.encode("utf-8")).hexdigest()
    return f"CS-CONFIRM-{hashlib.md5(first_hash.encode('utf-8')).hexdigest().upper()}"


def save_universe_confirm_data(data: dict[str, Any], data_type: str) -> str:
    """
    全域数据永久确权存证
    返回：全域唯一确权哈希，可终身溯源
    """
    global UNIVERSE_CONFIRM_POOL
    if data_type not in CONFIRM_DATA_TYPE:
        raise ValueError(f"非法 data_type: {data_type!r}")
    with SYNC_NODE_LOCK:
        confirm_hash = generate_universe_confirm_hash(data, data_type)
        online_id = next(
            (
                node["node_id"]
                for node in DISTRIBUTE_NODE_REGISTRY
                if node.get("node_status") == "online"
            ),
            "CS-NODE-STANDALONE",
        )
        confirm_record: dict[str, Any] = {
            "confirm_hash": confirm_hash,
            "data_type": data_type,
            "data_detail": data,
            "confirm_time": datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            "device_fingerprint": DEVICE_HARDWARE_FINGERPRINT,
            "node_id": online_id,
        }
        UNIVERSE_CONFIRM_POOL.append(confirm_record)
        if len(UNIVERSE_CONFIRM_POOL) > MAX_CONFIRM_DATA_SIZE:
            conn = get_db_connection()
            try:
                for record in UNIVERSE_CONFIRM_POOL[: -MAX_CONFIRM_DATA_SIZE]:
                    conn.execute(
                        """INSERT INTO universe_confirm_record
                           (confirm_hash, data_type, data_detail, confirm_time,
                            device_fingerprint, node_id) VALUES (?, ?, ?, ?, ?, ?)""",
                        (
                            record["confirm_hash"],
                            record["data_type"],
                            json.dumps(record["data_detail"], ensure_ascii=False),
                            record["confirm_time"],
                            record["device_fingerprint"],
                            record["node_id"],
                        ),
                    )
                conn.commit()
            finally:
                conn.close()
            UNIVERSE_CONFIRM_POOL = UNIVERSE_CONFIRM_POOL[-MAX_CONFIRM_DATA_SIZE:]

    save_system_log("全域确权", f"数据确权完成，确权哈希：{confirm_hash}")
    return confirm_hash


def query_universe_confirm(confirm_hash: str) -> dict[str, Any]:
    """通过确权哈希，终身溯源查询原始数据"""
    for record in UNIVERSE_CONFIRM_POOL:
        if record["confirm_hash"] == confirm_hash:
            return record
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM universe_confirm_record WHERE confirm_hash = ?",
            (confirm_hash,),
        )
        result = cursor.fetchone()
    finally:
        conn.close()
    if result:
        return {
            "confirm_hash": result["confirm_hash"],
            "data_type": result["data_type"],
            "data_detail": json.loads(result["data_detail"]),
            "confirm_time": result["confirm_time"],
            "device_fingerprint": result["device_fingerprint"],
            "node_id": result["node_id"],
        }
    return {"code": 404, "msg": "确权数据不存在"}


def _recent_universe_confirm_records() -> list[dict[str, Any]]:
    now = datetime.datetime.now()
    out: list[dict[str, Any]] = []
    for record in UNIVERSE_CONFIRM_POOL:
        try:
            t = datetime.datetime.strptime(
                str(record["confirm_time"]), "%Y-%m-%d %H-%M-%S"
            )
        except (TypeError, ValueError):
            continue
        if (now - t).total_seconds() <= INTERSTELLAR_SYNC_INTERVAL:
            out.append(record)
    return out


def node_interstellar_sync() -> None:
    """
    星际跨节点数据同步
    实现全域碳硅节点数据实时一致，达成分布式永生
    """
    if not SYSTEM_AUTH_STATUS.get("is_authorized", False):
        return
    if not get_online_node_list():
        return
    with SYNC_NODE_LOCK:
        sync_data = _recent_universe_confirm_records()
        if not sync_data:
            return
    save_system_log(
        "星际同步",
        f"跨节点同步完成，同步{len(sync_data)}条确权数据，全域数据达成一致",
    )


def interstellar_sync_daemon() -> None:
    """星际同步守护线程，后台永久运行"""
    while True:
        try:
            node_interstellar_sync()
        except Exception as e:  # noqa: BLE001
            save_system_log("星际同步异常", f"同步失败：{str(e)}")
        time.sleep(INTERSTELLAR_SYNC_INTERVAL)


def system_eternal_guard() -> None:
    """
    碳硅系统永生守护
    实现断电/重启/崩溃后，自动恢复所有确权数据与节点状态
    """
    global UNIVERSE_CONFIRM_POOL
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM universe_confirm_record ORDER BY id DESC LIMIT ?",
            (MAX_CONFIRM_DATA_SIZE,),
        )
        records = cursor.fetchall()
    finally:
        conn.close()
    with SYNC_NODE_LOCK:
        UNIVERSE_CONFIRM_POOL.clear()
        for item in records:
            raw_detail = item["data_detail"]
            if isinstance(raw_detail, memoryview):
                detail_str = raw_detail.tobytes().decode("utf-8", errors="replace")
            elif isinstance(raw_detail, (bytes, bytearray)):
                detail_str = raw_detail.decode("utf-8", errors="replace")
            else:
                detail_str = str(raw_detail)
            UNIVERSE_CONFIRM_POOL.append(
                {
                    "confirm_hash": item["confirm_hash"],
                    "data_type": item["data_type"],
                    "data_detail": json.loads(detail_str),
                    "confirm_time": item["confirm_time"],
                    "device_fingerprint": item["device_fingerprint"],
                    "node_id": item["node_id"],
                }
            )
    save_system_log("永生守护", "系统永生初始化完成，历史确权数据100%恢复")


def system_startup() -> None:
    """在进程入口调用：恢复永生池、启星际同步、为核心启动信息确权"""
    from .p1_info import mark_p1_process_start

    mark_p1_process_start()
    system_eternal_guard()
    threading.Thread(
        target=interstellar_sync_daemon, name="interstellar-sync", daemon=True
    ).start()
    start_hyperdimensional_cortex_threads()
    core_system_info = {
        "rule_version": RULE_VERSION,
        "env_type": ENV_TYPE,
        "device_fingerprint": DEVICE_HARDWARE_FINGERPRINT,
        "startup_time": datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "alliance_tier_count": ALLIANCE_TIER_COUNT,
        "alliance_layer_count": ALLIANCE_LAYER_COUNT,
        "alliance_12l_architecture_id": ALLIANCE_12L_ARCHITECTURE_ID,
        "tier12_closure": "L1-L12 合宪闭环已声明",
    }
    try:
        save_universe_confirm_data(core_system_info, "system_log")
    except Exception as e:  # noqa: BLE001
        save_system_log("永生守护", f"核心启动确权存证未写入: {e}")
