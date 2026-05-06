# The Pre-Execution Gap

## The Kernel’s Own Words

Inside `linux/kernel/fork.c`, after the new task has been constructed but before it is made visible to the rest of the system, the kernel states:

```c
/*
 * Make it visible to the rest of the system, but dont wake it up yet.
 * Need tasklist lock for parent etc handling!
 */
write_lock_irq(&tasklist_lock);
