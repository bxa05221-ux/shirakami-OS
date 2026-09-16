# β1.0 API Malformed JSON Verification Note

## Status

Verified behavior for the current β1.0 `POST /observe` boundary.

## Contract

A malformed JSON request body is an invalid request and is returned as HTTP 400.

## Verification

The behavior is covered at both verification levels:

- FastAPI `TestClient`
- a separately launched `uvicorn` HTTP process

The tests submit malformed JSON with `Content-Type: application/json` and assert HTTP 400.

## Scope

This verification does not add an endpoint, change the response contract, or expand `/observe` semantics. It closes an invalid-request handling gap at the HTTP boundary.
