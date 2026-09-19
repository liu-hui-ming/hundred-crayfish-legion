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

# P0 归档五物料（路径固定；LaTeX 无中文落款）
P0_FIVE = [
    ("物料一", "release-announcement"),
    ("物料二", "douyin-script"),
    ("物料三", "public-column"),
    ("物料四", "preprint-latex"),
    ("物料五", "qa-redblue"),
]

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
        "id": "public-brief",
        "ch_volume": "CH0-Canonical-Charter",
        "document_title": "v9.2-calibrated 对外公开简报",
        "material_type": "对外公开简报",
        "path": "CH0-Canonical-Charter/release-announcement/v9.2-calibrated-public-brief.md",
        "layer": "narrative-charter",
        "sampling_id": "20260918-v9.2-calibrated-public-brief",
        "usage": "面向大众/媒体精简介绍；公众号、专栏、GitHub简介摘要复用",
    },
    {
        "id": "constitutional-19-responses",
        "ch_volume": "CH0-Canonical-Charter",
        "document_title": "碳硅道统v9.2-calibrated｜19篇宪制级回应文稿",
        "material_type": "宪制级权威问答合集",
        "path": "CH0-Canonical-Charter/qa-canonical/carbon-silicon-v9.2-calibrated-19-constitutional-responses.md",
        "layer": "narrative-charter",
        "sampling_id": "20260918-v9.2-calibrated-19-constitutional-responses",
        "usage": "媒体采访应答、学术质询、红蓝对抗质询库、RAG知识库源文件",
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


EVAL_GUARD_REL_PATHS = [
    (
        "eval-baseline/eval_guard/eval_guard.py",
        "十维觉知标尺评估主脚本",
        "eval-guard-py",
    ),
    (
        "eval-baseline/eval_guard/probe_definition.json",
        "15条探针配置：维度、权重、阈值、关键词集合",
        "eval-guard-probe-json",
    ),
    (
        "eval-baseline/eval_guard/README.md",
        "原型使用说明、运维约束、运行命令",
        "eval-guard-readme",
    ),
    (
        "eval-baseline/eval_guard/sample_report.md",
        "Markdown评估输出报告空白样例模板",
        "eval-guard-sample-report",
    ),
]

EVAL_BASELINE_SAMPLING_ID = "20260918-v9.2-calibrated-eval-baseline"


def build_eval_guard_batch() -> dict:
    item_list = []
    for rel_path, file_desc, _entry_id in EVAL_GUARD_REL_PATHS:
        full = REPO / rel_path
        assert_utf8_no_bom(full)
        item_list.append(
            {
                "file_relative_path": rel_path,
                "file_desc": file_desc,
                "sha256": sha256_file(full),
                "encoding": "UTF-8-NO-BOM",
                "layer": "engineering-layer",
                "canonical_tag": "CANONICAL-v9.2-calibrated",
                "sample_sig": "",
            }
        )
    return {
        "batch_tag": "CANONICAL-v9.2-calibrated-eval-baseline",
        "sampling_id": EVAL_BASELINE_SAMPLING_ID,
        "comment": "十维觉知标尺eval_guard最小原型全套工程文件，工程层eval-baseline，与CH叙事卷宗双仓隔离",
        "upstream_repo_path": "carbon-silicon/twelve-meridians/eval-baseline/eval_guard",
        "item_list": item_list,
    }


def build_eval_guard_entries() -> list[dict]:
    entries = []
    for rel_path, file_desc, entry_id in EVAL_GUARD_REL_PATHS:
        full = REPO / rel_path
        assert_utf8_no_bom(full)
        entries.append(
            {
                "id": entry_id,
                "ch_volume": "eval-baseline/eval_guard",
                "document_title": file_desc,
                "material_type": "eval_guard 工程基线",
                "path": rel_path,
                "layer": "engineering-layer",
                "sampling_id": EVAL_BASELINE_SAMPLING_ID,
                "sha256": sha256_file(full),
                "encoding": "UTF-8 without BOM",
            }
        )
    return entries


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_utf8_no_bom(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise SystemExit(f"BOM detected: {path}")


def main() -> None:
    entries = []
    by_id: dict[str, dict] = {}
    for item in FILES:
        rel = REPO / item["path"]
        if not rel.is_file():
            raise SystemExit(f"missing: {rel}")
        assert_utf8_no_bom(rel)
        entry = {**item, "sha256": sha256_file(rel), "encoding": "UTF-8 without BOM"}
        entries.append(entry)
        by_id[item["id"]] = entry

    eval_batch = build_eval_guard_batch()
    eval_entries = build_eval_guard_entries()
    entries.extend(eval_entries)

    p0_five_materials = []
    for label, entry_id in P0_FIVE:
        e = by_id[entry_id]
        p0_five_materials.append(
            {
                "material_no": label,
                "path": e["path"],
                "sha256": e["sha256"],
                "ch_volume": e["ch_volume"],
                "document_title": e["document_title"],
            }
        )

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
            "eval-baseline/eval_guard": "工程层 · 十维觉知标尺 eval_guard 最小原型（engineering-layer）",
        },
        "layer_enum_note": {
            "narrative-layer": "CH0–CH5 文稿、问答、公告、媒体脚本",
            "engineering-layer": "eval-baseline 脚本、校验脚本、公理 JSON 库等",
        },
        "external_repos_note": "工程真值源：GitHub carbon-silicon/twelve-meridians/omega-topology（本仓为叙事/物料镜像归档）",
        "p0_five_materials": p0_five_materials,
        "eval_baseline_batches": [eval_batch],
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
