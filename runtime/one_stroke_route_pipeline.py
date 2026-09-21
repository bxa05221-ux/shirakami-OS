"""Human-gated pipeline from structural Route Candidate to verified Evidence.

This boundary separates candidate generation, human selection, one-stroke
execution, and verification. It does not infer semantic compatibility or
authorize a route on behalf of a human.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

try:
    from .evolution_bridge import ContextSnapshot, VerificationResult
    from .evolution_pipeline import EvidenceDrivenRuntime
    from .evidence import EvidenceRecord
    from .protocol_route import compose_route
    from .prototype import ExecutionResult
except ImportError:
    from evolution_bridge import ContextSnapshot, VerificationResult
    from evolution_pipeline import EvidenceDrivenRuntime
    from evidence import EvidenceRecord
    from protocol_route import compose_route
    from prototype import ExecutionResult


@dataclass(frozen=True)
class RouteSelection:
    """A human-selected structural candidate, before execution."""
    route_id: str
    candidate: tuple[str, ...]
    reviewer: str


@dataclass(frozen=True)
class VerifiedRouteRun:
    """Complete result of one selected-route execution cycle."""
    selection: RouteSelection
    execution: ExecutionResult
    verification: VerificationResult
    evidence: tuple[EvidenceRecord, ...]


class OneStrokeRoutePipeline:
    """Compose a selected route into the existing human-gated Runtime loop."""

    def __init__(self, runtime: EvidenceDrivenRuntime | None = None) -> None:
        self.runtime = runtime or EvidenceDrivenRuntime()
        self._selection: RouteSelection | None = None

    def select(
        self,
        route_id: str,
        candidate: Sequence[str],
        *,
        reviewer: str = "human",
        approved: bool = False,
    ) -> RouteSelection:
        """Register a candidate and require explicit Human Gate approval."""
        names = tuple(candidate)
        if len(names) < 2:
            raise ValueError("candidate must contain at least two Protocols")
        if len(set(names)) != len(names):
            raise ValueError("candidate must not reuse a Protocol")
        if any(not isinstance(name, str) or not name.strip() for name in names):
            raise ValueError("candidate Protocol names must be non-empty strings")
        if not route_id.strip():
            raise ValueError("route_id must be non-empty")
        if not reviewer.strip():
            raise ValueError("reviewer must be non-empty")

        self._selection = RouteSelection(route_id, names, reviewer)
        self.runtime.observe(
            {"route_id": route_id, "candidate": list(names)},
            ContextSnapshot(protocol_id=route_id),
        )
        self.runtime.analyze(route_id, protocol_exists=False, diff_ref=route_id)
        if not approved or not self.runtime.approve(approved=True, reviewer=reviewer):
            self._selection = None
            raise PermissionError("Human approval required before route execution")
        return self._selection

    def execute(
        self,
        protocols: Mapping[str, Any],
        input_data: Mapping[str, Any] | None = None,
    ) -> VerifiedRouteRun:
        """Execute the selected route once, then verify and retain Evidence."""
        if self._selection is None:
            raise RuntimeError("no human-approved route is selected")
        missing = [name for name in self._selection.candidate if name not in protocols]
        if missing:
            raise KeyError(f"missing Protocol implementations: {missing}")
        selected = [(name, protocols[name]) for name in self._selection.candidate]
        route = compose_route(self._selection.route_id, selected)
        execution = self.runtime.execute(
            route, self._selection.route_id, input_data
        )
        verification = self.runtime.verify(
            execution,
            expected_transition_kind=f"route.{self._selection.route_id}",
            diff_ref=self._selection.route_id,
        )
        evidence = self.runtime.store.by_protocol(self._selection.route_id)
        return VerifiedRouteRun(self._selection, execution, verification, evidence)
