#!/usr/bin/env python3
import hashlib
import json
import pathlib
import re
import sys
import tarfile
import tempfile

REQUIRED_INVARIANTS = {
    "Time", "Continuity", "Alignment", "Genesis",
    "Boundary", "Reference", "Causality", "Consciousness",
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def reject(message):
    raise SystemExit(f"REJECT {message}")

def safe_members(tf):
    for member in tf.getmembers():
        p = pathlib.PurePosixPath(member.name)
        if p.is_absolute() or ".." in p.parts:
            reject(f"unsafe archive path={member.name}")
        if member.issym() or member.islnk():
            reject(f"archive links are not permitted path={member.name}")
        yield member

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_release.py <artifact.tar.gz> <artifact.sha256>")

    artifact = pathlib.Path(sys.argv[1])
    sidecar = pathlib.Path(sys.argv[2])
    expected = sidecar.read_text(encoding="utf-8").strip().split()[0]
    actual = sha256(artifact)
    if actual != expected:
        reject(f"hash mismatch expected={expected} actual={actual}")

    with tempfile.TemporaryDirectory() as td:
        root_tmp = pathlib.Path(td)
        with tarfile.open(artifact, "r:gz") as tf:
            members = list(safe_members(tf))
            tf.extractall(root_tmp, members=members)

        roots = [p for p in root_tmp.iterdir() if p.is_dir()]
        if len(roots) != 1:
            reject("archive must contain exactly one release root")
        root = roots[0]

        manifest = root / "MANIFEST.sha256"
        receipt_path = root / "RELEASE_RECEIPT.json"
        invariants_path = root / "INVARIANTS.json"
        for required in (manifest, receipt_path, invariants_path):
            if not required.is_file():
                reject(f"missing required file={required.name}")

        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                reject("malformed manifest")
            digest, rel = parts
            rel = rel.lstrip("*").strip()
            target = (root / rel).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                reject(f"manifest escapes release root path={rel}")
            if not target.is_file():
                reject(f"manifest target missing path={rel}")
            if sha256(target) != digest:
                reject(f"manifest hash mismatch path={rel}")

        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        genesis = receipt.get("genesis_commit", "")
        if not re.fullmatch(r"[0-9a-f]{40}", genesis):
            reject("invalid genesis commit")
        if receipt.get("execution_rule") != "Nothing executes until it proves itself.":
            reject("execution rule mismatch")

        invariants = json.loads(invariants_path.read_text(encoding="utf-8"))
        if set(invariants) != REQUIRED_INVARIANTS:
            reject("8-invariant contract mismatch")

    print(f"PERMIT sha256={actual}")
    print("Continuity: internal manifest verified.")
    print("Genesis: release receipt contains a valid source commit.")
    print("Alignment/Boundary: defensive distribution contract present.")
    print("Reference: exact artifact matches sidecar receipt.")
    print("Consciousness/Observer: verification is independently reproducible.")

if __name__ == "__main__":
    main()
