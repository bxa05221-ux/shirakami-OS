# Shirakami OS — Phase 2: Runtime Verification

## Status

**Phase 2: In progress**

Phase 1 established the external entry point. Phase 2 begins the transition from **understanding** to **hands-on verification**.

The goal is deliberately narrow: make the existing Runtime path easy to run, inspect, and verify before expanding the architecture.

## First verification path

The repository already contains a dependency-light Quickstart that exercises the core path without GitHub credentials or external services:

```text
Matome YAML
    ↓
Protocol IR
    ↓
generic Protocol bridge
    ↓
Runtime
    ↓
Evidence
    ↓
Landscape State
```

Run:

```bash
python examples/quickstart/run.py
```

Expected terminal milestones:

```text
Protocol loaded: ...
Observation captured
Transition created
Evidence captured
Landscape State exposed
...
SUCCESS
```

The Quickstart explicitly reports failure with a non-zero exit code if the Runtime result is not `completed`.

## Phase 2 verification questions

The first pass should answer only these questions:

1. Can a fresh checkout execute the Quickstart without project-specific credentials?
2. Does Matome YAML load into the Protocol representation?
3. Does the generic Protocol bridge produce an executable Protocol?
4. Does Runtime execution produce a completed result?
5. Can the result be captured as Evidence?
6. Can Evidence be applied to an empty Landscape State?
7. Is the resulting Landscape State inspectable?
8. Does CI reproduce the same basic verification boundary?

## Evidence rule

A successful local run is useful evidence, but it is not the same as an externally validated architecture.

Phase 2 therefore records executable behavior first and leaves architectural interpretation to the reviewer workflow.

## Scope control

Do **not** expand Phase 2 by adding new conceptual Protocols merely to make the demo look larger.

The priority is:

```text
Existing implementation
        ↓
Reproducible execution
        ↓
Observable result
        ↓
Test coverage
        ↓
External review
```

## Exit criteria

Phase 2 can be considered complete when:

- the Quickstart is reproducible from a clean checkout;
- its success/failure boundary is covered by automated tests;
- the Runtime → Evidence → Landscape path is inspectable;
- the API execution path has a documented reproducible example;
- CI verifies the agreed minimum path;
- known limitations are documented rather than hidden.

Only after these criteria are met should Phase 3 focus on external architectural evaluation.
