#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from scpkg.policy import evaluate

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / "sc_preexec_gate_v2.patch"
PATCH_SHA = ROOT / "PATCH_SHA256"
REFERENCE = ROOT / "SOURCE_REFERENCE.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True)

def git(source: Path, *args: str) -> str:
    result = run(["git", "-C", str(source), *args])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()

def load_reference() -> dict:
    return json.loads(REFERENCE.read_text())

def build_evidence(source: Path, mode: str) -> dict:
    ref = load_reference()
    commit = git(source, "rev-parse", "HEAD^{commit}")
    fork = source / "kernel/fork.c"
    if not fork.exists():
        raise RuntimeError("kernel/fork.c is missing")
    expected_patch = PATCH_SHA.read_text().strip().split()[0]
    authorized = mode != "apply" or os.environ.get("SC_AUTHORIZED") == "1"
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "parent_digest": commit,
        "expected_parent_digest": ref["commit_sha1"],
        "intent_digest": expected_patch,
        "artifact_digest": sha256(PATCH),
        "genesis": f"linux-v7.0@{commit}",
        "authorized": authorized,
        "reference_digest": sha256(fork),
        "expected_reference_digest": ref["kernel_fork_c_sha256"],
        "cause": "verify exact source before consequence",
        "observer": socket.gethostname(),
        "mode": mode,
    }

def verify(source: Path, mode: str = "verify") -> dict:
    evidence = build_evidence(source, mode)
    check = run(["git", "apply", "--check", str(PATCH)], cwd=source)
    if check.returncode:
        raise RuntimeError(check.stderr.strip() or check.stdout.strip())
    decision = evaluate(evidence)
    result = {
        "allowed": decision.allowed,
        "failed": list(decision.failed),
        "checks": dict(decision.checks),
        "evidence": evidence,
        "patch_sha256": sha256(PATCH),
    }
    if not decision.allowed:
        raise RuntimeError("SC gate denied: " + ", ".join(decision.failed))
    return result
def write_receipt(source: Path, output: Path) -> Path:
    result = verify(source, "verify")
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return output

def apply_patch(source: Path) -> None:
    verify(source, "apply")
    result = run(["git", "apply", str(PATCH)], cwd=source)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())

def main() -> int:
    parser = argparse.ArgumentParser(description="Supreme Computation source-layer gate")
    parser.add_argument("command", choices=["verify", "receipt", "apply"])
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, default=ROOT / "results/SOURCE_LAYER_PROOF.json")
    args = parser.parse_args()
    try:
        if args.command == "verify":
            print(json.dumps(verify(args.source), indent=2, sort_keys=True))
        elif args.command == "receipt":
            print(write_receipt(args.source, args.out))
        else:
            apply_patch(args.source)
            print("PERMIT: authorized patch applied")
        return 0
    except Exception as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
