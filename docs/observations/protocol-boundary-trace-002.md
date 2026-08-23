# Protocol Boundary Trace 002

## Status

Observed. No architecture change authorized.

## Specimens

Three existing Protocol specimens were traced by structure and current bridge implementation:

1. `examples/quickstart/protocol.yaml` — mechanical baseline.
2. `protocols/manual/manga-user-manual.yaml` — intermediate / rendering-oriented.
3. `protocols/manual/symbolic-recurrence-boundary.yaml` — semantic-density specimen.

## Trace

### A. Quickstart

The Protocol declares a four-phase pipeline: observe, transition, evidence, landscape. Its actions are `capture_input`, `mark_observed`, `capture_evidence`, and `expose_state`.

The current generic bridge does not execute those actions individually. It carries the pipeline as data into a generic `matome.protocol.transition` Transition.

### B. Manga User Manual

The Protocol declares observation and evidence phases and carries rendering-oriented manual data, language choices, SVG dimensions, pages, narration, and dialogue.

The current generic bridge likewise preserves the declared pipeline and payload as data. Domain rendering meaning is not interpreted by the Runtime bridge itself.

### C. Symbolic Recurrence

The Protocol is semantically dense. It declares symbolic lineage preservation, recurrence as Protocol data, an observable recurrence transition, and lineage preservation in Evidence.

Despite the semantic density, the current generic bridge still performs no branch for symbolic recurrence. It carries the declared statement and pipeline as generic Protocol data and emits the same generic `matome.protocol.transition` kind.

## Observation

Across all three specimens, the same Runtime-facing transition shape is sufficient for the current β0.1 vertical slice.

The semantic density of the Protocol does **not**, by itself, produce a Runtime-side semantic interpreter.

This is strong evidence against introducing `TransitionPlan` solely because a Protocol contains meaning-rich actions.

## Important Finding

There are currently two Runtime-facing bridge concepts in the repository:

- `runtime/protocol_bridge.py` converts validated `ProtocolIR` into a generic Runtime-compatible callable and explicitly avoids domain-specific action branches.
- `runtime/protocol_runtime_bridge.py` adapts a loaded Protocol IR to the existing Runtime signature but delegates the actual transition callable supplied by the caller.

This is an implementation-boundary observation, not yet evidence that either should be renamed or merged.

## Semantic Authority Test

The current specimens do not demonstrate a stable need for a separate Interpreter that selects among alternative transitions based on Protocol semantics.

The strongest candidate, Symbolic Recurrence, currently remains declarative at the Runtime boundary. Its semantic claims are represented in Protocol data rather than interpreted by Runtime.

## TransitionPlan Test

No recurring, backend-neutral intermediate execution plan was observed across these three specimens. The current generic Transition is sufficient for the demonstrated vertical slice.

Therefore:

**TransitionPlan remains a hypothesis, not a demonstrated requirement.**

## Next Trigger for Re-observation

Re-open the boundary only when an existing or new Protocol requires one of the following:

- conditional transition selection;
- Landscape-dependent eligibility;
- verification that changes which transition is executed;
- multiple declared transitions where Runtime must select one;
- a semantic operation that cannot remain declarative data while still producing the intended observable transition.

Until such evidence appears, preserve the current boundary and avoid adding an Interpreter layer or RFC-0006 amendment solely for architectural symmetry.
