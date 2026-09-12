# 白神ラジオ — Language UI MVP

## Purpose

白神Runtime β1.0を第三者が体験できる最小の利用者入口を用意する。

このMVPは、新しい理論やRuntime意味論を追加するものではない。既存のProtocol / Runtime / Adapter / Renderer境界を前提に、利用者向けUIを先に切り出す。

## User path

```text
User
  ↓
Shirakami Radio Language UI
  ↓
Language Protocol / input boundary
  ↓
Shirakami Runtime
  ↓
Adapter
  ↓
External AI (future connection)
  ↓
Radio Renderer
  ↓
User
```

## MVP implementation

`examples/shirakami_radio_ui/index.html` is a dependency-free static UI.

It provides:

- Japanese conversation entry
- simple conversation display
- demo-mode response for UI testing
- optional Runtime endpoint field for operator testing
- explicit indication when no Runtime endpoint is connected

## Important boundary

The MVP does **not** claim that the external AI is already connected.

The default screen therefore runs in `Demo mode`. This is intentional: a UI response must not be represented as evidence of an external model execution.

The optional endpoint currently targets the existing `POST /v0.1/oppai/normalize` input-boundary API when supplied by an operator. That endpoint is an observation/preprocessing boundary, not a complete conversational AI backend.

## Non-goals

- voice UI
- authentication
- billing
- production hosting
- autonomous AI authority
- psychological diagnosis or hidden-intent determination
- automatic promotion of observations to theory
- replacement of the existing Runtime architecture

## Operational rollout

The intended next sequence is:

1. Verify the static UI locally.
2. Connect it to an explicitly supported Runtime/conversation endpoint.
3. Run a small third-party trial.
4. Record observable failures and useful interactions as Evidence.
5. Define the next implementation operation from those observations.

## Naming

This artifact uses the public name **Shirakami Radio**.

It does not redefine the existing `shirakami_radio` Protocol registry entry. The registry currently records that Protocol as `protocolized` while canonical protocol-version synchronization remains pending.

## Principle

> 理論を説明してから体験させるのではなく、体験から観測する。

> 描くとは、暴くことではない。巡礼の理由を持ったまま、もう一度歩かせる。
