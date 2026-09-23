#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SOURCE="${1:?usage: ./verify_local.sh /path/to/linux-v7.0-source}"

python3 "$ROOT/scctl.py" receipt "$SOURCE"   --out "$ROOT/results/SOURCE_LAYER_PROOF.json"

(
  cd "$ROOT"
  sha256sum     sc_preexec_gate_v2.patch     scctl.py     scpkg/policy.py     SOURCE_REFERENCE.json     > results/SOURCE_LAYER_ARTIFACTS.sha256
)

cat "$ROOT/results/SOURCE_LAYER_PROOF.json"
