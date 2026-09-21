# Changelog

## Unreleased — UI for AI Execution Handle α0.2

- Added stable `execution_id` handles for externally addressable Runtime executions.
- Added handle lookup and handle-based verification boundaries.
- Unknown execution IDs fail closed.
- Verification continues to produce Evidence without mutating the original execution record.


## PV1.1 / β1.1 — Evidence-Driven Runtime

Status: Operational Baseline

This release closes the first implementation boundary of the Shirakami Evolution Loop.

### Included

- Evidence-driven Runtime Loop
- Evidence Store and deterministic Evidence Query
- Context Snapshot as explicit Evidence
- Protocol Candidate with `diff_ref`
- Human Gate before Protocol adoption
- Verification with explicit uncertainty
- Formal Mismatch Evidence preserving expected vs observed
- Evidence lineage and append-only correction model
- Residue externalization as an architectural boundary
- Runtime / Specification separation through R0100
- CI-verified integration of the Evolution Loop and Evidence boundary

### Boundary

PV1.1 does not claim a finished product or complete Protocol semantics.

It establishes a reproducible, inspectable operational baseline:

**Observation → Evidence → Analysis → Protocol Candidate → Human Gate → Runtime → Verification → Mismatch → Evidence**

The next development boundary is API extraction and broader adapter/runtime contracts.

