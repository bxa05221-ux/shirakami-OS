# Evidence Replay Result 001

## Status

Observation result. No Evidence schema change is proposed.

## Test Model

Two valid transition Evidence records target the same Landscape key:

```text
A = { changed: true, phase: "A" }
B = { changed: true, phase: "B" }
```

Replay A → B and B → A against an empty Landscape.

## Result under β0.1 projection semantics

The Landscape projection is an ordered dictionary update. Therefore:

```text
A → B  => phase = "B"
B → A  => phase = "A"
```

The two replay orders do not produce the same Landscape.

## What this proves

1. Current Landscape projection is order-sensitive.
2. Evidence occurrence order is therefore semantically relevant whenever multiple Evidence records target the same state field.
3. β0.1 does not currently encode that order inside Evidence itself.
4. A replay performed from an externally supplied ordered collection can reproduce the result, but an unordered collection of Evidence cannot guarantee the same Landscape.

## What this does NOT prove

It does not prove that Evidence needs timestamps, sequence numbers, event IDs, causal parents, or Landscape versions.

Those fields solve different problems:

- timestamp: temporal observation, not necessarily total ordering;
- sequence: explicit ordering within a defined stream;
- event ID: occurrence identity/deduplication;
- causal parent: causal reconstruction;
- Landscape version: optimistic/concurrent state validation.

No one of these should be introduced without a concrete use case.

## Architectural Finding

The current boundary is sufficient for deterministic replay **when an ordered Evidence stream is already supplied**.

The unresolved contract is therefore not primarily Runtime semantics. It is the definition of the Evidence stream itself:

```text
Evidence records
      ↓
ordered stream ?
      ↓
Landscape projection
```

## Decision

Do not change the Evidence schema yet.

Do not introduce a ConflictResolver yet.

Record that β0.1 currently assumes ordering externally rather than representing ordering intrinsically.

## Next Observation

Test whether Shirakami OS requires any of the following concrete capabilities:

- persistence and later replay;
- deduplication;
- distributed/concurrent Evidence arrival;
- cross-session reconstruction;
- causal explanation of Landscape changes.

Only if one of these is required should the missing metadata be selected deliberately.
