from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

INVARIANTS = (
    "Time", "Continuity", "Alignment", "Genesis",
    "Boundary", "Reference", "Causality", "Consciousness",
)

@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    failed: tuple[str, ...]
    checks: Mapping[str, bool]

def evaluate(evidence: Mapping[str, Any]) -> GateDecision:
    expected_parent = evidence.get("expected_parent_digest")
    expected_reference = evidence.get("expected_reference_digest")
    checks = {
        "Time": bool(evidence.get("timestamp")),
        "Continuity": bool(expected_parent) and evidence.get("parent_digest") == expected_parent,
        "Alignment": bool(evidence.get("intent_digest")) and evidence.get("intent_digest") == evidence.get("artifact_digest"),
        "Genesis": evidence.get("genesis") == f"linux-v7.0@{expected_parent}",
        "Boundary": evidence.get("authorized") is True,
        "Reference": bool(expected_reference) and evidence.get("reference_digest") == expected_reference,
        "Causality": bool(evidence.get("cause")),
        "Consciousness": bool(evidence.get("observer")),
    }
    failed = tuple(name for name in INVARIANTS if not checks[name])
    return GateDecision(not failed, failed, checks)
