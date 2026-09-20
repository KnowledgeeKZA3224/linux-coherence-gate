# 🧠 How It Works — No Jargon Required

Imagine Linux has a locked door between **"a program wants to run"** and **"the program is now running."** 🐧🚪

Supreme Computation puts a proof check in front of that door for processes that are explicitly governed.

## The 6-step path

### 1. ✋ Stop before execution
The launcher creates the child process but stops it **before the new program starts**.

### 2. 🔎 Measure exactly what wants to run
Supreme Computation records the exact executable and context:

- process ID
- path + arguments
- device + inode
- file size + timestamps
- SHA-256 file hash
- running Linux kernel
- active Linux security modules

This prevents "approve one thing, run another."

### 3. 🧭 Run the Supreme Computation decision
Those exact facts become part of the transition evaluated by the eight invariants:

**Time · Continuity · Alignment · Genesis · Boundary · Reference · Causality · Observer**

### 4. 🎟️ Create permission only after PERMIT
Only `PERMIT` **plus** `execution_authorized=true` can create the kernel grant.

The grant is:

- for one exact process
- for one exact executable identity
- short-lived
- consumed once

### 5. 🐧 Linux makes the final enforcement check
At Linux's `bprm_check_security` security hook, the BPF-LSM program asks:

> Does this governed process have the exact live grant for this executable?

**Yes → execute.** ✅  
**No → EACCES.** 🛑

### 6. 🧾 Leave a receipt
The decision includes a transition ID, receipt hash and final proof. The BPF layer also emits an audit event for the kernel-side result.

---

## Why this matters

Most security systems are strongest **after** an event exists: they log it, detect it, alert on it or try to recover.

This mechanism moves the decision **before the governed execution**.

That is the whole idea:

> **Do not ask only whether something bad happened. Require the action to prove it may happen first.**
