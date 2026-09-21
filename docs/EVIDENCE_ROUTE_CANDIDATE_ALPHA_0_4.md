# Evidence → Route Candidate Bridge α0.4

## Purpose

This integration adds a conservative proposal boundary from existing immutable Evidence to structural n-gram Route Candidates.

Canonical flow:

`Evidence → Explicit Protocol Artifact Extraction → Structural n-gram Candidate Generation → Human Review → READY → One-Stroke Runtime → Verification → Evidence`

## Evidence boundary

Only Evidence records that explicitly contain `transition_data["protocol_path"]` are eligible as Protocol artifacts.

The bridge does not infer a path from prose, protocol identifiers, transition names, or arbitrary Evidence fields.

Duplicate artifact paths are collapsed deterministically before candidate generation.

## Candidate generation

`generate_candidates_from_evidence()` reuses the existing structural compatibility matrix and n-gram generator.

Therefore:
- candidates are structural suggestions only;
- semantic compatibility remains unverified;
- execution is not performed;
- authorization is not granted;
- the Evolution Loop state is not changed by proposal generation.

## Human Gate

`propose_candidates_from_evidence()` is proposal-only.

A selected candidate must still enter:

`prepare_candidate() → HUMAN_REVIEW → approve_candidate() → READY`

Only the existing R0100 Human Gate can authorize execution.

## Verification

After explicit approval, the existing One-Stroke Route Pipeline remains the execution boundary:

`READY → One-Stroke Runtime → Verify → ACCEPTED / DIFF → Evidence`

## Failure behavior

- Evidence without an explicit `protocol_path` is ignored.
- A malformed explicit `protocol_path` is rejected.
- Empty or invalid candidate routes remain fail-closed.
- Proposal generation alone cannot authorize execution.
- Verification mismatch remains `DIFF`.

## Non-goals

This α0.4 integration does not:
- infer semantic compatibility;
- automatically select a candidate;
- automatically authorize execution;
- infer Protocol artifact locations from arbitrary text;
- modify external reality;
- claim that a structurally generated route is correct.

## Relationship to α0.3

α0.3 connected Route Candidates to the canonical R0100 Human Gate.

α0.4 adds a conservative upstream proposal boundary:

`Evidence → Candidate Proposal → α0.3 Human Gate / One-Stroke Pipeline`

The Human Gate and Runtime execution boundaries remain unchanged.
