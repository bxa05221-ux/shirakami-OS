# API Boundary Inventory α0.1

Status: observation

## Purpose

Record the currently implemented and drafted API surfaces without changing Runtime semantics.

## Current surfaces

| Surface | Layer | State | Boundary responsibility |
|---|---|---|---|
| `/v1/chat` | Human / OPPAI | implemented reference | Human-facing conversational entry point |
| `/v0.1/execute` | Runtime | implemented | Protocol IR execution boundary |
| `/v0.1/oppai/normalize` | OPPAI | implemented | OPPAI observation/normalization boundary |
| `/v0.1/github/read` | Adapter | implemented | Backend observation through GitHub Adapter |
| `/v0.1/github/write` | Adapter | implemented | Controlled backend write with read-back |
| `/v1/landscapes/boot` | Landscape / Research API | draft contract | Landscape service contract proposal |
| `/v1/observations` | Observation / Research API | draft contract | Observation service contract proposal |
| `/v1/conferences` | Research / Coordination API | draft contract | Conference service contract proposal |

## Observations

1. Human-facing chat and direct Runtime execution are currently separate API surfaces.
2. OPPAI normalization is exposed as a distinct preprocessing boundary.
3. GitHub operations are exposed through an Adapter-facing boundary rather than direct backend calls from the documented API contract.
4. Landscape/Observation/Conference endpoints exist as a draft Matome API contract and are not treated here as implemented Runtime capabilities.
5. API version prefixes are currently heterogeneous (`/v1` and `/v0.1`). This inventory records the fact only; it does not prescribe a versioning change.

## Boundary questions for verification

- Does each implemented surface stay within its declared responsibility?
- Does the Runtime avoid owning Domain Semantic Truth?
- Does the Adapter remain responsible for backend interaction rather than Runtime meaning?
- Are Evidence and Landscape changes observable without hidden API-side judgment?
- Does `/v1/chat` remain an entry boundary rather than becoming a second Domain Runtime?

## Non-goals

- No endpoint renaming.
- No API version unification.
- No Runtime semantic changes.
- No Evidence schema changes.
- No automatic correctness judgment.

## Verification rule

One change → one verification → one confirmation.

If a boundary violation is observed, record it as Evidence/Observation before proposing implementation changes. Do not resolve a theoretical ambiguity inside the implementation layer.
