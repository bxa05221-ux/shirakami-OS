# R0092 OPPAI Connection Architecture Map

## Purpose

Record the implementation-side connection structure suggested by the existing β1.0 contracts, without introducing a new Protocol semantic or connection contract.

## Source-backed current structure

The existing implementation provides these independently verified boundaries:

```text
Human input
  ↓
OPPAI /v1/chat
  ↓
OPPAI runtime preparation / observation
```

and:

```text
Protocol Registry
  ↓
ProtocolRequest
  ↓
Protocol API invocation
  ↓
Runtime
  ↓
ExecutionResult
  ↓
EvidenceRecord
  ↓
LandscapeState
```

The existing Protocol-to-Runtime bridge is a thin implementation bridge and is intended to preserve Runtime boundaries without adding Protocol semantics.

## Working architecture map

The implementation-side composition can therefore be represented as:

```text
                         Human
                           │
                           ▼
                    ┌─────────────┐
                    │    OPPAI    │
                    │ input/context│
                    │ observation │
                    └──────┬──────┘
                           │
                    [UNKNOWN GAP]
                           │
                           ▼
                    Protocol API
                           │
                    ProtocolRequest
                           │
                           ▼
                  Protocol Runtime Bridge
                           │
                           ▼
                        Runtime
                           │
                 Observable execution
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       External Adapter             Evidence
              │                         │
              ▼                         ▼
        AI / external tool          Landscape
```

This diagram is an implementation map, not a new contract.

## Responsibility hypothesis to be verified

The following labels describe the role already suggested by the current implementation. They are not new semantic authority:

- OPPAI: human-facing input and observation boundary.
- Protocol API: Protocol resolution and parameterized invocation boundary.
- Protocol Runtime Bridge: structural bridge into the existing Runtime vertical slice.
- Runtime: execution and observable state-transition boundary.
- Adapter: replaceable external AI/tool/backend connection.
- Evidence: preservation of observable execution information.
- Landscape: resulting state representation.

## Explicit UNKNOWN boundaries

The following remain unresolved and must not be implemented by inference:

1. Ownership of Protocol selection between OPPAI and Protocol API/Registry.
2. The formal relationship between OPPAI's current runtime adapter and the Runtime Executor/Adapter boundary.
3. The formal mapping, if any, between OPPAI Observation/evidence data and `EvidenceRecord`.

## Direction

If these boundaries are later supplied as formal contracts, implementation should connect existing boundaries with the smallest possible bridge.

Until then:

- do not create new Protocol semantics;
- do not redesign the Landscape schema;
- do not silently map OPPAI observations into EvidenceRecord;
- do not equate an external AI Adapter with a Runtime Executor without a contract;
- do not treat this architecture map as proof of end-to-end execution.

## Result meaning

R0092 records a concrete implementation hypothesis derived from existing code and prior verification. It does not establish that the UNKNOWN boundaries are resolved.
