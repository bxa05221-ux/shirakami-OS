# OPPAI → Protocol → Pipeline → Adapter vertical flow v0.1

## Purpose

This observation closes the β0.1 execution path from natural-language input to a selected Protocol's Pipeline and an explicitly supplied Adapter.

## Canonical path

Human / Landscape → Natural Language → OPPAI → Candidate discovery → Human Gate → Selected Protocol → ProtocolRequest → PipelinePlan → PipelineAdapter → Backend / AI → Evidence / Observation → Human Judgment

## Boundary decisions

- OPPAI does not silently select a Protocol.
- Human Gate remains the authority for Protocol selection.
- Pipeline is derived from the selected Protocol artifact and execution context.
- Adapter is the explicit external execution boundary.
- Backend/AI selection is supplied to the Adapter from outside; the Adapter does not infer a vendor.
- The Runtime path does not promote backend output to verified Evidence.
- The same Protocol and Pipeline can be executed with different Adapters/backends.

## Implementation

runtime/oppai_runtime_flow.py now exposes execute_selected_pipeline().

The function composes: build_selected_protocol_request → build_pipeline_plan → PipelineAdapter.execute for every Pipeline step.

## Verification

The following tests cover the boundary:

- candidate discovery without silent selection
- PipelinePlan derivation from a selected Protocol
- PipelineAdapter execution
- same Protocol through multiple backends
- complete OPPAI → selected Protocol → Pipeline → Adapter vertical flow

The repository's Runtime β0.1 workflow is configured to run python -m pytest runtime tests -q for changes under runtime/** and tests/**.

## Status

Decision: adopted for Shirakami β development.

This is an execution-boundary completion, not a claim that automatic Protocol or AI selection has been solved. Automated ranking/selection remains outside this v0.1 contract.
