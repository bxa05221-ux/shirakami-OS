# R0090 OPPAI Contract Connection Audit

## Purpose

Determine whether the existing OPPAI `/v1/chat` entry can connect to the existing Protocol → Runtime → Evidence → Landscape path using only existing formal contracts.

This is an inspection and verification operation. It does not introduce a new connection contract.

## Baseline

`ff729f9d67d1ee2b20943cd693fc4e3c742fdca1`

## Findings

### 1. Human-facing OPPAI entry

The existing `/v1/chat` HTTP wrapper delegates to `ShirakamiRuntime.chat()`. The minimal runtime preserves the supplied context and passes the normalized raw input/context to a replaceable model adapter.

Verified boundary:

`HTTP /v1/chat → ShirakamiRuntime.chat() → OPPAI listen() → replaceable model adapter`

### 2. ProtocolRequest / Registry

The existing `ProtocolAPI` can resolve a registered Protocol through `ProtocolRegistry` and produce a `ProtocolRequest` containing `protocol_id`, resolved `version`, and input mapping.

Verified existing contract:

`ProtocolRegistry → build_protocol_request() → ProtocolRequest`

`invoke_protocol()` accepts that existing `ProtocolRequest` and delegates it unchanged to an executor.

### 3. ProtocolRequest → Runtime

R0085 already provides the `ProtocolRequest → Runtime entry` boundary through `execute_protocol_request()`.

R0088 already verifies the downstream Protocol → Runtime → ExecutionResult path through the existing `protocol_runtime_bridge`.

Therefore the downstream Runtime path is available as an existing implementation boundary.

### 4. Runtime → Evidence → Landscape

The existing Runtime produces `ExecutionResult`.

`capture_evidence()` converts that result into an immutable `EvidenceRecord`.

The existing projection boundary applies `EvidenceRecord` to `LandscapeState`.

This path is independently available and was structurally verified in the preceding R0088 work.

### 5. OPPAI evidence metadata

OPPAI currently produces an `evidence` mapping containing metadata such as `schema`, `version`, preservation flags, and `confidence`.

That mapping is not an `EvidenceRecord` and there is no existing formal conversion contract between the OPPAI metadata mapping and `EvidenceRecord`.

In particular, this audit does not infer that OPPAI `confidence` should populate `EvidenceRecord.confidence`.

### 6. Connection status

The two sides therefore exist independently:

`OPPAI HTTP → OPPAI adapter boundary`

and

`ProtocolRegistry → ProtocolRequest → Runtime → ExecutionResult → EvidenceRecord → LandscapeState`

The current repository does not provide an existing formal contract that directly connects the human-facing `/v1/chat` boundary to the canonical ProtocolRequest/Runtime path.

## Boundary status

**UNKNOWN / implementation gap**

The gap is not treated as an error and is not filled by inference.

A future implementation may connect the boundaries only after an explicit contract establishes the required mapping and ownership.

## Non-goals

- no new Protocol semantics
- no new OPPAI contract
- no Protocol Registry behavior change
- no Evidence schema change
- no Landscape schema change
- no Adapter contract change
- no autonomous execution claim
- no AI/model quality evaluation
- no inferred mapping from OPPAI confidence to Runtime Evidence

## Verification

R0090 verifies two facts independently:

1. The existing downstream Protocol → Runtime → Evidence → Landscape contracts can compose without changing their interfaces.
2. The existing OPPAI `/v1/chat` reference entry remains an adapter-facing boundary and does not silently become a canonical Protocol entry.

A passing R0090 test therefore confirms the boundary distinction, not end-to-end β1.0 composition.

## Result

The correct implementation state after R0090 is:

`OPPAI HTTP entry` — implemented

`Protocol → Runtime → Evidence → Landscape` — implemented/verified

`OPPAI HTTP entry → canonical ProtocolRequest path` — UNKNOWN

No contract has been invented to close the gap.
