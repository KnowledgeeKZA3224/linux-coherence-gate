# 📦 Supreme Computation Defensive Distribution

## Same source. Same bytes. Same proof.

This directory answers one question:

> How do you move the gate to another authorized machine without turning verification into trust?

The path is:

`SOURCE → BUILD → HASH → PACKAGE → VERIFY → AUTHORIZED DEPLOY → RECEIPT`

The release now carries the whole circuit:

- 🧠 Linux gate artifacts;
- 🚧 explicit deployment boundary;
- 🧾 source reference, hashes, invariant verifier, and proof receipt;
- 🐧 live BPF-LSM integration files;
- 🔩 source-layer patch blueprint.

## Build

```bash
./distribution/build_release.sh
```

## Verify

```bash
python3 distribution/verify_release.py   dist/sc-linux-coherence-gate-*.tar.gz   dist/sc-linux-coherence-gate-*.tar.gz.sha256
```

Verification checks the outer artifact hash, every internal file hash, the eight-invariant contract, the pinned Linux source identity, the source-layer proof receipt, and the patch digest.

## Deploy boundary

The Ansible and Puppet adapters are for machines you own or are explicitly authorized to administer.

They do **not** secretly apply the source patch.

Source patch application remains a separate explicit consequence:

```bash
SC_AUTHORIZED=1 ./install_local.sh /path/to/linux-v7.0-source
```

No silent installation. No credential bypass. No propagation to unapproved hosts.

## Mirrors

The artifact SHA-256 is the cross-mirror identity.

GitHub Releases, approved object storage, IPFS, Arweave, or another mirror may carry the same artifact.

**Different bytes must never share the same release identity.**
