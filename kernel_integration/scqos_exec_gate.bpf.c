// SPDX-License-Identifier: GPL-2.0
// SCQOS kernel source-layer v3: lifecycle-bound, one-shot exec authorization.
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include <bpf/bpf_core_read.h>

char LICENSE[] SEC("license") = "GPL";

enum audit_reason {
    SCQOS_REASON_PERMIT = 0,
    SCQOS_REASON_GOVERNED_EXPIRED = 1,
    SCQOS_REASON_CGROUP_MISMATCH = 2,
    SCQOS_REASON_CREDENTIAL_MISMATCH = 3,
    SCQOS_REASON_FILE_MISSING = 4,
    SCQOS_REASON_INODE_MISSING = 5,
    SCQOS_REASON_GRANT_MISSING = 6,
    SCQOS_REASON_GRANT_EXPIRED = 7,
    SCQOS_REASON_NONCE_MISMATCH = 8,
    SCQOS_REASON_EXPIRY_MISMATCH = 9,
};

struct governed_key {
    __u32 tgid;
};

struct governed_value {
    __u64 expires_ns;
    __u64 decision_nonce;
    __u64 cgroup_id;
    __u64 uid_gid;
};

struct exec_key {
    __u32 tgid;
    __u32 pad;
    __u64 cgroup_id;
    __u64 dev;
    __u64 ino;
    __u64 size;
};

struct grant_value {
    __u64 expires_ns;
    __u64 decision_nonce;
};

struct audit_event {
    __u64 ts_ns;
    __u64 decision_nonce;
    __u64 cgroup_id;
    __u64 uid_gid;
    __u64 dev;
    __u64 ino;
    __u64 size;
    __u32 tgid;
    __u32 reason;
    __s32 result;
    __u32 pad;
};

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 4096);
    __type(key, struct governed_key);
    __type(value, struct governed_value);
} governed SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 16384);
    __type(key, struct exec_key);
    __type(value, struct grant_value);
} exec_grants SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 1 << 22);
} events SEC(".maps");

static __always_inline void audit(__u32 tgid, __u64 cgroup_id,
                                  __u64 uid_gid, __u64 dev, __u64 ino,
                                  __u64 size, __u64 nonce, __u32 reason,
                                  int result)
{
    struct audit_event *e = bpf_ringbuf_reserve(&events, sizeof(*e), 0);
    if (!e)
        return;
    e->ts_ns = bpf_ktime_get_ns();
    e->decision_nonce = nonce;
    e->cgroup_id = cgroup_id;
    e->uid_gid = uid_gid;
    e->dev = dev;
    e->ino = ino;
    e->size = size;
    e->tgid = tgid;
    e->reason = reason;
    e->result = result;
    e->pad = 0;
    bpf_ringbuf_submit(e, 0);
}

SEC("lsm/bprm_check_security")
int BPF_PROG(scqos_exec_gate, struct linux_binprm *bprm, int ret)
{
    if (ret)
        return ret;

    __u64 now = bpf_ktime_get_ns();
    __u32 tgid = (__u32)(bpf_get_current_pid_tgid() >> 32);
    __u64 cgroup_id = bpf_get_current_cgroup_id();
    __u64 uid_gid = bpf_get_current_uid_gid();
    struct governed_key gk = {.tgid = tgid};
    struct governed_value *g = bpf_map_lookup_elem(&governed, &gk);

    // Linux stays outside this gate unless the stopped child was explicitly
    // enrolled by the SCQOS launcher.
    if (!g)
        return 0;

    __u64 nonce = g->decision_nonce;

    if (g->expires_ns < now) {
        bpf_map_delete_elem(&governed, &gk);
        audit(tgid, cgroup_id, uid_gid, 0, 0, 0, nonce,
              SCQOS_REASON_GOVERNED_EXPIRED, -13);
        return -13;
    }

    if (g->cgroup_id != cgroup_id) {
        bpf_map_delete_elem(&governed, &gk);
        audit(tgid, cgroup_id, uid_gid, 0, 0, 0, nonce,
              SCQOS_REASON_CGROUP_MISMATCH, -13);
        return -13;
    }

    if (g->uid_gid != uid_gid) {
        bpf_map_delete_elem(&governed, &gk);
        audit(tgid, cgroup_id, uid_gid, 0, 0, 0, nonce,
              SCQOS_REASON_CREDENTIAL_MISMATCH, -13);
        return -13;
    }

    struct file *file = BPF_CORE_READ(bprm, file);
    if (!file) {
        audit(tgid, cgroup_id, uid_gid, 0, 0, 0, nonce,
              SCQOS_REASON_FILE_MISSING, -13);
        return -13;
    }

    struct inode *inode = BPF_CORE_READ(file, f_inode);
    if (!inode) {
        audit(tgid, cgroup_id, uid_gid, 0, 0, 0, nonce,
              SCQOS_REASON_INODE_MISSING, -13);
        return -13;
    }

    __u64 ino = BPF_CORE_READ(inode, i_ino);
    __u64 size = (__u64)BPF_CORE_READ(inode, i_size);
    struct super_block *sb = BPF_CORE_READ(inode, i_sb);
    __u64 dev = sb ? BPF_CORE_READ(sb, s_dev) : 0;

    struct exec_key key = {
        .tgid = tgid,
        .pad = 0,
        .cgroup_id = cgroup_id,
        .dev = dev,
        .ino = ino,
        .size = size,
    };

    struct grant_value *grant = bpf_map_lookup_elem(&exec_grants, &key);
    if (!grant) {
        audit(tgid, cgroup_id, uid_gid, dev, ino, size, nonce,
              SCQOS_REASON_GRANT_MISSING, -13);
        return -13;
    }

    if (grant->expires_ns < now) {
        bpf_map_delete_elem(&exec_grants, &key);
        bpf_map_delete_elem(&governed, &gk);
        audit(tgid, cgroup_id, uid_gid, dev, ino, size, nonce,
              SCQOS_REASON_GRANT_EXPIRED, -13);
        return -13;
    }

    if (grant->decision_nonce != nonce) {
        bpf_map_delete_elem(&exec_grants, &key);
        bpf_map_delete_elem(&governed, &gk);
        audit(tgid, cgroup_id, uid_gid, dev, ino, size, nonce,
              SCQOS_REASON_NONCE_MISMATCH, -13);
        return -13;
    }

    // Both map records are created from one userspace decision. Requiring the
    // same deadline prevents combining records from different generations.
    if (grant->expires_ns != g->expires_ns) {
        bpf_map_delete_elem(&exec_grants, &key);
        bpf_map_delete_elem(&governed, &gk);
        audit(tgid, cgroup_id, uid_gid, dev, ino, size, nonce,
              SCQOS_REASON_EXPIRY_MISMATCH, -13);
        return -13;
    }

    // Consume authority before returning allow. A retry must obtain a new
    // decision and a new nonce.
    bpf_map_delete_elem(&exec_grants, &key);
    bpf_map_delete_elem(&governed, &gk);
    audit(tgid, cgroup_id, uid_gid, dev, ino, size, nonce,
          SCQOS_REASON_PERMIT, 0);
    return 0;
}
