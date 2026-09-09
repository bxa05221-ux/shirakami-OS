# R0089 OPPAI HTTP Entry Boundary

## Purpose

Verify the existing human-facing `/v1/chat` reference entry without introducing a new contract.

## Verified boundary

`HTTP /v1/chat → ShirakamiRuntime.chat() → OPPAI listen() → replaceable model adapter`

## Observation

The existing HTTP wrapper accepts `/v1/chat` and delegates directly to the existing `ShirakamiRuntime.chat()` implementation. The minimal runtime preserves the supplied context and passes the normalized raw input/context to a replaceable adapter.

The existing OPPAI runtime flow separately exposes `prepare()` / `execute()` and records OPPAI observation data, including raw-input preservation and confidence, but its downstream execution adapter remains abstract.

Therefore this verification does not claim that the HTTP `/v1/chat` path currently reaches the canonical β1.0 path through `ProtocolRequest → ExecutionRequest → OperationPlan → PlannedExecution → ExecutionBoundary → OperationExecutor → OperationResult → Evidence → Landscape`.

## Boundary status

The HTTP/OPPAI entry is implemented and independently testable.

The connection from that human-facing entry into the canonical Runtime/Evidence/Landscape path remains an implementation gap / UNKNOWN boundary and must not be inferred away.

## Non-goals

- no new Protocol semantics
- no Protocol Registry changes
- no new OPPAI contract
- no Evidence schema changes
- no Landscape schema changes
- no Adapter contract changes
- no autonomous execution claim
- no AI/model quality evaluation

## Result meaning

A passing test establishes the existing HTTP/OPPAI entry boundary only. It does not establish end-to-end β1.0 composition.
