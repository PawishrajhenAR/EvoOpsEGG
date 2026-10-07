"""Policy Guard — identity, scope, sensitivity, approval, loop limits."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from evoops.tools.registry import ToolCall


class DecisionKind(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class PolicyDecision:
    kind: DecisionKind
    reason: str


class PolicyGuard:
    """Deterministic authorization matrix before any tool side effect."""

    def evaluate(self, call: ToolCall, role: str) -> PolicyDecision:
        raise NotImplementedError("Phase 10")
