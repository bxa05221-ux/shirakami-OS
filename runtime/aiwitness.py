"""AIwitness integration for routing and simulation MVP."""

from dataclasses import dataclass
from typing import Any, Mapping

from .simulation import SimulationResult


@dataclass(frozen=True)
class WitnessRecord:
    witness_id: str
    prompt_id: str
    protocol_id: str
    simulation_id: str
    evidence_refs: tuple[str, ...]
    context_version: str | None
    simulation_status: str
    observation: Mapping[str, Any]
    simulation: Mapping[str, Any]
    uncertainty: tuple[str, ...]


def record_simulation_witness(
    *,
    witness_id: str,
    prompt: Any,
    simulation_result: SimulationResult,
) -> WitnessRecord:
    """Create an immutable witness record linking state, prompt and simulation."""
    if prompt.prompt_id != simulation_result.prompt_id:
        raise ValueError("prompt and simulation result do not match")
    if prompt.protocol_id != simulation_result.protocol_id:
        raise ValueError("protocol and simulation result do not match")

    return WitnessRecord(
        witness_id=witness_id,
        prompt_id=prompt.prompt_id,
        protocol_id=prompt.protocol_id,
        simulation_id=simulation_result.simulation_id,
        evidence_refs=tuple(prompt.evidence),
        context_version=prompt.context.get("context_version"),
        simulation_status=simulation_result.status,
        observation={"kind": "input_references", "evidence_refs": tuple(prompt.evidence)},
        simulation={"kind": "simulation", "output": dict(simulation_result.output)},
        uncertainty=tuple(prompt.uncertainty),
    )
