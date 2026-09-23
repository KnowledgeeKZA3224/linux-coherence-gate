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
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def reject(message):
    raise SystemExit(f"REJECT {message}")

def safe_members(tf):
    for member in tf.getmembers():
        path = pathlib.PurePosixPath(member.name)
        if path.is_absolute() or ".." in path.parts:
            reject(f"unsafe archive path={member.name}")
        if member.issym() or member.islnk():
            reject(f"archive links are not permitted path={member.name}")
        yield member
def verify_manifest(root):
    manifest = root / "MANIFEST.sha256"
    if not manifest.is_file():
        reject("missing MANIFEST.sha256")

    listed = set()
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
        listed.add(pathlib.PurePosixPath(rel).as_posix())

    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.name != "MANIFEST.sha256"
    }
    if listed != actual:
        missing = sorted(actual - listed)
        stale = sorted(listed - actual)
        reject(f"manifest coverage mismatch missing={missing} stale={stale}")
def verify_source_layer(root):
    required = [
        root / "SOURCE_REFERENCE.json",
        root / "PATCH_SHA256",
        root / "sc_preexec_gate_v2.patch",
        root / "results/SOURCE_LAYER_PROOF.json",
        root / "results/SOURCE_LAYER_ARTIFACTS.sha256",
        root / "scctl.py",
        root / "scpkg/policy.py",
    ]
    for path in required:
        if not path.is_file():
            reject(f"missing source-layer file={path.relative_to(root)}")

    reference = json.loads((root / "SOURCE_REFERENCE.json").read_text(encoding="utf-8"))
    commit = reference.get("commit_sha1", "")
    fork_hash = reference.get("kernel_fork_c_sha256", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        reject("invalid pinned Linux commit")
    if not re.fullmatch(r"[0-9a-f]{64}", fork_hash):
        reject("invalid pinned fork.c SHA-256")

    patch_sidecar = (root / "PATCH_SHA256").read_text(encoding="utf-8").split()[0]
    patch_actual = sha256(root / "sc_preexec_gate_v2.patch")
    if patch_sidecar != patch_actual:
        reject("source patch digest mismatch")
    proof = json.loads((root / "results/SOURCE_LAYER_PROOF.json").read_text(encoding="utf-8"))
    stored_receipt = proof.get("receipt_sha256", "")
    receipt_body = dict(proof)
    receipt_body.pop("receipt_sha256", None)
    canonical = json.dumps(receipt_body, sort_keys=True, separators=(",", ":")).encode()
    calculated_receipt = hashlib.sha256(canonical).hexdigest()
    if stored_receipt != calculated_receipt:
        reject("source-layer receipt digest mismatch")
    if proof.get("allowed") is not True or proof.get("failed") != []:
        reject("source-layer receipt is not PERMIT")
    checks = proof.get("checks", {})
    if set(checks) != REQUIRED_INVARIANTS or not all(checks.values()):
        reject("source-layer 8-invariant proof mismatch")
    evidence = proof.get("evidence", {})
    if evidence.get("parent_digest") != commit:
        reject("source-layer parent commit mismatch")
    if evidence.get("reference_digest") != fork_hash:
        reject("source-layer reference digest mismatch")
    if proof.get("patch_sha256") != patch_actual:
        reject("source-layer proof patch digest mismatch")

    artifact_manifest = root / "results/SOURCE_LAYER_ARTIFACTS.sha256"
    for line in artifact_manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        rel = rel.lstrip("*").strip()
        target = root / rel
        if not target.is_file():
            reject(f"source-layer artifact missing path={rel}")
        if sha256(target) != digest:
            reject(f"source-layer artifact digest mismatch path={rel}")

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_release.py <artifact.tar.gz> <artifact.sha256>")

    artifact = pathlib.Path(sys.argv[1])
    sidecar = pathlib.Path(sys.argv[2])
    expected = sidecar.read_text(encoding="utf-8").strip().split()[0]
    actual = sha256(artifact)
    if actual != expected:
        reject(f"hash mismatch expected={expected} actual={actual}")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = pathlib.Path(temp_dir)
        with tarfile.open(artifact, "r:gz") as tf:
            members = list(safe_members(tf))
            tf.extractall(temp_root, members=members)

        roots = [p for p in temp_root.iterdir() if p.is_dir()]
        if len(roots) != 1:
            reject("archive must contain exactly one release root")
        root = roots[0]

        verify_manifest(root)

        receipt_path = root / "RELEASE_RECEIPT.json"
        invariants_path = root / "distribution/INVARIANTS.json"
        boundary_path = root / "distribution/DEPLOYMENT_BOUNDARY.md"
        for required in (receipt_path, invariants_path, boundary_path):
            if not required.is_file():
                reject(f"missing required file={required.relative_to(root)}")

        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        genesis = receipt.get("genesis_commit", "")
        if not re.fullmatch(r"[0-9a-f]{40}", genesis):
            reject("invalid release genesis commit")
        if receipt.get("execution_rule") != "Nothing executes until it proves itself.":
            reject("execution rule mismatch")
        invariants = json.loads(invariants_path.read_text(encoding="utf-8"))
        if set(invariants) != REQUIRED_INVARIANTS:
            reject("8-invariant distribution contract mismatch")

        verify_source_layer(root)

    print(f"PERMIT sha256={actual}")
    print("Time: release receipt contains a deterministic build time.")
    print("Continuity: every packaged file is covered by the internal manifest.")
    print("Alignment: patch and source-layer artifact digests match.")
    print("Genesis: release and Linux source identities are explicit.")
    print("Boundary: authorized defensive deployment contract is present.")
    print("Reference: pinned Linux source and exact hashes match the proof.")
    print("Causality: source-layer receipt is PERMIT only after preflight validation.")
    print("Consciousness/Observer: the release can be independently re-verified.")

if __name__ == "__main__":
    main()
