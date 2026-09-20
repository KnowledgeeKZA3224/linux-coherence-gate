# Kernel integration source

These files mirror the **live v2 Linux execution boundary** from the Supreme Computation reference implementation.

## What each file does

- `scqos_exec_gate.bpf.c` — Linux BPF-LSM hook. For an explicitly governed process, the exact grant must exist or exec is denied with `EACCES`.
- `scqos_exec_gate_loader.c` — loads the BPF object, pins the maps and attaches the LSM program.
- `scqos_kernel_exec.py` — stops the child before exec, binds the exact executable facts into Supreme Computation governance, then creates the one-time grant only after PERMIT.
- `activate_v2.sh` — validates the host and stages/activates the kernel gate fail-closed.

## Important dependency

The launcher calls the full Supreme Computation governance runtime from:

https://github.com/KnowledgeeKZA3224/scqos-reference-implementation

This repository is the **Linux-focused proof + source mirror**. It intentionally does not duplicate the entire SCQOS runtime.

## Proven boundary

Current live proof: **explicitly governed process exec** through Linux BPF-LSM `bprm_check_security`.

It does not claim every file/socket/capability operation is governed by v2 yet.
