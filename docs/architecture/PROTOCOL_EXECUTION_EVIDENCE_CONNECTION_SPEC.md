# Protocol Execution / Evidence Connection Specification

Status: proposal for β1.0 Runtime follow-up.

This document defines a candidate connection from Matome YAML through ProtocolIR, Registry selection, the protocol bridge, Runtime execution, ExecutionResult, and immutable EvidenceRecord. It does not change Runtime behavior, Protocol semantics, or the external HTTP API.

## Invariants

- ProtocolIR remains the semantic handoff representation for the β0.1 Matome subset.
- Registry lifecycle rules remain authoritative.
- The bridge adds no domain meaning.
- Evidence is immutable after creation.
- Existing prepared-snapshot behavior is not silently replaced.
- POST /observe remains observation-only.
- No automatic natural-language-to-Protocol generation.
- No unification of protocol_loader.py and protocol_loader_v2.py.

## Verification required

Tests must cover ProtocolIR → bridge → Runtime → ExecutionResult → EvidenceRecord, Registry lifecycle preservation, and preservation of the existing prepared-snapshot path. Post-merge inspection of main is required.

## Adoption

Implementation must be a separate change after this specification is reviewed and accepted. Until then, this file records the intended boundary only.
