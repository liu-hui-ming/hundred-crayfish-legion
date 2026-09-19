#!/usr/bin/env python3
"""Build manifest.json for a single docs/issue-exports/xian-daily-* folder."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build(folder_rel: str) -> None:
    folder = REPO / folder_rel.replace("/", "\\") if False else REPO / folder_rel
    if not folder.is_dir():
        raise SystemExit(f"not a directory: {folder}")
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.name != "manifest.json")
    entries = []
    for p in files:
        raw = p.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise SystemExit(f"BOM: {p}")
        entries.append(
            {
                "file_name": p.name,
                "path": f"{folder_rel}/{p.name}".replace("\\", "/"),
                "sha256": sha256_file(p),
                "encoding": "UTF-8 without BOM",
                "layer": "narrative-layer",
            }
        )
    sampling_id = folder.name
    manifest = {
        "schema": "docs/issue-exports/manifest.v1",
        "sampling_id": sampling_id,
        "folder": folder_rel.replace("\\", "/"),
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entries": entries,
        "encoding": "UTF-8 without BOM",
    }
    out = folder / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["manifest_sha256"] = sha256_file(out)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    rel = sys.argv[1] if len(sys.argv) > 1 else "docs/issue-exports/xian-daily-2026-09-17"
    build(rel)
