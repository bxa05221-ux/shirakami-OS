# Shirakami OS β1.0 Public API

## Status

Implementation contract for the β1.0 Public API.

The API is the public boundary for external applications and services to invoke Shirakami Runtime capabilities. It is not the Runtime itself and does not expose backend-specific transport semantics.

## Boundary

```text
Client
  ↓
Shirakami OS β1.0 Public API
  ↓
Runtime
  ↓
Protocol / Landscape / Evidence
  ↓
Adapter
  ↓
External Backend
```

## Principles

- Protocol First
- Landscape First
- Runtime is a service to Landscape
- Backend-specific transport remains inside Adapters
- API requests must not contain backend credentials
- Observable transitions produce evidence; evidence is preserved, not rewritten
- β1.0 is a public integration boundary, not a production SaaS specification

## v1 endpoints

### `GET /health`

Returns service health and API version.

```json
{"status":"ok","version":"1.0.0"}
```

### `POST /v1/execute`

Executes a supported Protocol transition through Runtime.

Request:

```json
{
  "protocol": {},
  "input": {}
}
```

The API accepts Protocol IR and delegates execution to Runtime. The API does not implement Protocol semantics itself.

### `POST /v1/landscape/observe`

Requests an observation of Landscape state through the appropriate Runtime/Adapter boundary.

Request:

```json
{
  "target": {},
  "context": {}
}
```

### `POST /v1/evidence/observe`

Returns evidence associated with an observable Runtime transition.

Request:

```json
{
  "transition_id": "..."
}
```

### `POST /v1/adapter/invoke`

Invokes an installed Adapter through the Runtime boundary.

Request:

```json
{
  "adapter": "...",
  "operation": "...",
  "input": {}
}
```

Backend-specific credentials and transport details remain outside the request contract.

## Compatibility

The existing α0.1 endpoints remain available during migration. β1.0 introduces the stable public boundary; existing experimental endpoints may be mapped internally without preserving their implementation structure.

## Explicitly out of scope

- Authentication protocol
- Authorization model
- Rate limiting
- Billing
- Persistence specification
- Multi-tenant isolation
- Deployment topology
- Backend-specific API semantics
- Expansion of Protocol semantics

These concerns may be addressed by later contracts without changing the β1.0 Runtime boundary.
