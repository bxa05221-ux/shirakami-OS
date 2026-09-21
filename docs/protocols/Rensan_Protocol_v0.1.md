# Rensan Protocol v0.1

## 1. Purpose

Rensan (連山) is a protocol for connecting related contexts, viewpoints, and Protocol Candidates without collapsing them into a single authoritative conclusion.

It treats knowledge as a connected landscape: each mountain retains its own identity, evidence, uncertainty, and local conditions while remaining linkable to neighboring mountains.

## 2. Core Principle

**Connect contexts without erasing their differences.**

A connection is a navigational relation, not proof of equivalence, causality, priority, or agreement.

## 3. Allowed Functions

Rensan may:

- identify explicit and proposed relationships between contexts;
- preserve source references and provenance;
- expose shared terms, dependencies, tensions, and gaps;
- show multiple routes between related topics;
- support human inspection of possible synthesis.

Rensan must not:

- merge distinct contexts silently;
- infer truth, consent, authority, or safety from proximity;
- treat repeated association as proof;
- remove contradictory or isolated nodes for narrative convenience;
- authorize execution or replace Evidence verification.

## 4. Relation Types

Every relation should be typed where possible, for example:

- `references`
- `depends_on`
- `contrasts_with`
- `supports`
- `questions`
- `shares_context`
- `proposes_transfer`
- `unknown`

Uncertain or inferred relations must be marked as candidates rather than facts.

## 5. Node Requirements

Each node should retain:

- stable identifier;
- origin and context reference;
- stated intent;
- observations and interpretations separately;
- evidence references, if available;
- assumptions and uncertainty;
- current status and human decision boundary.

## 6. Connection Procedure

1. Identify the contexts to be connected.
2. State the intended purpose of the connection.
3. Describe the proposed relation and its basis.
4. Preserve alternative interpretations and non-connections.
5. Identify missing evidence, conflicts, and possible harms.
6. Present the connected landscape for human review.
7. Keep execution, verification, and acceptance external to the connection process.

## 7. Change and History

Connections are versioned observations of a changing landscape. Removing, weakening, or revising a relation must not erase its historical record.

When context, intent, authority, consent, evidence, or environmental conditions change, the relation should be re-evaluated rather than silently reused.

## 8. Illustrative Output

```yaml
rensan:
  id: rensan-001
  intent_ref: intent-001
  nodes:
    - id: context-a
      origin_ref: source-a
    - id: context-b
      origin_ref: source-b
  relations:
    - from: context-a
      to: context-b
      type: contrasts_with
      basis_refs: [evidence-001]
      confidence: unknown
      status: candidate
  alternatives:
    - relation: no_connection
      reason: insufficient_context
  uncertainty_refs: [uncertainty-001]
  human_review:
    required: true
    decision: pending
```

## 9. Stop Conditions

Pause connection work when:

- the intended purpose is unclear;
- provenance cannot be distinguished from interpretation;
- the relation could be mistaken for authorization or proof;
- relevant consent, responsibility, or safety boundaries are unresolved;
- contradictions or missing context materially affect interpretation.

## 10. Non-Goals

This protocol does not aim to create a universal knowledge graph, guarantee semantic compatibility, automate synthesis, or transfer decision authority to AI.

## 11. Status

This is a documentation-level protocol candidate. Runtime implementation, semantic verification, authorization, and Evidence acceptance remain separate concerns.
