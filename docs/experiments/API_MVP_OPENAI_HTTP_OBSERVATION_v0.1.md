# Shirakami API MVP — OpenAI HTTP Observation v0.1

## Purpose

Verify a real OpenAI Responses API call inside Shirakami's HTTP execution path:

`HTTP /v1/execute → async provider adapter → OpenAI Responses API → Runtime → Evidence → Trace → AIwitness → verification`

This is separate from the direct model observation experiment. A successful direct API call alone does not satisfy the HTTP provider gate.

## Run

The workflow is `.github/workflows/openai-http-observation.yml`.

Required repository Actions secrets:

- `OPENAI_API_KEY` — OpenAI API key.
- `OPENAI_MODEL` — model identifier accepted by the OpenAI Responses API.

Run the workflow manually, or push a change to the dedicated feature branch. The script fails closed when either secret is absent; it does not silently switch to a fixture.

## Acceptance markers

A passing live run must emit:

- `LIVE_PROVIDER_OBSERVED=true`
- `BOUNDARY_OBSERVED=true`
- `TRACEABILITY_VALID=true`
- `VERIFICATION_STATUS=pass`
- `MODEL_OUTPUT_NONEMPTY=true`

It retrieves linked Evidence, Trace, and AIwitness through the HTTP API and checks that they refer to the same Evidence ID and preserve a passing verification result.

## Security and authority boundary

- The API key is read from the environment and never printed or placed into Evidence/Trace.
- The response is reduced to output text and non-secret trace metadata; encrypted reasoning payloads are not copied into the artifact.
- `execution_authorized`, `publish_authorized`, and `merge_authorized` must remain false.
- `human_gate_required` must remain true.
- The script makes an explicit harness approval request to exercise the approval boundary. This is a test harness action, not production identity verification or an interactive human approval UI.

## Scope

This validates one live-provider path using the in-process HTTP test client. It does not by itself prove deployment behind a public network server, production authentication/authorization, multi-user isolation, or durable external persistence. Those are separate production-hardening concerns.
