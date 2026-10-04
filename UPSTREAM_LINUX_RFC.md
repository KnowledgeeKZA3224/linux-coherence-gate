# 📡 Upstream Linux / LSM Review Packet

## What is being proposed for review?

A **scoped, one-shot pre-execution authorization pattern** built on the existing Linux BPF-LSM `bprm_check_security` hook.

The live v2 prototype does **not** require patching Linux itself. The v3 hardening candidate in this branch strengthens the binding contract without expanding the kernel-facing scope.

For an explicitly governed process:

1. stop the child before exec;
2. bind the executable and runtime identity into an external governance decision;
3. create a short-lived governed record and matching one-shot exec grant only after authorization;
4. resume the child;
5. let BPF-LSM enforce the final allow/deny at `bprm_check_security`;
6. consume both authority records before the matching exec is allowed.

Missing, expired or mismatched authorization returns `-EACCES`.

## v3 lifecycle hardening

The candidate now requires one decision generation to remain coherent across:

- TGID
- cgroup-v2 ID
- effective UID/GID
- executable device
- executable inode
- executable size
- decision nonce
- exact expiry

The launcher rechecks the stopped child, cgroup, credentials and full userspace file identity immediately before map installation. The LSM independently rechecks the kernel-visible boundary. The governed record is installed before the grant so any partial installation fails closed.

Successful authorization consumes both records before the hook returns allow.

## Why bring this to Linux / LSM reviewers?

The technical question is not "does Linux need Supreme Computation?"

The useful upstream question is:

> **Is a scoped, one-shot decision-generation binding a sound way to connect a userspace authorization decision to one exact exec consequence through BPF-LSM without machine-wide lockout or stale-authority reuse?**

A second, narrower question remains open:

> **What existing kernel integrity primitive should bind the exact executable bytes across the final userspace-to-bprm interval: fs-verity, IMA, an immutable/pre-opened executable object, or another LSM-native mechanism?**

That residual question is explicit. The branch does not claim cryptographic content verification inside BPF-LSM.

## Live evidence already established by v2

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

Full v2 receipt: [LIVE_PROOF.md](./LIVE_PROOF.md)

The v3 branch adds lifecycle/cross-map hardening and its own compile/regression CI. It must earn fresh runtime proof before replacing the v2 evidence claim.

## Code for review

- [BPF-LSM hook](./kernel_integration/scqos_exec_gate.bpf.c)
- [loader](./kernel_integration/scqos_exec_gate_loader.c)
- [governed launcher](./kernel_integration/scqos_kernel_exec.py)
- [v3 hardening notes](./V3_HARDENING.md)

## Exact non-claims

- No claim that Linux source was patched.
- No claim that every Linux operation is governed.
- No claim that this should be merged upstream as-is.
- No claim that an external governance engine should be part of the kernel.
- No claim that v3 has eliminated every executable-content TOCTOU edge.

The review target is the **kernel-facing authorization pattern**.

## Correct upstream route

Linux kernel contribution guidance directs patches and RFCs through the appropriate subsystem maintainers and mailing lists rather than using GitHub as a normal issue tracker.

For this work, the technically relevant review communities are **BPF** and **Linux Security Module (LSM)**.

Before any formal patch submission, the human submitter must review the final patch, take responsibility for it, and add their own DCO `Signed-off-by` if applicable.

## Suggested RFC subject

`[RFC v2] bpf-lsm: lifecycle-bound one-shot userspace authorization for exec`

## Suggested opening

> This RFC asks for review of a narrow BPF-LSM pattern: binding one external userspace authorization decision to a stopped process and one executable consequence, with cgroup, credential, file identity, nonce and expiry continuity enforced at bprm_check_security. The prototype consumes authority before allow and fails closed on missing or mismatched state. I am specifically asking whether the remaining executable-content integrity edge should use fs-verity, IMA, a pre-opened immutable object, or another existing kernel primitive.
