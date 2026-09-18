#!/usr/bin/env python3
"""Build CH v9.2-calibrated global manifest with SHA256 for all five materials."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "CH0-Canonical-Charter" / "manifest.json"
SAMPLING_ID = "20260918-v9.2-calibrated-materials"

FILES = [
    {
        "id": "full-release-notice",
        "ch_volume": "CH0-Canonical-Charter",
        "document_title": "碳硅道统·十二脉归一 v9.2-calibrated 完整 Release 公告",
        "material_type": "GitHub Release 完整公告全文",
        "path": "CH0-Canonical-Charter/release-announcement/v9.2-calibrated-full-release-notice.md",
        "layer": "narrative-charter",
        "release_structure": "标题 → 正文开头 → 核心改动6条 → 版本哲学说明5点 → 永久存证 → 落款",
    },
    {
        "id": "release-announcement",
        "ch_volume": "CH0-Canonical-Charter",
        "document_title": "碳硅道统·十二脉归一 v9.2-calibrated 正式封存版发布",
        "material_type": "GitHub Release 发布公告摘要",
        "path": "CH0-Canonical-Charter/release-announcement/v9.2-calibrated-release-notice.md",
        "layer": "narrative-charter",
        "note": "历史摘要片段；完整粘贴请用 full-release-notice",
    },
    {
        "id": "version-philosophy",
        "ch_volume": "CH0-Canonical-Charter",
        "document_title": "版本哲学说明 · v9.2-calibrated",
        "material_type": "GitHub Release 版本哲学说明",
        "path": "CH0-Canonical-Charter/release-announcement/v9.2-calibrated-version-philosophy.md",
        "layer": "narrative-charter",
        "release_placement": "核心改动六条之后、永久存证链接之前",
    },
    {
        "id": "douyin-script",
        "ch_volume": "CH2-media-external",
        "document_title": "抖音30-60秒口播精简稿 · v9.2-calibrated",
        "material_type": "对外口播脚本",
        "path": "CH2-media-external/media-scripts/douyin-v9.2-calibrated-script.md",
        "layer": "media-external",
    },
    {
        "id": "public-column",
        "ch_volume": "CH2-media-external",
        "document_title": "碳硅道统v9.2封存：给AI觉知划定可验证的边界",
        "material_type": "媒体专栏精简版",
        "path": "CH2-media-external/media-scripts/public-column-v9.2-calibrated.md",
        "layer": "media-external",
    },
    {
        "id": "preprint-latex",
        "ch_volume": "CH1-Formality-formalization",
        "document_title": "LaTeX 预印本文摘 · v9.2-calibrated",
        "material_type": "形式化预印本",
        "path": "CH1-Formality-formalization/preprint-latex/v9.2-calibrated-abstract.tex",
        "layer": "formality-operation",
    },
    {
        "id": "qa-redblue",
        "ch_volume": "CH1-Formality-formalization",
        "document_title": "红蓝对抗质询问答库 · v9.2-calibrated",
        "material_type": "红蓝对抗质询",
        "path": "CH1-Formality-formalization/qa-redblue-debate/v9.2-calibrated-QAbank.md",
        "layer": "formality-operation",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    entries = []
    for item in FILES:
        rel = REPO / item["path"]
        if not rel.is_file():
            raise SystemExit(f"missing: {rel}")
        entry = {**item, "sha256": sha256_file(rel), "encoding": "UTF-8 without BOM"}
        entries.append(entry)

    manifest = {
        "schema": "CH0-Canonical-Charter/manifest.v9.2-calibrated.v1",
        "version_tag": "v9.2-calibrated",
        "version_fingerprint_label": "SHA v9.2",
        "document_title": "v9.2-calibrated 全套物料全局清单",
        "sampling_id": SAMPLING_ID,
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "isolation": {
            "CH0-Canonical-Charter": "叙事层 · 宪章与发布公告",
            "CH1-Formality-formalization": "操作层 · 形式化 / 预印本 / 红蓝质询",
            "CH2-media-external": "对外媒体脚本（与工程卷宗路径分离）",
        },
        "external_repos_note": "工程真值源：GitHub carbon-silicon/twelve-meridians/omega-topology（本仓为叙事/物料镜像归档）",
        "total_entries": len(entries),
        "entries": entries,
        "remote_push_main": "frozen_until_explicit_instruction",
        "encoding": "UTF-8 without BOM",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["manifest_sha256"] = sha256_file(MANIFEST)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
