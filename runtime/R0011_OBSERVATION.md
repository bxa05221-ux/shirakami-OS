# R0011 Symbolic Recurrence Boundary Observation

Status: protocol fixture added; Runtime semantic expansion not yet implemented.

## Purpose

Verify that 象徴再帰 can cross the existing Matome YAML -> ProtocolIR -> Runtime -> Evidence boundary without requiring the Runtime to own domain meaning.

## Fixture

`protocols/manual/symbolic-recurrence-boundary.yaml`

The fixture declares four observable operations:

- preserve symbolic lineage
- carry symbolic reference as protocol data
- expose recurrence as an observable transition
- preserve recurrence lineage

## Current Runtime boundary

The β0.1 loader accepts the fixture because it uses the existing Matome subset: `title`, `version`, `statement`, and `pipeline`.

The current Runtime bridge should transport the declared pipeline as ProtocolIR data. It must not interpret `preserve_symbolic_lineage` or `carry_symbolic_reference_as_protocol_data` as domain-specific executable semantics.

## Expected observation

A successful boundary test must demonstrate:

1. the symbolic-recurrence protocol is loadable;
2. its declared pipeline survives ProtocolIR conversion;
3. Runtime execution produces an observable Transition containing the protocol declaration;
4. Evidence preserves that Transition without rewriting its declared semantics.

## Explicit non-goals

- Do not add symbolic-recognition logic to Runtime.
- Do not make Runtime understand who an "おじいちゃん" is.
- Do not create a fixed AI personality from the protocol.
- Do not introduce a new semantic DSL.
- Do not modify the existing Protocol contract merely to make the experiment pass.

## Interpretation boundary

The experiment concerns whether symbolic recurrence can be represented and transported as Landscape-relevant protocol data. Whether a particular symbolic reference should actually recur in a user-facing interaction remains a Protocol/Human Authority question and is not delegated to the generic Runtime.
