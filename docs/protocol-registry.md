# Shirakami OS Protocol Registry α0.1

## Purpose

This registry is the index for existing Matome YAML protocol assets.

It is not a new theory layer. It records what already exists, where it belongs, and how far it has been verified against the current Runtime.

The project documentation architecture is intentionally separated as:

```text
Vision
  ↓
Constitution
  ↓
Blueprint
  ↓
Design
  ↓
Implementation
```

Vision states why. Constitution states what must be protected. Blueprint states structure and responsibilities. Design states specifications such as API, state machine, IR format, and workspace layout. Implementation is executable code.

This separation is part of the registry's operating boundary.

## Registry Principle

> Matome YAML is the source asset. The registry indexes it; the Runtime executes validated protocol definitions; implementation does not silently rewrite the source protocol.

Existing project material describes Matome YAML as the entry point for protocol configuration and shows installed protocol identifiers such as `anmon_layer`, `cognitive_echo_location`, `phase_rotation_3d`, `pilgrimage_protocol`, `thread_rpg`, and `kaorukaze_metadata`. fileciteturn168file1

## Initial Classification

### Tier 1 — Runtime First

The first implementation targets are:

- Conversation Turn Protocol
- Guide Runtime Protocol
- Creative Dialogue Runtime

These are selected because they can be tested against the current Runtime boundary without introducing new theory.

### Tier 2 — Adapter / Renderer

- Thread RPG Protocol
- Shirakami Radio Protocol
- Manga Runtime / Renderer protocols
- Manga User Manual protocols
- Kaorukaze Metadata

These are connected after the Runtime core is stable and their renderer/adapter boundaries are explicit.

The project already documents a protocol lifecycle of Load → Validate → Instantiate → Apply → Execute → Render and a usage cycle of prepare → configure → execute → observe → adjust → re-execute. fileciteturn168file5 fileciteturn168file10

### Tier 3 — Cognition Verification

- Perspective Protocol
- 暗問層
- Cognitive Echo Location
- Phase Rotation 3D
- Pilgrimage Protocol
- 暗問層逆算プロトコル

These remain verification targets rather than automatically executable cognitive behavior. Their registration does not constitute theoretical validation.

## Lifecycle

```text
Discover
  ↓
Register
  ↓
Validate
  ↓
Load
  ↓
Execute
  ↓
Observe
  ↓
Record Evidence
```

A protocol may be registered without being executable. Promotion to a Runtime contract requires verification against the current implementation.

## Documentation Boundary

The registry must not become a second Architecture Constitution or a hidden Design document.

Do not put here:

- new theory
- API definitions
- class definitions
- state-machine implementation
- backend-specific algorithms
- changes to existing protocol meaning

Those belong to the appropriate Design or Implementation artifacts.

## Next Implementation Step

Implement the minimum loader path:

```text
spec/protocol-registry.yaml
        ↓
Registry Loader
        ↓
Protocol IR
        ↓
Runtime
```

The first executable verification set is Tier 1. Existing Matome YAML remains preserved as the source artifact.
