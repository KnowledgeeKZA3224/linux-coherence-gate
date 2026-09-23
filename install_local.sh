#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SOURCE="${1:?usage: SC_AUTHORIZED=1 ./install_local.sh /path/to/linux-v7.0-source}"
if [[ "${SC_AUTHORIZED:-0}" != "1" ]]; then
  echo "REJECT: SC_AUTHORIZED=1 is required" >&2
  exit 2
fi
python3 "$ROOT/scctl.py" apply "$SOURCE"
