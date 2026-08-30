"""Minimal OPPAI -> Protocol -> Runtime flow.

This module intentionally keeps the downstream execution adapter abstract.
It demonstrates the vertical boundary without coupling OPPAI to a model vendor.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from runtime.oppai_schema import OppaiObservation, normalize


@dataclass(frozen=True)
class OppaiRuntimeResult:
    observation: OppaiObservation
    protocol: str
    input_for_runtime: str
    evidence: Mapping[str, Any]


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
