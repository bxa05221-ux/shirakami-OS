# Shirakami API

Shirakami OS β1.0 の外部API境界を定義する最小構成です。

## Position

このAPIは、既存Runtimeの責務を外部から利用可能にするための契約です。
新しい理論やDomain LogicをAPI層に追加しません。

```text
Client
  ↓
Shirakami API
  ↓
Runtime
  ├─ Landscape
  ├─ Evidence
  ├─ Protocol
  └─ State Transition
  ↓
Adapter
  ↓
External AI / Backend
```

## β0.1 scope

最初の公開境界は `POST /observe` のみとします。

```text
POST /observe
```

入力としてLandscape IDと観測対象を受け取り、Runtimeによる観測結果と、利用可能なEvidence / provenanceを返します。

## Design rules

- Landscape is the continuity boundary.
- Evidence is preserved, not rewritten.
- Protocol remains the semantic authority.
- Runtime executes and observes; it does not invent domain theory.
- Adapter is replaceable.
- AI self-report is not verification evidence by itself.
- Unverified behavior is not reported as successful.

## Files

- `openapi.yaml` — API contract
- `docs/architecture.md` — mapping between API and β1.0 architecture
- `examples/observe.json` — minimal request example

## Status

`experimental / implementation candidate`

This is an API boundary extracted from the β1.0 Runtime. It is not yet a claim of production readiness.
