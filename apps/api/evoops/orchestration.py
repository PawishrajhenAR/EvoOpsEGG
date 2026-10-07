"""Orchestrator and planner — task lifecycle (deterministic + LLM plan)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RunStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskRequest:
    """Inbound operational task from UI or API."""

    task_id: str
    org_id: str
    text: str
    agent_version_id: str
    created_by: str


@dataclass
class RouteDecision:
    """Planner/Router output — which workflow and tools are in scope."""

    workflow: str
    confidence: float
    allowed_tool_names: list[str] = field(default_factory=list)
    rationale: str = ""


class PlannerRouter:
    """Hybrid router: policy tables first, LLM only when ambiguous."""

    def route(self, task: TaskRequest, policies: dict[str, Any]) -> RouteDecision:
        raise NotImplementedError("Phase 3")


class Orchestrator:
    """Owns session/task lifecycle, budgets, and tracing hooks."""

    def __init__(self, router: PlannerRouter) -> None:
        self.router = router

    def submit(self, task: TaskRequest) -> str:
        """Enqueue a run; returns run_id."""
        raise NotImplementedError("Phase 3")

    def execute_run(self, run_id: str) -> RunStatus:
        raise NotImplementedError("Phase 3")
