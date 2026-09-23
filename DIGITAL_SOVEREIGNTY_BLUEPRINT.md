# 🌐 Digital Sovereignty Blueprint

## The machine should prove before it obeys

A computer normally treats a valid command as permission to create a consequence.

Supreme Computation adds another question:

> **Can this exact consequence prove it is allowed to exist?**

That changes the operating model from:

`OBEY → OBSERVE → REACT`

to:

`PROVE → PERMIT → EXECUTE → WITNESS`

This repository documents that pattern in public so the rule is inspectable, reproducible, and portable.

---

## The one circuit

There are three pieces.

### 🧠 1. The gate

The gate sits before the governed consequence.

For the source-layer Linux blueprint, the patch targets `copy_process()` in Linux v7.0 after `copy_thread()` and before the new task reaches the later visibility path.

The gate asks whether the process state is internally coherent before Linux continues.
The patch is opt-in. It is disabled by default and is enabled with the kernel command-line switch:

`sc_preexec_gate=1`

That is deliberate. A sovereignty mechanism should not secretly seize control of a machine.

### 🚧 2. The boundary

A correct gate can still be abused if deployment has no boundary.

This repository therefore treats deployment as part of the proof.

The release and deployment path must preserve:

- exact source identity;
- exact artifact digest;
- explicit administrator authorization;
- declared target machines;
- no silent propagation;
- no credential bypass;
- no hidden persistence;
- reproducible verification.

The existing `distribution/` directory packages the defensive release. `deploy/` refuses source-layer application without explicit authorization.

### 🧾 3. The receipt

A decision that cannot be independently checked is still trust.

`scctl.py` produces evidence for the eight Supreme Computation invariants and can write a receipt another observer can inspect.

The receipt binds:

- source commit;
- source-file digest;
- patch digest;
- authorization mode;
- timestamp;
- observer;
- invariant results.
---

## The eight invariants

### ⏱️ Time
The decision exists at a real moment. Old permission is not automatically current permission.

### 🔗 Continuity
The source state must connect to the exact pinned state expected by the proof.

### 🎯 Alignment
The artifact being evaluated must match the artifact that was approved.

### 🌱 Genesis
The system records where the source state came from.

### 🚧 Boundary
Verification is harmless. Application requires explicit authorization.

### 📍 Reference
The exact `kernel/fork.c` bytes must match the pinned upstream reference.

### ➡️ Causality
The patch is not allowed to apply unless the preflight proof succeeds.

### 👁️ Consciousness / Observer
The result identifies a witness and leaves a reproducible receipt.

All eight are evaluated together. Missing proof is not silently converted into permission.

---

## Exact upstream anchor

This blueprint is pinned to Linux v7.0.
- Tag: `v7.0`
- Tag object: `3131ff5a117498bb4b9db3a238bb311cbf8383ce`
- Commit: `028ef9c96e96197026887c0f092424679298aae8`
- `kernel/fork.c` SHA-256: `b393692a3f342f9a197da17a3f94754faafc4a44ef06b35e9867d5dc6dc8baa0`
- SC v2 patch SHA-256: `9991d9ff62cddb0033b2d6e7e73452f699959f73ae1bd361d0e4258f7dc0e554`

Upstream references:

- https://github.com/torvalds/linux/releases/tag/v7.0
- https://github.com/torvalds/linux/commit/028ef9c96e96197026887c0f092424679298aae8
- https://github.com/torvalds/linux/blob/028ef9c96e96197026887c0f092424679298aae8/kernel/fork.c#L2232-L2368
- https://docs.kernel.org/security/lsm.html
- https://docs.kernel.org/bpf/prog_lsm.html

The machine-readable version is [SOURCE_REFERENCE.json](SOURCE_REFERENCE.json).

---

## What the local proof actually proves

The local proof verifies that:

1. the reference Linux commit is the pinned v7.0 commit;
2. `kernel/fork.c` matches the pinned SHA-256;
3. the patch bytes match `PATCH_SHA256`;
4. the patch passes `git apply --check` against that source;
5. the eight invariant contract returns PERMIT;
6. the verifier and policy unit tests pass;
7. a JSON receipt and artifact manifest are produced.
Current receipt:

- [results/SOURCE_LAYER_PROOF.json](results/SOURCE_LAYER_PROOF.json)
- [results/SOURCE_LAYER_ARTIFACTS.sha256](results/SOURCE_LAYER_ARTIFACTS.sha256)

Receipt SHA-256 recorded inside the proof:

`f7ba5f5be5848331acf1fe8b78a3630796299fa8962456c432c96227feb5af17`

---

## What it does **not** prove yet

The source-layer patch has **not** been claimed as a booted production kernel.

That next proof requires a separate sequence:

`PATCH → BUILD → BOOT → TRACE → STRESS → DENY TEST → RECEIPT`

Those steps must produce their own evidence.

The existing BPF-LSM path in this repository is different: that path has already been demonstrated live for explicitly governed process execution. See [LIVE_PROOF.md](LIVE_PROOF.md).

Keeping those two proofs separate prevents a blueprint from being mislabeled as a deployment.

---

## Why this matters

Security usually asks:

> “What happened?”

Supreme Computation asks one layer earlier:

> **“Why should this be allowed to happen at all?”**

That same pattern is portable.

An AI agent can request a tool call.
A bank system can request a transfer.
A robot can request movement.
A cloud controller can request infrastructure change.
A Linux process can request execution.
The domain changes.

The governing question does not:

`Does this exact requested consequence have enough coherent proof to cross the boundary?`

---

## Reproduce it

Verify:

```bash
./verify_local.sh /path/to/linux-v7.0-source
```

Authorized source application:

```bash
SC_AUTHORIZED=1 ./install_local.sh /path/to/linux-v7.0-source
```

Run the invariant tests:

```bash
python3 -m unittest -v tests/test_policy.py
```

Build the deterministic defensive distribution:

```bash
./distribution/build_release.sh
```

Verify a release:

```bash
python3 distribution/verify_release.py dist/sc-linux-coherence-gate-*.tar.gz dist/*.sha256
```

---

## The point of publishing it

The blueprint is public so nobody has to believe the creator.

Read it.
Hash it.
Break it.
Reproduce it.
Improve it.
Keep the boundary explicit.
Leave a receipt.

**That is what digital sovereignty looks like in code.**
