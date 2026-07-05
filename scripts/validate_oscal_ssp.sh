#!/usr/bin/env bash
# Validate an OSCAL SSP emitted by generate_oscal_ssp.py using compliance-trestle.
#
# Requires: pip install compliance-trestle
# Usage (from repo root):
#   ./scripts/validate_oscal_ssp.sh output/ssp.oscal.json
#   ./scripts/validate_oscal_ssp.sh output/ssp.oscal.json --workspace ./trestle-workspace

set -euo pipefail

OSCAL_FILE=""
WORKSPACE="./trestle-workspace"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      WORKSPACE="${2:?missing path after --workspace}"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 <ssp.oscal.json> [--workspace <dir>]" >&2
      exit 0
      ;;
    *)
      if [[ -z "${OSCAL_FILE}" ]]; then
        OSCAL_FILE="$1"
      else
        echo "unexpected argument: $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "${OSCAL_FILE}" ]]; then
  echo "Usage: $0 <ssp.oscal.json> [--workspace <trestle-workspace-dir>]" >&2
  exit 1
fi

if [[ ! -f "${OSCAL_FILE}" ]]; then
  echo "error: OSCAL file not found: ${OSCAL_FILE}" >&2
  exit 1
fi

if ! command -v trestle >/dev/null 2>&1; then
  cat >&2 <<'EOF'
error: compliance-trestle is not installed.

Install:
  pip install compliance-trestle

Then initialize a workspace (or use compliance-trestle-skills):
  trestle init -d trestle-workspace

See references/grc/companion-stack.md and references/multi-framework-crosswalk.md.
EOF
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OSCAL_ABS="$(cd "$(dirname "${OSCAL_FILE}")" && pwd)/$(basename "${OSCAL_FILE}")"

mkdir -p "${WORKSPACE}"
cd "${REPO_ROOT}/${WORKSPACE}"

if [[ ! -f .trestle/config.json ]]; then
  echo "initializing trestle workspace at ${WORKSPACE}"
  trestle init
fi

IMPORT_NAME="cmmc-imported-ssp"
echo "importing ${OSCAL_ABS} as ${IMPORT_NAME}"
trestle import -f "${OSCAL_ABS}" -o "${IMPORT_NAME}"

echo "validating ${IMPORT_NAME}"
trestle validate -f "${IMPORT_NAME}"

echo "OSCAL validation passed for ${OSCAL_FILE}"
