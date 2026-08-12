# Shirakami Runtime API α0.1

## Status

Experimental Public Alpha API.

This API exposes the existing Protocol IR → Runtime vertical slice for external observation and integration testing.

## Endpoints

### `GET /health`

Returns:

```json
{"status":"ok","version":"0.1.0"}
```

### `POST /v0.1/execute`

Request:

```json
{
  "protocol": {
    "matome": {
      "title": "Example",
      "version": "0.1"
    }
  },
  "operation": "echo",
  "input": {"example": "landscape"}
}
```

Response:

```json
{
  "protocol": {
    "title": "Example",
    "version": "0.1"
  },
  "success": true,
  "event": "execution.completed",
  "output": {"example": "landscape"},
  "error": null
}
```

## Scope

α0.1 intentionally exposes only an `echo` transition. It exists to verify the API boundary, not to define the final Protocol execution language.

The API does not yet define authentication, persistence, scheduling, multi-user isolation, or production deployment requirements.

## Architecture

```text
Client
  ↓
Runtime API α0.1
  ↓
Protocol Runtime Bridge
  ↓
Runtime
  ↓
ExecutionResult / Evidence boundary
```

## Compatibility Principle

The API must remain a thin interface over the existing Runtime. API-specific semantics must not silently become Protocol or Runtime Core semantics.
