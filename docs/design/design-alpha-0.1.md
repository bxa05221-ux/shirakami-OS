# Shirakami Design α0.1

## Position

This document translates the Architecture Blueprint α0.1 into concrete design responsibilities. It does not redefine Vision, Constitution, or Blueprint.

## Design Scope

- API boundaries
- State Machine boundaries
- Protocol IR representation boundary
- Workspace/document layout
- Validation boundary

## API Boundary

### Protocol boundary

The Protocol API accepts a registered protocol definition and constructs a runtime-facing protocol request.

Responsibilities:
- identify the protocol
- preserve protocol version/state
- carry protocol input
- keep protocol meaning outside Runtime ownership

### Runtime boundary

Runtime receives structured input and executes a declared transition.

Responsibilities:
- accept execution context
- execute a transition
- return an observable execution result
- preserve transition data for Evidence capture

Runtime must not:
- invent domain meaning
- declare semantic truth
- replace human final judgment

### Landscape boundary

Landscape execution receives a LandscapeState and produces observable evidence of a state transition.

Landscape remains the holder of contextual state; Runtime does not become the owner of that context.

### Adapter boundary

Adapter connects a protocol/runtime request to an external backend.

Adapter exchange must not require changes to Landscape semantics or Protocol meaning.

### Renderer boundary

Renderer receives projectable Landscape/runtime information and produces a presentation artifact.

Renderer output is presentation, not semantic authority.

## State Machine Boundary

The minimum observable transition is:

`input → transition → execution result → evidence → landscape state`

The protocol execution path is:

`protocol registration → protocol request → runtime execution → observable result → evidence`

The state machine records observable transitions. It does not infer psychological, semantic, or causal truth unless such meaning is explicitly supplied by the Protocol layer.

## Protocol IR Boundary

Protocol IR is the structural handoff between Protocol and Runtime.

It carries the declared execution structure required by Runtime, including:

- protocol identity
- version/state
- applicable conditions
- verification requirements
- referenced state
- declared transitions
- input required for execution

Protocol IR does not become a repository for domain truth owned by Runtime.

## Evidence Boundary

Evidence captures observable execution/state change.

Required properties:

- immutable observation after capture
- transition data sufficient to identify the observed change
- reference continuity where an earlier Evidence item is explicitly referenced

Evidence must not silently add:

- intent
- emotion
- diagnosis
- causality
- semantic equivalence

## Workspace Boundary

The documentation hierarchy is:

```text
Vision/
Constitution/
Blueprint/
Design/
Implementation/
```

Architecture documents describe structure. Design documents describe concrete specifications. Implementation contains executable code and tests.

## Validation Boundary

Validation is performed at the narrowest relevant boundary.

Rules:

1. One change, one verification.
2. Do not mark unverified behavior as successful.
3. Preserve unknowns as unknowns.
4. Verify continuity across exchange boundaries.
5. Verify that Renderer and external AI do not acquire semantic authority.

## Current Verified Path

The repository currently contains a verified State Machine continuity test covering:

`OPPAI observation → i-field → Evidence → Protocol → Runtime → Evidence → Landscape`

This Design document does not reinterpret that test; it defines the specification boundaries that the implementation must preserve.

## Unresolved Design Items

The following remain open and must not be silently resolved here:

- final Evidence Lineage granularity
- final Protocol IR format constraints
- complete Runtime execution semantics
- complete Landscape/Evidence persistence granularity

These require separate verification or research handoff.
