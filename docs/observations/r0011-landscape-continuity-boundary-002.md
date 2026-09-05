# R0011 — Landscape Continuity Boundary Observation 002

## Status

- Experiment: R0011-B
- Theme: Protocol version transition
- Status: experimental
- Scope: structural continuity only

## Fixture

```yaml
landscape:
  state_id: "landscape-r0011-001"
  content:
    note: "same human landscape"

v1:
  protocol_id: "r0011.protocol.v1"
  evidence:
    evidence_id: "evidence-v1-001"
    transition_id: "transition-v1-001"
  resulting_landscape_state: "landscape-r0011-001"

v2:
  protocol_id: "r0011.protocol.v2"
  input_landscape_state: "landscape-r0011-001"
  evidence:
    evidence_id: "evidence-v2-001"
    transition_id: "transition-v2-001"
  resulting_landscape_state: "landscape-r0011-002"

continuity_claim:
  status: "unverified"
  question: "Is landscape-r0011-002 a continuation of landscape-r0011-001?"
```

## Observation

The same Landscape is used as the input boundary for two Protocol versions. Each version has its own transition and Evidence identity, while the resulting Landscape State is represented separately.

The fixture deliberately does not assert that the two resulting states are equivalent or continuous.

## Expected Boundary

Runtime may preserve:

- source Landscape state
- Protocol identity
- Evidence identity
- Transition identity
- resulting Landscape state
- continuity question

Runtime must not infer the continuity claim merely from shared input state or matching data.

## Non-goals

This experiment does not define:

- Protocol equivalence
- semantic compatibility
- migration correctness
- replay correctness
- continuity scoring
- automatic lineage judgment

## Result

The experiment is a structural fixture for observing whether lineage remains explicit when Protocol versions change. A successful transport of this fixture is evidence of representational continuity support, not proof of semantic Landscape continuity.