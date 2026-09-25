# Shirakami OS — Reviewer Entry Point

## Purpose

This is the shortest evidence-backed route for an external reviewer or AI system to inspect Shirakami OS without relying on prior knowledge.

The repository is one implementation layer within a larger Shirakami Landscape. Stable normative specifications are maintained in `shirakami-specification`; this repository contains Runtime, adapters, plugins, tests, and executable artifacts.

## Repository Roles

```text
shirakami-model
    ↓ conceptual foundation
shirakami-research
    ↓ observation / experiment
shirakami-specification
    ↓ normative contract
shirakami-OS
    ↓ runtime / implementation
Evidence / Observation
    ↺ research
```

## Recommended Reading Order

1. **Repository README** — implementation-layer scope and architecture
2. **Normative Specification** — [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification)
3. **Current verified Evolution Loop** — [Evidence → Route Candidate Bridge α0.4](../EVIDENCE_ROUTE_CANDIDATE_ALPHA_0_4.md)
4. **Foundation / implementation boundary** — [spec/README.md](../../spec/README.md)
5. **Architecture baseline** — [docs/Shirakami_OS_Alpha2.2.md](../Shirakami_OS_Alpha2.2.md)
6. **Active / historical RFCs** — [docs/rfc/](../rfc/)
7. **Runtime implementation** — [runtime/](../../runtime/)
8. **Adapters / plugins** — [plugins/](../../plugins/)
9. **Evidence / observation records** — [docs/observations/](../observations/)
10. **Examples / protocol source artifacts** — [examples/](../../examples/) and [protocols/](../../protocols/)

## MVP Execution Path

For a quick implementation check, follow this concrete path:

```text
Protocol Source
      ↓
Protocol Loader
      ↓
Current Selection
      ↓
MTM Compatibility
      ↓
Runtime Execution
      ↓
Inspectable Result
```

The minimum executable entry point is `runtime/execute.py`. It deliberately stops at a prepared Runtime result; AI-provider invocation is outside the current MVP boundary.

The corresponding execution test is `tests/test_execute.py`.

Run the verification suite with:

```bash
python -m pytest runtime tests -q
```

The MVP boundary is considered healthy when this suite is green.

## Specification Boundary

The canonical home for stable normative contracts is `shirakami-specification`.

The `docs/rfc/` directory in this repository is now an RFC history and active-design area. RFC-0001 through RFC-0005 have promoted specifications; RFC-0006 remains Draft.

Do not treat implementation-side documents as normative merely because they are present in this repository.

## Kernel Boundary

The current implementation should be reviewed around these boundaries:

```text
Human Landscape
      ↓
Matome / Protocol Source
      ↓
Protocol IR
      ↓
Runtime
      ↓
Execution Result
      ↓
Evidence
      ↓
Projection
      ↓
Landscape State
      ↓
Replay / Restore
```

The following are Kernel concerns:

- Landscape State
- Protocol / Protocol IR
- Transition execution
- Evidence preservation
- Projection boundary
- Replay / determinism boundary
- Adapter boundary

The following remain outside the Runtime Kernel:

- Domain-specific meaning
- LLM-specific control flow
- UI rendering
- Backend-specific storage semantics
- Research hypotheses not accepted as Foundation contracts

## Architecture Review Questions

An external review should answer these questions from repository evidence rather than from the project name or README alone.

### Protocol / Runtime

- Does the Runtime execute generic Protocol structure without hard-coded domain meaning?
- Does Protocol define allowed transitions rather than merely encode a workflow sequence?
- Where does semantic authority reside when richer semantics are introduced?

### Evidence

- Is Evidence immutable?
- Can an execution result be traced to the Protocol that produced it?
- Is Evidence distinct from an ordinary operational log?

### Projection / Landscape

- Is Evidence separated from its projection into Landscape State?
- Is Landscape State the state/context used by subsequent Protocol evaluation?
- Is Landscape a runtime state model rather than merely an audit-log read model?

### Comparison with Existing Systems

Do not begin by asking whether Shirakami resembles Event Sourcing, Workflow Engines, Policy Engines, or Agent Frameworks.

Instead ask:

> If the system were reduced to ordinary Event Sourcing plus Workflow execution, which current Kernel responsibilities would be lost?

The answer must be derived from the actual Protocol, Evidence, Projection, Landscape, and Replay boundaries in the repository.

## Multi-Agent Review Boundary

Shirakami also supports a reviewer-oriented path in which multiple reviewers can register their own Matome YAML context and submit observations separately.

### Architecture Map

See [Reviewer → AIwitness → Traceability Architecture Map](./REVIEWER_AIWTNESS_TRACEABILITY_MAP.md) for the detailed four-layer boundary.

For independent re-review, use the [Blind External Review Protocol](./BLIND_EXTERNAL_REVIEW_PROTOCOL.md). It requires the reviewer to begin from this entry point without being given the expected conclusion or prior review result.

```text
Reviewer A ─┐
Reviewer B ─┼→ Reviewer Bundle → Comparative Trace → AIwitness → Traceability
Reviewer C ─┘                                      ↓
                                             Human Gate remains
```

The four layers have distinct responsibilities:

| Layer | Primary role | Authority |
|---|---|---|
| Reviewer | Observation producer | none |
| Comparative Trace | Comparison / preservation | none |
| AIwitness | Provenance / observation boundary | none |
| Traceability | Continuity validation | none |

The comparative layer preserves:

- reviewer identity;
- each reviewer's Matome YAML context;
- submitted observations;
- proposals;
- Evidence IDs;
- shared Evidence;
- divergent Evidence.

A comparative trace does **not** produce a decision. `decision` remains null, `authority_granted` remains false, `decision_authorized` remains false, and `human_gate_required` remains true.

AIwitness records the resulting provenance and traceability as an observation boundary. It does not convert reviewer agreement, Evidence, verification status, or an AI-generated interpretation into authority.

Traceability validates continuity and rejects authority escalation. It checks the comparative decision/authority boundary and, for execution traces, Evidence, identity, verification, commit, and execution/publish/merge authority continuity.

For the implementation boundary, inspect:

- `reviewer/registry.py`
- `reviewer/comparative_trace.py`
- `reviewer/aiwitness_bridge.py`
- `aiwitness/traceability.py`
- `reviewer/test_comparative_aiwitness_integration.py`
- `aiwitness/test_traceability.py`
- `aiwitness/AIWITNESS_BOUNDARY_CONTRACT.yaml`
- [Reviewer → AIwitness → Traceability Architecture Map](./REVIEWER_AIWTNESS_TRACEABILITY_MAP.md)

This allows an external reviewer or AI reviewer to contribute observations without becoming the project's decision-maker.

## Evidence Policy

External AI observations are **observations**, not authoritative facts.

Repository code, tests, immutable Evidence, and accepted specifications are the primary evidence sources.

When external reviews disagree:

```text
External Observation
       ↓
Candidate Question
       ↓
Repository / Test Verification
       ↓
Accepted Evidence
```

Do not silently reconcile contradictory external interpretations.

## 30-Minute Review Route

For a timed first-pass external review, use the [30-Minute External Review Guide](../EXTERNAL_REVIEW_GUIDE_30MIN.md). It follows the same evidence boundary as this entry point and the Public Verification Pack.

## Public Verification

For a compact, reproducible external review route, use [Public Verification Pack](../PUBLIC_VERIFICATION_PACK.md).

It is intentionally not a certification or production-readiness claim; it defines the current public verification boundary.

## External Review API Route

For reviewers using the HTTP boundary, the shortest executable route is:

```text
Reviewer Entry Point
        ↓
Blind Review Matome YAML
        ↓ POST /v1/reviews/blind
Validator
        ↓
ReviewerBundle
        ↓ POST /v1/reviews/blind/comparative/aiwitness
Comparative Trace
        ↓
AIwitness Context
        ↓
Comparative Traceability
        ↓
Human Gate
```

The API capability surface advertises this route through `GET /v1/capabilities`:

- `blind_review_ingestion`
- `blind_review_aiwitness_traceability`

The HTTP route does not grant execution, publication, merge, or decision authority. Invalid blind-review payloads are rejected before they enter the Reviewer Bundle. A successful traceability response demonstrates boundary validation for that request; it does not certify the architecture as a whole.

For implementation inspection, see `api/http.py`, `reviewer/blind_review.py`, `scripts/validate_blind_review_result.py`, and `reviewer/test_comparative_aiwitness_integration.py`.

## Current Review Status

- Repository entry point: established
- Repository role boundary: established
- Normative specification navigation: established
- Runtime implementation navigation: established
- Adapter / plugin navigation: established
- Observation / Evidence navigation: established
- MVP execution path: established
- Multi-Agent Reviewer → AIwitness → Traceability Map: established
- Event Sourcing / Workflow divergence: pending external review
- Landscape layer placement: pending verification
- Rich Protocol Semantics boundary: deferred
- Evidence → structural Route Candidate proposal: implemented (α0.4)
- Route Candidate → Human Gate → One-Stroke Runtime → Verification: implemented (α0.3)
- Migration policy: pending explicit contract

## Review Rule

Do not infer the project's intended meaning from the name `Shirakami OS`.

Read the normative specification, follow the implementation path, inspect the tests and observations, and only then classify the architecture.
