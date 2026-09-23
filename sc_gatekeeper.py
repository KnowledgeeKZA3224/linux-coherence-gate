#!/usr/bin/env python3
"""Compatibility entry point. The canonical gate is scctl.py."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

if len(sys.argv) < 2:
    raise SystemExit("usage: sc_gatekeeper.py /path/to/linux-v7.0-source")

cmd = [sys.executable, str(ROOT / "scctl.py"), "verify", sys.argv[1]]
raise SystemExit(subprocess.run(cmd).returncode)
