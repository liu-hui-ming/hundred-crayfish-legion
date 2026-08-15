#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract DT-188 188-item volumes from 188篇.one (OneNote UTF-16 payload)."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONE = ROOT / "188篇.one"
OUT_ROOT = ROOT / "_extract_188"
THEOREM_ROOT = ROOT / "碳硅道统核心十三卷宗" / "定理体"

TITLE_TABLE = ROOT / (
    "碳硅道统核心十三卷宗/内核典藏卷/188项全域工程整改总纲/"
    "碳硅道统_188项AI全域工程整改清单_标题总表_V2.0公理合规终版.md"
)

VOLUME_MAP: list[tuple[int, int, str, str]] = [
    (1, 30, "Earth/HW", "HW"),
    (31, 60, "Earth/SW", "SW"),
    (61, 90, "Earth/COMP", "COMP"),
    (91, 120, "Earth/CORP", "CORP"),
    (121, 150, "Earth/HCI", "HCI"),
    (151, 188, "Earth/Carrier", "Carrier"),
]

GARBAGE_PARA_RE = re.compile(
    r"(峂贀|撄谀|悴肀|怌肀|瀔肀|젞肀|炰需|娀聰|Microsoft YaHei|"
    r"Cambria Math|䴀椀挀|钩㦯|ꌄꨗ|됀佑|眀㓐|嶒裯|灚肀|㽀騁|枝䭓|"
    r"⸳䔠|⸲吠|扜来|敜摮|慍彰|MimeType|EntryAligned)"
)
NOISE_RE = re.compile(
    r"(PageTitle|PageDateTime|Calibri|OneNote|绰垰|纵垰|ᰀ|ᵺ|㐬|᳾|蠀|ᴉ|ᰃ|ᰟ|㓝|ࠄ|"
    r"^[\s\u200b-\u200f\u202a-\u202e\u0000-\u001f]+$)"
)
KEYWORD_RE = re.compile(
    r"(Match_Law|Topology|DY-|Map_|Trigger_|Constraint_|T-02|Y-04|w_\{Si|"
    r"【|】|整改|公理|拓扑|熵增|熔断|碳基|硅基|SHA256|GitHub|Earth/|DeepSpace)"
)


def load_title_index() -> dict[int, str]:
    text = TITLE_TABLE.read_text(encoding="utf-8")
    idx: dict[int, str] = {}
    for m in re.finditer(r"碳硅道统·AI全域工程整改清单（第(\d{3})项）(.+?)整改", text):
        idx[int(m.group(1))] = m.group(2).strip()
    return idx


def volume_for(num: int) -> tuple[str, str]:
    for lo, hi, path, code in VOLUME_MAP:
        if lo <= num <= hi:
            return path, code
    raise ValueError(num)


def slug_dir(num: int, slug: str) -> str:
    return f"{num:03d}-{slug}整改"


def title_needle(num: int) -> bytes:
    return f"碳硅道统·AI全域工程整改清单（第{num:03d}项）".encode("utf-16-le")


def chinese_ratio(s: str) -> float:
    if not s:
        return 0.0
    cjk = sum(1 for c in s if "\u4e00" <= c <= "\u9fff")
    return cjk / len(s)


def junk_ratio(s: str) -> float:
    if not s:
        return 1.0
    junk = 0
    for c in s:
        o = ord(c)
        if "\u4e00" <= c <= "\u9fff":
            continue
        if c in " \t\n\r，。；：、（）【】《》%+-=<>/\\|_[]{}":
            continue
        if "A" <= c <= "Z" or "a" <= c <= "z" or "0" <= c <= "9":
            continue
        if o < 0x80:
            continue
        junk += 1
    return junk / len(s)


def keep_segment(seg: str) -> bool:
    seg = seg.strip()
    if len(seg) < 6:
        return False
    if GARBAGE_PARA_RE.search(seg):
        return False
    if seg.count("肀") >= 1 and chinese_ratio(seg) < 0.25:
        return False
    if "贀" in seg and chinese_ratio(seg) < 0.35:
        return False
    if NOISE_RE.search(seg):
        return False
    if junk_ratio(seg) > 0.55 and chinese_ratio(seg) < 0.08:
        return False
    if chinese_ratio(seg) >= 0.22:
        return True
    if KEYWORD_RE.search(seg):
        return True
    if re.search(r"[A-Za-z_]{3,}", seg) and chinese_ratio(seg) >= 0.05:
        return True
    return False


def strip_tail_garbage(text: str) -> str:
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    while paras:
        p = paras[-1]
        if chinese_ratio(p) >= 0.12 or KEYWORD_RE.search(p):
            break
        if junk_ratio(p) > 0.18 or GARBAGE_PARA_RE.search(p):
            paras.pop()
            continue
        break
    return "\n\n".join(paras)


def polish_body(text: str) -> str:
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    kept: list[str] = []
    for p in paras:
        if not keep_segment(p):
            continue
        if len(p) > 24 and chinese_ratio(p) < 0.03 and junk_ratio(p) > 0.35:
            continue
        if kept and kept[-1] == p:
            continue
        kept.append(p)
    return strip_tail_garbage("\n\n".join(kept))


def decode_slice(raw: bytes) -> str:
    text = raw.decode("utf-16-le", errors="ignore")
    parts = re.split(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text)
    kept: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if keep_segment(part):
            kept.append(part)
    # dedupe consecutive
    out: list[str] = []
    for ln in kept:
        if out and out[-1] == ln:
            continue
        out.append(ln)
    return polish_body("\n\n".join(out))


def find_title_offsets(data: bytes) -> dict[int, list[int]]:
    offsets: dict[int, list[int]] = {}
    for num in range(1, 189):
        needle = title_needle(num)
        start = 0
        hits: list[int] = []
        while True:
            pos = data.find(needle, start)
            if pos < 0:
                break
            hits.append(pos)
            start = pos + 2
        if hits:
            offsets[num] = hits
    return offsets


def build_boundaries(data: bytes, offsets: dict[int, list[int]]) -> list[tuple[int, int, int]]:
    """Return sorted (pos, num) boundaries across all title hits."""
    points: list[tuple[int, int]] = []
    for num, ps in offsets.items():
        for p in ps:
            points.append((p, num))
    points.sort(key=lambda x: x[0])
    return points


def extract_item_bodies(data: bytes) -> dict[int, str]:
    offsets = find_title_offsets(data)
    points = build_boundaries(data, offsets)
    bodies: dict[int, list[str]] = {}

    for i, (pos, num) in enumerate(points):
        end = points[i + 1][0] if i + 1 < len(points) else len(data)
        chunk = decode_slice(data[pos:end])
        if chunk:
            bodies.setdefault(num, []).append(chunk)

    merged: dict[int, str] = {}
    for num, chunks in bodies.items():
        merged[num] = max(chunks, key=len)
    return merged


def yaml_header(num: int, vol_code: str) -> str:
    return (
        "---\n"
        f"document_id: DT188-{num:03d}\n"
        f"series: 碳硅道统·AI全域工程整改清单\n"
        f"volume: {vol_code}\n"
        "catalog: 碳硅道统核心十三卷宗/定理体\n"
        "base_axiom: 0⁰=1\n"
        "version: v2.0.0-FINAL\n"
        "checksum_sha256: [RESERVED_HASH_SLOT]\n"
        "archive_platform: GitHub\n"
        "permit_modify: false\n"
        "---\n\n"
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_markdown(num: int, slug: str, body: str, vol_code: str) -> str:
    title = f"碳硅道统·AI全域工程整改清单（第{num:03d}项）{slug}整改"
    header = yaml_header(num, vol_code)
    if not body.strip():
        md = header + f"# {title}\n\n> ⚠️ 源文件 `188篇.one` 未检出正文，待补录。\n"
    else:
        if not body.lstrip().startswith("#"):
            body = f"# {title}\n\n{body.strip()}\n"
        md = header + body
    digest = sha256_text(md)
    return md.replace("[RESERVED_HASH_SLOT]", digest)


def main() -> None:
    if not ONE.exists():
        raise SystemExit(f"missing {ONE}")
    data = ONE.read_bytes()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    titles = load_title_index()
    bodies = extract_item_bodies(data)
    missing = sorted(set(range(1, 189)) - set(bodies))
    print(f"items_extracted={len(bodies)} missing={missing}")

    manifest: list[str] = []
    stats: list[tuple[int, int]] = []

    for num in range(1, 189):
        slug = titles[num]
        vol_path, vol_code = volume_for(num)
        dir_name = slug_dir(num, slug)
        rel_dir = THEOREM_ROOT / vol_path / dir_name
        rel_dir.mkdir(parents=True, exist_ok=True)
        fname = f"碳硅道统·AI全域工程整改清单（第{num:03d}项）{slug}整改.md"
        out_path = rel_dir / fname

        body = bodies.get(num, "")
        content = build_markdown(num, slug, body, vol_code)
        out_path.write_text(content, encoding="utf-8")
        (OUT_ROOT / f"item_{num:03d}.md").write_text(content, encoding="utf-8")
        stats.append((num, len(body)))
        manifest.append(f"{num:03d}\t{vol_path}\t{dir_name}\t{len(body)}\t{num in bodies}")

    (OUT_ROOT / "manifest.tsv").write_text(
        "num\tvolume\tdir\tbody_chars\tpresent\n" + "\n".join(manifest) + "\n",
        encoding="utf-8",
    )
    small = [n for n, ln in stats if ln < 200 and n in bodies]
    print("short bodies (<200 chars):", small[:20], "count", len(small))
    print("wrote theorem tree under", THEOREM_ROOT)


if __name__ == "__main__":
    main()
