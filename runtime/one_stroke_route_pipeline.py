"""Human-gated pipeline from structural Route Candidate to verified Evidence.

This boundary separates candidate generation, human selection, one-stroke
execution, and verification. It does not infer semantic compatibility or
authorize a route on behalf of a human.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

try:
    from .approval_envelope import ApprovalEnvelope
    from .approval_route_bridge import require_approved_route
    from .evolution_bridge import ContextSnapshot, VerificationResult
    from .evolution_pipeline import EvidenceDrivenRuntime
    from .evidence import EvidenceRecord
    from .protocol_route import compose_route
    from .prototype import ExecutionResult
except ImportError:
    from approval_envelope import ApprovalEnvelope
    from approval_route_bridge import require_approved_route
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
        self._approval: ApprovalEnvelope | None = None

    def _validate_selection(
        self,
        route_id: str,
        candidate: Sequence[str],
        reviewer: str,
    ) -> tuple[str, ...]:
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
        return names

    def propose_candidates_from_evidence(
        self,
        evidence: Sequence[EvidenceRecord],
        *,
        n: int = 2,
    ) -> list[tuple[str, ...]]:
        """Derive structural route candidates from explicit Evidence artifacts.

        This is proposal-only: it does not select, authorize, or mutate the
        Evolution Loop state. Human selection still enters through
        prepare_candidate and the existing R0100 Human Gate.
        """
        from tools.protocol_route_candidates import generate_candidates_from_evidence

        return generate_candidates_from_evidence(evidence, n)

    def prepare_candidate(
        self,
        route_id: str,
        candidate: Sequence[str],
        *,
        reviewer: str = "human",
    ) -> RouteSelection:
        """Enter R0100 HUMAN_REVIEW without granting execution authority."""
        names = self._validate_selection(route_id, candidate, reviewer)
        if self.runtime.loop.state.value not in {"IDLE", "ACCEPTED"}:
            raise RuntimeError(
                f"Evolution Loop not ready for a new route candidate: "
                f"{self.runtime.loop.state.value}"
            )

        self._selection = RouteSelection(route_id, names, reviewer)
        self._approval = None
        self.runtime.observe(
            {"route_id": route_id, "candidate": list(names)},
            ContextSnapshot(protocol_id=route_id),
        )
        self.runtime.analyze(route_id, protocol_exists=False, diff_ref=route_id)
        if self.runtime.loop.state.value != "HUMAN_REVIEW":
            self._selection = None
            raise RuntimeError("route candidate did not reach HUMAN_REVIEW")
        return self._selection

    def approve_candidate(self, *, approved: bool = True) -> RouteSelection:
        """Resolve Human Gate and materialize its explicit execution envelope."""
        if self._selection is None:
            raise RuntimeError("no route candidate is awaiting human review")
        if not self.runtime.approve(
            approved=approved,
            reviewer=self._selection.reviewer,
        ):
            if not approved:
                self._selection = None
                self._approval = None
                raise PermissionError("route candidate rejected by Human Gate")
            raise PermissionError("Human approval required before route execution")
        if approved:
            self._approval = ApprovalEnvelope(
                candidate_id=self._selection.route_id,
                protocol_id=self._selection.route_id,
                provenance=(self._selection.route_id,),
            ).authorize_execution(self._selection.reviewer)
            return self._selection
        raise PermissionError("route candidate rejected by Human Gate")

    def select_candidate(
        self,
        route_id: str,
        candidate: Sequence[str],
        *,
        reviewer: str = "human",
        approved: bool = False,
    ) -> RouteSelection:
        """Accept one generated Route Candidate at the Human Gate boundary."""
        self.prepare_candidate(route_id, candidate, reviewer=reviewer)
        if not approved:
            raise PermissionError("Human approval required before route execution")
        return self.approve_candidate(approved=True)

    def select(
        self,
        route_id: str,
        candidate: Sequence[str],
        *,
        reviewer: str = "human",
        approved: bool = False,
    ) -> RouteSelection:
        """Backward-compatible alias for select_candidate."""
        return self.select_candidate(
            route_id,
            candidate,
            reviewer=reviewer,
            approved=approved,
        )

    def execute(
        self,
        protocols: Mapping[str, Any],
        input_data: Mapping[str, Any] | None = None,
    ) -> VerifiedRouteRun:
        """Execute only when Human Gate state and approval envelope both agree."""
        if self._selection is None:
            raise RuntimeError("no human-approved route is selected")
        if self.runtime.loop.state.value != "READY":
            raise RuntimeError(
                f"route is not authorized for execution: "
                f"{self.runtime.loop.state.value}"
            )
        if self._approval is None:
            raise RuntimeError("execution approval envelope is missing")

        selection = require_approved_route(self._selection, self._approval)

        missing = [name for name in selection.candidate if name not in protocols]
        if missing:
            raise KeyError(f"missing Protocol implementations: {missing}")
        selected = [(name, protocols[name]) for name in selection.candidate]
        route = compose_route(selection.route_id, selected)
        execution = self.runtime.execute(
            route, selection.route_id, input_data
        )
        verification = self.runtime.verify(
            execution,
            expected_transition_kind=f"route.{selection.route_id}",
            diff_ref=selection.route_id,
        )
        evidence = self.runtime.store.by_protocol(selection.route_id)
        return VerifiedRouteRun(selection, execution, verification, evidence)
