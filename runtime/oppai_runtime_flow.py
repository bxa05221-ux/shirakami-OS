"""Minimal OPPAI -> Protocol -> Runtime flow.

This module intentionally keeps the downstream execution adapter abstract.
It demonstrates the vertical boundary without coupling OPPAI to a model vendor.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from runtime.oppai_schema import OppaiObservation, normalize
from runtime.protocol_api import ProtocolRequest, build_protocol_request
from runtime.protocol_registry import ProtocolRegistry


@dataclass(frozen=True)
class OppaiRuntimeResult:
    observation: OppaiObservation
    protocol: str
    input_for_runtime: str
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class OppaiProtocolCandidate:
    """An explicitly discoverable Protocol candidate, not a selection."""

    protocol_id: str
    basis: str
    metadata: Mapping[str, Any]


def prepare(
    text: str,
    protocol: str = "default",
    context: Mapping[str, Any] | None = None,
) -> OppaiRuntimeResult:
    """Prepare natural human input for a replaceable Runtime adapter."""
    if not isinstance(protocol, str) or not protocol.strip():
        raise ValueError("protocol must be a non-empty string")

    observation = normalize(text, context)
    return OppaiRuntimeResult(
        observation=observation,
        protocol=protocol,
        input_for_runtime=observation.canonical_prompt,
        evidence={
            "event": "oppai.runtime.prepared",
            "schema": "OPPAI",
            "version": "0.1",
            "raw_preserved": True,
            "corrections_preserved": True,
            "interaction_separated_from_fact": True,
            "confidence": observation.confidence,
        },
    )


def discover_protocol_candidates(
    text: str,
    registry: ProtocolRegistry,
    context: Mapping[str, Any] | None = None,
) -> tuple[OppaiProtocolCandidate, ...]:
    """Expose currently available Protocol candidates without selecting one.

    This is deliberately a registry-level discovery experiment. Semantic
    matching, ranking, automatic selection, and Pipeline identity remain
    outside this function.
    """
    observation = normalize(text, context)
    candidates: list[OppaiProtocolCandidate] = []

    for entry in registry.list_current_candidates():
        artifact = entry.artifact
        metadata: dict[str, Any] = {
            "state": entry.state,
            "lifecycle": entry.lifecycle,
        }
        for field in ("title", "version", "statement", "pipeline"):
            value = getattr(artifact, field, None)
            if value is not None:
                metadata[field] = value

        metadata["oppai_canonical_prompt"] = observation.canonical_prompt
        metadata["oppai_unresolved"] = tuple(observation.unresolved)
        candidates.append(
            OppaiProtocolCandidate(
                protocol_id=entry.protocol_id,
                basis="registry.current",
                metadata=metadata,
            )
        )

    return tuple(candidates)


def build_selected_protocol_request(
    text: str,
    registry: ProtocolRegistry,
    selected_protocol: str,
    context: Mapping[str, Any] | None = None,
) -> ProtocolRequest:
    """Bridge an explicit OPPAI selection into the canonical ProtocolRequest path.

    Selection is intentionally explicit: this helper does not choose a Protocol.
    It represents the post-Human-Gate handoff from OPPAI observation to the
    existing ProtocolRegistry/ProtocolRequest boundary.
    """
    prepared = prepare(text, protocol=selected_protocol, context=context)
    return build_protocol_request(
        registry,
        selected_protocol,
        {
            "raw_input": prepared.observation.raw_input,
            "canonical_prompt": prepared.observation.canonical_prompt,
            "context": dict(context or {}),
            "oppai_unresolved": list(prepared.observation.unresolved),
        },
    )


def execute(
    text: str,
    runtime_adapter: Callable[[str, str], Any],
    protocol: str = "default",
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the prepared input through an external Runtime adapter."""
    prepared = prepare(text, protocol=protocol, context=context)
    output = runtime_adapter(prepared.input_for_runtime, prepared.protocol)
    return {
        "protocol": prepared.protocol,
        "input": prepared.input_for_runtime,
        "output": output,
        "evidence": dict(prepared.evidence),
        "observation": {
            "raw_input": prepared.observation.raw_input,
            "corrections": list(prepared.observation.corrections),
            "interaction_signals": list(prepared.observation.interaction_signals),
            "unresolved": list(prepared.observation.unresolved),
        },
    }
