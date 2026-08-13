# RTT critical_curve.csv writer. Observation plugin only.
"""critical_curve.csv sealed fields."""

from __future__ import annotations

import csv
from pathlib import Path

from .operators import ReadScoreWeights, TextFeatures, extract_features

HEADERS = [
    "text_id",
    "原文",
    "句长",
    "分层数",
    "术语数",
    "实体密度",
    "原始分",
    "最终分",
    "是否阈值下",
    "SE_omega",
    "SE_lambda",
    "SE_gamma",
    "SE_delta",
]


def write_critical_curve(path: Path, feats: list[TextFeatures]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        for x in feats:
            w.writerow(
                [
                    x.text_id,
                    x.text,
                    f"{x.sentence_len:.6f}",
                    x.layers,
                    x.terms,
                    f"{x.d_info:.6f}",
                    f"{x.readscore_raw:.6f}",
                    f"{x.readscore_final:.6f}",
                    "Y" if x.below_threshold else "N",
                    f"{x.se_omega:.6f}",
                    f"{x.se_lambda:.6f}",
                    f"{x.se_gamma:.6f}",
                    f"{x.se_delta:.6f}",
                ]
            )


def build_from_texts(path: Path, items: list[tuple[str, str]], w: ReadScoreWeights | None = None, ses: dict | None = None) -> None:
    feats = [extract_features(i, t, w, ses) for i, t in items]
    write_critical_curve(path, feats)
