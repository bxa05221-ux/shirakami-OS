# Shirakami OS — Cross-Layer Architecture Audit

Date: 2026-09-25  
Status: audit baseline / implementation verification in progress

## Scope

This audit checks whether the current implementation preserves the same boundary semantics across Landscape, Evidence, Semantic Handoff, Runtime, API, Reviewer, AIwitness, and Human Gate.

This is an observation document. It does not certify the repository, grant authority, or replace human review.

## Observed Architecture

```text
Landscape
   ↓
Evidence
   ↓
Protocol / Specification
   ↓
Semantic Handoff
   ↓
Runtime
   ↓
API / Adapter
   ↓
External Reviewer / AI
   ↓
Blind Review
   ↓
Comparative Trace
   ↓
AIwitness
   ↓
Traceability
   ↓
Candidate Evidence
   ↓
Verification
   ↓
Human Gate
   ↓
Accepted Evidence
```

## Boundary Findings

### Evidence

`EvidenceRecord` is implemented as an immutable runtime record. The repository also contains an `EvidenceStore` boundary and replay/projection paths that consume Evidence rather than silently rewriting the past.

### Semantic Handoff

The documented context-routing path is:

`Request → Context Routing → SemanticHandoff → Runtime → Backend → Evidence`

The current routing documentation describes explicit reference routing and distinguishes it from later persistence, semantic retrieval, ranking, authorization, and provider-specific memory APIs.

### Runtime

The documented runtime loop requires explicit human review before execution of generated route candidates. The repository describes Runtime as executing Protocol structure without owning domain truth.

### API

The current reviewer API exposes blind-review ingestion and comparative AIwitness traceability. The API route is an observation/verification boundary, not an authority channel.

### Reviewer / AIwitness

Reviewer and AIwitness roles are separated by observation responsibility. Comparative traceability preserves reviewer provenance and does not convert agreement into authority.

### Human Gate

The review path preserves the following boundary conditions:

- `decision = null`
- `authority_granted = false`
- `decision_authorized = false`
- `human_gate_required = true`

Evidence promotion requires explicit Human Gate approval and resolves reviewer-supplied Evidence IDs against already-recorded immutable EvidenceRecords. Review ingestion does not create or mutate EvidenceRecords.

## Authority Flow

The intended authority direction is one-way:

```text
Observation → Verification → Human Gate → Accepted Evidence
```

The following reverse transitions are prohibited as automatic side effects:

```text
Evidence → Decision Authority
Reviewer → Execution Authority
AIwitness → Evidence Acceptance Authority
HTTP Success → Decision Authority
Comparative Agreement → Evidence Acceptance Authority
```

## Verification Matrix

| Layer | Current observation | Verification state |
|---|---|---|
| Landscape | Explicit architectural object | documented |
| Evidence | Immutable EvidenceRecord / store paths | implemented; CI verification pending |
| Semantic Handoff | Reference-routing path documented | implemented/documented |
| Runtime | Executes without owning domain truth | implemented/documented |
| API | Blind-review HTTP boundary | implemented; CI verification pending |
| Reviewer | Blind independent observation | implemented/documented |
| Comparative Trace | Shared/divergent evidence preserved | implemented; CI verification pending |
| AIwitness | Traceability without authority | implemented; CI verification pending |
| Evidence Promotion | Human-gated resolution of existing Evidence IDs | implemented; CI verification pending |
| Human Gate | Required before acceptance | implemented/documented |

## Open Verification Items

1. Run the full CI matrix after the latest boundary changes.
2. Verify that the Evidence Promotion tests pass together with the existing Runtime, API, Semantic Handoff, and AIwitness suites.
3. Check that README, specification, reviewer documentation, and implementation use the same terminology for Evidence, authority, and Human Gate.
4. Review the current license statement separately before the 2026-10-01 INPIT consultation. The README currently describes the repository as open-source; licensing/commercialization decisions are intentionally not treated as implementation facts by this audit.
5. Preserve the distinction between technical implementation evidence and any future patentability/legal conclusions.

## INPIT Preparation Boundary

For the 2026-10-01 INPIT consultation, separate three layers:

### A. Technical facts

- immutable EvidenceRecord
- stable Evidence identity
- Semantic Handoff reference routing
- Runtime execution boundary
- reviewer / AIwitness separation
- comparative traceability
- Human Gate
- Evidence promotion boundary

### B. Architectural combination

The potentially relevant architectural combination is the controlled movement of context and observations across these boundaries while preventing observation, Evidence, and AI output from becoming execution or decision authority automatically.

### C. Legal conclusion

Patentability, novelty, inventive step, copyright scope, and licensing consequences require professional/legal evaluation and are not concluded by this repository audit.

## Human Gate

Required: true  
Decision: pending
