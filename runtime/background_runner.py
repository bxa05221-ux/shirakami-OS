"""Minimal lifecycle runner for explicitly registered Background Protocols.

This module provides an execution boundary only. It does not infer human intent,
select an Application Protocol, or define the semantics of any Background Protocol.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .evidence import EvidenceRecord, capture_evidence
from .landscape import LandscapeState
from .prototype import Runtime, Transition

BackgroundProtocol = Callable[[Mapping[str, Any]], Transition]


@dataclass(frozen=True)
class BackgroundExecution:
    protocol_id: str
    result: Any
    evidence: EvidenceRecord


class BackgroundRunner:
    """Execute explicitly registered background protocols on each tick."""

    def __init__(self, landscape: LandscapeState | None = None) -> None:
        self.landscape = landscape or LandscapeState.empty()
        self.runtime = Runtime()
        self._protocols: dict[str, BackgroundProtocol] = {}

    def register(self, protocol_id: str, protocol: BackgroundProtocol) -> None:
        if not isinstance(protocol_id, str) or not protocol_id.strip():
            raise ValueError("protocol_id must be a non-empty string")
        if not callable(protocol):
            raise ValueError("background protocol must be callable")
        if protocol_id in self._protocols:
            raise ValueError(f"background protocol already registered: {protocol_id}")
        self._protocols[protocol_id] = protocol

    def tick(self, input_data: Mapping[str, Any] | None = None) -> tuple[BackgroundExecution, ...]:
        """Run all registered Background Protocols once.

        Repeated calls provide the lifecycle hook for continuous operation;
        scheduling is deliberately left outside this semantic boundary.
        """
        executions: list[BackgroundExecution] = []
        normalized = dict(input_data or {})
        for protocol_id, protocol in self._protocols.items():
            result = self.runtime.execute(protocol_id, protocol, normalized)
            evidence = capture_evidence(result)
            self.landscape.apply_evidence(evidence)
            executions.append(BackgroundExecution(protocol_id, result, evidence))
        return tuple(executions)

    def registered_protocol_ids(self) -> tuple[str, ...]:
        return tuple(self._protocols)
