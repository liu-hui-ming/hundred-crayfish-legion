"""P1: bundle metadata — Rust core version, paths, and runtime."""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import Any

# Repo root: .../python/carbon_silicon_universe/ -> .../hundred-crayfish-legion
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_CARGO_TOML = _REPO_ROOT / "core" / "Cargo.toml"
_PROCESS_START: float | None = None


def _read_rust_crate_version() -> str:
    if not _CARGO_TOML.is_file():
        return "unknown"
    try:
        text = _CARGO_TOML.read_text(encoding="utf-8")
    except OSError:
        return "unknown"
    m = re.search(
        r'^\s*version\s*=\s*"([^"]+)"\s*$',
        text,
        re.MULTILINE,
    )
    return m.group(1) if m else "unknown"


def mark_p1_process_start() -> None:
    global _PROCESS_START
    if _PROCESS_START is None:
        _PROCESS_START = time.time()


def p1_status_payload() -> dict[str, Any]:
    """For `/api/ops/p1` and dashboard."""
    t0 = _PROCESS_START
    return {
        "p1": "P1-底层基座成型期 (kernel, web, deploy, basic ops, basic autonomy)",
        "python": {
            "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "executable": sys.executable,
        },
        "rust_core": {
            "crate": "hcl-core",
            "version": _read_rust_crate_version(),
            "path": str(_CARGO_TOML.parent),
        },
        "hcl_rust_pyext": try_import_hcl_rust(),
        "alliance_12l": "see GET /api/architecture/layers (auth)",
        "uptime_s": (round(time.time() - t0, 1) if t0 is not None else None),
    }


def try_import_hcl_rust() -> str | None:
    try:
        import hcl_core  # type: ignore[import-not-found]

        return str(getattr(hcl_core, "version", "unknown"))
    except Exception:  # noqa: BLE001
        return None


def check_data_plane_ready() -> tuple[bool, str | None]:
    try:
        from .confirm_sync import get_db_connection

        conn = get_db_connection()
        try:
            conn.execute("SELECT 1")
        finally:
            conn.close()
        return True, None
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
