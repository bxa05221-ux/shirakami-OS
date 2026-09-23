# Backend Contract v0.1

## Boundary

`SemanticHandoff -> Backend -> BackendResponse -> EvidenceRecord`

The Backend is replaceable and transport/execution oriented. It does not create Decision authority, bypass HumanGate, or infer authority from payload metadata.

## Reference implementation

`EchoBackend` is dependency-free and exists only to prove the contract and Evolution Loop wiring. Real model/service adapters can replace it without changing the Runtime Evidence schema.

## Freeze criteria

- Backend identity is explicit.
- Response status is explicit.
- Payload is treated as observed data.
- Returned output can become immutable EvidenceRecord.
- Authority remains `not_inferred` unless separately established by the HumanGate path.
