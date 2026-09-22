#!/usr/bin/env python3
import hashlib
import pathlib
import sys

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_release.py <artifact.tar.gz> <artifact.sha256>")
    artifact = pathlib.Path(sys.argv[1])
    receipt = pathlib.Path(sys.argv[2])
    expected = receipt.read_text(encoding="utf-8").strip().split()[0]
    actual = sha256(artifact)
    if actual != expected:
        raise SystemExit(f"REJECT hash mismatch expected={expected} actual={actual}")
    print(f"PERMIT sha256={actual}")
    print("Reference: exact artifact matches receipt.")
    print("Boundary: verification does not install or execute the artifact.")

if __name__ == "__main__":
    main()
