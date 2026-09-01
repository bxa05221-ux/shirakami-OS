# MTM Protocol — Compatibility-Oriented Protocol Format

Status: experimental
Version: 0.1

## 1. Purpose

MTM Protocol (的目 Protocol) defines a compatibility-oriented way to carry Shirakami Protocol definitions across Runtime generations.

The purpose is not to replace existing Protocol formats immediately. Existing formats may be normalized into a common Runtime representation through compatibility adapters.

## 2. Architectural position

Landscape is the center.

Protocol governs observable transitions.
Runtime executes Protocol-defined transitions.
Adapters translate between external systems and the Landscape.
Evidence records observable state changes.

MTM therefore describes a Protocol at the boundary between human-readable intent and Runtime execution. The Runtime must not acquire Domain Semantic Authority merely by loading an MTM document.

## 3. Canonical compatibility boundary

```text
Protocol Document
      |
      v
Format / Version Detection
      |
      v
Compatibility Adapter
      |
      v
Current Protocol Representation
      |
      v
Shirakami Runtime
```

The internal Runtime representation remains singular even when input formats are multiple.

## 4. Common envelope

An MTM-compatible Protocol SHOULD expose the following semantic areas:

- identity: protocol id, name, version, status
- purpose: why the Protocol exists
- principles: declared operating principles
- participants: participants and their declared responsibilities/authority
- learning_cycle: observable phases or progression, when applicable
- evidence: evidence distinctions and preservation rules, when applicable
- rules: explicit constraints and prohibitions, when applicable

A format MAY omit areas that are not applicable. Compatibility adapters MUST preserve available information and MUST NOT invent domain facts.

## 5. Compatibility rule

Backward compatibility is preferred over format replacement.

A legacy document may be accepted when an adapter can normalize it without changing its declared meaning.

The adapter MAY:

- rename equivalent structural fields
- wrap legacy fields in the common envelope
- derive a stable protocol identifier from an explicitly declared title when no identifier exists
- preserve unknown fields for later processing when safe

The adapter MUST NOT:

- invent missing domain meaning
- convert interpretation into fact
- silently overwrite declared values
- make regional, human, or domain decisions
- discard evidence lineage when it is explicitly present

## 6. Versioning

Protocol version and loader/adapter version are separate concepts.

```text
Protocol version  !=  Runtime version  !=  Adapter version
```

A Runtime may support multiple Protocol versions through adapters.

Breaking changes to the common MTM envelope require an explicit compatibility decision rather than an implicit parser change.

## 7. Runtime boundary

Runtime responsibilities remain limited to structural validation, permission validation, applicability checks, execution of declared transitions, and recording observable results.

Runtime does not own Landscape, Protocol meaning, Domain truth, or human judgment.

This preserves the existing Runtime boundary established by the Shirakami architecture.

## 8. Conformance direction

An MTM-compatible implementation should eventually provide conformance tests for:

1. identity preservation
2. purpose preservation
3. principles preservation
4. participant preservation
5. transition/learning-cycle preservation
6. evidence-rule preservation
7. unknown-field handling
8. legacy-format normalization
9. rejection of semantic invention

The exact conformance suite is intentionally deferred until implementation evidence is sufficient.

## 9. Relationship to existing Matome YAML

"Matome YAML" remains a valid historical/runtime input format where already supported.

MTM Protocol is the compatibility-oriented specification boundary; it does not require immediate migration of existing documents.

Existing Matome YAML and newer Protocol YAML can coexist behind the compatibility layer.

## 10. Design principle

> Standardize the boundary, not the Landscape.

> Preserve continuity while allowing Protocol formats to evolve.

The goal is not homogenization. The goal is that rapidly evolving Protocol documents can continue to be executed by a stable Runtime without losing their declared intent.

## 11. Source alignment

This specification is an implementation-side consolidation of existing Shirakami architecture material. It does not introduce a new cognitive theory. Questions about the theoretical meaning of MTM remain subject to future research and validation.
