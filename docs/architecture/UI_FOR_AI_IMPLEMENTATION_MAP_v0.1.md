# UI for AI — Implementation Mapping v0.1

Status: implementation mapping
Basis: UI for AI Formal Specification v0.1
Scope: current `main` implementation only

## 1. Canonical boundary

UI for AI is mapped as the human-side Interaction / Observation Boundary for Shirakami Runtime.

```text
Human
  ↓
UI for AI
  ↓
Observation / Context
  ↓
OPPAI
  ↓
Unresolved / i-field
  ↓
Evidence
  ↓
Protocol / ProtocolRequest
  ↓
Shirakami Runtime
  ↓
Adapter
  ↓
AI / Backend
```

This diagram is an implementation mapping target, not a claim that every arrow is currently a single canonical API call.

## 2. Specification mapping

| UI for AI requirement | Current implementation | Status | Boundary note |
|---|---|---|---|
| Human Input Boundary | `runtime/oppai_schema.py`, `runtime/oppai_runtime_flow.py` | IMPLEMENTED | OPPAI preserves raw input and separates interaction signals from facts. |
| Observation Boundary | `shirakami-ui-for-ai` repository boundary; OPPAI observation objects | IMPLEMENTED | Observation and interpretation remain distinct. |
| Context | OPPAI `context` input; Landscape/Runtime context | IMPLEMENTED | Context is passed explicitly; no hidden truth is inferred. |
| Uncertainty / unresolved | `runtime/i_field.py` | IMPLEMENTED | `ImaginaryTerm` remains unresolved until explicitly resolved with an evidence reference. |
| Evidence | `runtime/evidence.py` / `EvidenceRecord` | IMPLEMENTED | Evidence is an immutable record of an observed Runtime transition. |
| Evidence → Landscape | projection / replay path | VERIFIED | Projection is kept separate from Evidence capture. |
| Protocol source | `runtime/protocol_loader.py`, Matome YAML | IMPLEMENTED | Protocol remains a source artifact. |
| Protocol registry | `runtime/protocol_registry.py` | IMPLEMENTED | Registry resolves registered Protocols. |
| Protocol request | `runtime/protocol_api.py` | IMPLEMENTED | `ProtocolRequest` is a distinct boundary object. |
| Runtime boundary | `runtime/` in `shirakami-OS` | IMPLEMENTED | Runtime is separated from UI and backend-specific code. |
| Adapter boundary | Adapter layer / exchange tests | VERIFIED | Backend/model replacement is kept outside Runtime semantics. |
| Backend independence | Adapter contract | VERIFIED | UI for AI does not directly depend on a model vendor. |
| Research boundary | `shirakami-research` + `的目yaml` handoff | ALIGNED | Research claims are not promoted automatically into Runtime. |

## 3. Important distinction: OPPAI direct flow vs canonical Protocol API

`runtime/oppai_runtime_flow.py` provides a minimal OPPAI → Protocol-labelled Runtime adapter flow. Its `protocol` value is a string supplied to the flow and its downstream executor is deliberately abstract.

The canonical Protocol API is separate:

```text
ProtocolRegistry
  ↓
build_protocol_request()
  ↓
ProtocolRequest
  ↓
invoke_protocol()
  ↓
executor
```

Therefore the existence of `oppai_runtime_flow.execute()` does not by itself prove that OPPAI performs Protocol Registry resolution.

The existing R0091 contract tests intentionally preserve this distinction.

## 4. i-field mapping

Current `main` contains the domain-neutral unresolved-term boundary:

```text
ImaginaryTerm
    ↓
IField.unresolved
    ↓
resolve(term_id, value, evidence_ref)
    ↓
ResolvedTerm
```

The current `main` implementation requires an `evidence_ref` for resolution but does not yet contain the later `required_evidence` extension from the open feature PR.

No new Evidence fields are required for this mapping.

## 5. Canonical interaction path status

Target:

```text
OPPAI
  → Observation
  → i / unresolved
  → Evidence
  → ProtocolRequest
  → Runtime
  → Adapter
```

Current status by edge:

- OPPAI → Observation: IMPLEMENTED
- Observation → unresolved/i: AVAILABLE AS COMPOSABLE BOUNDARY; no single canonical call identified
- i → Evidence: EVIDENCE REFERENCE CONTRACT EXISTS; no automatic conversion is claimed
- Evidence → ProtocolRequest: SEPARATE CONTRACTS; no automatic ownership transfer is claimed
- ProtocolRequest → Runtime: IMPLEMENTED
- Runtime → Adapter: IMPLEMENTED / VERIFIED

Overall: COMPOSITIONAL PATH EXISTS, but the complete path is not yet proven as one canonical end-to-end API invocation.

## 6. Verification rule

This document does not promote any research-only feature into Runtime semantics.

In particular, the following remain outside the implementation claim:

- ambiguity measurement
- SFR / complete reasoning-path capture
- Traversal as a formal execution mechanism
- automatic Protocol selection
- automatic interpretation of unresolved items
- hidden-truth inference

## 7. Next verification target

The next implementation verification should test composition without introducing new domain semantics:

1. submit natural human input through OPPAI
2. preserve an unresolved item
3. obtain/attach an Evidence reference
4. resolve the unresolved item
5. construct a canonical `ProtocolRequest` through the Registry
6. invoke the Runtime executor
7. preserve the resulting Runtime Evidence
8. verify that no UI-layer interpretation was promoted to Evidence or Protocol semantics

Success would upgrade the mapping from `COMPOSITIONAL PATH EXISTS` to `END-TO-END VERIFIED PATH`.
