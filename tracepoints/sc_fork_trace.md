# SC Fork Tracepoint Design

## Purpose

The v1 patch uses a direct gate. The next version needs tracepoints so the pre-visibility window can be measured without logging every fork into the kernel log.

## Why Tracepoints

`pr_info()` on every fork is not acceptable for real workloads.

Tracepoints allow the gate to emit structured measurement data only when tracing is enabled.

## Target Event

`sc_preexec_gate`

The event should record:

- parent pid
- child pid if available
- gate result
- reason
- clone flags
- timestamp

## Measurement Goal

Measure the window between:

`copy_thread()` completion  
and  
task visibility beginning at `write_lock_irq(&tasklist_lock)`

## Test Workloads

```bash
stress-ng --fork 4 --fork-ops 100000
