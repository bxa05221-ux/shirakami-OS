"""Minimal OPPAI -> Protocol -> Runtime flow.

This module intentionally keeps the downstream execution adapter abstract.
It demonstrates the vertical boundary without coupling OPPAI to a model vendor.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping
import re

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


def _observable_terms(text: str) -> set[str]:
    """Extract conservative lexical terms without inferring hidden intent."""
    return {
        term
        for term in re.findall(r"[\\wぁ-んァ-ヶ一-龯]{2,}", text.lower())
        if term not in {"です", "ます", "する", "した", "して", "ください"}
    }


def discover_protocol_candidates(
    text: str,
    registry: ProtocolRegistry,
    context: Mapping[str, Any] | None = None,
) -> tuple[OppaiProtocolCandidate, ...]:
    """Expose Protocol candidates without selecting one.

    context["protocol_candidates"] is an explicit upstream hint only.
    It may narrow discovery, but OPPAI does not infer or rank the hint.
    Without the hint, all current non-archived Protocols remain candidates.
    """
    observation = normalize(text, context)
    hinted_ids = None
    input_terms = _observable_terms(observation.raw_input)
    if context is not None and "protocol_candidates" in context:
        raw_hints = context["protocol_candidates"]
        if not isinstance(raw_hints, (list, tuple)):
            raise ValueError("context.protocol_candidates must be a list or tuple")
        hinted_ids = {str(protocol_id) for protocol_id in raw_hints}

    candidates: list[OppaiProtocolCandidate] = []
    for entry in registry.list_current_candidates():
        if hinted_ids is not None and entry.protocol_id not in hinted_ids:
            continue

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
        basis = "context.protocol_candidates" if hinted_ids is not None else "registry.current"
        if hinted_ids is None:
            searchable = " ".join(
                str(metadata.get(field, "")) for field in ("title", "statement")
            ).lower()
            matched_terms = tuple(
                sorted(term for term in input_terms if term in searchable)
            )
            if matched_terms:
                basis = "observable.lexical_match"
                metadata["matched_terms"] = matched_terms

        candidates.append(
            OppaiProtocolCandidate(
                protocol_id=entry.protocol_id,
                basis=basis,
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
