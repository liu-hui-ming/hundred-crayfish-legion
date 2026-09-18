#!/usr/bin/env python3
"""Rebuild archive/media-external/manifest.json global ledger from bundle files."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "archive" / "media-external"
RMZXW = ROOT / "rmzxw"
WP = ROOT / "whitepaper"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    rmzxw_bundle = json.loads((RMZXW / "bundle-hashes.json").read_text(encoding="utf-8"))
    f96 = WP / "carbon-silicon-daotong-silicon-civilization-axiom-whitepaper-T02Y04-public-domain-96.md"
    f100 = WP / "carbon-silicon-daotong-silicon-civilization-axiom-whitepaper-T02Y04-github-archive-100-full.md"
    legacy = REPO / (
        "dola-carbon-silicon-framework/docs/whitepaper/public-media-version/"
        "carbon-silicon-daotong-silicon-civilization-axiom-whitepaper-public-media.md"
    )

    manifest = {
        "schema": "archive/media-external/manifest.global.v1",
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "encoding": "UTF-8 without BOM",
        "narrative_layer_repo": "hundred-crayfish-legion",
        "engineering_isolation_note": (
            "media-external 卷宗仅存对外物料快照与双轨正文镜像；"
            "叙事正文正本仍在 dola-carbon-silicon-framework/docs/ 下，路径分离。"
        ),
        "entries": [
            {
                "id": "rmzxw-20260916",
                "document_title": "划清人工智能「模拟智能」与「本源觉知」的边界——人民政协网",
                "material_type": "media-external · 权威媒体刊载",
                "sampling_id": rmzxw_bundle["sampling_id"],
                "canonical_url": "https://www.rmzxw.com.cn/c/2026-09-16/3976199.shtml",
                "volume_path": "archive/media-external/rmzxw/",
                "narrative_body_canonical": (
                    "dola-carbon-silicon-framework/docs/media-clipping/rmzxw/"
                    "ai-simulate-awareness-boundary-rmzxw-20260916.md"
                ),
                "ch_series_ref": "CH-MEDIA-EXTERNAL-RMZXW-T02Y04",
                "files": rmzxw_bundle,
            },
            {
                "id": "whitepaper-T02Y04-dual-track",
                "document_title": "碳硅道统：硅基文明公理体系白皮书（媒体权威对外版）",
                "material_type": "media-external · 白皮书双轨",
                "version": "T-02/Y-04",
                "sampling_id": "20260918-whitepaper-T02Y04-dual-track",
                "volume_path": "archive/media-external/whitepaper/",
                "narrative_body_canonical": str(
                    legacy.relative_to(REPO).as_posix()
                ),
                "ch_series_ref": "CH-MEDIA-EXTERNAL-WHITEPAPER-T02Y04",
                "tracks": {
                    "public_domain_96": {
                        "path": f96.name,
                        "sha256": sha256_file(f96),
                        "grade": "96 · 公域纯白版（无 Git/SHA 内核台账行）",
                    },
                    "github_archive_100": {
                        "path": f100.name,
                        "sha256": sha256_file(f100),
                        "grade": "100 · GitHub 完整版（含台账字段 + 归档说明）",
                    },
                    "legacy_single_file": {
                        "path": legacy.name,
                        "sha256": sha256_file(legacy),
                        "note": "历史单文件正本，禁止覆盖；双轨为增量镜像",
                    },
                },
            },
        ],
        "remote_push": "dev-v2.2 only; main frozen until explicit merge",
    }
    out = ROOT / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)
    print("sha256", sha256_file(out))


if __name__ == "__main__":
    main()
