# Runtime β0.1 Design Preparation Observation α0.1

Date: 2026-08-09
Status: Observation Record
Repository: bxa05221-ux/shirakami-OS

## 1. Purpose

This record observes the boundary between the existing Foundation / RFC layer and the future Runtime β0.1 Design layer.

It does not define APIs, schemas, classes, state machines, storage models, implementation algorithms, or code.

## 2. Observed Architectural Chain

The current repository material supports the following conceptual chain:

Landscape
↓
Protocol
↓
Runtime Context
↓
Execution
↓
State Transition
↓
Observation
↓
Output / Rendering

This is an observation of relationships already expressed across the Foundation and RFC material, not a new architectural principle.

## 3. Design Boundary Candidates

### Protocol

The Design layer may need to specify how an existing Protocol is selected, loaded, validated, and made available to Runtime execution.

The Protocol itself remains outside Runtime ownership.

### Runtime Context

The Design layer may need to specify how the conceptual execution context described by the Runtime Interface Contract is assembled for one execution.

The current observation does not establish a concrete Context Pack schema.

### Execution

The Design layer may need to describe the lifecycle of Protocol execution and its relationship to Runtime lifecycle.

The current observation does not establish a concrete execution engine or state machine.

### State Transition

RFC-0006 identifies State Transition Information as part of conceptual execution output. A future Design may need to define how a transition is represented and committed to Landscape state.

No independent Landscape State Model is established by this observation.

### Observation

RFC-0006 identifies Observation Signals, including runtime events, state transitions, errors, and health signals. A future Design may need to distinguish execution observations from durable Evidence.

No independent Evidence Contract is established by this observation.

### Output / Rendering

The current RFC material distinguishes conceptual execution results and renderable output. A future Design may need to define the boundary between Runtime results and Renderer responsibilities.

Renderer implementation is not defined here.

## 4. Component Boundaries

### Runtime ↔ Protocol

Runtime executes Protocols. Runtime does not redefine Foundation Protocol semantics.

### Runtime ↔ Plugin

Plugins extend Runtime capability within the existing Plugin Contract boundary. Plugin-specific implementation remains outside the Runtime core definition.

### Runtime ↔ Adapter

Adapters connect Runtime capabilities to external systems or backends. Backend-specific behavior must remain outside the Runtime core.

### Runtime ↔ Observer

Observation is exposed through the existing Observer concept. The Design layer may need to determine how observation signals are emitted without turning Observer behavior into Runtime business logic.

### Runtime ↔ Renderer

Runtime produces conceptual results / renderable outputs; Renderer handles presentation. The exact transport boundary remains a Design concern.

### Runtime ↔ Landscape

Landscape remains the permanent architectural asset. Runtime operates on observable Landscape state but does not become the owner of the Landscape as an architectural concept.

## 5. Design Questions Still Open

The following questions should be answered during Design, not invented during Foundation:

1. What is the minimal execution context required by a Protocol?
2. What is the lifecycle of one Protocol execution?
3. At what exact point does a state transition become observable?
4. How is Evidence distinguished from transient Observation Signals?
5. What minimum information crosses the Adapter boundary?
6. How does Runtime expose results without coupling itself to a Renderer implementation?
7. How is Runtime replaceability tested without making a specific Runtime implementation normative?

These are Design questions, not new Foundation claims.

## 6. Explicit Non-Goals

This observation does not establish:

- API endpoints
- class or module structure
- schema definitions
- storage technology
- database model
- message bus
- event format
- state machine
- programming language
- LLM provider integration
- UI implementation
- authentication mechanism
- permission implementation

## 7. Design Readiness

Status: `Ready for Design Drafting`

The repository contains enough architectural material to begin a constrained Runtime β0.1 Design draft, provided that the Design remains traceable to the existing RFC/Foundation layer and does not promote unresolved observations into normative Foundation.

## 8. Recommended Design Sequence

1. Execution Context boundary
2. Protocol loading / validation boundary
3. Execution lifecycle
4. Transition and observation boundary
5. Evidence preservation boundary
6. Plugin / Adapter attachment boundary
7. Renderer output boundary
8. Replaceability / conformance verification

The sequence is intended to minimize implementation bias.

## 9. Architectural Invariant

The Design layer must preserve the following observed orientation:

Landscape First
↓
Protocol First
↓
Runtime as execution service
↓
Adapter as backend boundary
↓
LLM / backend replaceability

If a proposed Design reverses this orientation, it must be treated as an architectural conflict and returned to Observation rather than silently adopted.

## 10. Record Boundary

This document records the observed preparation state for Runtime β0.1 Design.

It does not itself constitute the Runtime Design specification.
