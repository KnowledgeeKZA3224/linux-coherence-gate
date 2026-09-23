# The Pre-Execution Gap

## Exact Linux source boundary

Pinned source: Linux v7.0 commit `028ef9c96e96197026887c0f092424679298aae8`.

Inside `kernel/fork.c`, `copy_process()` builds a new task through a long sequence of checks and copies.

Near line 2232:

```c
retval = copy_thread(p, args);
if (retval)
    goto bad_fork_cleanup_io;
```

Later, near line 2366, Linux contains the comment:

```c
/*
 * Make it visible to the rest of the system, but dont wake it up yet.
 * Need tasklist lock for parent etc handling!
 */
write_lock_irq(&tasklist_lock);
```

Source:
https://github.com/torvalds/linux/blob/028ef9c96e96197026887c0f092424679298aae8/kernel/fork.c#L2232-L2368
## Why Supreme Computation targets this area

The question is not “is Linux broken?”

The question is:

> Before the new task crosses further toward visibility, can an optional policy gate require one more coherent proof?

`sc_preexec_gate_v2.patch` inserts that optional check after `copy_thread()`.

The gate checks relationships Linux expects to be coherent, including:

- task / clone arguments exist;
- credentials exist;
- signal structures exist;
- namespace state exists;
- file context is coherent;
- memory context is coherent for non-kernel threads;
- `CLONE_THREAD` implies `CLONE_SIGHAND`;
- `CLONE_SIGHAND` implies `CLONE_VM`.

If enabled and a check fails, the fork path returns an error through Linux's existing cleanup path.

## Important boundary

The patch is disabled by default.

Enable switch:

`sc_preexec_gate=1`

The current repository proves clean application against the pinned source. It does **not** claim this source patch has already been built and booted in production.
