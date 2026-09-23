# Context Lineage E2E v0.1

## Objective

Verify that a request-scoped Context Bundle remains traceable from API admission through Backend execution to the final EvidenceRecord.

## Boundary

`HTTP/API request → Context Routing → Evidence Resolver → Context Bundle → Evolution Runtime → Backend → Evidence`

## Required lineage

- `request_id`
- `evidence_ids`
- `protocol_ids`
- `runtime_ids`

## Invariants

- Evidence IDs remain in the selected order.
- Unrequested Evidence is not admitted.
- The Evidence store is not passed to the Backend.
- Context lineage is copied into observed Evidence.
- Backend output becomes Evidence, not Decision.
- Evidence explicitly records that authority was not inferred.

## Freeze criterion

The Context-to-Evidence lineage is considered verified for v0.1 when the E2E test passes and the existing Runtime verification suite remains green.
