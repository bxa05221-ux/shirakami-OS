# Runtime β0.1 GitHub Read Observation

Status: Verification Gate
Version: 0.1
Date: 2026-08-11

## Observation Target

The repository itself is the first observable external Landscape.

No new `landscape.json` file is introduced at this stage.

The Runtime observes the existing GitHub repository root through a read-only adapter.

## Boundary

```text
GitHub Repository
      ↓
GitHub Contents Client
      ↓
Repository Landscape Adapter
      ↓
Observable Landscape State
```

## Why Read-Only First

The repository already has an established Foundation Base Point. Creating a new canonical Landscape file solely to satisfy the Runtime would reverse the intended dependency and allow implementation to define Landscape.

Therefore the first real Backend observation is read-only.

## Observed Repository

The current `main` root exposes, among other entries:

- `.github/`
- `README.md`
- `docs/`
- `examples/`
- `plugins/`
- `runtime/`
- `spec/`

The README identifies the repository as Foundation α2.2 / Foundation Freeze and states that Landscape First is a core principle.

## Verification Gate

The implementation must prove only that an external GitHub repository can be observed as Landscape without requiring a predeclared Landscape JSON schema.

No write operation is part of this gate.

## Next Gate

After the read path is verified, define the smallest safe Controlled Write target. It must not modify Foundation files or redefine canonical Landscape semantics.
