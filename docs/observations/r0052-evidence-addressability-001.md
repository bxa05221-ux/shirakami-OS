# R0052 — Evidence Addressability Observation

## Question

Can multiple Evidence records remain separately addressable in the existing LandscapeState while the current Landscape snapshot remains distinct from Evidence lineage?

## Change

Add one deterministic boundary test using the existing Runtime, Evidence, and LandscapeState contracts. Two distinct Protocol identities produce separate Evidence records carrying the same explicitly supplied interpretation-like payload, and both records are applied to one LandscapeState.

## Verification boundary

Multiple Evidence records → LandscapeState evidence collection + current state snapshot

## Verification

- Evidence A and Evidence B remain separate records after sequential application.
- Their Protocol provenance remains separately addressable by position in the existing `LandscapeState.evidence` collection.
- The identical external interpretation-like payload does not merge the Evidence records.
- The current Landscape snapshot reflects the latest applied transition data.
- The current snapshot does not replace or reconstruct the stored Evidence records.

## Non-goals

- Interpretation schema
- Interpretation lineage
- Provenance Graph
- Evidence lineage reconstruction
- semantic equivalence
- artifact reconciliation
- universal Adapter interoperability
- Runtime theory changes

## Result boundary

A passing test demonstrates only this current implementation boundary: multiple Evidence records can remain separately addressable in the existing `LandscapeState.evidence` collection while the current state snapshot remains a separate view of the latest applied transition.

It does not establish a general Evidence query/indexing system or complete lineage reconstruction.

## Architectural boundary

```text
Evidence A ─┐
            ├→ LandscapeState.evidence
Evidence B ─┘

LandscapeState.snapshot()
        ≠
Evidence lineage
```

R0052 therefore observes addressability using the existing contract without introducing a new Evidence-management subsystem.
