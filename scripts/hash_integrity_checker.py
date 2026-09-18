#!/usr/bin/env python3
"""One-shot integrity check for archive/media-external/manifest.json entries."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "archive" / "media-external"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(base: Path, rel: str, expected: str | None) -> bool:
    path = base / rel
    if not path.is_file():
        print(f"MISSING {path}")
        return False
    actual = sha256_file(path)
    if expected and actual != expected:
        print(f"MISMATCH {rel}\n  expected {expected}\n  actual   {actual}")
        return False
    print(f"OK {rel} {actual}")
    return True


def main() -> int:
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.is_file():
        print("No manifest.json")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ok = True
    for entry in manifest.get("entries", []):
        eid = entry.get("id", "?")
        print(f"--- entry {eid} ---")
        if eid.startswith("rmzxw"):
            base = ROOT / "rmzxw"
            files = entry.get("files", {})
            for key in ("markdown", "source_metadata", "snapshot_png", "snapshot_mhtml"):
                block = files.get(key, {})
                rel = block.get("path")
                if rel:
                    ok &= check_file(base, rel, block.get("sha256"))
            leg = files.get("legacy_html_attachment", {})
            if leg.get("path"):
                ok &= check_file(base, leg["path"], leg.get("sha256"))
        elif "whitepaper" in eid:
            base = ROOT / "whitepaper"
            tracks = entry.get("tracks", {})
            for track in tracks.values():
                rel = track.get("path")
                if rel and (base / rel).exists():
                    ok &= check_file(base, rel, track.get("sha256"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
