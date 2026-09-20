# 🔴 LIVE PROOF — Supreme Computation × Linux

**Status:** LIVE ✅  
**Date:** 2026-09-19  
**Host:** Ubuntu 26.04.1 LTS  
**Kernel:** `7.0.0-31-generic`

## What was proven

A governed executable was bound to an exact Supreme Computation transition before execution.

### Authorized path ✅

Supreme Computation returned:

- `decision = PERMIT`
- `execution_authorized = true`
- exact executable identity bound into the decision
- short-lived one-time kernel grant created
- Linux allowed the matching exec
- child exited successfully

Recorded live receipt:

- **transition_id:** `7b30ecbd6f2234c0b49d03af2896af7b1300d43ebda31238a7fed23d53424c4d`
- **receipt_hash:** `b6df0f1d280b1de640467576d312a580946b975211bbeec6145db084f5dad98c`
- **final_proof:** `96f848132b78df3d4985828ae928a3263e8b9c6b5e8947461140bd458736898e`
- **resolved executable:** `/usr/bin/gnutrue`
- **SHA-256:** `913a39cd38f353497086bcf317b12f91f93c23b51869cea763b8340b4f84cfd3`

## Fail-closed path 🛑

A second child was deliberately marked **governed** but received **no execution grant**.

When resumed:

- Linux reached the BPF-LSM `bprm_check_security` hook
- no matching grant existed
- the kernel returned **EACCES**
- the requested program did not execute
- the proof harness recorded exit sentinel `77`

**Result:** `SCQOS_KERNEL_DENY_PROOF_GREEN` ✅

That is the difference between **observing** a decision and **enforcing** it.

## Live kernel state

```text
Kernel: 7.0.0-31-generic
LSM: lockdown,capability,landlock,yama,apparmor,bpf,ima,evm
scqos-kernel-v2.service: active
scqos-kernel-v2.service: enabled
legacy scqos-lsm.service: inactive
governed map: present
exec_grants map: present
events map: present
```

## Validation receipts

- 🧪 25 / 25 local tests green
- 🛡️ 6 / 6 ProofGate adversarial cases green
- 🟩 GitHub CI green
- 🟩 GitHub main-integrity green
- 🟩 GitHub kernel-v2 workflow green
- ☁️ AWS Systems Manager live-node control verified

## Visual receipt

![Live Linux kernel proof](http://SupremeComputation.org/proofs/SCQOS_LINUX_KERNEL_LIVE_PROOF_FINAL.png)

## Exact scope

The proven enforcement boundary is **process exec** for processes explicitly enrolled by the Supreme Computation launcher.

This proof does **not** claim every Linux operation is governed, and it does **not** claim the Linux source tree itself was patched. The enforcement is attached using Linux's supported **BPF-LSM** security mechanism.
