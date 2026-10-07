"""Evolution engine — pattern → candidate config → eval → promote."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VersionStatus(str, Enum):
    DRAFT = "DRAFT"
    EVALUATING = "EVALUATING"
    PASSED = "PASSED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    FAILED_EVALUATION = "FAILED_EVALUATION"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass
class Signal:
    signal_id: str
    kind: str
    task_run_id: str
    payload: dict


@dataclass
class Pattern:
    pattern_id: str
    kind: str
    occurrence_count: int
    summary: str


@dataclass
class CandidateVersion:
    version_id: str
    parent_version_id: str
    status: VersionStatus
    config_diff: dict
    creation_reason: str


class SignalExtractor:
    """Deterministic mapping of feedback and errors → signals."""

    def extract(self, feedback_row: dict) -> list[Signal]:
        raise NotImplementedError("Phase 8")


class PatternDetector:
    """Cluster recurring signals into patterns."""

    def detect(self, signals: list[Signal]) -> list[Pattern]:
        raise NotImplementedError("Phase 8")


class EvolutionProposer:
    """LLM proposes allowed config diffs only (never production source)."""

    def propose(self, pattern: Pattern, parent_version_id: str) -> CandidateVersion:
        raise NotImplementedError("Phase 8")


class PromotionService:
    """Deterministic state machine + activate version after approval."""

    def transition(self, version_id: str, to: VersionStatus) -> VersionStatus:
        raise NotImplementedError("Phase 8")


class EvolutionEngine:
    """Observation → Signal → Pattern → Hypothesis → Candidate → … → Promotion."""

    def __init__(
        self,
        signals: SignalExtractor,
        patterns: PatternDetector,
        proposer: EvolutionProposer,
        promotion: PromotionService,
    ) -> None:
        self.signals = signals
        self.patterns = patterns
        self.proposer = proposer
        self.promotion = promotion

    def run_cycle(self) -> list[CandidateVersion]:
        raise NotImplementedError("Phase 8")
