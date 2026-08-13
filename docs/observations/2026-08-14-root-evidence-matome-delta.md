# Root Evidence / Matome Delta Observation

## Status

Exploration / provisional architectural observation.

## Observation

The current working model suggests that Evidence should be separated from the derived Matome YAML representation.

The proposed relationship is:

```text
Root Evidence
  ↓
Dialogue / Observation
  ↓
Difference (Delta)
  ↓
Matome YAML
```

Root Evidence is not limited to documentary evidence. It may include the subject's baseline identity, baseline context, individual characteristics, and foundational understanding.

The subject type is part of the root context and must distinguish, at minimum, whether the subject is human or AI. Other subject types may be introduced only when required by implementation or observation.

## Working model

```text
Root Evidence
├─ Subject
│  ├─ identity
│  └─ type: human / ai / ...
├─ baseline context
├─ characteristics
└─ foundational understanding
       ↓
   dialogue / observation
       ↓
      delta
       ↓
   Matome YAML
```

## Matome YAML role

Matome YAML is treated provisionally as a derived representation of dialogue-generated differences rather than the source of record itself.

It may compress, organize, preserve, and carry forward deltas between dialogue contexts.

It must not silently redefine, mutate, or replace Root Evidence.

Loss or distortion introduced by Matome compression is therefore a property of the derived representation and must remain distinguishable from a change in the underlying Evidence.

## Counter-Evidence hypothesis

Where useful, a Counter-Evidence observation may be introduced as an opposing or boundary condition against which the persistence of an Evidence state can be observed.

This is not a truth-versus-falsehood mechanism. Its purpose is to distinguish:

- transient dialogue changes;
- stable changes;
- context-dependent changes;
- unresolved or unstable states.

A change that persists under relevant Counter-Evidence may provide stronger evidence of a durable state transition than a single conversational statement.

## Architectural constraint

Do not yet promote this model into Foundation terminology or introduce a dedicated RootEvidence or CounterEvidence runtime abstraction solely on the basis of this observation.

First verify whether the existing Evidence, Observation, Landscape, Runtime, and Matome boundaries can represent the lifecycle without theoretical expansion.

## Verification target

Construct a controlled dialogue sequence in which:

1. a baseline subject state is recorded;
2. dialogue produces a measurable delta;
3. the delta is serialized as Matome YAML;
4. a Counter-Evidence condition is introduced where appropriate;
5. the subject state is re-observed;
6. the reconstructed state is compared with the original baseline and the observed delta.

The comparison should distinguish:

- baseline Evidence;
- observed Delta;
- Matome-derived reconstruction;
- Counter-Evidence response;
- genuinely persistent state change.
