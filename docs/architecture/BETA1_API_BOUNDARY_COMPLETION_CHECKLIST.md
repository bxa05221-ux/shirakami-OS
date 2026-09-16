# β1.0 API Boundary Completion Checklist

Status: verification checklist for the current β1.0 prototype baseline.

The frozen external API boundary remains `POST /observe`.

## Confirmed scope

- External boundary remains limited to `POST /observe`.
- Required request fields are `landscape_id` and object-shaped `input`.
- Invalid request-body forms are normalized to HTTP 400.
- Response invariants are validated by the API implementation.
- OpenAPI describes the implemented response contract.
- `evidence_id` remains nullable and is not manufactured by the API.
- `protocol_id` remains an explicit client reference.

## Verified invalid-input classes

Covered at TestClient and separately launched `uvicorn` process boundaries where applicable:

- missing or empty `landscape_id`
- non-object `input`
- non-object top-level body
- malformed JSON
- empty body

## Required Submission Check

Before declaring a change complete:

1. Confirm target and base branches.
2. Confirm the diff contains only intended changes.
3. Confirm CI corresponds to the current head SHA.
4. Distinguish submitted, merged, and canonicalized states.
5. Confirm the merge commit and `main` branch.
6. Retrieve and inspect the changed artifact from `main` after merge.

## Explicitly out of scope

Authentication, persistent Evidence storage, production deployment, rate limiting, full Protocol execution over HTTP, provider-specific AI invocation, and new `/chat`, `/generate`, `/agent`, or `/diagnostic` endpoints require separate decisions.

## Principle

Passing tests verifies tested behavior. It does not alone verify correct delivery to the canonical branch.
