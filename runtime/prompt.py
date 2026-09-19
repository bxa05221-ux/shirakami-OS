"""Prompt assembly boundary for Shirakami routing MVP.

Prompt assembly converts a recorded routing decision into an explicit,
versioned Runtime input. It does not call an AI provider.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class PromptSpec:
    prompt_id: str
    version: str
    protocol_id: str
    runtime_target: str
    instructions: tuple[str, ...]
    context: Mapping[str, Any]
    evidence: tuple[str, ...]
    uncertainty: tuple[str, ...]


def assemble_prompt(
    *,
    prompt_id: str,
    version: str,
    routing_result: Any,
    context: Mapping[str, Any],
    protocol_id: str | None = None,
    runtime_target: str = "simulation",
) -> PromptSpec:
    """Assemble a deterministic PromptSpec from routing state.

    A blocked routing result cannot be converted into an executable prompt.
    """
    selected = protocol_id or getattr(routing_result, "selected_protocol", None)
    status = getattr(routing_result, "status", None)
    if status != "ready" or not selected:
        raise ValueError("cannot assemble prompt from blocked routing result")

    matrix = getattr(routing_result, "matrix", None)
    matrix_context = {
        "priority": getattr(matrix, "priority", 0),
        "phase": getattr(matrix, "phase", 0),
        "relation": getattr(matrix, "relation", 0),
    }

    evidence = tuple(str(item) for item in context.get("evidence", ()))
    uncertainty = tuple(str(item) for item in context.get("uncertainty", ()))

    instructions = (
        "Treat Evidence references as observed inputs.",
        "Keep Simulation separate from Reality.",
        "Do not invent missing Evidence.",
        "Do not make a final human decision.",
    )

    assembled_context = {
        "matrix": matrix_context,
        "context_version": context.get("version"),
    }

    return PromptSpec(
        prompt_id=prompt_id,
        version=version,
        protocol_id=selected,
        runtime_target=runtime_target,
        instructions=instructions,
        context=assembled_context,
        evidence=evidence,
        uncertainty=uncertainty,
    )
