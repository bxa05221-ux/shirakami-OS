# Phase 3 Traceability Boundary

## Purpose

Expose a read-only verification boundary for the provenance chain produced by the Runtime and AIwitness layers.

## Chain

`Evidence → Handoff → Execution → Trace → Witness → Verification`

## Endpoint

`GET /v1/traceability/{trace_id}`

The endpoint returns a machine-checkable `valid` flag and the normalized `TraceabilityRecord`.

## Authority rule

Traceability is observational. A valid record does not authorize execution, publication, merge, or any other decision. The returned record must preserve:

- `execution_authorized: false`
- `publish_authorized: false`
- `merge_authorized: false`
- `human_gate_required: true`

## Failure semantics

- `404`: the trace or its execution/witness is unavailable.
- `409`: the available records disagree or an authority boundary is violated.

The endpoint is therefore a verification surface, not an approval surface.
