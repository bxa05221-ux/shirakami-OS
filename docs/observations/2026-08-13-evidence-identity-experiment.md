# Evidence Identity Experiment

## Purpose

Verify whether the same immutable Evidence record can support different Landscape projections or interpretations without modifying the Evidence itself.

## Current hypothesis

Evidence is a frozen record of a confidence-bearing observation.

The record is immutable, while its interpretation and projection into a Landscape may change as additional observations become available.

## Existing implementation boundary

`runtime/evidence.py` currently represents `EvidenceRecord` as a frozen dataclass. Its transition data is protected by a read-only mapping wrapper, while `runtime/landscape.py` applies transition evidence to mutable Landscape State.

## Experiment

Given one `EvidenceRecord X`:

- Observation Point A consumes X and produces Projection A.
- Observation Point B consumes the same X and produces Projection B.
- X must remain unchanged.
- Projection A and Projection B may differ.
- A later observation may produce a new Evidence record without rewriting X.

## Verification criteria

1. Evidence identity is preserved across consumers.
2. Evidence contents are not mutated during projection.
3. Different consumers may derive different projections from the same Evidence.
4. A new observation produces new Evidence rather than rewriting previous Evidence.
5. Existing β0.1 Evidence and Landscape boundaries remain valid.

## Non-goals

- Do not add fields to `EvidenceRecord` yet.
- Do not define Evidence persistence.
- Do not formalize a three-state model.
- Do not introduce temperature as a causal quantity.
- Do not change the Foundation contract based on this experiment alone.

## Interpretation rule

A successful experiment supports the following provisional distinction:

> Evidence is immutable as a record; its interpretation and Landscape projection are not necessarily immutable.

This is an observation target, not yet a Foundation-level contract.
