# 🐧 LKML Submission — Supreme Computation × Linux

## Subject

`[RFC] BPF-LSM one-shot authorization at the execution boundary`

## Plain-English summary

This prototype asks Linux one simple question:

> **Can a machine action be forced to prove it has permission before Linux lets it execute?**

The live answer is **yes for the proven scope: explicitly governed process execution through BPF-LSM.**

## What is live

- 🐧 Ubuntu 26.04.1 / Linux `7.0.0-31-generic`
- 🔒 BPF-LSM active
- 🎟️ Short-lived, one-time execution grants
- ✅ Valid governed execution passes
- 🛑 Governed execution with no valid grant is denied with `EACCES` before the requested program starts
- 🧪 25 / 25 local tests green
- 🛡️ 6 / 6 ProofGate adversarial cases green
- 🟩 CI, integrity, and kernel validation green

## What Linux reviewers are being asked to judge

The review target is narrow:

1. Is the one-shot grant pattern a sound way to bind a userspace authorization decision to one exact exec consequence?
2. Is the current process/executable identity binding strong enough?
3. What race conditions remain between userspace revalidation and `bprm_check_security`?
4. Is there an existing Linux primitive that can make the binding stronger or simpler?
5. Are the TTL, one-shot consumption, and cleanup semantics correct?

## Exact scope

- ✅ Live BPF-LSM enforcement for explicitly governed process exec
- ❌ No claim that Linux source itself was patched
- ❌ No claim that every kernel operation is governed
- ❌ No claim that this is ready to merge upstream as-is

## Review links

- [Main repository](https://github.com/KnowledgeeKZA3224/linux-coherence-gate)
- [Live proof](./LIVE_PROOF.md)
- [How it works](./HOW_IT_WORKS.md)
- [BPF-LSM source](./kernel_integration/scqos_exec_gate.bpf.c)
- [Userspace launcher](./kernel_integration/scqos_kernel_exec.py)

## Public submission text

Hello LKML, BPF, and LSM reviewers,

I’m requesting technical review of a live BPF-LSM prototype that binds a short-lived, one-time userspace authorization grant to one exact governed program execution at the Linux security boundary.

The live system is running on Ubuntu 26.04.1 / Linux 7.0.0-31-generic.

Observed result:
- authorized governed execution succeeds;
- governed execution without a valid grant is denied by Linux with EACCES before the requested program starts;
- BPF LSM is active;
- the governed / exec_grants / events maps are active;
- 25/25 local tests are green;
- 6/6 ProofGate adversarial tests are green;
- CI, integrity, and kernel validation are green.

The review question is intentionally narrow: is this one-shot authorization binding pattern sound, and are there stronger existing Linux primitives for carrying an external authorization decision to the execution boundary?

Repository:
https://github.com/KnowledgeeKZA3224/linux-coherence-gate

Live proof:
https://github.com/KnowledgeeKZA3224/linux-coherence-gate/blob/main/LIVE_PROOF.md

Mechanism:
https://github.com/KnowledgeeKZA3224/linux-coherence-gate/blob/main/HOW_IT_WORKS.md

The Linux source tree itself was not patched. The proven scope is explicitly governed process execution through BPF-LSM.

Knowledgee KZA
http://SupremeComputation.org
