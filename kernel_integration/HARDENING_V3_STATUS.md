# SCQOS hardening v3 status

This isolated branch is the active Linux hardening review track. Main and the proven v2 path remain unchanged until the v3 path is validated.

## Closed in this branch

The launcher now opens the executable before governance, hashes and identifies that exact open file object, retains the descriptor across the governance interval, revalidates the same descriptor immediately before the grant, rejects pathname drift, and executes the already-open object.

That closes pathname-substitution TOCTOU: replacing the filename after governance can no longer cause a different inode to be executed under the old permit.

## Still held

The BPF-LSM grant currently binds TGID + device + inode. An inode's bytes could still be modified in place after the final userspace digest check and before the kernel consumes the grant.

That remaining content-mutation interval is not being declared solved.

The v3 direction is to bind the executable to Linux fs-verity (or another kernel-enforced immutable-content primitive) so the content identity enforced by the kernel is the same content identity admitted by SCQOS.

## Required validation before merge

- authorized fd-bound exec succeeds;
- missing, expired, mismatched and replayed grants fail closed;
- pathname rename/replacement after governance cannot substitute another executable;
- pathname drift is rejected before release;
- in-place content mutation is explicitly reproduced against the non-fs-verity path;
- fs-verity content identity is bound and mutation is rejected by the kernel;
- lifecycle/PID-reuse behavior is falsified;
- one-shot grant consumption and audit receipt continuity remain intact.

## Boundary

This branch does not claim Linux upstream acceptance and does not alter main. It exists to turn the remaining TOCTOU question into a smaller falsifiable kernel-facing contract.
