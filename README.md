# shirakami-OS

> **Shirakami OS is not another AI model.**
> It is a runtime for preserving, observing, and transferring human context across AI systems.

[English](README.md) | [日本語](README.ja.md)

----
Version: Prototype v1.1 (PV1.1)  
Status: β1.1 Evidence-Driven Runtime / Operational Baseline

## 5-Minute Orientation

If you are new to Shirakami, you do not need to read the whole repository first.

1. **Understand it** → [What Shirakami Is](#what-shirakami-is)
2. **See the structure** → [Repository Map](docs/architecture/REPOSITORY_MAP.md)
3. **Review the architecture** → [Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)
4. **Run it** → [MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)

In one sentence:

> **Shirakami OS is a runtime for preserving, observing, and transferring human context independently of a particular AI model or provider.**

The shortest conceptual path is:

**Landscape → Evidence → Protocol → Runtime → Adapter → External System / AI**

## Information Flow / Protocol Gearbox

Shirakami can also be understood as an **information water system**. Information held in a Landscape can be diverted through different Protocol routes and reused for different needs. Protocols act like a gearbox: the route can be changed by composing different Protocols and boundaries without requiring a different AI model for every use case.

```text
Information / Landscape
          ↓
       diversion
      ↙    ↓    ↘
 Protocol A  B  C
      ↘    ↓    ↙
        Evidence
           ↓
      re-observation
           ↓
       Landscape
```

This is an architectural interpretation of the existing implementation, not a claim of unrestricted arbitrary Protocol permutation. See **[Information Watershed Model](docs/architecture/INFORMATION_WATERSHED_MODEL.md)** for the evidence and verification boundary.

### n-gram / One-stroke Route

The route model can be made more precise by treating Protocol connections as local transitions. An **n-gram** represents a short sequence of Protocol transitions (for example, `A → B` or `A → B → C`) and can be used to generate candidate routes. Protocol input/output boundaries and verification constrain which transitions are admissible; Runtime executes the route and Evidence records what actually happened.

```text
Protocol A → Protocol B → Protocol D
        candidate one-stroke route
```

Here, “one-stroke” means a continuous chain of compatible Protocol transitions. It is not a claim of unrestricted Protocol permutation or an Eulerian-path algorithm. The model is a route-construction mechanism, not an AI authority.

## Current Verified Runtime Loop

The current implementation connects a conservative Evolution Loop to structural Protocol route generation and one-stroke execution:

```text
Evidence
   ↓
Explicit Protocol Artifact
   ↓
Structural n-gram Candidate
   ↓
HUMAN_REVIEW
   ↓
Human Gate
   ↓
READY
   ↓
One-Stroke Runtime
   ↓
Verification
   ↓
ACCEPTED / DIFF
   ↓
Evidence
   ↺
```

The important boundary is intentional: **Evidence can generate a candidate, but it cannot authorize execution.** Semantic compatibility is not inferred from structural matching. Execution requires explicit human approval through the existing R0100 Human Gate, and verification records the observed result as Evidence.

See [Evidence → Route Candidate Bridge α0.4](docs/EVIDENCE_ROUTE_CANDIDATE_ALPHA_0_4.md) for the implementation boundary.

## What Shirakami Is

Shirakami OS is an open-source **Personal AI Runtime / development architecture** for preserving and working with human context independently of a particular LLM or AI provider.

It makes these boundaries explicit:

- **Landscape** — observable human/AI/project/context environment
- **Protocol** — declares meaning and execution structure
- **Runtime** — executes Protocols without owning domain truth
- **Evidence** — preserves observable transitions
- **Projection / Replay** — reconstruct and inspect Landscape state
- **Adapter** — separates the Runtime from external AI and backend systems

For readers coming from **AI memory, human context preservation, personal AI infrastructure, protocol-driven AI, evidence-driven AI, AI agents, or model-independent AI runtimes**, this repository is the implementation-oriented entry point.

## A Different Question

AI models change.
AI providers change.
Interfaces change.

But human context should not have to disappear with them.

Shirakami explores a different question:

> **What if the valuable asset is not the AI model, but the human landscape the AI learns to inherit?**

**Landscape First.** The runtime is a service to Landscape, not the other way around.

## The Residue Problem

Shirakami began from a practical question:

> **What happens to the residue that remains around an AI interaction?**

By “residue,” we mean context that can otherwise remain implicit: conversation noise, unintended associations, stale context, ambiguous assumptions, unexplained influences, or other traces that may affect the next step without being clearly visible.

The point is not to claim that all such influence can be extracted from an AI's internal state. Instead, Shirakami asks how much of the **externally observable influence** can be made explicit, recorded, inspected, and carried forward as part of the human Landscape.

```text
Observation
    ↓
Evidence
    ↓
Analysis
    ↓
Protocol Candidate
    ↓
Human Gate
    ↓
Runtime
    ↓
Verification
    ↓
Mismatch
    ↓
Evidence
    ↺
```

A mismatch is not simply discarded as an error. The expected and observed states can be preserved separately as **Mismatch Evidence**, including uncertainty, context, and an optional diff reference.

Shirakami does not try to make residue disappear.

> **It tries to externalize what would otherwise remain implicit.**

That applies not only to AI-related effects. Human mistakes, ambiguous decisions, failed assumptions, and environmental changes can also become observable Evidence. They can then be inspected, corrected, reused, or rejected without silently rewriting the past.

This is one reason Shirakami treats **Evidence as a first-class architectural boundary**.

## Reviewer Entry Point

For external review, start here:

- **[Repository Map](docs/architecture/REPOSITORY_MAP.md)** — the repository structure and entry points by visitor intent.
- **[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)** — evidence-backed reading order and architecture boundaries.
- **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)** — the shortest route to running and testing the implementation.

Recommended reading order:

**Landscape → Evidence → Specification / Protocol → Runtime → Adapter → Execution → Observation**

## Architecture

```text
Landscape
    ↓
Evidence
    ↓
Protocol / Specification
    ↓
Runtime
    ↓
Adapter
    ↓
External System / AI
```

Shirakami OS treats protocols, evidence, observable state, and human context as explicit architectural objects so that the surrounding AI model can change without forcing the human's accumulated context to disappear.

## Minimal Executable OS

The repository exposes one concrete vertical slice as the executable entry point:

```text
boot Landscape
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
python shirakami_os.py
```

The entry point is intentionally small. It does not claim to be the final architecture; it makes the minimum OS boundary directly executable and inspectable. The implementation is covered by `tests/test_shirakami_os.py`.

## Public Service Artifact

The current public service artifact is **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** — a UI-for-AI dialogue protocol / multi-voice conversation system.

Thread RPG is the public entry point for experiencing Shirakami concepts in a concrete form. It demonstrates how Protocol-driven interaction can produce a human-observable Landscape and serve as a basis for further observation.

Other experimental artifacts, including Matome API v3.2 and related Evidence work, remain development/research artifacts and are not presented here as public service products.

→ **[Service Artifact Index](products/)**

## Getting Started

- **MVP Quickstart → [docs/architecture/MVP_QUICKSTART.md](docs/architecture/MVP_QUICKSTART.md)**
- Foundation / implementation boundary → [spec/](spec/)
- Architecture → [docs/](docs/)
- **User Manual (manga)** → [docs/manual/](docs/manual/)
- Historical / active RFCs → [docs/rfc/](docs/rfc/)
- Examples → [examples/](examples/)
- Japanese introduction → [README.ja.md](README.ja.md)
- Normative specifications → **[shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification)**

## Scope

Included:
- Runtime implementation
- Reference architecture implementation
- Adapters and plugins
- Executable examples
- Evidence and observation mechanisms

Out of scope:
- Research Notes
- Historical Discussions
- Stable normative specifications owned by `shirakami-specification`
- Private user Landscape

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
- spec/ — implementation-side Foundation and transition specifications
- docs/ — architecture and reference notes
- examples/ — minimal examples for runtime boundary
- protocols/ — protocol source artifacts used by implementations
- runtime/ — Runtime implementation
- plugins/ — plugin and adapter implementations
- products/ — public service artifact and reference implementations

## User Manual (Manga)

The repository includes an experimental multilingual manga-style manual renderer.

- [Manual index](docs/manual/)
- [Japanese SVG](docs/manual/manga-user-manual.ja.svg)
- [English SVG](docs/manual/manga-user-manual.en.svg)
- [Matome YAML source](protocols/manual/manga-user-manual.yaml)
- [Rendering contract](spec/manual-rendering.md)

The same manual structure can be rendered in different languages without changing the page structure. This is an experimental UI/documentation adapter, not a general manga-generation engine.

## Contributing
Please open issues for proposed changes to the Foundation. For patches or documentation fixes, create a branch named `fix/...` or `feat/...` and submit a PR against `main`.

## License

Shirakami OS now uses a **layered licensing model**:

- **Source code and executable implementation artifacts** → MIT License (`LICENSE`)
- **Specifications, protocols, schemas, architecture documents, and documentation** → CC BY 4.0 (`LICENSE-SPECIFICATION.md`)
- **Shirakami OS name, logos, and project marks** → not granted as trademark or official-brand rights by either license
- **Official certification, endorsement, commercial branding, and Enterprise offerings** → may be governed by separate terms or agreements

This separation is intentional. The implementation is open for use and adaptation, while the specification and documentation remain reusable with attribution, and the project's identity and official status remain separately governed.

See [`LICENSE`](LICENSE) and [`LICENSE-SPECIFICATION.md`](LICENSE-SPECIFICATION.md).
