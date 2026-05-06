# SC Coherence Policy

## Purpose

v1 names the boundary.

v2 measures the boundary.

v3 must enforce something Linux does not currently enforce as a unified pre-visibility policy.

That is where Supreme Computation moves from observation into contribution.

## Candidate Invariant 1

### Capability Namespace Coherence

If a process enters a new user namespace:

CLONE_NEWUSER

its effective capabilities must not exceed the capability bounds of the target namespace.

### Research Question

Does Linux guarantee this implicitly?

Or can it be asserted explicitly at the pre-visibility boundary?

## Candidate Invariant 2

### PID Namespace Ancestry

A task created in a nested PID namespace must maintain visible ancestry across every namespace level.

### Research Question

Can namespace ancestry be asserted before PID allocation?

## Candidate Invariant 3

### cgroup Pre Admission

Before visibility:

the target cgroup must:

- exist
- not be dying
- not exceed task limits

### Research Question

Can admission be denied before task list insertion?

## Integrity Rule

No invariant is claimed novel until:

- kernel source is verified
- behavior is measured
- failure cases are reproduced
- traces are published

No exceptions.
