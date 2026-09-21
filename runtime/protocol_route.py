"""One-stroke execution adapter for a selected Protocol route.

The adapter composes already-selected Protocol callables into one Runtime
execution. It records the ordered transition trace in the final transition;
it does not infer semantic compatibility or authorize the route.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

try:
    from .prototype import ExecutionContext, Transition
except ImportError:
    from prototype import ExecutionContext, Transition


def compose_route(
    route_id: str,
    protocols: Sequence[tuple[str, Any]],
):
    """Return one Protocol callable representing an ordered route."""
    if not route_id.strip():
        raise ValueError("route_id must be non-empty")
    if len(protocols) < 2:
        raise ValueError("route must contain at least two Protocols")
    if len({name for name, _ in protocols}) != len(protocols):
        raise ValueError("route must not reuse a Protocol")

    names = tuple(name for name, _ in protocols)
    if any(not isinstance(name, str) or not name.strip() for name in names):
        raise ValueError("route Protocol names must be non-empty strings")
    if any(not callable(protocol) for _, protocol in protocols):
        raise ValueError("route entries must be callable")

    def route_protocol(context: ExecutionContext) -> Transition:
        current: Mapping[str, Any] = dict(context.input)
        trace: list[dict[str, Any]] = []

        for name, protocol in protocols:
            step_context = ExecutionContext(protocol_id=name, input=current)
            transition = protocol(step_context)
            if not isinstance(transition, Transition):
                raise TypeError(f"Protocol {name!r} must return Transition")
            trace.append(
                {
                    "protocol_id": name,
                    "transition_kind": transition.kind,
                    "transition_data": dict(transition.data),
                }
            )
            current = dict(transition.data)

        return Transition(
            kind=f"route.{route_id}",
            data={
                "route_id": route_id,
                "route": names,
                "trace": trace,
                "final": dict(current),
                "changed": True,
            },
        )

    return route_protocol
