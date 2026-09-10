# R0091 OPPAI Contract Gap

## Purpose

Pinpoint the implementation contracts missing between the existing human-facing OPPAI entry and the existing canonical Protocol → Runtime → Evidence → Landscape path.

This operation records the gap. It does not create the missing contract.

## Baseline

`0e328339113bbca5134388fd161ca415ab27d055`

## Findings

### 1. Protocol resolution ownership

`ProtocolAPI.build_protocol_request()` requires a `ProtocolRegistry` and a `protocol_id`. The existing OPPAI `prepare()` / `execute()` flow accepts a protocol string but does not receive or resolve a `ProtocolRegistry`.

Therefore the executable ownership/dependency boundary for resolving an OPPAI protocol name into a registered ProtocolRequest is not currently defined between these components.

### 2. Adapter versus Protocol executor contract

The existing OPPAI `execute()` contract calls a replaceable adapter with `(input_for_runtime, protocol)`.

The existing Protocol API `invoke_protocol()` accepts a `ProtocolRequest` and an executor callable receiving that `ProtocolRequest`.

These are different callable contracts. No existing adapter layer in the inspected path maps one to the other.

### 3. OPPAI observation versus EvidenceRecord

OPPAI `prepare()` produces an evidence mapping containing OPPAI metadata such as schema, preservation flags, and confidence.

`EvidenceRecord` requires `protocol_id`, `status`, `transition_kind`, `transition_data`, `signals`, and `confidence`.

The repository does not currently define a formal conversion contract between these two representations. In particular, no inference is made that OPPAI confidence should populate Runtime Evidence confidence.

### 4. ExecutionRequest is a separate boundary

`ExecutionRequest` identifies an operation execution through `(operation_id, execution_id)`. It does not contain Protocol ID or human input.

The existing `ExecutionRequest → OperationPlan → PlannedExecution → ExecutionBoundary → OperationResult` path therefore cannot be treated as an implicit substitute for the missing OPPAI → ProtocolRequest mapping.

## Contract-gap matrix

| Boundary | Current state | Missing item |
|---|---|---|
| OPPAI protocol string → ProtocolRequest | UNKNOWN | Protocol resolution ownership/dependency |
| OPPAI adapter callable → Protocol executor | UNKNOWN | Callable/adapter mapping contract |
| OPPAI evidence mapping → EvidenceRecord | UNKNOWN | Evidence conversion contract |
| ProtocolRequest → Runtime | VERIFIED | none identified in this audit |
| Runtime → EvidenceRecord | VERIFIED | none identified in this audit |
| EvidenceRecord → LandscapeState | VERIFIED | none identified in this audit |

## Result

R0091 narrows the R0090 UNKNOWN boundary to three concrete contract gaps:

1. Protocol resolution ownership
2. Adapter/executor callable mapping
3. OPPAI observation → EvidenceRecord conversion

No new contract is introduced by this operation.

The appropriate next step is to obtain or establish an explicit handoff for the required connection contract before implementation changes are made.

## Non-goals

- no new Protocol semantics
- no new OPPAI semantics
- no Registry behavior changes
- no Evidence schema changes
- no Landscape schema changes
- no Adapter contract changes
- no autonomous execution claim
- no AI/model quality evaluation
