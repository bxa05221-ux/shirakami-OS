# R0012-C: End-to-End Matome Vertical Slice

## Question

Can the source-to-result path be inspected end-to-end through the actual Matome execution entry point, without Runtime inferring semantic continuity?

## Observed path

The experiment uses the existing `execute_matome()` composition:

`Matome YAML → ProtocolIR → Runtime → ExecutionResult → Evidence → Projection → Landscape`

The input contains an observable source Landscape identifier:

`landscape-r0012-001`

The resulting Evidence preserves the Runtime protocol identity, transition kind, and input snapshot. Projection then exposes that carried input in the resulting Landscape state.

## Boundary observation

The current vertical slice provides an inspectable structural lineage from Protocol input through Transition/Evidence to projected Landscape state.

It does not establish that the resulting Landscape is a continuation of the source Landscape in a semantic sense.

No continuity score, continuity claim, migration operation, replay interpretation, or semantic lineage detector is introduced.

## Important distinction

`lineageを追跡できる` ≠ `continuityを証明できる`

The experiment therefore supports structural lineage observation only.

## Implementation impact

No Runtime, ProtocolIR, or Evidence schema change is justified by R0012-C.

The existing vertical slice is sufficient to observe the current boundary. Any future semantic interpretation of continuity should remain outside the Kernel unless a stabilized specification explicitly promotes it.

## Status

- structural lineage: observed
- end-to-end vertical slice: observed
- semantic continuity: not established
- migration: not implemented
- replay semantics: not implemented
- Kernel schema change: not justified
