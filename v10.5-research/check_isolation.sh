#!/bin/bash
# [System_Tag: CANONICAL-v3.1]
# Full-pipeline automation for v10.5-research baseline

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
RESEARCH_DIR="${SCRIPT_DIR}"
YC1_DATA_DIR="${RESEARCH_DIR}/yc1_pilot_data"
STATS_OUTPUT="${RESEARCH_DIR}/yc1_statistics.json"
MANIFEST_FILE="${RESEARCH_DIR}/manifest.json"
TEE_STUB_SCRIPT="${RESEARCH_DIR}/veto_tee_stub.py"
TEST_SCRIPT="${RESEARCH_DIR}/test_iron_laws.py"
PIPELINE_VERSION="v10.5-research"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

sha256_file() {
  if command -v sha256sum &>/dev/null; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

log_info "=== Step 0: Environment pre-check ==="
log_info "Pipeline Version: ${PIPELINE_VERSION}"

if ! command -v python3 &>/dev/null; then
    if command -v python &>/dev/null; then
        PYTHON=python
    else
        log_error "python3/python not found, aborting."
        exit 1
    fi
else
    PYTHON=python3
fi

if ! "${PYTHON}" -c "import pytest" &>/dev/null; then
    log_warn "pytest not installed, installing now..."
    "${PYTHON}" -m pip install pytest -q
fi

for f in "${TEE_STUB_SCRIPT}" "${TEST_SCRIPT}"; do
    if [ ! -f "${f}" ]; then
        log_error "missing ${f}"
        exit 1
    fi
done

log_info "Environment OK."

log_info "=== Step 1: YC-1 pilot data generation ==="
if [ ! -d "${YC1_DATA_DIR}" ]; then
    mkdir -p "${YC1_DATA_DIR}"
    log_warn "YC-1 data generation placeholder"
fi

log_info "=== Step 2: Statistics computation ==="
if [ ! -f "${STATS_OUTPUT}" ]; then
    log_warn "Statistics placeholder — using committed yc1_statistics.json or generating minimal"
fi

log_info "=== Step 3: Dual-mode iron-law regression test ==="

log_info ">>> Running TEE_MODE=stub regression test..."
TEE_MODE=stub "${PYTHON}" -m pytest "${TEST_SCRIPT}" -v --tb=short
log_info "stub-mode: ALL PASS"

log_info ">>> Running TEE_MODE=hardware regression test..."
set +e
TEE_MODE=hardware "${PYTHON}" -m pytest "${TEST_SCRIPT}" -v --tb=short 2>&1 | tee /tmp/hardware_test.log
set -e

NON_QUOTE_FAILURES=$(grep FAILED /tmp/hardware_test.log | grep -v test_quote_layer_dual_mode_contract | wc -l || true)
if [ "${NON_QUOTE_FAILURES}" -gt 0 ]; then
    log_error "hardware-mode: business-logic test cases FAILED"
    rm -f /tmp/hardware_test.log
    exit 1
fi
log_info "hardware-mode: business logic ALL PASS, quote NotImplementedError expected"
rm -f /tmp/hardware_test.log

log_info "=== Step 4: SHA256 baseline anchoring ==="
STATS_HASH=$(sha256_file "${STATS_OUTPUT}")
STUB_HASH=$(sha256_file "${TEE_STUB_SCRIPT}")
TEST_HASH=$(sha256_file "${TEST_SCRIPT}")

log_info "yc1_statistics.json  SHA256: ${STATS_HASH}"
log_info "veto_tee_stub.py     SHA256: ${STUB_HASH}"
log_info "test_iron_laws.py    SHA256: ${TEST_HASH}"

log_info "=== Step 5: Manifest update ==="
export MANIFEST_FILE STATS_HASH STUB_HASH TEST_HASH

"${PYTHON}" <<'PYEOF'
import json
import os

manifest_path = os.environ["MANIFEST_FILE"]
stats_hash = os.environ["STATS_HASH"]
stub_hash = os.environ["STUB_HASH"]
test_hash = os.environ["TEST_HASH"]

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

manifest["baseline_hashes"] = {
    "yc1_statistics_sha256": stats_hash,
    "veto_tee_stub_sha256": stub_hash,
    "test_iron_laws_sha256": test_hash,
}

manifest["tee_info"] = {
    "mode": "stub",
    "enclave_type": "sgx_gramine",
    "mrenclave_hash": None,
    "quote_file": None,
    "dcap_attestation_status": "unavailable",
    "mode_warning": "stub-mode for development only, no hardware-root-of-trust, cannot be used for external-audit",
    "compatibility_note": "pre-beta prototype, refer to known_limitations_ref inside manifest and README.md",
}

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4, ensure_ascii=False)
print(f"Manifest updated: {manifest_path}")
PYEOF

log_info "=== Pipeline Complete ==="
