# RFC-0006 — Runtime Interface Contract (Draft)

Status: Draft

Date: 2026-08-01

Author: Shirakami OS Architecture Team (draft)

Summary

RFC-0006 defines the high-level Runtime Interface Contract: the stable, architecture-level expectations that govern how the Shirakami OS Runtime interacts with external components. This document intentionally defines conceptual contracts and principles only — it excludes implementation details such as API endpoints, programming languages, storage choices, or UI design.

Purpose

This RFC describes the Runtime Interface Contract. The contract defines how the Runtime interacts with four categories of external components:

- Protocols — formal protocol definitions the Runtime executes
- Plugins — optional, extensible components that provide capabilities or sensors
- Adapters — translators between external systems and the Runtime's internal model
- Renderers — components that transform runtime outputs into human- or system-facing representations

The goal is to provide stable expectations so implementers and integrators can build compatible components while preserving an architecture-first separation between normative specification and implementation.

Runtime Role

The Runtime is responsible for:

- Loading protocol definitions and making protocol semantics available to execution engines.
- Validating execution context and preconditions required by a protocol.
- Managing protocol execution lifecycle (initialize, execute, observe, finalize).
- Connecting component contracts (plugins, adapters, renderers) to protocol execution at defined attachment points.
- Producing runtime outputs and outcome metadata for downstream consumers.

The Runtime explicitly does not own or claim responsibility for:

- Human Landscapes: human processes, decisions, or organizations outside runtime execution.
- External repositories: source-of-truth or third-party repositories that live outside the Runtime boundary.
- Plugin-specific internal knowledge: plugins retain responsibility for their own internal semantics and state.
- Implementation-specific data: storage layouts, persistence details, and transport formats are out of scope for this contract.

Input Contract

Runtime inputs are conceptual payloads the Runtime accepts for protocol execution. The contract describes required input categories and their intent. Implementations may encode these inputs in any representation, provided the conceptual meaning is preserved.

Core input categories:

- Protocol Definition
  - A structured description of the protocol to execute. It is normative for execution semantics and may reference normative terms in the Glossary/Spec.

- Context Pack
  - Execution environment information: identity of the requester, time bounds, resource allowances, and relevant environment tags.

- Expression Pack
  - Domain-specific expressions or parameters required to customize protocol execution (variables, expressions, templates). These are not executable code in the runtime's implementation sense, but parameterized inputs.

- Permission Information
  - Authorization and capability declarations describing what actions the Runtime is permitted to perform on behalf of the requester.

Conceptual YAML example (illustrative only):

```yaml
protocol: "example-protocol@1.0"
context:
  requester: "actor:alice"
  timestamp: "2026-08-01T00:00:00Z"
  environment: ["staging"]
expression:
  variables:
    foo: 42
permissions:
  allowed_actions: ["read-state", "emit-observation"]
```

Output Contract

Runtime outputs are conceptual artifacts produced after protocol execution. These outputs are intended for downstream systems (renderers, observers, storage) and must be semantically stable across runtime implementations.

Core output categories:

- Execution Result
  - The high-level outcome of the protocol run (success, partial-success, failure) and any primary result data.

- State Transition Information
  - Descriptions of state changes produced or requested during execution (deltas, intended new state markers). The Runtime should produce machine-readable transition descriptors rather than prescribing storage.

- Observation Signals
  - Telemetry-style observations and events emitted during execution (timing, warnings, checkpoints). Observers may subscribe to these signals.

- Renderable Output
  - Render-target agnostic content intended for renderers to present to end-users or systems (structured documents, message envelopes, event summaries).

Conceptual YAML example (illustrative only):

```yaml
result:
  status: "success"
  data:
    value: "computed-value"
state_transitions:
  - path: "/resource/42"
    delta: {"count": +1}
observations:
  - id: "obs-1"
    type: "latency"
    value_ms: 123
render:
  mime: "application/x.shirakami.result+yaml"
  payload: "..."
```

Component Interaction

This section describes how the Runtime models and exchanges metadata with components.

Plugin

Plugins are pluggable capability providers that the Runtime may invoke during protocol execution. The Runtime relies on a small, stable plugin contract describing identity, capability and lifecycle signals.

Required plugin metadata:

- identity — unique identifier for the plugin (namespace-qualified)
- version — declared semantic version or range
- capability — declared capabilities or feature set the plugin provides
- status — operational status and health metadata (optional in lightweight implementations)

Behavioral expectations:

- Plugins declare their capabilities and do not implicitly alter the core Runtime behavior.
- Plugins own their internal state and do not override protocol semantics.
- The Runtime may rely on plugin-declared capabilities to resolve protocol steps but must fail safely if capabilities are absent.

Adapter

Adapters translate between external system models and the Runtime's internal contract. They:

- Translate external representations into the Runtime's conceptual input structures and vice versa for outputs.
- Validate and sanitize external data to preserve Runtime invariants.
- Do not own the external system; they are translators and mappings only.

Renderer

Renderers transform runtime outputs into human- or system-facing presentations. Renderers:

- Accept renderable output and produce presentation artifacts (documents, formatted messages, UI fragments) without altering execution semantics.
- Do not affect the Runtime's decision-making or execution results.

Principles

The Runtime Interface Contract adheres to these principles:

- Runtime depends on Contracts.
  - Explicit, versioned contracts (protocols, plugin manifests, adapter descriptors) are first-class. The Runtime resolves behavior from contracts rather than ad-hoc integration logic.

- Runtime does not depend on implementation details.
  - Implementations may vary; the contract specifies the stable surface area only.

- Protocols describe Landscapes.
  - Protocol definitions are the normative descriptions of behavior within a Landscape; they do not embed implementation-specific instructions.

- Runtime executes Protocols.
  - The Runtime's responsibility is to instantiate and manage protocol execution according to the protocol's semantics and the contextual inputs.

- External systems connect through Adapters.
  - Adapters isolate the Runtime from idiosyncratic external models and enable consistent runtime semantics.

Out of Scope

This RFC intentionally excludes the following:

- API endpoint definitions or network protocol wire formats.
- Programming language choices or implementation frameworks.
- Storage implementation and persistence schemas.
- LLM integration specifics, model choices, or prompts.
- User interface design, UI components, or front-end behavior.

Future Extensions

Potential future RFCs that refine and extend this contract include:

- Runtime API Contract — a separate RFC that defines network-level APIs and message formats for runtime control and observation.
- Memory Interface Contract — defines how runtime state and memory interfaces are modeled and queried.
- Observer Interface Contract — defines subscription and telemetry semantics for observation systems.
- Permission Model — formalizes the permission and capability declarations consumed by the Runtime.

Notes & Governance

- This RFC defines stable conceptual expectations only. Any concrete API, protocol encoding, or storage choice must be proposed in follow-up RFCs.
- Label protocol documents and RFCs as Normative or Informative according to the project's normative policy (see CONTRIBUTING / spec governance when available).

---

End of Draft RFC-0006
