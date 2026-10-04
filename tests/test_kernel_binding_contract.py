import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BPF = (ROOT / "kernel_integration" / "scqos_exec_gate.bpf.c").read_text()
LAUNCHER = (ROOT / "kernel_integration" / "scqos_kernel_exec.py").read_text()


class KernelBindingContractTests(unittest.TestCase):
    def test_governed_record_is_generation_bound(self):
        self.assertIn("struct governed_value", BPF)
        self.assertIn("__u64 decision_nonce;", BPF)
        self.assertIn("__u64 cgroup_id;", BPF)
        self.assertIn("__u64 uid_gid;", BPF)
        self.assertIn("grant->decision_nonce != nonce", BPF)
        self.assertIn("grant->expires_ns != g->expires_ns", BPF)

    def test_exec_key_binds_runtime_and_file_identity(self):
        for token in [
            "__u64 cgroup_id;",
            "__u64 dev;",
            "__u64 ino;",
            "__u64 size;",
            "bpf_get_current_cgroup_id()",
            "bpf_get_current_uid_gid()",
        ]:
            self.assertIn(token, BPF)

    def test_permit_is_consumed_before_allow(self):
        delete_grant = BPF.index(
            "bpf_map_delete_elem(&exec_grants, &key);",
            BPF.index("SCQOS_REASON_EXPIRY_MISMATCH"),
        )
        delete_governed = BPF.index(
            "bpf_map_delete_elem(&governed, &gk);", delete_grant
        )
        final_audit = BPF.index("SCQOS_REASON_PERMIT", delete_governed)
        final_allow = BPF.index("return 0;", final_audit)
        self.assertLess(delete_grant, delete_governed)
        self.assertLess(delete_governed, final_allow)

    def test_userspace_map_layout_matches_kernel_contract(self):
        self.assertRegex(LAUNCHER, r'struct\.pack\(\s*"<IIQQQQ"')
        self.assertRegex(LAUNCHER, r'struct\.pack\(\s*"<QQQQ"')
        self.assertRegex(
            LAUNCHER,
            r'struct\.pack\(\s*"<QQ"\s*,\s*expires_ns\s*,\s*nonce\s*\)',
        )

    def test_fail_closed_map_install_order(self):
        governed = LAUNCHER.index("_bpftool_update(GOVERNED")
        grant = LAUNCHER.index("_bpftool_update(EXEC_GRANTS")
        release = LAUNCHER.index("os.kill(pid, signal.SIGCONT)")
        self.assertLess(governed, grant)
        self.assertLess(grant, release)

    def test_final_continuity_checks_precede_grant(self):
        checks = [
            "_child_is_stopped(pid)",
            "_cgroup_v2_id(pid) != cgroup_id",
            "_uid_gid() != uid_gid",
            "_file_identity(exe) != identity",
        ]
        grant = LAUNCHER.index("_bpftool_update(GOVERNED")
        for check in checks:
            self.assertLess(LAUNCHER.index(check), grant)


if __name__ == "__main__":
    unittest.main()
