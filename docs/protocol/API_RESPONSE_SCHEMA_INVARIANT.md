# Shirakami `/observe` Response Schema Invariant v0.1

Status: **implementation verification — β1.0 external API boundary**

This document records the implementation-side invariant for the already frozen `POST /observe` response contract.

## Purpose

The OpenAPI contract defines the external boundary. This invariant adds runtime validation so the implementation does not silently return a malformed successful response.

It does not expand the API and does not change the frozen `/observe` contract.

## Invariant

A successful `/observe` implementation result is validated as:

- `landscape_id`: string
- `observation_id`: 16 lowercase hexadecimal characters
- `state`: `observed`
- `evidence_id`: nullable string
- `protocol_id`: nullable string
- `result`: object
- `provenance.runtime`: string
- `provenance.transition`: boolean

## Boundary rule

This is an implementation invariant, not a new external endpoint or a new semantic layer.

The API continues to expose only:

```text
POST /observe
```

The existing contract remains the external source of truth; this invariant makes the implementation conform to the response it already claims to return.

## Verification

The invariant is checked in `shbb-api/app.py` and exercised by `tests/test_shbb_api.py`.

The test suite verifies both:

1. a real `/observe` response satisfies the schema;
2. invalid state and invalid observation identifiers are rejected by the schema.
