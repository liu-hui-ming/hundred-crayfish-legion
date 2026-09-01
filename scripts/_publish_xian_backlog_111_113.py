#!/usr/bin/env python3
"""Publish XIAN daily issues #111-#113 (2026-08-29 .. 2026-08-31)."""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from _publish_xian_backlog_from_85 import (  # noqa: E402
    REPO,
    append_changelog,
    append_issue_ledger,
    append_registry,
    ensure_export_files,
    gh_json,
    issue_exists_for_date,
)

START = date(2026, 8, 29)
END = date(2026, 8, 31)


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += __import__("datetime").timedelta(days=1)


def main() -> int:
    created: list[tuple[int, date, str]] = []
    for day in daterange(START, END):
        existing = issue_exists_for_date(day)
        if existing:
            print(f"skip {day} existing #{existing}")
            continue
        ensure_export_files(day)
        title = (
            ROOT / "docs" / "issue-exports" / f"xian-daily-{day.strftime('%Y-%m-%d')}-title.txt"
        ).read_text(encoding="utf-8").strip()
        body = (
            ROOT / "docs" / "issue-exports" / f"xian-daily-{day.strftime('%Y-%m-%d')}-body.md"
        ).read_text(encoding="utf-8")
        out = subprocess.check_output(
            [
                "gh",
                "issue",
                "create",
                "--repo",
                REPO,
                "--title",
                title,
                "--body",
                body,
                "--label",
                "P1-Roadmap",
                "--label",
                "documentation",
            ],
            text=True,
            encoding="utf-8",
        ).strip()
        num = int(out.rstrip("/").split("/")[-1])
        url = out if out.startswith("http") else f"https://github.com/{REPO}/issues/{num}"
        print(f"created #{num} {day}")
        append_registry(num, day, url)
        append_issue_ledger(num, day)
        created.append((num, day, url))

    if created:
        block_prefix = f"\n[2026-09-01] XIAN一日一发积压补齐（#110后续，共{len(created)}条）\n"
        lines = [block_prefix]
        for num, day, url in created:
            lines.append(
                f"• #{num} {day.isoformat()}（采样标识 {day.isoformat()}）：{url}；"
                f"父链基线 dd41661；#79回执对账标记已纳入条目正文。\n"
            )
        changelog = ROOT / "CHANGELOG.md"
        with changelog.open("a", encoding="utf-8") as f:
            f.write("".join(lines))

    print(f"DONE created={len(created)}")
    for num, day, url in created:
        print(f"  #{num} {day} {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
