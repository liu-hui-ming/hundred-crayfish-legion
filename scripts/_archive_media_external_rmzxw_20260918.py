#!/usr/bin/env python3
"""Full-page PNG + MHTML snapshot for rmzxw + source metadata (media-external)."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "archive" / "media-external" / "rmzxw"
URL = "https://www.rmzxw.com.cn/c/2026-09-16/3976199.shtml"
SAMPLING_ID = "20260916-rmzxw-ai-simulate-awareness-boundary"
BODY_SRC = (
    REPO
    / "dola-carbon-silicon-framework/docs/media-clipping/rmzxw"
    / "ai-simulate-awareness-boundary-rmzxw-20260916.md"
)
LEGACY_HTML = (
    REPO
    / "dola-carbon-silicon-framework/docs/media-clipping/rmzxw"
    / "ai-simulate-awareness-boundary-rmzxw-20260916-snapshot.html"
)
BASE = "20260916-rmzxw-ai-simulate-awareness-boundary"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    att = OUT / "attachments"
    att.mkdir(exist_ok=True)

    png = OUT / f"{BASE}-snapshot.png"
    mhtml = OUT / f"{BASE}.mhtml"
    meta_path = OUT / f"{BASE}-source-metadata.json"
    body_out = OUT / f"{BASE}.md"

    shutil.copy2(BODY_SRC, body_out)
    if LEGACY_HTML.is_file():
        shutil.copy2(LEGACY_HTML, att / LEGACY_HTML.name)

    title = ""
    http_status = 0
    status = "ok"
    err = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        page = context.new_page()
        try:
            resp = page.goto(URL, wait_until="networkidle", timeout=120_000)
            http_status = resp.status if resp else 0
            page.wait_for_timeout(3000)
            title = page.title()
            page.screenshot(path=str(png), full_page=True)
            cdp = context.new_cdp_session(page)
            snap = cdp.send("Page.captureSnapshot", {"format": "mhtml"})
            mhtml.write_text(snap.get("data") or "", encoding="utf-8", newline="\n")
        except Exception as exc:  # noqa: BLE001
            status = "error"
            err = str(exc)[:500]
        finally:
            page.close()
            browser.close()

    meta = {
        "schema": "archive/media-external/rmzxw/source-metadata.v1",
        "sampling_id": SAMPLING_ID,
        "canonical_url": URL,
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "page_title": title,
        "http_status": http_status,
        "access_status": status,
        "error": err,
        "narrative_body_path": str(
            BODY_SRC.relative_to(REPO).as_posix()
        ),
        "dola_clipping_path": "dola-carbon-silicon-framework/docs/media-clipping/rmzxw/",
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    bundle = {
        "sampling_id": SAMPLING_ID,
        "markdown": {"path": body_out.name, "sha256": sha256_file(body_out)},
        "source_metadata": {"path": meta_path.name, "sha256": sha256_file(meta_path)},
        "snapshot_png": {"path": png.name, "sha256": sha256_file(png) if png.exists() else None},
        "snapshot_mhtml": {"path": mhtml.name, "sha256": sha256_file(mhtml) if mhtml.exists() else None},
    }
    if LEGACY_HTML.is_file():
        legacy_copy = att / LEGACY_HTML.name
        bundle["legacy_html_attachment"] = {
            "path": f"attachments/{legacy_copy.name}",
            "sha256": sha256_file(legacy_copy),
        }
    (OUT / "bundle-hashes.json").write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(bundle, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
