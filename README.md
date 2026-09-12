# shirakami-OS

> **Shirakami is not another AI model.**
> It is a runtime and protocol-based interface for preserving, observing, and transferring human context across AI systems.

[English](README.md) | [日本語](README.ja.md)

---

## 👋 New here? Start here.

You do **not** need to understand GitHub to try Shirakami.

If you only want to understand what this project is, use this path:

1. **[Shirakami Model Launch Protocol](docs/protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)** — what is being launched
2. **[Shirakami Radio Language UI](examples/shirakami_radio_ui/)** — the simplest human-facing interface
3. **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)** — run the implementation
4. **[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)** — inspect the architecture and evidence boundaries
5. **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** — an existing public service artifact

### In one sentence

**Shirakami explores how a human can keep their context and judgment when the AI changes.**

The AI is a simulator, observer, and hypothesis generator — **not the final authority**.

---

## Current status

**β1.0 → Launch Model → Operational Rollout**

This repository is moving from verified shakedown into real operational observation.

Launch does **not** mean finished product. It means that a verified boundary is ready to be placed into real use, observed, and improved through evidence.

For the current launch declaration, see:

**[Shirakami Model Launch Protocol v1.0](docs/protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)**

---

## What Shirakami Is

Shirakami is an open-source **human-context / AI runtime architecture** designed to keep Landscape, Protocol, Evidence, and human judgment explicit and portable across changing AI systems.

It makes these boundaries explicit:

- **Landscape** — observable human / AI / project / context environment
- **Evidence** — observed transitions and facts, separated from inference
- **Protocol** — processing and interaction rules
- **Runtime** — executes Protocols without owning domain truth
- **Adapter** — separates Runtime from external AI, UI, and backend systems
- **Renderer / UI** — presents interaction without becoming semantic authority

Recommended architecture reading order:

**Landscape → Evidence → Protocol → Runtime → Adapter → Execution → Observation**

---

## Try the Human-facing Interface

### Shirakami Radio

**[Open the Shirakami Radio Language UI](examples/shirakami_radio_ui/)**

This is the smallest current interface for experiencing the Shirakami approach as a conversation.

The current MVP is intentionally simple:

- browser-based
- Japanese conversation UI
- Demo mode
- optional Runtime endpoint
- no account required by the static UI itself
- no claim that an external AI is connected by default

The UI is a **human-facing entry point**, not the Runtime itself.

Audio is not required for this first rollout. Voice UI can be added later as a separate versioned interface.

---

## Architecture

```text
Human
  ↓
Shirakami Radio / UI
  ↓
Language UI Adapter
  ↓
Protocol
  ↓
Runtime
  ↓
AI / Backend Adapter
  ↓
External AI or Service
  ↓
Response
  ↓
Renderer / UI
  ↓
Human
```

The surrounding AI can change. The human Landscape and the boundaries around it are intended to remain portable.

---

## Core Principles

- **Human final authority** — AI does not receive final decision-making authority.
- **Landscape First** — human context is not subordinate to the model.
- **Hypotheses remain provisional** — inferred intent, emotion, or personality is not treated as fact.
- **Uncertainty is preserved** — what is not understood is not silently filled in.
- **Contradictions are signals** — disagreement and correction can update the working hypothesis.
- **Evidence is preserved** — observed history is not silently rewritten.
- **Runtime is replaceable** — the architecture should not depend on one AI vendor.
- **One change, one verification** — operational changes are introduced and checked incrementally.

---

## Launch is an operation, not a completion certificate

The launch model follows a continuous cycle:

```text
Observe
  ↓
Hypothesis
  ↓
Dialogue
  ↓
Echo
  ↓
Update
  ↓
Consistency Check
  ↓
Observe
```

The quality target is therefore not simply “did the AI answer correctly?”

We also observe:

- cognitive echoes
- contradictions
- misunderstandings
- unresolved questions
- protocol deviations
- Runtime dependency
- human corrections

**Launch → Observe → Evidence → Refine → Verify → Next version**

---

## Minimal Executable Runtime

The repository also contains a minimal executable vertical slice:

```text
Landscape
   ↓
Protocol
   ↓
Runtime
   ↓
Observable Transition
   ↓
Evidence
   ↓
Landscape State
   ↓
Inspectable Result
```

Run:

```bash
python examples/quickstart/run.py
```

For implementation details, see **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)**.

---

## Public Service Artifact

The current public service artifact is **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** — a UI-for-AI dialogue protocol / multi-voice conversation system.

Other experimental artifacts remain development or research artifacts unless explicitly identified as public service artifacts.

→ **[Service Artifact Index](products/)**

---

## For reviewers

If you are here to evaluate the project rather than simply try it, start with:

**[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)**

It provides the evidence-backed reading order and architecture boundaries.

The repository deliberately distinguishes:

- current implementation
- normative specifications
- observations / evidence
- experiments
- historical artifacts
- research questions

A file existing in the repository does **not** by itself mean that an experiment succeeded or that a concept is implemented in the canonical Runtime path.

---

## Scope

Included:
- Runtime implementation
- Reference architecture implementation
- Adapters and plugins
- Executable examples
- Evidence and observation mechanisms
- Human-facing experimental UI

Out of scope:
- Private user Landscape
- Research notes as normative implementation
- Historical discussions as current specification
- Stable normative specifications owned by `shirakami-specification`

---

## Repository structure

- `spec/` — implementation-side specifications
- `docs/` — architecture, protocols, observations, and reference documentation
- `examples/` — executable examples and UI prototypes
- `protocols/` — protocol source artifacts
- `runtime/` — Runtime implementation
- `plugins/` — plugins and adapters
- `products/` — public service artifacts

---

## Related repositories

- [shirakami-model](https://github.com/bxa05221-ux/shirakami-model) — Model / Vision
- [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification) — Specification
- [shirakami-research](https://github.com/bxa05221-ux/shirakami-research) — Research / theory
- **shirakami-OS** — Runtime / Implementation

---

## License

Shirakami uses a layered licensing model:

- **Source code and executable implementation artifacts** → MIT License (`LICENSE`)
- **Specifications, protocols, schemas, architecture documents, and documentation** → CC BY 4.0 (`LICENSE-SPECIFICATION.md`)
- **Shirakami name, logos, and project marks** → not granted as trademark or official-brand rights by either license
- **Official certification, endorsement, commercial branding, and Enterprise offerings** → may be governed by separate terms or agreements

See [`LICENSE`](LICENSE) and [`LICENSE-SPECIFICATION.md`](LICENSE-SPECIFICATION.md).

---

## Contributing

Questions, criticism, experiments, and alternative approaches are welcome.

For patches or documentation changes, create a `fix/...` or `feat/...` branch and submit a PR against `main`.
