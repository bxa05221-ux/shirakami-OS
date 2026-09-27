# Agent Activity Ingestion Boundary v0.2

## Purpose

Convert locally captured external-Agent activity records into the existing
provider-neutral `AgentActivity` representation.

The ingestion boundary is observational only.

```
Copilot CLI Hook
  ↓
metadata-only JSONL
  ↓
AgentActivityIngestor
  ↓
AgentActivity (unverified)
  ↓
ActivityObservation
  ↓
Independent Verification
  ↓
Human Gate
  ↓
Evidence
  ↓
ExecutionTrace
  ↓
AIwitness
```

## Invariants

- Ingestion does not execute an operation.
- Ingestion does not create Evidence.
- Ingestion does not grant execution, publication, or merge authority.
- Hook records remain unverified until an independent verification step.
- Malformed input is rejected rather than silently converted.
- Provider-specific hook fields are mapped into the provider-neutral AgentActivity shape.

## Trust boundary

A hook event is an observation supplied by an external runtime. Even when the
hook is emitted by the local Copilot CLI, the record is not itself proof that
the underlying operation occurred as claimed.

The verifier may later establish a stronger claim using independent evidence.

## Human Gate

Human Gate remains a separate explicit transition. Ingestion never infers,
simulates, or manufactures human approval.

## Privacy

The ingestion boundary accepts the metadata-only JSONL emitted by the current
Copilot hook collector. Raw prompts, tool arguments, tool results, and
credentials should not be persisted by the collector merely to support
ingestion.

## Provider neutrality

Copilot CLI is one producer. Other agents may emit the same AgentActivity
fields without changing the Shirakami Runtime boundary.
