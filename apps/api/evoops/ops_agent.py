"""Ops Agent — LLM-driven IT triage actor bound to an agent_version config."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from evoops.orchestration import RouteDecision, TaskRequest
from evoops.tools.registry import ToolRegistry
from evoops.knowledge.retriever import Retriever
from evoops.security.policy import PolicyGuard


@dataclass
class AgentVersionConfig:
    """Reproducible behaviour — the only thing evolution mutates."""

    version_id: str
    parent_version_id: str | None
    model: str
    system_instructions: str
    tool_names: list[str]
    routing: dict[str, Any]
    retrieval: dict[str, Any]
    thresholds: dict[str, float]


@dataclass
class AgentAnswer:
    text: str
    classification: str | None
    tool_call_ids: list[str]
    citations: list[str]


class OpsAgent:
    """Classify → retrieve → select tools → act → answer."""

    def __init__(
        self,
        config: AgentVersionConfig,
        retriever: Retriever,
        tools: ToolRegistry,
        policy: PolicyGuard,
    ) -> None:
        self.config = config
        self.retriever = retriever
        self.tools = tools
        self.policy = policy

    def run(self, task: TaskRequest, route: RouteDecision) -> AgentAnswer:
        raise NotImplementedError("Phase 3–6")
