# Local Repository Runtime Evidence Boundary v0.1

## Purpose

Verify the missing vertical slice identified by the existing Runtime specification-gap observation:

Local Repository -> Protocol Loader -> Protocol IR -> Runtime -> Evidence -> Landscape

## Verified boundary

A Matome YAML file stored in a local repository checkout can be:

1. loaded by the existing `LocalRepositoryProtocolLoader`;
2. parsed into the existing `ProtocolIR`;
3. bridged into the existing Runtime callable boundary;
4. executed by the existing Runtime;
5. captured as immutable `EvidenceRecord`;
6. applied to the current `LandscapeState`.

The implementation is composition only. It does not add domain semantics, select a provider, or treat model output as authoritative.

## Verification scope

This is a deterministic boundary test. It does not prove:

- Git synchronization;
- GitHub authentication or mutation;
- external LLM compatibility;
- model quality;
- semantic correctness of a Protocol;
- Human Gate completion.

`human_gate: pending` remains observable input data; the Runtime does not resolve it.

## Relation to #287

This closes the Local Repository -> ProtocolIR -> Runtime -> Evidence -> Landscape portion of the minimum integration path.

The replaceable LLM boundary remains separately verified by PR #422.
