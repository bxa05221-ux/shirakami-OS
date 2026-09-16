# β1.0 API Empty-Body Verification Note

Status: **implementation verification — β1.0 external API boundary**

The frozen external boundary remains `POST /observe`.

## Scope

An HTTP request with an empty body and `Content-Type: application/json` is an invalid observation request and is expected to return HTTP 400.

## Verification boundary

The behavior is covered at both levels:

- FastAPI TestClient
- independently launched `uvicorn` HTTP process

This verifies the behavior at the HTTP process boundary rather than only inside the application test client.

## Non-scope

This note does not introduce a new endpoint, expand the response contract, change Protocol semantics, manufacture Evidence, or invoke a provider-specific AI service.
