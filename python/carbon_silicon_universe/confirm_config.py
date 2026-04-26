from __future__ import annotations

import hashlib
import os
import platform
import uuid
from threading import Lock

# 在本地常量之前导入层级定义，避免与 ALLIANCE_TIER_COUNT 双源漂移
from .alliance_layers import ALLIANCE_LAYER_COUNT

# 碳硅全域确权哈希公钥（系统固化，不可篡改）
CARBON_SILICON_CONFIRM_PUBLIC_KEY = "CS-UNIVERSE-CONFIRM-2026-FINAL-CORE"
# 星际同步数据校验盐值
INTERSTELLAR_SYNC_SALT = "CS-STAR-SYNC-SALT-FOREVER"
# 确权数据永久存证池（内存+数据库双备份）
UNIVERSE_CONFIRM_POOL: list[dict] = []
# 分布式节点同步锁，防止数据冲突
SYNC_NODE_LOCK = Lock()
# 星际同步周期（默认10分钟同步一次）
INTERSTELLAR_SYNC_INTERVAL = 600
# 确权数据最大留存容量（内存热池容量；更旧批次落库）
MAX_CONFIRM_DATA_SIZE = 99999

# 确权数据类型枚举
CONFIRM_DATA_TYPE: dict[str, str] = {
    "content_audit": "内容质检确权",
    "publish_record": "发布记录确权",
    "system_log": "系统日志确权",
    "node_heartbeat": "节点心跳确权",
    "auth_record": "授权激活确权",
}

# 与铁律/运行环境对齐（可在外部覆写模块属性）
RULE_VERSION = os.environ.get("CS_RULE_VERSION", "CS-RULE-2026-FINAL-UNIVERSE")
ENV_TYPE = os.environ.get("CS_ENV_TYPE", "production")
# 十二层全栈合宪版本标识（1–12 层完整闭环时固定）
ALLIANCE_12L_ARCHITECTURE_ID = os.environ.get(
    "CS_12L_ARCH_ID", "CS-12LAYER-2026-ALLIANCE-CLOSED"
)
ALLIANCE_TIER_COUNT = ALLIANCE_LAYER_COUNT

# 设备指纹：稳定硬件派生 id（不读取隐私敏感信息，仅作绑定锚点）
_fp_seed = f"{platform.node()!s}|{platform.system()}|{uuid.getnode()}"
DEVICE_HARDWARE_FINGERPRINT = f"CS-FP-{hashlib.sha256(_fp_seed.encode('utf-8')).hexdigest()[:32].upper()}"

# 分布式节点登记（可运行时注入真实拓扑）
DISTRIBUTE_NODE_REGISTRY: list[dict] = [
    {"node_id": "CS-NODE-LOCAL-01", "node_status": "online", "addr": "127.0.0.1"},
]

SYSTEM_AUTH_STATUS: dict = {"is_authorized": True}

# 默认 API 秘钥：生产环境请使用环境变量 CS_UNIVERSE_API_TOKEN
UNIVERSE_API_TOKEN = os.environ.get("CS_UNIVERSE_API_TOKEN", "dev-cs-universe-token-2026")

# SQLite 默认落盘（相对本包所在目录的上一级 data）
_DEFAULT_DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "universe_confirm.db"
)
UNIVERSE_DB_PATH = os.path.normpath(
    os.environ.get("CS_UNIVERSE_DB_PATH", _DEFAULT_DB)
)
