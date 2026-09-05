#!/usr/bin/env python3
"""AES-256-CBC encrypt OpenClaw production backup archive."""
from __future__ import annotations

import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

ROOT = Path(__file__).resolve().parents[1] / "backups"
SRC = ROOT / "2026-09-01T14-07-38.616Z-openclaw-backup.tar.gz"
ENC = SRC.with_suffix(SRC.suffix + ".aes")
META = ROOT / "BACKUP-KEY-README.txt"


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source archive: {SRC}")

    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    plain = SRC.read_bytes()

    padder = padding.PKCS7(128).padder()
    padded = padder.update(plain) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded) + encryptor.finalize()

    ENC.write_bytes(encrypted)

    meta = f"""OpenClaw production backup encryption metadata
Created: {datetime.now(timezone.utc).isoformat()}
Source archive: {SRC.name}
Encrypted file: {ENC.name}
Algorithm: AES-256-CBC + PKCS7
Key (Base64, store offline): {__import__('base64').b64encode(key).decode()}
IV (Base64): {__import__('base64').b64encode(iv).decode()}
NOTE: Do NOT commit key to git. Delete plaintext tar.gz after verifying decrypt.
"""
    META.write_text(meta, encoding="utf-8")
    print(f"Encrypted -> {ENC} ({ENC.stat().st_size} bytes)")
    print(f"Key metadata -> {META}")


if __name__ == "__main__":
    main()
