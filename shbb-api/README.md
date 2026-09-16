# Shirakami API

Shirakami OS β1.0 の外部API境界を定義する最小構成です。

## Position

このAPIは、既存Runtimeの責務を外部から利用可能にするための最小契約です。
新しい理論やDomain LogicをAPI層に追加しません。

```text
Client
  ↓
POST /observe
  ↓
Shirakami Runtime
  └─ Landscape observation
  ↓
Observable response
```

## β1.0 scope

現在の公開境界は `POST /observe` のみです。

```text
POST /observe
```

入力としてLandscape IDと観測対象を受け取り、Runtimeによる観測結果を返します。
`protocol_id` は明示的に指定されたProtocol参照として保持され、`metadata` はクライアントメタデータとして扱われます。

## Design rules

- Landscape is the continuity boundary.
- Evidence is preserved, not rewritten.
- Protocol remains the semantic authority.
- Runtime executes and observes; it does not invent domain theory.
- Adapter is replaceable.
- AI self-report is not verification evidence by itself.
- Unverified behavior is not reported as successful.
- `/observe` does not claim a state transition; `provenance.transition` is `false`.
- `evidence_id` may remain `null`; the API does not manufacture Evidence.

## Files

- `openapi.yaml` — API contract
- `docs/architecture.md` — mapping between API and β1.0 architecture
- `examples/observe.json` — minimal request example

## Status

`β1.0 boundary candidate / prototype baseline`

The external contract is frozen for the current PV1.0 baseline. This is not a claim of production readiness or feature completeness.
