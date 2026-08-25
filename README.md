# Shirakami OS

> **Shirakami OS is not another AI model.**
> It is a Protocol-driven runtime for preserving, observing, and transferring human context across AI systems.

[日本語](README.ja.md)

---

## What can it do?

Shirakami OS provides an implementation layer between a human's **Landscape** and interchangeable AI / backend systems.

In practical terms, it can:

- execute Protocol-driven operations through a Runtime / API boundary
- represent Protocols and compressed context as **Matome YAML (的目YAML)**
- record observable transitions as **Evidence**
- preserve Landscape state separately from the AI model
- connect external systems through **Adapters / Plugins**
- test the execution boundary automatically with CI

### A concrete example

The public **Shirakami Model v3.2** Matome YAML has been used as an API execution fixture:

```text
Shirakami Model v3.2
        ↓
   /v1/execute
        ↓
 Shirakami Runtime
        ↓
   API result
        ↓
 GitHub Actions
        ↓
      PASS
```

This is an implementation test, not a claim that v3.2 is a complete executable Protocol specification.

---

## Architecture at a glance

```text
Landscape
    ↓
Evidence
    ↓
Protocol / Specification
    ↓
Runtime
    ↓
API / Adapter
    ↓
External System / AI
```

The central design principle is **Landscape First**: the Runtime is a service to Landscape, not the other way around.

The minimum executable loop is:

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

---

## Why Shirakami?

AI models change.
AI providers change.
Interfaces change.

The project asks a different question:

> **What if the valuable asset is not the AI model, but the human landscape the AI learns to inherit?**

The Foundation therefore treats LLMs as replaceable and Landscape as the persistent architectural asset.

---

## Repository Landscape

The project is intentionally separated into four roles:

- **[shirakami-model](https://github.com/bxa05221-ux/shirakami-model)** — cognitive model, principles, and conceptual foundation
- **[shirakami-research](https://github.com/bxa05221-ux/shirakami-research)** — observations, experiments, hypotheses, and exploratory artifacts
- **[shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification)** — stable specifications, schemas, and normative protocol contracts
- **shirakami-OS** — Runtime, reference implementation, adapters, plugins, and executable artifacts

This repository is the implementation/runtime layer. Stable normative specifications belong in `shirakami-specification` rather than being duplicated here.

---

## Current implementation status

The repository currently contains:

- Foundation architecture
- Runtime prototype
- Runtime API α0.1 work
- Evidence boundary
- Landscape State handling
- Matome YAML / Protocol loading experiments
- Protocol IR
- GitHub Adapter / Backend boundary
- executable examples
- automated tests and GitHub Actions CI

The project is still experimental. In particular, the current API and Protocol Loader should not be interpreted as a complete implementation of every Shirakami Protocol.

---

## Try the runtime

Minimal executable example:

```bash
python shirakami_os.py
```

Quickstart:

```bash
git clone https://github.com/bxa05221-ux/shirakami-OS.git
cd shirakami-OS
python examples/quickstart/run.py
```

For architecture review, start with:

**Landscape → Evidence → Specification / Protocol → Runtime → Adapter → Execution → Observation**

See [Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md).

---

## Public service artifact

The current public service artifact is **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** — a UI-for-AI dialogue protocol / multi-voice conversation system.

It provides a concrete way to experience Protocol-driven interaction and observe a resulting human-readable Landscape.

→ [Service Artifact Index](products/)

Other experimental artifacts remain development/research artifacts and are not presented here as finished public products.

---

## Repository structure

```text
spec/       implementation-side Foundation / transition specifications
docs/       architecture and reference notes
examples/   minimal executable examples
protocols/  protocol source artifacts used by implementations
runtime/    Runtime implementation
plugins/    adapters and plugins
products/   public service artifacts / reference implementations
tests/      automated tests
```

---

## User Manual (Manga)

The Public Alpha includes a minimal multilingual manga-style manual renderer.

- [Manual index](docs/manual/)
- [Japanese SVG](docs/manual/manga-user-manual.ja.svg)
- [English SVG](docs/manual/manga-user-manual.en.svg)
- [Matome YAML source](protocols/manual/manga-user-manual.yaml)
- [Rendering contract](spec/manual-rendering.md)

This is an experimental UI/documentation adapter, not a general manga-generation engine.

---

## Common Misconceptions

Shirakami OS is sometimes mistaken for an AI model, an LLM project, or a vendor-specific AI application.

It is not intended to:

- replace ChatGPT or another specific AI
- develop a new LLM itself
- lock the runtime to a particular AI vendor
- serve merely as a repository for research notes

The focus is the **Runtime layer that allows human Landscape and Protocol to remain usable even when the underlying AI changes.**

---

## Contributing

Please open issues for proposed changes to the Foundation. For patches or documentation fixes, create a branch named `fix/...` or `feat/...` and submit a PR against `main`.

## License

This repository is licensed under the MIT License — see `LICENSE`.
