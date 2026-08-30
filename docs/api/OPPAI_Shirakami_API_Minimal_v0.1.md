# OPPAI-Shirakami API Minimal Specification v0.1

Status: implementation specification

## 1. Purpose

Provide a minimal, model-independent API boundary through which a human can communicate naturally while Shirakami Runtime handles context, protocol processing, and model adaptation.

The API does not attempt to make the downstream model intrinsically more capable. Its purpose is to preserve the human's natural operating method while allowing the downstream model to be replaced.

## 2. Boundary

```text
Human
  ↓
OPPAI
  ↓
Shirakami Runtime
  ↓
Model Adapter
  ↓
LLM / AI Model
```

The downstream model is an implementation detail of the Runtime boundary.

## 3. Minimal endpoint

`POST /v1/chat`

### Request

```json
{
  "input": "自然な会話をそのまま送る",
  "context": {},
  "session_id": "optional-session-id"
}
```

### Request fields

- `input` — required string. The user's natural-language input. It must not require prompt-engineering syntax.
- `context` — optional object. Caller-supplied context available to the Runtime.
- `session_id` — optional string. Identifies a continuing conversation.

## 4. Processing contract

The Runtime MUST:

1. accept natural user language without requiring a special prompt format;
2. preserve relevant conversational context;
3. distinguish user input from Runtime inference;
4. avoid silently converting uncertainty into fact;
5. ask for clarification only when required for safe or meaningful execution;
6. pass the normalized request to a Model Adapter;
7. allow the Model Adapter to be replaced without changing the human-facing API.

The Runtime MUST NOT require the user to learn the internal OPPAI representation.

## 5. Response

```json
{
  "response": "model response",
  "session_id": "session-id",
  "context_delta": {},
  "status": "ok"
}
```

### Response fields

- `response` — generated response or Runtime clarification.
- `session_id` — session identifier when a session is used.
- `context_delta` — optional changes to the Runtime-managed conversational context.
- `status` — minimal processing status.

## 6. OPPAI boundary

OPPAI is logically responsible for the following concerns:

- Listener
- Context Preservation
- Intent Separation
- Clarification
- Canonicalization
- Execution
- Evidence boundary

These responsibilities do not require seven public API endpoints. They are internal protocol responsibilities behind the single conversational boundary.

## 7. Model independence

The API MUST NOT expose model-specific interaction requirements to the human caller.

A caller should not need a different prompt style merely because the Runtime changes from one model adapter to another.

```text
same human input
       ↓
     OPPAI
       ↓
   Runtime
    ↙   ↓   ↘
 model A B model C
```

## 8. Error handling

The minimal implementation should distinguish at least:

- invalid request
- unavailable model adapter
- Runtime processing failure
- clarification required

The API should return an explicit status rather than silently fabricating a successful response.

## 9. Non-goals

Version 0.1 does not define:

- a vendor-specific authentication scheme
- streaming
- tool calling
- billing
- model routing policy
- persistent long-term memory
- a universal quality score
- a claim of model-performance equivalence

Those concerns remain outside the minimal boundary until implementation requires them.

## 10. Design principle

> The human should operate the conversation, not the model.

The API is successful when the caller can think and speak naturally while the Runtime absorbs the operational differences between downstream models.

## 11. Implementation status

This specification is intended to be implemented against the existing Shirakami Runtime and Model Adapter boundary. It is deliberately minimal so that real usage can determine which additional contracts are actually necessary.
