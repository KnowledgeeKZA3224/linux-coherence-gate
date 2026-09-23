import unittest
from scpkg.policy import evaluate

PIN = "028ef9c96e96197026887c0f092424679298aae8"
FORK = "b393692a3f342f9a197da17a3f94754faafc4a44ef06b35e9867d5dc6dc8baa0"

GOOD = {
    "timestamp": "2026-09-23T00:00:00+00:00",
    "parent_digest": PIN,
    "expected_parent_digest": PIN,
    "intent_digest": "same",
    "artifact_digest": "same",
    "genesis": f"linux-v7.0@{PIN}",
    "authorized": True,
    "reference_digest": FORK,
    "expected_reference_digest": FORK,
    "cause": "authorized test",
    "observer": "local-witness",
}

class PolicyTests(unittest.TestCase):
    def test_all_eight_permit(self):
        decision = evaluate(dict(GOOD))
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.failed, ())

    def test_each_invariant_fails_closed(self):
        mutations = {
            "Time": ("timestamp", ""),
            "Continuity": ("parent_digest", "wrong"),
            "Alignment": ("artifact_digest", "wrong"),
            "Genesis": ("genesis", "wrong"),
            "Boundary": ("authorized", False),
            "Reference": ("reference_digest", "wrong"),
            "Causality": ("cause", ""),
            "Consciousness": ("observer", ""),
        }
        for name, (key, value) in mutations.items():
            with self.subTest(name=name):
                evidence = dict(GOOD)
                evidence[key] = value
                self.assertIn(name, evaluate(evidence).failed)

if __name__ == "__main__":
    unittest.main()
