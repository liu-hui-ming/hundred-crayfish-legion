from __future__ import annotations

import os
import sys
from datetime import datetime

from .confirm_config import DISTRIBUTE_NODE_REGISTRY, UNIVERSE_DB_PATH

_LOG_DIR = os.path.dirname(os.path.abspath(UNIVERSE_DB_PATH))
_LOG_NAME = "cs_universe_system.log"


def save_system_log(category: str, message: str) -> None:
    line = f"{datetime.now().isoformat()}\t[{category}]\t{message}\n"
    if os.environ.get("CS_UNIVERSE_VERBOSE", "").lower() in ("1", "true", "yes"):
        print(line, end="", file=sys.stderr)
    try:
        if _LOG_DIR:
            os.makedirs(_LOG_DIR, exist_ok=True)
        log_path = os.path.join(_LOG_DIR, _LOG_NAME) if _LOG_DIR else _LOG_NAME
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass


def get_online_node_list() -> list[dict]:
    return [n for n in DISTRIBUTE_NODE_REGISTRY if n.get("node_status") == "online"]
