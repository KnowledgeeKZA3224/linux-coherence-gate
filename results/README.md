# Measurement Results

## Status

Pending.

This directory remains intentionally empty until real hardware produces real traces.

## What Will Be Stored Here

### fork_trace_run1.txt

Raw trace output from:

```bash
stress-ng --fork 4 --fork-ops 100000
```

### fork_trace_run2.txt

Container workload traces.

### timing_analysis.md

Distribution of:

- T0 copy_thread complete
- T1 gate complete
- T2 PID allocation
- T3 task visibility

### false_positive_analysis.md

Any incorrect gate firing.

### gate_firing_log.md

Any legitimate gate denial.

## Integrity Rule

No measurements will be fabricated.

No timing claims will be estimated.

No performance claims will be published until:

- patch applies cleanly
- kernel boots
- tracepoints fire
- workloads complete
- traces are archived

Real hardware.

Real traces.

Real science.
