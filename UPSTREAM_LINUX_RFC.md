# 📡 Upstream Linux / LSM Review Packet

## What is being proposed for review?

A **scoped, one-shot pre-execution authorization pattern** built on the existing Linux BPF-LSM `bprm_check_security` hook.

The live prototype does **not** require patching Linux itself.

For an explicitly governed process:

1. stop the child before exec;
2. bind the exact executable identity into an external governance decision;
3. create a short-lived BPF map grant only after authorization;
4. resume the child;
5. let BPF-LSM enforce the final allow/deny at `bprm_check_security`;
6. consume the grant on the first matching exec.

Missing, expired or mismatched authorization returns `-EACCES`.

## Why bring this to Linux / LSM reviewers?

The technical question is not "does Linux need Supreme Computation?"

The useful upstream question is:

> **Is the scoped, one-shot grant pattern a sound way to bind a userspace authorization decision to a specific exec consequence through BPF-LSM without introducing machine-wide lockout or a TOCTOU gap?**

That question is narrow, falsifiable and reviewable.

## Live evidence

- Ubuntu 26.04.1 LTS
- Linux `7.0.0-31-generic`
- active LSM chain includes `bpf`
- BPF-LSM gate active
- exact process + executable identity bound before grant
- valid grant → exec succeeds
- governed process with no grant → Linux returns `EACCES`
- 25/25 local tests green
- ProofGate 6/6 green
- GitHub CI / integrity / kernel validation green

Full receipt: [LIVE_PROOF.md](./LIVE_PROOF.md)

## Code for review

- [BPF-LSM hook](./kernel_integration/scqos_exec_gate.bpf.c)
- [loader](./kernel_integration/scqos_exec_gate_loader.c)
- [governed launcher](./kernel_integration/scqos_kernel_exec.py)
- [activation path](./kernel_integration/activate_v2.sh)

## Exact non-claims

- No claim that Linux source was patched.
- No claim that every Linux operation is governed.
- No claim that this should be merged upstream as-is.
- No claim that an external governance engine should be part of the kernel.

The review target is the **kernel-facing authorization pattern**.

## Correct upstream route

The `torvalds/linux` GitHub issue tracker restricts issue creation, and Linux kernel contribution guidance directs patches and RFCs through the appropriate subsystem maintainers and mailing lists rather than using GitHub as a normal issue tracker.

For this work, the technically relevant review communities are **BPF** and **Linux Security Module (LSM)**.

Before any formal patch submission, the human submitter must review the final patch, take responsibility for it, and add their own DCO `Signed-off-by` if applicable.

## Suggested RFC subject

`[RFC] bpf-lsm: scoped one-shot userspace authorization binding for exec`

## Suggested opening

> This RFC asks for review of a narrow BPF-LSM pattern: binding an external userspace authorization decision to one exact process/executable pair, with a short-lived one-shot grant consumed at `bprm_check_security`. A live prototype demonstrates both an authorized exec and a missing-grant `EACCES` deny. The goal is to test whether this pattern has sound kernel-facing semantics, not to move the external policy engine into the kernel.
