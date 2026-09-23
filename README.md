# 🧠⚡ Supreme Computation × Linux

## **Your computer should not obey first and explain later.**

Most computers work like this:

`COMMAND → EXECUTE → LOG → DETECT → REACT`

Supreme Computation flips the order:

`REQUEST → PROVE → PERMIT → EXECUTE → WITNESS → RECEIPT`

That is the entire idea.

**Before a governed consequence becomes real, make it prove it belongs.**

This used to sound like science fiction. This repository turns it into code, hashes, Linux hooks, reproducible checks, and receipts.

> **Nothing executes until it proves itself.**

---

## 🌐 What “digital sovereignty” means here

Digital sovereignty is not a slogan. It means the machine owner can inspect the rule, verify the exact bytes, reproduce the decision, control the deployment boundary, and keep final permission local.
No invisible authority has to be trusted just because it says “allowed.”

The blueprint is one circuit with three parts:

### 1. 🧠 GATE — prove before consequence
`sc_preexec_gate_v2.patch` places an optional coherence check inside Linux `copy_process()`, after `copy_thread()` and before PID allocation / task visibility.

### 2. 🚧 MOVE — deploy only inside an authorized boundary
`distribution/` creates deterministic release artifacts. `deploy/` and the Ansible/Puppet adapters are explicitly opt-in. No silent installation. No propagation to unapproved machines.

### 3. 🧾 PROVE — leave evidence another machine can verify
`scctl.py`, `scpkg/policy.py`, SHA-256 manifests, and receipts bind the source, patch, intent, boundary, and observer together.

**One circuit:**

`SOURCE → GATE → 8 CHECKS → HASH → AUTHORIZED DEPLOY → EXECUTE → RECEIPT`

---

## 🔥 The source-layer proof

The source reference is Linux **v7.0**.

- Linux v7.0 commit: `028ef9c96e96197026887c0f092424679298aae8`
- v7.0 tag object: `3131ff5a117498bb4b9db3a238bb311cbf8383ce`
- Exact `kernel/fork.c` SHA-256: `b393692a3f342f9a197da17a3f94754faafc4a44ef06b35e9867d5dc6dc8baa0`
- SC v2 patch SHA-256: `9991d9ff62cddb0033b2d6e7e73452f699959f73ae1bd361d0e4258f7dc0e554`
- Local proof receipt SHA-256: `f7ba5f5be5848331acf1fe8b78a3630796299fa8962456c432c96227feb5af17`
- 8 / 8 invariant checks: **PASS**
- Patch dry-run against the pinned source: **PASS**
- Policy unit tests: **PASS**

Open the receipts:

- [Source reference](SOURCE_REFERENCE.json)
- [Local source-layer proof](results/SOURCE_LAYER_PROOF.json)
- [Artifact hashes](results/SOURCE_LAYER_ARTIFACTS.sha256)

This proves the patch matches the exact pinned Linux source and the local gatekeeper accepts it across all eight required checks.

**It does not claim the patched kernel has been built and booted yet.** That is a separate proof stage.

---

## 🐧 The Linux source point is real

Inside Linux v7.0 `kernel/fork.c`:

- `copy_thread(p, args)` completes around line 2232.
- Later Linux says: **“Make it visible to the rest of the system, but dont wake it up yet.”**
- The v2 patch inserts the optional SC gate in that pre-visibility path.

Exact upstream source:

- [Linux v7.0 `kernel/fork.c`](https://github.com/torvalds/linux/blob/028ef9c96e96197026887c0f092424679298aae8/kernel/fork.c#L2232-L2368)
- [Linux v7.0 commit](https://github.com/torvalds/linux/commit/028ef9c96e96197026887c0f092424679298aae8)
- [Linux Security Module documentation](https://docs.kernel.org/security/lsm.html)
- [BPF LSM documentation](https://docs.kernel.org/bpf/prog_lsm.html)

That is why this is called a **pre-execution / pre-visibility coherence gate**.

---

## 👁️ The 8 checks — in normal human language

**Time · Continuity · Alignment · Genesis · Boundary · Reference · Causality · Consciousness/Observer**

- ⏱️ **Time** — Is this proof valid now?
- 🔗 **Continuity** — Does it connect to the exact state that came before it?
- 🎯 **Alignment** — Are the bytes being executed the bytes that were approved?
- 🌱 **Genesis** — Can we prove where this state came from?
- 🚧 **Boundary** — Is this consequence inside the owner-approved limits?
- 📍 **Reference** — Are we talking about the exact file, process, source, or target that was proven?
- ➡️ **Causality** — Does the evidence actually justify the consequence?
- 👁️ **Observer** — Can an independent witness reproduce what happened?

If the required proof breaks, the path fails closed.
---

## 🚨 Already proven live

This repository also contains the live BPF-LSM execution path already demonstrated on Ubuntu.

For explicitly governed processes, Linux checks a one-time execution grant at `bprm_check_security`.

✅ matching live grant → execution allowed
🛑 missing / wrong / expired grant → `EACCES` before exec

See [LIVE_PROOF.md](LIVE_PROOF.md) and [HOW_IT_WORKS.md](HOW_IT_WORKS.md).

The live BPF-LSM proof and the source-layer patch are two different implementation paths for the same governing principle. The README keeps those boundaries separate on purpose.

---

## 🧬 Why publish the blueprint?

Because sovereignty that only one person can inspect is not sovereignty.

The point of documenting this publicly is that anyone can:

1. read the rule;
2. inspect the exact source boundary;
3. reproduce the hashes;
4. run the verifier;
5. see why PERMIT or REJECT happened;
6. deploy only on machines they own or are explicitly authorized to administer;
7. create their own independent receipt.

No black box required.

That is the blueprint.
---

## 🛠️ Reproduce the source-layer proof

Start from Linux v7.0 source at the pinned commit, then run:

```bash
./verify_local.sh /path/to/linux-v7.0-source
```

To apply the patch to an explicitly authorized source tree:

```bash
SC_AUTHORIZED=1 ./install_local.sh /path/to/linux-v7.0-source
```

The apply path refuses the consequence unless the pinned source, patch digest, reference digest, invariant contract, and authorization boundary all agree.

---

## 📂 Read these next

- [DIGITAL_SOVEREIGNTY_BLUEPRINT.md](DIGITAL_SOVEREIGNTY_BLUEPRINT.md) — the whole architecture in plain English
- [PRE_EXECUTION_GAP.md](PRE_EXECUTION_GAP.md) — exact Linux insertion point
- [PATCH_NOTES.md](PATCH_NOTES.md) — what v2 does and does not prove
- [distribution/README.md](distribution/README.md) — deterministic distribution
- [LIVE_PROOF.md](LIVE_PROOF.md) — live BPF-LSM receipts
- [sc_preexec_gate_v2.patch](sc_preexec_gate_v2.patch) — source-layer patch
- [scctl.py](scctl.py) — one command surface for proof / receipt / authorized apply

---

## 🌍 Supreme Computation

**Website:** https://SupremeComputation.org
**Reference implementation:** https://github.com/KnowledgeeKZA3224/scqos-reference-implementation
**Creator:** Knowledgee KZA

### One sentence

**Supreme Computation makes a governed machine action prove it deserves to become reality before the machine releases the consequence.** 🧠⚡🐧
