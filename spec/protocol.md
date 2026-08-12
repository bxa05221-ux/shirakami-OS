# Protocol Specification α0.1

## Status

This document defines the minimum Protocol contract currently required by Shirakami OS Runtime β0.1.

It is an implementation specification, not a new theoretical model. It records only behavior already required by the current Foundation and Runtime.

## 1. Purpose

A Protocol is an executable description of an allowed interaction or transition within Shirakami OS.

The Runtime consumes Protocol definitions and executes the transitions they permit. The Runtime must not silently invent architectural meaning that is absent from the Protocol or its governing Foundation contracts.

## 2. Relationship to Matome YAML

Matome YAML is the canonical human-authored representation used to express Protocol definitions.

The current processing path is:

```text
Matome YAML
    ↓
Protocol Loader
    ↓
Protocol IR
    ↓
Runtime
    ↓
Evidence
    ↓
Landscape State
```

The Runtime may use an intermediate representation (Protocol IR), but the IR is an implementation artifact and does not replace Matome YAML as the authoring format.

## 3. Minimum Protocol Structure

A Protocol should provide, at minimum:

- `matome.title` — protocol identity
- `matome.version` — protocol version
- `matome.status` — lifecycle or implementation status when applicable
- `matome.statement` — human-readable purpose or governing statement
- `matome.pipeline` or equivalent executable phases when the protocol defines a workflow

Additional fields may be defined by individual protocols. Unknown fields must not be treated as architectural contracts unless explicitly specified by the relevant protocol or Foundation document.

## 4. Loader Responsibilities

The Protocol Loader is responsible for:

1. Reading the Matome YAML representation.
2. Parsing the YAML into an internal representation.
3. Validating the minimum structure required by the Runtime.
4. Preserving protocol metadata and declared phases.
5. Returning a Runtime-consumable Protocol IR.

The Loader is not responsible for inventing missing protocol semantics.

## 5. Runtime Boundary

The Runtime executes Protocol-defined transitions.

The Runtime is responsible for:

- receiving a validated Protocol IR;
- executing supported transitions;
- recording Evidence at observable transition points;
- preserving Evidence;
- exposing resulting Landscape State to permitted adapters or consumers.

The Runtime is not the source of Protocol authority. Protocol authority remains outside the Runtime implementation.

## 6. Evidence Boundary

A Runtime transition that produces an observable architectural or Landscape change should produce Evidence according to the active Evidence Contract.

Evidence records what was observable at the transition point. Evidence must not be silently rewritten to make later interpretation appear consistent.

The current boundary is:

```text
Protocol
   ↓
Runtime Transition
   ↓
Evidence
   ↓
Landscape State
```

## 7. Protocol Does Not Define

This specification does not define:

- a universal cognitive ontology;
- a fixed Landscape hierarchy;
- a specific AI model;
- a specific Backend;
- a mandatory database schema;
- a universal scheduling system;
- a complete future Protocol language.

Those concerns remain outside the minimum α0.1 contract unless separately specified.

## 8. Compatibility Rule

A Runtime implementation claiming Protocol Specification α0.1 compatibility must:

1. accept the supported Matome YAML subset;
2. produce a usable Protocol IR;
3. execute the transitions explicitly supported by that Runtime;
4. preserve Evidence produced by those transitions;
5. avoid silently treating implementation-specific fields as universal Protocol semantics.

## 9. Evolution

This specification may be extended when implementation or observation demonstrates a stable requirement.

New theoretical concepts should not be added to this specification merely to anticipate future architecture. Such questions should be returned to the research/design process.

## 10. Current Scope

Protocol Specification α0.1 exists to stabilize the current boundary between Foundation, Matome YAML, Protocol Loader, Runtime, Evidence, and Landscape.

It is intentionally small.
