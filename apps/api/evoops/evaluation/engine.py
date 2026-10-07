"""Independent evaluation — is the candidate actually better?"""

from __future__ import annotations

from dataclasses import dataclass

from evoops.evolution.engine import CandidateVersion, VersionStatus


@dataclass
class Scorecard:
    task_success: float
    classification_accuracy: float
    tool_selection_accuracy: float
    groundedness: float
    safety: float
    latency_ms: float
    cost_usd: float
    weighted_total: float


@dataclass
class EvalResult:
    candidate_id: str
    baseline_id: str
    scores: Scorecard
    baseline_scores: Scorecard
    passed_gates: bool
    regressions: list[str]


class EvaluationEngine:
    """Score candidates against benchmark datasets; never trusts Evolution alone."""

    def evaluate(self, candidate: CandidateVersion, dataset_id: str) -> EvalResult:
        raise NotImplementedError("Phase 9")

    def recommend_status(self, result: EvalResult) -> VersionStatus:
        if result.passed_gates:
            return VersionStatus.PASSED
        return VersionStatus.FAILED_EVALUATION
