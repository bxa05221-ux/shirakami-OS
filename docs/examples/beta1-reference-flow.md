# Shirakami OS β1.0 Reference Application Flow

This is the smallest concrete picture of how an external application uses Shirakami OS.

## The picture

```text
User
  |
  v
Your application
  |
  | POST /v1/execute
  v
Shirakami OS β1.0 Public API
  |
  v
ShirakamiOS Runtime
  |
  +--> Protocol
  +--> Landscape
  +--> Evidence
  |
  v
Your application receives the observable result
```

The reference implementation is intentionally in-memory. It demonstrates the boundary; it is not a production persistence or authentication design.

## One concrete interaction

Imagine a small care or work-support application. A person enters:

```json
{
  "message": "hello landscape"
}
```

The application wraps that input with a Protocol reference and calls:

```http
POST /v1/execute
```

Example request:

```json
{
  "protocol": {
    "matome": {
      "title": "demo.landscape.message",
      "version": "0.1"
    }
  },
  "operation": "message",
  "input": {
    "message": "hello landscape"
  }
}
```

The response contains three things that matter to the application:

```json
{
  "status": "completed",
  "transition": {
    "kind": "landscape.message.received",
    "data": {
      "changed": true,
      "message": "hello landscape"
    }
  },
  "evidence": {
    "protocol_id": "demo.landscape.message",
    "status": "completed",
    "transition": "landscape.message.received"
  },
  "landscape": {
    "message": "hello landscape"
  }
}
```

The important point is not the demo message. The point is the direction of responsibility:

- The application owns the user-facing experience.
- Shirakami OS owns the Runtime boundary and observable Landscape transition.
- Evidence records what transition was observed.
- The application can observe the current Landscape through `POST /v1/landscape/observe`.
- The application can observe accumulated reference Evidence through `POST /v1/evidence/observe`.

## What an application developer gets

The developer does **not** need to implement the Runtime execution loop in the application.

They integrate a small public boundary:

```text
send Context
   -> execute Protocol
   -> receive Transition + Evidence + Landscape
```

This is the intended β1.0 mental model.

## What this demo does not claim

It does not yet define production authentication, authorization, persistence, multi-user isolation, billing, deployment topology, or a generic backend Adapter invocation mechanism. Those remain outside the reference flow.
