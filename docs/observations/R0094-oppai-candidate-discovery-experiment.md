# R0094 — OPPAI Candidate Discovery Experiment

## Purpose

Define the smallest safe experiment for OPPAI Protocol Candidate Discovery.

## Hypothesis

OPPAI's primary routing work may be to expose a small set of Protocol candidates from natural-language input and current context, before any Protocol is activated.

## Candidate model

Each candidate contains:

- `protocol_id`
- `basis`: observable reason for inclusion
- `status`: `candidate`
- optional context signals

No candidate is treated as selected merely because it has the highest confidence.

## Boundary

```
Natural Language
  ↓
OPPAI Observation
  ↓
Protocol Candidates
  ↓
Human Gate
  ↓
Selected Protocol
  ↓
ProtocolRegistry
  ↓
ProtocolRequest
  ↓
Runtime
```

## Selection authority

OPPAI may discover or propose candidates.

OPPAI must not silently activate a Protocol.

ProtocolRegistry resolves an explicitly selected Protocol.

Human Gate remains the authority for ambiguous or consequential Protocol selection.

## Pipeline status

Pipeline is intentionally not a Runtime object in this experiment.

The experiment only records whether a selected Protocol can later be associated with a different execution path, Adapter, or generation model. That relationship remains an implementation observation until separately specified.

## Minimal experiment

Given the same human input, vary:

1. current context;
2. available Protocol set;
3. time/operation phase.

Observe whether the candidate set changes.

Record:

- input;
- context;
- available Protocols;
- candidate Protocols;
- basis for each candidate;
- selected Protocol;
- execution adapter/model used;
- resulting Evidence.

## Non-goals

- autonomous Protocol selection
- model ranking
- vendor ranking
- new Pipeline runtime object
- automatic Protocol activation
- Evidence semantic changes

## Expected finding

If candidate sets consistently vary with context, available Protocols, or operation phase, OPPAI's routing role is supported.

If not, the current OPPAI→Protocol hypothesis must be narrowed.

