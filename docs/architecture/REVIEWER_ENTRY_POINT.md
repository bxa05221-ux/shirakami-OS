# Shirakami OS — Reviewer Entry Point

## Evidence Promotion Boundary

Blind review output is an external observation until independently verified and explicitly accepted through a Human Gate. Reviewer-supplied Evidence IDs are references only.

```text
External Review
      ↓
Observed Result
      ↓
Candidate Evidence IDs
      ↓
Repository / Test Verification
      ↓
Human Gate: approved
      ↓
Existing immutable EvidenceRecord(s) accepted for the reviewed purpose
```

The promotion boundary does not create new EvidenceRecords and does not mutate the EvidenceStore. It only resolves reviewer references against already-recorded immutable EvidenceRecords after explicit approval. Pending or rejected review cannot promote Evidence, and unknown Evidence IDs are rejected.

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

## Multi-Agent Review Boundary

Multiple reviewers can register their own Matome YAML context and submit observations separately. Use the [Blind External Review Protocol](./BLIND_EXTERNAL_REVIEW_PROTOCOL.md) and follow the HTTP route advertised by `GET /v1/capabilities`.

```text
Reviewer A ─┐
Reviewer B ─┼→ Reviewer Bundle → Comparative Trace → AIwitness → Traceability
Reviewer C ─┘                                      ↓
                                             Human Gate remains
```

The reviewer, comparative, AIwitness, and traceability layers have no decision authority. `decision` remains null, `authority_granted` remains false, `decision_authorized` remains false, and `human_gate_required` remains true throughout the review path.

## External Review API Route

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

The API capability surface advertises `blind_review_ingestion` and `blind_review_aiwitness_traceability`. Invalid blind-review payloads are rejected before ingestion. A successful traceability response demonstrates boundary validation for that request; it does not certify the architecture as a whole.

## Review Rule

Do not infer the project's intended meaning from the name `Shirakami OS`. Read the normative specification, follow the implementation path, inspect the tests and observations, and only then classify the architecture.
