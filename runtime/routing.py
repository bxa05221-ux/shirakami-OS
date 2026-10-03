"""Minimal State -> Matrix -> Protocol routing boundary.

This is an executable MVP slice. It does not make human decisions and does not
invoke an external AI provider.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class MatrixState:
    priority: int
    phase: int
    relation: int


@dataclass(frozen=True)
class ProtocolCandidate:
    protocol_id: str
    compatibility: int
    required_evidence: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class RoutingResult:
    status: str
    matrix: MatrixState
    candidates: tuple[ProtocolCandidate, ...]
    selected_protocol: str | None


def derive_matrix_state(context: Mapping[str, Any]) -> MatrixState:
    """Derive a deterministic MVP matrix state from explicit context fields."""
    matrix = context.get("matrix", {})
    if not isinstance(matrix, Mapping):
        matrix = {}
    return MatrixState(
        priority=int(matrix.get("priority", 0)),
        phase=int(matrix.get("phase", 0)),
        relation=int(matrix.get("relation", 0)),
    )


def route_protocol(
    context: Mapping[str, Any],
    available_protocols: Mapping[str, Mapping[str, Any]],
) -> RoutingResult:
    """Return compatible Protocol candidates without executing any Protocol."""
    matrix = derive_matrix_state(context)
    evidence = set(context.get("evidence", ()))
    candidates: list[ProtocolCandidate] = []

    for protocol_id, spec in available_protocols.items():
        required = tuple(spec.get("required_evidence", ()))
        missing = tuple(item for item in required if item not in evidence)

        states = spec.get("accepted_states", ())
        compatibility = 0
        if not states:
            compatibility = 1
        else:
            for state in states:
                if (
                    int(state.get("priority", matrix.priority)) == matrix.priority
                    and int(state.get("phase", matrix.phase)) == matrix.phase
                    and int(state.get("relation", matrix.relation)) == matrix.relation
                ):
                    compatibility = 1
                    break

        if compatibility and not missing:
            candidates.append(
                ProtocolCandidate(
                    protocol_id=protocol_id,
                    compatibility=compatibility,
                    required_evidence=required,
                    missing_evidence=missing,
                )
            )

    candidates.sort(key=lambda item: (-item.compatibility, item.protocol_id))
    selected = candidates[0].protocol_id if candidates else None
    return RoutingResult(
        status="ready" if selected else "blocked",
        matrix=matrix,
        candidates=tuple(candidates),
        selected_protocol=selected,
    )
