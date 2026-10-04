# Kernel integration source

These files mirror the Linux execution boundary from the Supreme Computation reference implementation.

## What each file does

- `scqos_exec_gate.bpf.c` — Linux BPF-LSM hook. For an explicitly governed process, the exact lifecycle-bound grant must exist or exec is denied with `EACCES`.
- `scqos_exec_gate_loader.c` — loads the BPF object, pins the maps and attaches the LSM program.
- `scqos_kernel_exec.py` — stops the child before exec, binds executable facts plus cgroup and effective credentials into Supreme Computation governance, then creates one decision-generation grant only after PERMIT.
- `activate_v2.sh` — existing v2 activation path. Do not treat the v3 branch as runtime-proven until it is compiled and exercised on a live BPF-LSM host.
- `../V3_HARDENING.md` — exact v3 changes, closed gaps and residual boundary.

## Important dependency

The launcher calls the full Supreme Computation governance runtime from:

https://github.com/KnowledgeeKZA3224/scqos-reference-implementation

This repository is the **Linux-focused proof + source mirror**. It intentionally does not duplicate the entire SCQOS runtime.

## Proven boundary

Current live proof remains **v2 explicitly governed process exec** through Linux BPF-LSM `bprm_check_security`.

The v3 branch adds cgroup, effective-credential, executable-size, shared-nonce and exact-expiry continuity plus fail-closed partial-map cleanup. Those additions are candidate hardening until fresh live execution evidence is recorded.

It does not claim every file/socket/capability operation is governed, and it does not claim the LSM hook cryptographically hashes executable bytes.
