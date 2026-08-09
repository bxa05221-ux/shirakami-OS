# Runtime β0.1 Design

Status: Design Draft
Version: 0.1
Date: 2026-08-09

## 1. Purpose

This document translates the existing Shirakami Foundation, Contract Layer, Runtime Interface Contract, Runtime Lifecycle, Plugin Contract, and Runtime β0.1 Blueprint into a constrained Design-level description.

It does not redefine Foundation semantics and does not prescribe a programming language, API framework, storage technology, LLM provider, or UI implementation.

## 2. Traceability

Primary architectural sources:

- Foundation / README: Landscape First; Protocols describe Landscapes; Runtime executes Protocols; LLMs are replaceable; Landscape remains.
- RFC-0003: Runtime lifecycle and Runtime boundary.
- RFC-0004: Plugin contract and plugin boundary.
- RFC-0005: Contract Layer categories.
- RFC-0006: Runtime Interface Contract.
- Runtime β0.1 Blueprint.
- Runtime β0.1 Design Preparation Observation α0.1.

## 3. Design Orientation

The Runtime is designed as a Landscape Maintenance Service and Protocol execution service.

Conceptual flow:

Landscape
↓
Protocol Selection / Loading
↓
Execution Context
↓
Protocol Execution
↓
Transition
↓
Observation
↓
Execution Result / Renderable Output

External systems are reached through Adapter boundaries. Presentation is delegated to Renderer boundaries. Plugins extend Runtime capability without becoming part of Foundation semantics.

## 4. Execution Context

### 4.1 Purpose

Execution Context is the bounded context supplied to one Protocol execution.

### 4.2 Conceptual Contents

The Design recognizes the following conceptual inputs from RFC-0006:

- Protocol Definition
- Context Pack
- Expression Pack
- Permission Information

The Design does not establish a concrete serialized schema for these elements.

### 4.3 Boundary

Execution Context is assembled for execution and must not become a replacement for the persistent Landscape.

## 5. Protocol Loading and Validation

### 5.1 Loading

Runtime must be able to make an existing Protocol available to an execution context.

Protocol semantics remain defined outside the Runtime.

### 5.2 Validation

Runtime validates that the Protocol and required execution inputs satisfy the established Runtime/Protocol boundary before execution proceeds.

The precise validation schema and validation implementation remain implementation concerns.

### 5.3 Failure

A Protocol that cannot satisfy the Runtime execution boundary must not be executed as if valid. Failure must remain observable through the existing Observation / execution result boundary.

## 6. Execution Lifecycle

A single Protocol execution is conceptually organized as:

1. Context acquisition
2. Protocol availability
3. Pre-execution validation
4. Execution
5. Transition processing
6. Observation emission
7. Result formation
8. Output handoff

This is a Design lifecycle, not a normative implementation state machine.

The broader Runtime lifecycle remains governed by RFC-0003:

- Startup
- Plugin Discovery
- Activation
- Execution
- Monitoring
- Shutdown

## 7. Transition Boundary

State Transition Information is a conceptual execution result identified by RFC-0006.

The Design therefore treats a transition as the point at which Protocol execution produces an observable change relevant to Landscape state.

The Design does not yet define an independent Landscape State Model or a concrete transaction mechanism.

A transition must remain distinguishable from:

- transient execution activity,
- Observation Signals,
- final Renderable Output.

## 8. Observation Boundary

RFC-0006 identifies Observation Signals including:

- Runtime Events
- State Transitions
- Errors
- Health Signals

The Runtime Design treats these as observable execution information.

Observation emission must not require the Observer to become responsible for Protocol execution logic.

The distinction between transient Observation Signals and durable Evidence remains an explicit design concern and is not silently promoted to a new Evidence Contract here.

## 9. Evidence Preservation Boundary

Where an observable transition is required to produce durable Evidence, the Runtime must preserve the information at the transition boundary rather than reconstructing it later from mutable state.

This document does not define an independent Evidence Contract because such a contract has not yet been formally established in the repository.

Therefore the Design establishes only the boundary requirement:

Observation at transition
↓
Evidence preservation boundary

The concrete Evidence representation remains open.

## 10. Plugin Boundary

Plugins are Runtime extensions governed by the existing Plugin Contract.

The Runtime core:

- discovers plugins according to the existing lifecycle,
- activates eligible plugins,
- provides the execution environment required by their contract,
- observes plugin execution through the established observation boundary.

Plugin-specific business logic remains outside Runtime core semantics.

## 11. Adapter Boundary

Adapters connect Runtime capabilities to external systems and backends.

The Runtime core must not encode backend-specific assumptions that belong to an Adapter.

Conceptually:

Runtime capability
↓
Adapter boundary
↓
External Backend

The exact Adapter interface remains governed by the existing Contract Layer and requires further Design only where the current contracts leave a concrete boundary unspecified.

## 12. Renderer Boundary

Runtime produces conceptual execution results and renderable output.

Renderer responsibilities begin at presentation / rendering of those results.

Conceptually:

Protocol Execution
↓
Execution Result / Renderable Output
↓
Renderer

The Runtime must not become coupled to a particular presentation technology.

## 13. Runtime / Landscape Boundary

Landscape remains the permanent architectural asset.

Runtime may observe and transition Landscape state through Protocol execution, but the architectural concept of Landscape is not reduced to an internal Runtime data structure.

The Design therefore avoids defining a Runtime-owned canonical Landscape database or equivalent storage model.

## 14. Runtime Replaceability

Runtime implementation is replaceable if it conforms to the same Foundation, Contract Layer, Protocol, and Runtime Interface boundaries.

The Design therefore defines conformance at the boundary level rather than at the implementation level.

A future Verification layer may test whether independent Runtime implementations preserve these observable contracts.

No specific test framework or harness is prescribed here.

## 15. Failure and Observation

Failures are treated as observable execution outcomes rather than hidden Runtime behavior.

At minimum, the Design recognizes:

- invalid or unavailable Protocol execution context,
- execution failure,
- transition failure,
- plugin failure,
- adapter failure,
- renderer handoff failure.

The exact error model remains a later Design / Verification concern.

## 16. Design Invariants

The following must remain true:

1. Runtime executes Protocols; it does not redefine Foundation Protocol semantics.
2. Landscape remains the permanent architectural asset.
3. Backend-specific behavior remains behind Adapter boundaries.
4. Presentation-specific behavior remains behind Renderer boundaries.
5. Plugin-specific behavior remains behind Plugin boundaries.
6. Observation does not become Runtime business logic.
7. Evidence, when required, is captured at the relevant observable transition boundary rather than reconstructed arbitrarily later.
8. Runtime implementation remains replaceable.
9. LLM/provider selection does not become a Runtime architectural dependency.
10. Unresolved architectural observations are not silently promoted into Foundation.

## 17. Explicitly Deferred

The following are intentionally not defined by Runtime β0.1 Design:

- concrete API endpoints
- concrete schemas
- classes / modules
- storage engine
- database model
- event bus
- message protocol
- authentication implementation
- permission implementation
- LLM integration implementation
- UI implementation
- independent Evidence Contract
- independent Landscape State Model
- Repository Event Contract
- Conformance test framework

## 18. Design Readiness for Implementation

Status: `Not Yet Ready for Implementation`

The Design boundary is now sufficiently explicit for subsequent detailed Design work, but implementation should not begin until the remaining concrete boundaries required by the selected implementation scope are specified and verified.

The next step is not to add arbitrary infrastructure. It is to select the smallest executable Runtime slice and derive only the concrete Design artifacts required by that slice.

## 19. Next Design Observation

The next observation should determine the minimal executable vertical slice for Runtime β0.1, preferably covering:

Protocol
→ Context
→ Execution
→ Observable Transition
→ Result

while leaving backend integration and presentation as replaceable boundaries.

This provides the smallest path from Foundation to an executable Runtime without prematurely fixing the full implementation architecture.
