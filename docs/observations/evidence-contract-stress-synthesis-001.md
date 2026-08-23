# Evidence Contract Stress Synthesis 001

## Status

Observation synthesis. No Evidence schema change is authorized.

## Current β0.1 Evidence shape

```text
protocol_id
status
transition_kind
transition_data
signals
```

`EvidenceRecord` is immutable, but its current identity is effectively the combination of protocol and captured transition data. It does not currently carry explicit event identity, creation timestamp, causal parent, sequence number, or Landscape version.

## Observed consequences

### 1. Immutability is present

Once created, an EvidenceRecord cannot be mutated through the dataclass interface. This preserves the observed execution record.

### 2. Provenance is minimal

`protocol_id` identifies the producing Protocol, but does not uniquely identify an individual occurrence of the same Protocol.

### 3. Causality is not represented

The current Evidence shape cannot explicitly express "this transition was produced from Evidence X" or "this transition observed Landscape version Y".

### 4. Ordering is external

Landscape application order is determined by the order in which `apply_evidence()` is called. The Evidence itself does not carry a sequence contract.

### 5. Conflict detection is therefore not currently possible from Evidence alone

Two valid Evidence records can both assert `changed: true` and target the same Landscape key. Landscape currently applies the later mapping update.

## Important distinction

This does **not** demonstrate that the Evidence schema is deficient for β0.1.

It demonstrates only that stronger guarantees such as causal reconstruction, deterministic conflict detection, replay ordering, or concurrent merge semantics would require additional information somewhere in the architecture.

## Existing Architecture Evidence

The existing symbolic recurrence experiment already describes the intended path as:

```text
Historical Evidence
→ Lineage
→ Current Landscape
→ Recurrence Candidate
→ Human Authority
→ Transition
→ Evidence
```

and explicitly requires Human Authority to accept or reject a recurrence before it becomes new Evidence. This indicates that semantic selection can remain outside the Runtime execution boundary when the experiment is modeled as a human-authorized transition.

## Current Decision

Do not add timestamp, version, sequence, causal-parent, or event-id fields merely because they are conventional.

First determine which guarantees Shirakami OS actually requires:

- auditability;
- replayability;
- causal lineage;
- concurrency;
- conflict detection;
- deterministic reconstruction;
- historical Landscape comparison.

Only the required guarantee should create a new Evidence contract field.

## Architectural Observation

The stress tests so far have produced two different kinds of missing semantics:

```text
Protocol → Runtime
    no demonstrated need for Interpreter yet

Evidence → Landscape
    conflict policy is unspecified
```

This suggests that the next architectural question is not "where do we put more intelligence?" but:

> What minimum information must an immutable Evidence record carry so that a Landscape can remain an observable, reconstructable state rather than merely a last-write-wins dictionary?

## Next Test

Construct a minimal replay test:

1. Start with empty Landscape.
2. Apply Evidence A.
3. Apply Evidence B.
4. Reconstruct the same final Landscape from the Evidence sequence.
5. Reverse A/B.
6. Compare whether the resulting Landscape is expected to differ.

If order matters, determine whether that ordering is an intended semantic property or an accidental implementation detail.

Do not introduce a version/sequence field until this test establishes the requirement.
