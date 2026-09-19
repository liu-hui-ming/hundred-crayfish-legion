#!/bin/bash
# [System_Tag: CANONICAL-v3.1]
# v10.5-research One-click bootstrap & baseline freeze

set -euo pipefail

BOOTSTRAP_VERSION="v10.5-research"
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "${SCRIPT_DIR}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[BOOTSTRAP-INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[BOOTSTRAP-WARN]${NC} $1"; }
log_error() { echo -e "${RED}[BOOTSTRAP-ERROR]${NC} $1"; }

log_info "=============================================="
log_info "  v10.5-research Full Bootstrap Starter"
log_info "  System_Tag: CANONICAL-v3.1 | Version: ${BOOTSTRAP_VERSION}"
log_info "=============================================="

REQUIRED_FILES=(
    "check_isolation.sh"
    "veto_tee_stub.py"
    "enclave_entry.py"
    "test_iron_laws.py"
    "v105-enclave.manifest.template"
    "manifest.json"
)

log_info "Step1: Validate core baseline files exist"
for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "${f}" ]; then
        log_error "Missing required file: ${f}"
        exit 1
    fi
done
log_info "All core baseline files present"

log_info "Step2: Set executable permission for pipeline script"
chmod +x check_isolation.sh
log_info "chmod +x check_isolation.sh done"

log_info "Step3: Launch full pipeline check_isolation.sh"
./check_isolation.sh

log_info "Step4: Try inject git commit id to manifest.json"
if git rev-parse --is-inside-work-tree &>/dev/null; then
    GIT_COMMIT_ID=$(git rev-parse HEAD)
    ISO_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    log_info "Detected git repository, HEAD commit: ${GIT_COMMIT_ID}"
    export GIT_COMMIT_ID ISO_TIMESTAMP

    PYTHON=python3
    if ! command -v python3 &>/dev/null; then
        PYTHON=python
    fi

    "${PYTHON}" <<'PYPATCH'
import json
import os

manifest_path = "manifest.json"
git_commit = os.environ["GIT_COMMIT_ID"]
iso_ts = os.environ["ISO_TIMESTAMP"]
with open(manifest_path, "r", encoding="utf-8") as fp:
    data = json.load(fp)
if data.get("baseline_meta") is None:
    data["baseline_meta"] = {}
data["baseline_meta"]["git_commit_id"] = git_commit
data["baseline_meta"]["creation_timestamp"] = iso_ts
with open(manifest_path, "w", encoding="utf-8") as fp:
    json.dump(data, fp, indent=4, ensure_ascii=False)
print("manifest.json updated: git_commit_id & creation_timestamp filled")
PYPATCH
else
    log_warn "Current directory is not git repository, skip filling git commit id"
fi

log_info ""
log_info "Bootstrap-baseline freeze workflow FINISHED (internal archive — no public Release)"
