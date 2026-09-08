# R0050 — Provenance Separation Observation

## Question

When Evidence records from different Protocol identities carry the same external interpretation-like payload, does the current Runtime/Adapter boundary keep their provenance distinct?

## Change

Add one deterministic boundary test using the existing Runtime, Evidence, and Landscape Adapter contracts. Two distinct Protocol identities receive the same interpretation-like payload and are captured as separate Evidence records.

## Verification boundary

Same external interpretation-like payload → separate Evidence provenance → Landscape Adapter

## Verification

- Evidence A and Evidence B remain separate records.
- Protocol A and Protocol B remain separately identifiable as Evidence provenance.
- The same external interpretation-like payload may be present in both Evidence records without making their provenance identical.
- The Landscape Adapter can carry the same payload for independently produced Evidence records.
- No semantic reconciliation or truth judgment is performed.

## Non-goals

- Interpretation schema
- Interpretation lineage model
- Provenance Graph
- semantic equivalence
- artifact reconciliation
- Evidence lineage reconstruction
- Runtime theory changes

## Result boundary

A passing test demonstrates only this minimal boundary: identical external interpretation-like payload does not imply identical Evidence provenance when the Evidence records originate from distinct Protocol identities. It does not establish semantic equivalence, Interpretation authority, or complete provenance reconstruction.

## Architectural boundary

Same payload
    ≠
Same Evidence provenance

Protocol A → Evidence A → Landscape Adapter
Protocol B → Evidence B → Landscape Adapter

R0050 therefore observes provenance separation without creating or reconciling Interpretation semantics.
