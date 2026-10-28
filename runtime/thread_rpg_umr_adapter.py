"""Bridge ThreadRPG pipeline requests to Universal Model Runtime."""

from typing import Any

from runtime.adapter import PipelineAdapter, PipelineAdapterRequest
from runtime.umr_backend import UMRBackend


def create_thread_rpg_umr_adapter(
    *,
    base_url: str = "http://127.0.0.1:8766",
    engine: str = "mock",
    timeout: float = 30.0,
    transport: Any = None,
) -> PipelineAdapter:
    """Create a replaceable ThreadRPG-to-UMR adapter."""

    options: dict[str, Any] = {
        "base_url": base_url,
        "engine": engine,
        "timeout": timeout,
    }
    if transport is not None:
        options["transport"] = transport

    backend = UMRBackend(**options)

    def execute(request: PipelineAdapterRequest) -> Any:
        previous_outputs = [
            {
                "output": item.output,
                "backend": item.backend,
                "evidence": dict(item.evidence),
            }
            for item in request.previous_outputs
        ]

        response = backend.execute(
            {
                "input": {
                    "protocol_id": request.protocol_id,
                    "version": request.version,
                    "phase": request.phase,
                    "action": request.action,
                    **dict(request.input),
                },
                "context_bundle": dict(request.context),
                "previous_outputs": previous_outputs,
            }
        )

        if response.status != "completed":
            raise RuntimeError("UMR did not complete ThreadRPG execution")

        return response.payload["output"]

    return PipelineAdapter(
        backend=execute,
        backend_id=backend.backend_id,
    )
