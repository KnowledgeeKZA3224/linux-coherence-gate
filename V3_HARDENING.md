# SCQOS v3 lifecycle hardening

This branch hardens the existing scoped, one-shot BPF-LSM exec gate without changing the public claim into something larger than the evidence.

## What changed

A governed exec now binds one decision generation across both pinned maps.

The kernel requires all of these to agree at `bprm_check_security`:

- TGID
- cgroup-v2 ID
- effective UID/GID
- executable device
- executable inode
- executable size
- decision nonce
- exact expiry generation

A mismatch is a deny. A successful match consumes both authority records before the hook returns allow.

The launcher also verifies that the child is still stopped, still in the same cgroup, still under the same effective credentials, and still points at the same full userspace file identity immediately before it installs the maps. Partial map installation is cleaned up on every abnormal path.

## What this closes

This removes the ability to combine a stale governed marker with a grant from another decision generation. It also prevents a grant from surviving a cgroup or credential boundary change and adds executable size to the kernel-side file identity.

The two-map write order remains fail-closed: governed state is written first. If release happened unexpectedly before the grant existed, the LSM denies exec rather than treating the process as ungoverned.

## What this does not claim

This is not a claim that all TOCTOU questions are solved.

The userspace proposition contains SHA-256, mtime and ctime, but the BPF-LSM hook does not cryptographically hash file contents. A same-inode, same-size content mutation in the narrow interval after the final userspace identity check remains a review question.

The next upstream question is whether that content-integrity edge should be closed with an existing kernel primitive such as fs-verity / IMA measurement, an immutable pre-opened executable object, or another LSM-native binding. The branch intentionally exposes that residual boundary instead of calling it solved.

## Review target

Review whether the added generation, cgroup, credential and file-size bindings are sound and whether the remaining content-integrity edge should be solved outside BPF-LSM or through an existing kernel integrity facility.
