"""Structured human feedback — first-class learning signal."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FeedbackType(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    UNSAFE = "unsafe"
    MISSING_CONTEXT = "missing_context"
    WRONG_TOOL = "wrong_tool"
    WRONG_ACTION = "wrong_action"
    POOR_ANSWER = "poor_answer"
    UNNECESSARY_ACTION = "unnecessary_action"


@dataclass
class FeedbackRecord:
    feedback_id: str
    task_id: str
    run_id: str
    agent_version_id: str
    feedback_type: FeedbackType
    expected_decision: str | None
    human_correction: str
    reason: str
    reviewer_id: str


class FeedbackNormalizer:
    """Validate and persist UI feedback into the feedback table."""

    def normalize(self, raw: dict) -> FeedbackRecord:
        raise NotImplementedError("Phase 7")
