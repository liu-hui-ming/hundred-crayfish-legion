# [System_Tag: CANONICAL-v3.1]
"""enclave_entry.py — Enclave minimal entrypoint (stdin JSON → stdout JSON)"""

import json
import sys

from veto_tee_stub import generate_tee_quote, sha256_bytes, verify_isolation_boundary

__version__ = "v10.5-research"


def main():
    raw_input = sys.stdin.read()
    payload_hash = sha256_bytes(raw_input.encode("utf-8"))
    input_obj = json.loads(raw_input)

    payload = input_obj["payload"]
    context = input_obj["context"]

    verify_result = verify_isolation_boundary(payload, context)
    quote = generate_tee_quote(payload_hash)

    output = {
        "system_tag": "CANONICAL-v3.1",
        "version": __version__,
        "payload_sha256": payload_hash,
        "boundary_verify": verify_result,
        "tee_quote": quote,
    }
    sys.stdout.write(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
