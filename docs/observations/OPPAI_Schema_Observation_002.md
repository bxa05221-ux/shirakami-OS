# OPPAI Schema Observation 002

## Status

Observational hypothesis. Not a formal Shirakami OS specification.

## Source-derived observation

Existing Shirakami OS design material already establishes several structures that are relevant to the current OPPAI Schema hypothesis:

- Landscape is the center of the architecture; AI and Runtime serve the Landscape.
- Matome YAML is treated as Protocol IR.
- Evidence records observable Transitions and is preserved without rewriting.
- The development loop is explicitly Human Question → Matome Protocol → Runtime Implementation → External AI Review → Independent Criticism → Experiment → Evidence → Architecture Revision.
- The Runtime is not the authority for Domain Semantic Truth or the human's final judgment.
- The anmon_layer_reverse protocol explicitly preserves questions between surface behavior and interpretation and includes the rule "わかったつもりを禁止する".
- 3D-PRUIM is described as judgment preprocessing / thought assistance, while anmon_layer is its safety valve for avoiding premature fixation of meaning.

These structures are documented in the existing Foundation material and are therefore treated here as prior architecture, not newly introduced theory.

## Current hypothesis

The OPPAI Schema hypothesis may be understood as an input-boundary application of existing Shirakami principles:

Human natural input
→ observation / listening
→ context and intent candidates
→ uncertainty / unresolved questions
→ Protocol / Matome IR
→ AI backend

The hypothesis is not that OPPAI is identical to the anmon layer. The narrower observation is that both preserve uncertainty and prevent premature semantic closure before subsequent processing.

## Architectural correspondence

| Existing structure | Relevant property | OPPAI hypothesis |
|---|---|---|
| anmon_layer_reverse | preserve questions; prohibit premature certainty | preserve uncertainty / unresolved input meaning |
| 3D-PRUIM | preprocessing before judgment | preprocessing before AI interpretation |
| Matome YAML | Protocol IR boundary | candidate representation for mediated input |
| Evidence | preserve observable transitions | preserve interpretation / correction lineage as evidence candidate |
| Landscape | human-centered persistent environment | user context remains primary over model interpretation |
| Development Loop | experiment before assertion | OPPAI remains hypothesis until tested |

## Important distinction

This document does not establish that OPPAI Schema improves model performance.

It records a stronger but narrower observation:

> The existing Shirakami architecture already contains the conceptual ingredients required for a mediated input boundary, and OPPAI can be tested as an application of those existing principles rather than as an unrelated new theory.

## Next experiment

Run a multi-turn comparison of:

1. Raw natural input
2. Human-engineered prompt input
3. Protocol/Schema-mediated input

Measure:

- intent misinterpretation
- context loss
- premature semantic closure
- disappearance of unresolved questions
- correction count
- continuity across turns
- whether prior evidence changes subsequent interpretation

Do not treat a positive result as proof of general superiority. Record the result as Evidence and determine whether a formal protocol change is justified.
