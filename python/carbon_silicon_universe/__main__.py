from __future__ import annotations

import os

from .api_app import API_APP
from .confirm_sync import system_startup


def main() -> None:
    system_startup()
    host = os.environ.get("CS_UNIVERSE_HOST", "127.0.0.1")
    port = int(os.environ.get("CS_UNIVERSE_PORT", "8765"))
    API_APP.run(host=host, port=port, use_reloader=False, debug=False)


if __name__ == "__main__":
    main()
