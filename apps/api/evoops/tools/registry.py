"""Deterministic tool discovery, authorization handoff, invoke, audit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Awaitable


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]
    run_id: str
    agent_version_id: str
    actor_id: str


@dataclass
class ToolResult:
    ok: bool
    data: dict[str, Any] | None
    error: str | None
    requires_approval: bool = False
    audit_id: str | None = None


ToolHandler = Callable[[ToolCall], Awaitable[ToolResult]]


class ToolRegistry:
    """Registers connectors (Supabase, Resend, mock IT job) behind one envelope."""

    def __init__(self) -> None:
        self._handlers: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        self._handlers[name] = handler

    def list_tools(self) -> list[str]:
        return sorted(self._handlers)

    async def invoke(self, call: ToolCall) -> ToolResult:
        raise NotImplementedError("Phase 4")
