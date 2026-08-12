# shirakami-OS

Shirakami OS — Foundation Base Point

[English](README.md) | [日本語](README.ja.md)

----
Version: α2.2  
Status: Foundation Freeze

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

----

## Principles
- Landscape First.
- Protocols describe Landscapes.
- Runtime executes Protocols.
- LLMs are replaceable. Landscape remains.

## Repository structure
- spec/ — Foundation specifications
- docs/ — Concept documents and reference notes
- examples/ — Minimal examples for runtime boundary
- protocols/ — Protocol source artifacts
- runtime/ — Runtime implementation

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
