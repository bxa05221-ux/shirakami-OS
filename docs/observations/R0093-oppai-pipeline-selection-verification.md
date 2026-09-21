# R0093 — OPPAI Pipeline Selection Contract Verification

## Purpose

Verify the OPPAI Pipeline Selection Contract against the current implementation without changing Runtime semantics.

## Verified

1. `ProtocolRegistry.list_current_candidates()` can expose multiple non-archived Protocol artifacts.
2. `ProtocolRegistry.select_current(protocol_id)` resolves a selected Protocol.
3. `ProtocolAPI.build_protocol_request()` converts a resolved Protocol into `ProtocolRequest`.
4. `RouteMap.next_protocols()` and `can_transition()` expose declared reachable Protocol IDs.
5. The existing ProtocolRequest → Runtime path remains independently available.

## Gap A — Pipeline identity is not yet a runtime concept

The proposed contract introduces `pipeline_id`, but the current `RegistryEntry` and `ProtocolRequest` contain no pipeline field.

Therefore the contract currently describes a semantic distinction that is not represented by the implementation.

Classification: SEMANTIC-MAPPING-GAP.

Do not add `pipeline_id` to Runtime structures until the meaning and ownership of Pipeline are confirmed.

## Gap B — OPPAI still bypasses ProtocolRequest

`runtime/oppai_runtime_flow.py` currently accepts a protocol string and calls:

`runtime_adapter(canonical_prompt, protocol)`

It does not call `ProtocolRegistry`, `build_protocol_request()`, or the canonical ProtocolRequest → Runtime boundary.

Classification: IMPLEMENTATION-CONNECTION-GAP.

## Gap C — RouteMap does not currently constrain selection

`RouteMap.can_transition()` can test a declared edge, but `ProtocolAPI.build_protocol_request()` does not receive a RouteMap and does not enforce route reachability.

`record_transition()` records a dispatch after the fact and may add an observed destination.

Therefore RouteMap is currently an observation/route structure, not an authoritative OPPAI selection constraint.

Classification: CONTRACT-BOUNDARY-GAP.

## Gap D — Human Gate is conceptual only

The proposed contract requires Human Gate authority for unresolved Protocol selection, but no corresponding implementation boundary currently exists between OPPAI candidate discovery and ProtocolRequest construction.

Classification: SEMANTIC-MAPPING-GAP.

## Result

The hypothesis that OPPAI is a Protocol Pipeline selection boundary is supported by the repository architecture, especially the existing OPPAI Runtime Position document. However, the implementation does not yet establish Pipeline as an independent runtime object or connect OPPAI to the canonical ProtocolRequest path.

The next implementation step should therefore NOT be a broad Runtime rewrite.

The smallest useful experiment is:

Natural Language
→ OPPAI observation
→ candidate Protocol IDs
→ explicit selected Protocol
→ existing ProtocolRegistry
→ existing ProtocolRequest
→ existing Runtime

Pipeline/backend selection should remain an adapter-side experiment until its contract is separately established.

## Non-goals

- no ProtocolRegistry redesign
- no Evidence schema change
- no automatic Protocol selection
- no model/vendor ranking
- no new Pipeline runtime object
