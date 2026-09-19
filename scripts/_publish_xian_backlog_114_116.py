#!/usr/bin/env python3
"""Publish XIAN daily issues #114-116 for 2026-09-01 .. 2026-09-03."""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

# Reuse helpers from sibling script
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _publish_xian_backlog_from_85 import (  # noqa: E402
    REPO,
    append_changelog,
    append_issue_ledger,
    append_registry,
    daterange,
    ensure_export_files,
    issue_exists_for_date,
)

EXPORTS = Path(__file__).resolve().parent.parent / "docs" / "issue-exports"


def main() -> int:
    start = date(2026, 9, 1)
    end = date(2026, 9, 3)
    created: list[tuple[int, date, str]] = []
    for day in daterange(start, end):
        existing = issue_exists_for_date(day)
        if existing:
            print(f"skip {day} existing #{existing}")
            continue
        ensure_export_files(day)
        title = (EXPORTS / f"xian-daily-{day.strftime('%Y-%m-%d')}-title.txt").read_text(encoding="utf-8").strip()
        body = (EXPORTS / f"xian-daily-{day.strftime('%Y-%m-%d')}-body.md").read_text(encoding="utf-8")
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
        append_changelog(created)
    print(f"DONE created={len(created)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
