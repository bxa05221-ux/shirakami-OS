# R0012-A — Landscape Lineage Boundary Fixture

## Purpose

Observe whether the existing Runtime boundaries can represent an inspectable lineage:

`Landscape State → Protocol → Transition → Evidence → Projection → resulting Landscape State`

This fixture does not define semantic continuity.

## Fixture

```yaml
source_landscape:
  state_id: "landscape-r0012-001"
  content:
    note: "source observable landscape"

protocol:
  protocol_id: "r0012.lineage.v1"
  version: "0.1"

transition:
  transition_id: "transition-r0012-001"
  kind: "r0012.landscape.transition"
  changed: true
  source_landscape_state: "landscape-r0012-001"
  resulting_landscape_state: "landscape-r0012-002"

evidence:
  evidence_id: "evidence-r0012-001"
  transition_id: "transition-r0012-001"
  protocol_id: "r0012.lineage.v1"

projection:
  operation: "apply_evidence"
  target_landscape_state: "landscape-r0012-002"

lineage_observation:
  status: "open"
  question: "Can this source-to-result lineage be inspected end-to-end without Runtime inferring semantic continuity?"
```

## Non-goals

- no continuity scoring;
- no semantic continuity detector;
- no migration;
- no replay semantics;
- no new Kernel schema;
- no interpretation of domain meaning.

## Expected Observation

The identifiers for Landscape, Protocol, Transition, and Evidence should remain distinguishable. Projection should remain an operation on Landscape state rather than a semantic claim about identity or continuity.
