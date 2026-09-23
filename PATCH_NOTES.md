# Patch Notes

## `sc_preexec_gate_v2.patch`

### Status

**Locally verified against pinned Linux v7.0 source.**

Pinned commit:

`028ef9c96e96197026887c0f092424679298aae8`

Pinned `kernel/fork.c` SHA-256:

`b393692a3f342f9a197da17a3f94754faafc4a44ef06b35e9867d5dc6dc8baa0`

Patch SHA-256:

`9991d9ff62cddb0033b2d6e7e73452f699959f73ae1bd361d0e4258f7dc0e554`

---

## What v2 does

- adds an optional `sc_preexec_gate()` inside `kernel/fork.c`;
- places the check after `copy_thread()`;
- checks task, credential, signal, namespace, file, memory, and clone-flag relationships;
- returns `-EPERM` on a denied state;
- uses Linux's existing fork cleanup path;
- rate-limits denial logging;
- remains disabled unless `sc_preexec_gate=1` is supplied.
## What v2 proves today

- exact upstream source is pinned;
- exact source-file bytes are hashed;
- exact patch bytes are hashed;
- `git apply --check` passes against that source;
- all eight SC invariant checks pass in the local verifier;
- the policy tests fail closed when any one invariant is broken;
- a machine-readable proof receipt is stored under `results/`.

## What v2 does **not** prove yet

- no claim that this patched source has been built into the currently running kernel;
- no claim that the patched kernel has booted;
- no tracepoint timing claim yet;
- no performance claim yet;
- no claim that this gate covers every Linux consequence.

Those are separate proof stages.

## Relationship to the live BPF-LSM path

The repository's BPF-LSM execution gate is already documented as a live enforcement path for explicitly governed process exec.

The source patch is a second implementation path: a deeper source-level blueprint around process creation.

Do not merge those claims.

Exact boundaries are part of the proof.
