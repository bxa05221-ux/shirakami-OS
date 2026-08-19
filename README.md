# shirakami-OS

> **Shirakami OS is not another AI model.**
> It is a runtime for preserving, observing, and transferring human context across AI systems.

[English](README.md) | [日本語](README.ja.md)

----
Version: α2.2  
Status: Foundation Freeze

## A Different Question

AI models change.
AI providers change.
Interfaces change.

But human context should not have to disappear with them.

Shirakami explores a different question:

> **What if the valuable asset is not the AI model, but the human landscape the AI learns to inherit?**

**Landscape First.** The runtime is a service to Landscape, not the other way around.

## Reviewer Entry Point

For external architecture review, start here:

- **[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)** — evidence-backed reading order and Kernel boundary review questions.

The recommended path is:

**Foundation → Protocol Contract → Architecture → Runtime → Evidence / Observations → Tests → Replay**

Please classify the architecture from repository evidence rather than from the project name or prior assumptions.

## Architecture

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
AI
```

Shirakami OS treats protocols, evidence, observable state, and human context as explicit architectural objects so that the surrounding AI model can change without forcing the human's accumulated context to disappear.

## Service Artifacts

Shirakami OS also produces concrete protocols and services that make the architecture observable in practice.

- **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** — UI-for-AI dialogue protocol / multi-voice conversation
- **[Service Artifact Index](products/)** — current runnable/reference artifacts

The Foundation describes the architecture. The service artifacts show what that architecture can produce.

## Getting Started

- Foundation → [spec/](spec/)
- Architecture → [docs/](docs/)
- **User Manual (manga)** → [docs/manual/](docs/manual/)
- RFC → [docs/rfc/](docs/rfc/)
- Examples → [examples/](examples/)
- Japanese introduction → [README.ja.md](README.ja.md)

## Overview

Shirakami OS is an open specification project for preserving and utilizing Human Landscapes across generations of AI technologies.  
This repository contains the current Foundation Base Point used as the architectural baseline for future research, implementation, and development.

## Scope
Included:
- Foundation Architecture
- Core Concepts
- Terminology
- Runtime Boundary
- Repository Structure
- Runtime Interface

----

Out of scope:
- Research Notes
- Historical Discussions
- Implementation Details
- Plugins
- Applications

## Principles
- Landscape First.
- Protocols describe Landscapes.
- Runtime executes Protocols.
- LLMs are replaceable. Landscape remains.

## Why This Matters

We are not trying to build a better model inside the model race.

We are exploring the layer around the model:

> **How can a human keep their Landscape when the AI changes?**

This is an experimental open-source project. We welcome comparison, criticism, experiments, and alternative approaches.

## Repository structure
- spec/ — Foundation specifications
- docs/ — Concept documents and reference notes
- examples/ — Minimal examples for runtime boundary
- protocols/ — Protocol source artifacts
- runtime/ — Runtime implementation
- products/ — Service artifacts and reference implementations

## User Manual (Manga)

The Public Alpha includes a minimal multilingual manga-style manual renderer.

- [Manual index](docs/manual/)
- [Japanese SVG](docs/manual/manga-user-manual.ja.svg)
- [English SVG](docs/manual/manga-user-manual.en.svg)
- [Matome YAML source](protocols/manual/manga-user-manual.yaml)
- [Rendering contract](spec/manual-rendering.md)

The same manual structure can be rendered in different languages without changing the page structure. This is an experimental UI/documentation adapter, not a general manga-generation engine.

## Contributing
Please open issues for proposed changes to the Foundation. For patches or documentation fixes, create a branch named `fix/...` or `feat/...` and submit a PR against `main`.

## License
This repository is licensed under the MIT License — see LICENSE.
