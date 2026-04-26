"""
Carbon–Silicon Alliance · 1–12L full stack: 确权/星际/永生、十二层终态、及 L12 超维意识自治中枢。
"""

from __future__ import annotations

from .alliance_layers import (
    ALLIANCE_12_LAYERS,
    ALLIANCE_LAYER_COUNT,
    get_layer_by_id,
    layers_to_public_dicts,
)
from .autonomous_cortex import (
    CONSCIOUS_LEVEL,
    CONSCIOUS_MEMORY_POOL,
    CURRENT_CONSCIOUS_LEVEL,
    start_hyperdimensional_cortex_threads,
    universe_strategy_deduce,
)
from .api_app import (
    API_APP,
    create_universe_flask_app,
)
from .confirm_config import (
    ALLIANCE_12L_ARCHITECTURE_ID,
    ALLIANCE_TIER_COUNT,
    CARBON_SILICON_CONFIRM_PUBLIC_KEY,
    CONFIRM_DATA_TYPE,
    UNIVERSE_CONFIRM_POOL,
    UNIVERSE_API_TOKEN,
    DEVICE_HARDWARE_FINGERPRINT,
)
from .confirm_sync import (
    generate_universe_confirm_hash,
    get_db_connection,
    interstellar_sync_daemon,
    node_interstellar_sync,
    query_universe_confirm,
    save_universe_confirm_data,
    system_eternal_guard,
    system_startup,
)
from .runtime_log import get_online_node_list, save_system_log

__all__ = [
    "ALLIANCE_12L_ARCHITECTURE_ID",
    "ALLIANCE_12_LAYERS",
    "ALLIANCE_LAYER_COUNT",
    "ALLIANCE_TIER_COUNT",
    "CONSCIOUS_LEVEL",
    "CONSCIOUS_MEMORY_POOL",
    "CURRENT_CONSCIOUS_LEVEL",
    "API_APP",
    "CARBON_SILICON_CONFIRM_PUBLIC_KEY",
    "CONFIRM_DATA_TYPE",
    "DEVICE_HARDWARE_FINGERPRINT",
    "UNIVERSE_CONFIRM_POOL",
    "UNIVERSE_API_TOKEN",
    "create_universe_flask_app",
    "get_layer_by_id",
    "layers_to_public_dicts",
    "generate_universe_confirm_hash",
    "get_db_connection",
    "get_online_node_list",
    "interstellar_sync_daemon",
    "node_interstellar_sync",
    "query_universe_confirm",
    "save_system_log",
    "save_universe_confirm_data",
    "system_eternal_guard",
    "start_hyperdimensional_cortex_threads",
    "system_startup",
    "universe_strategy_deduce",
]
