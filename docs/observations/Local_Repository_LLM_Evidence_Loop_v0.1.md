# Local Repository LLM Evidence Loop v0.1

## Purpose

Verify the minimum compositional loop that connects the already-established boundaries:

Local Repository -> ProtocolIR -> Pipeline -> Replaceable LLM Adapter -> Runtime observation -> Evidence -> Landscape

## What is verified

- one local Matome YAML remains the Protocol source artifact;
- the same Protocol produces the same PipelinePlan across backend A and backend B;
- backend identity changes only at PipelineAdapter;
- deterministic adapter output can be carried into the Runtime as explicitly labeled input observation;
- Runtime execution captures that observation as EvidenceRecord;
- transition Evidence can update LandscapeState;
- Human Gate remains explicit input and is not resolved by the Runtime.

## Important boundary

The adapter output is not treated as verified truth or authority. It becomes Evidence only because the test explicitly passes it into the Runtime as an observed input field. The Runtime does not evaluate the output.

This test therefore verifies data flow and boundary preservation, not LLM quality, truth, or semantic correctness.

## Relation to #287

This completes the deterministic minimum integration loop using replaceable backend stand-ins. Real provider adapters and external model verification remain separate work.