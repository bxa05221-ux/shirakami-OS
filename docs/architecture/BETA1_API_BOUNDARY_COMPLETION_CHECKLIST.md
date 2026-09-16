# β1.0 API Boundary Completion Checklist

Status: **verification checklist — β1.0 external API boundary**

The frozen external API boundary remains `POST /observe`.

## Completion scope

This checklist applies to the current prototype baseline. It does not authorize a new endpoint, provider-specific AI invocation, Protocol semantic expansion, or production-readiness claim.

## Contract checks

- [x] External boundary is limited to `POST /observe`.
- [x] Required request fields are `landscape_id` and object-shaped `input`.
- [x] Invalid request-body forms are normalized to HTTP 400.
- [x] Response shape is validated by the Runtime-facing API implementation.
- [x] OpenAPI describes the implemented response invariants.
- [x] `evidence_id` remains nullable and is not manufactured by the API.
- [x] `protocol_id` remains an explicit client reference and is not reinterpreted by the API.

## HTTP boundary checks

The following invalid-input classes are covered at both the FastAPI TestClient level and the separately launched `uvicorn` process boundary where applicable:

- missing `landscape_id`
- empty `landscape_id`
- non-object `input`
- non-object top-level request body
- malformed JSON
- empty request body

## Submission Check

Before declaring a change complete, verify:

1. The target branch and base branch are correct.
2. The diff contains only the intended files and behavior.
3. CI results correspond to the current head SHA.
4. The pull request state is distinguished from merge state.
5. The merge commit and `main` branch are confirmed.
6. The changed artifact is retrieved from `main` after merge.

## Remaining boundary decisions

The following are intentionally outside this checklist and require separate decisions:

- authentication and authorization
- persistent Evidence storage
- production deployment and rate limiting
- full Protocol execution over HTTP
- provider-specific AI invocation
- `/chat`, `/generate`, `/agent`, or `/diagnostic` endpoints
- physical or robotic control endpoints

## Principle

Passing tests demonstrates verified behavior for the tested scope. It does not, by itself, demonstrate that the change was correctly delivered to the canonical branch. Both verification and submission state must be checked.
