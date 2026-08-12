# Shirakami Runtime API α0.1

## Status

Experimental Public Alpha API.

The API exposes the current Protocol IR → Runtime vertical slice and the minimum GitHub Adapter boundary for external observation and controlled write/read-back experiments.

## Endpoints

### `GET /health`

Returns:

```json
{"status":"ok","version":"0.1.0"}
```

### `POST /v0.1/execute`

Executes the currently supported Protocol transition.

### `POST /v0.1/github/read`

Reads a repository file through the GitHub Adapter. The API does not directly call GitHub-specific transport code; the Adapter owns that boundary.

### `POST /v0.1/github/write`

Performs a controlled write using the supplied current blob SHA and immediately reads the resulting file back through the Adapter.

A GitHub token is required by the Adapter for writes (`GITHUB_TOKEN`). The API never accepts the token as request data.

Conceptually:

```text
Client
  ↓
Runtime API
  ↓
GitHub Adapter
  ↓
GitHub Backend
  ↓
Read-back
  ↓
Evidence
```

## Safety Boundary

The controlled-write endpoint requires an existing blob SHA. This provides an optimistic concurrency boundary and prevents an unconditional replacement operation from being treated as a Runtime transition.

The adapter must retain the Backend-specific transport details. Runtime Core remains unaware of GitHub APIs.

## Scope

α0.1 is an integration proof, not a production service specification. Authentication, authorization, rate limiting, persistence, multi-user isolation, deployment, and broader Protocol execution semantics remain outside this version.
