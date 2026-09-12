"""Minimal activation pump for the verified OPPAI -> Protocol -> Runtime -> AI path.

This module only connects existing boundaries. It does not select protocol meaning,
interpret human intent, or add vendor-specific behavior.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .oppai_runtime_flow import prepare
from .protocol_api import build_protocol_request
from .protocol_registry import ProtocolRegistry
from .protocol_runtime_bridge import execute_protocol
from .prototype import Transition


@dataclass(frozen=True)
class ActivationResult:
    protocol_id: str
    protocol_version: str | None
    runtime_result: Any
    ai_output: Any


def activate(
    text: str,
    *,
    registry: ProtocolRegistry,
    protocol_id: str,
    transition: Callable[[Mapping[str, Any]], Transition],
    ai_adapter: Callable[[str, str], Any],
    context: Mapping[str, Any] | None = None,
) -> ActivationResult:
    """Connect the existing boundaries into one explicit execution path."""
    prepared = prepare(text, context=context)
    entry = registry.select_current(protocol_id)
    request = build_protocol_request(
        registry,
        protocol_id,
        input_data={"text": prepared.input_for_runtime},
    )
    artifact = entry.artifact
    protocol_ir = {
        "matome": {
            "title": artifact.title,
            "version": artifact.version,
            "statement": artifact.statement,
            "pipeline": list(artifact.pipeline),
        }
    }
    runtime_execution = execute_protocol(
        protocol_ir,
        transition,
        input_value=request.input,
    )
    ai_output = ai_adapter(prepared.input_for_runtime, request.protocol_id)
    return ActivationResult(
        protocol_id=request.protocol_id,
        protocol_version=request.version,
        runtime_result=runtime_execution.result,
        ai_output=ai_output,
    )
