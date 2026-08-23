# Specification Transition Status

## Purpose

This file makes the current boundary between Canonical, Archive, and Experimental specification material explicit inside the reference implementation repository.

## Canonical

Stable normative specifications are maintained in `shirakami-specification`.

- Plugin Classification
- Plugin Contract
- Plugin Lifecycle Contract
- Runtime Lifecycle Contract
- Contract Layer Overview
- Protocol Specification α0.1
- Adapter Contract α0.1

## Archive / Transition

The following implementation-side files are retained temporarily for provenance and migration context:

- `spec/protocol.md` → `shirakami-specification/protocols/PROTOCOL_SPECIFICATION_ALPHA_0_1.md`
- `spec/adapter-contract.md` → `shirakami-specification/contracts/ADAPTER_CONTRACT_ALPHA_0_1.md`
- `docs/rfc/RFC-0001_Plugin_Classification.md` → promoted specification
- `docs/rfc/RFC-0002_Plugin_Lifecycle.md` → promoted specification
- `docs/rfc/RFC-0003_Runtime_Lifecycle.md` → promoted specification
- `docs/rfc/RFC-0004_Plugin_Contract.md` → promoted specification
- `docs/rfc/RFC-0005_Contract_Layer_Overview.md` → promoted specification

These files should not be used as the canonical source for new normative references.

## Experimental

- `spec/manual-rendering.md` — Public Alpha UI/documentation adapter; explicitly not part of the core Runtime Contract.

The document itself states that it is experimental and should not be treated as a finalized architectural specification.

## Removal Rule

No legacy file is deleted solely because a specification has been promoted.

Deletion or archival should occur only after repository references have been migrated and provenance remains recoverable.

## Boundary Rule

```text
Canonical     = what implementations are expected to preserve
Archive       = what explains how the current contract came to exist
Experimental  = what is being observed before it becomes a contract
```

The distinction is more important than the directory name.
