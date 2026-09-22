# Supreme Computation Defensive Distribution

One source state, one deterministic release, many independently verifiable mirrors.

Pipeline:

SOURCE -> BUILD -> 8-INVARIANT CHECK -> HASH -> PACKAGE -> AUTHORIZED DEPLOY -> MIRROR -> VERIFY -> RECEIPT

This layer does not silently install, hide inside unrelated dependencies, or deploy without authorization. It packages the existing Linux pre-execution gate as auditable defensive infrastructure.

## Invariants

Time, Continuity, Alignment, Genesis, Boundary, Reference, Causality, Consciousness/Observer.

## Commands

Build a release bundle:

```bash
./distribution/build_release.sh
```

Verify a bundle:

```bash
python3 distribution/verify_release.py dist/sc-linux-coherence-gate-*.tar.gz dist/*.sha256
```

Deploy only to systems you administer or have explicit authorization to manage:

```bash
ansible-playbook distribution/ansible/playbook.yml -i inventory --limit authorized_hosts
```

The Puppet adapter is under `distribution/puppet`.

## Mirrors

The generated SHA-256 digest is the canonical cross-mirror reference. Publish the same release artifact to GitHub Releases, approved object storage, and optional content-addressed mirrors such as IPFS/Arweave. Never publish different bytes under the same release identity.
