# API Architecture Audit Note

## Scope

This note records the verified β1.0 `shbb-api` boundary as implemented on `main`.

## Verified current behavior

- The only public endpoint is `POST /observe`.
- The request requires a non-empty `landscape_id` and an object-valued `input`.
- `protocol_id` is preserved as a client-supplied reference when present.
- `metadata` is accepted as client metadata and is not included in the Runtime observation snapshot.
- The response state is `observed`.
- `provenance.transition` is always `false` for this boundary.
- `evidence_id` is nullable and the endpoint does not manufacture Evidence.
- Malformed JSON, an empty body, non-object bodies, and invalid request fields are normalized to HTTP 400.

## Explicit non-claims

The current endpoint does **not** claim to:

- perform a state transition;
- persist or create Evidence;
- resolve or execute Protocol semantics;
- invoke a provider-specific AI backend;
- expose chat, generation, agent, or diagnostic endpoints;
- provide production readiness or complete Runtime functionality.

## Audit finding

The former architecture description listed capture, Protocol resolution/application, and state transition as Runtime actions in the API request flow. Those are broader architectural capabilities, not verified behavior of the current minimal `POST /observe` implementation. The canonical description should therefore distinguish the broader Runtime architecture from the currently exposed observation-only boundary.

## Verification boundary

This note is documentation-only. Behavioral verification remains represented by the existing API tests and CI checks. Passing tests and successful CI do not, by themselves, establish that a change was delivered to the canonical `main` branch; post-merge inspection is required.
