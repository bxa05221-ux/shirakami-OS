# Evolution Loop × One-Stroke Route Pipeline α0.3

## Purpose

This integration connects the generated structural Route Candidate to the
existing R0100 Evolution Loop without bypassing its Human Gate.

Canonical flow:

`Observation → Evidence → Analysis → Protocol Candidate → Human Review → READY → One-Stroke Runtime → Verify → Evidence`

A route candidate remains a proposal until an explicit human approval moves
the Evolution Loop from `HUMAN_REVIEW` to `READY`.

## Boundary

`prepare_candidate()`:

- records the candidate through the existing EvidenceDrivenRuntime;
- enters `PROTOCOL_CANDIDATE → HUMAN_REVIEW`;
- does not authorize execution.

`approve_candidate()`:

- resolves the existing R0100 Human Gate;
- requires an explicit approval;
- moves the loop to `READY`.

`execute()`:

- requires `READY`;
- composes only the selected Protocol sequence into one Runtime operation;
- verifies the resulting route transition;
- retains the resulting Evidence.

## Failure behavior

- missing human approval: execution is not authorized;
- missing Protocol implementation: execution fails closed;
- verification mismatch: the Evolution Loop enters `DIFF`;
- mismatch does not silently advance to `ACCEPTED`.

## Non-goals

This integration does not:

- infer semantic compatibility;
- automatically select a route;
- automatically authorize a route;
- claim universal correctness;
- modify external reality without an explicit downstream authority.

## Relationship to existing components

The integration reuses the existing:

- R0100 `EvolutionLoop`;
- `EvidenceDrivenRuntime`;
- structural n-gram candidate generator;
- `OneStrokeRoutePipeline`;
- immutable Evidence boundary.

The implementation therefore adds a bridge at the orchestration boundary rather
than introducing a second approval state machine.
