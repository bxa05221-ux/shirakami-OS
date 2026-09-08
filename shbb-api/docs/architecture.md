# Shirakami API Architecture

## Boundary

`shbb-api` is an external interface over the existing Shirakami OS β1.0 Runtime.

```text
Landscape
   ↓
Evidence
   ↓
Protocol
   ↓
Runtime
   ↓
Adapter
   ↓
Backend
```

The API sits at the Runtime boundary:

```text
Client
   ↓ HTTP
Shirakami API
   ↓
Runtime
   ├── Observe Landscape
   ├── Capture Evidence
   ├── Resolve / apply Protocol
   └── Perform State Transition
   ↓
Adapter
```

## First endpoint

### `POST /observe`

The endpoint exposes observation as the first stable external operation.

It accepts:

- `landscape_id` — target Landscape
- `input` — observable client input
- optional `protocol_id` — explicit protocol reference
- optional `metadata` — client metadata

It may return:

- observation state
- observation identifier
- Evidence identifier when produced
- Protocol reference when applicable
- execution provenance when available

## Responsibility boundary

| Layer | Responsibility |
|---|---|
| Client | Supply input and consume result |
| API | Validate/transport the external contract |
| Runtime | Execute observation and state handling |
| Landscape | Maintain observable continuity |
| Evidence | Preserve observable transitions |
| Protocol | Define domain meaning and applicability |
| Adapter | Connect replaceable external AI/services |
| Backend | External persistence/service boundary |

The API does not become the semantic authority merely because it is externally visible.

## Extension rule

Future endpoints such as transition, evidence retrieval, protocol resolution, and execution should only be added when their existing Runtime responsibility and verification boundary are clear.

Do not add endpoints merely because a Runtime capability exists. Each new endpoint requires a defined contract and verification.
