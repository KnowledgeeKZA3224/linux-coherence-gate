# Patch Notes

**sc_preexec_gate — v1**

## Honest Assessment

v1 is an assertion layer, not a final enforcement gate.

This is stated plainly because the kernel community values technical honesty. Presenting v1 as more than it is would weaken the research.

## What v1 Does

- Adds a named `sc_preexec_gate()` inside `kernel/fork.c`
- Places the gate after `copy_thread()` and before PID allocation and task visibility
- Checks task, credential, signal, namespace, file, memory, and clone flag relationship invariants
- Returns `-EPERM` if the gate fails
- Uses existing fork cleanup path on failure

## What v1 Does Not Do

- It does not yet catch a new class of kernel failure
- It reasserts state Linux should already guarantee
- It does not yet include tracepoints
- It does not yet include a Kconfig guard
- It does not yet include a loadable policy hook

## Why v1 Still Matters

v1 names the boundary.

That matters because the research contribution begins with identifying the exact pre-visibility insertion point, anchoring it in real kernel code, and creating a path toward traceable and policy-extensible enforcement.

## Patch File Status

`sc_preexec_gate_v1.patch` must be validated against a pinned Linux kernel tag using `git apply --check`.

## Version Roadmap

| Version | Goal |
|---|---|
| v1 | Assertion layer. Named boundary. |
| v2 | Tracepoints. Kconfig. |
| v3 | Policy hooks. |
| v4 | Novel invariant enforcement. |
