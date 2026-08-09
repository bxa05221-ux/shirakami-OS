# Shirakami Runtime β0.1 Prototype

Status: Prototype
Version: 0.1

This directory contains the minimum executable Runtime slice defined by the Runtime β0.1 Minimal Vertical Slice design.

## Scope

The prototype demonstrates only:

Protocol
→ Context
→ Execution
→ Observable Transition
→ Result

It intentionally does not implement:

- external backends
- GitHub integration
- authentication
- persistent database infrastructure
- renderer integration
- LLM-provider integration
- plugins
- independent Evidence Contract
- independent Landscape State Model

## Prototype Boundary

The prototype treats a Protocol as an existing executable description. Runtime receives the Protocol and execution input, constructs a bounded execution context, executes the protocol, records an observable transition, and returns an inspectable result.

The implementation is deliberately dependency-light so that the Runtime boundary can be tested without selecting a backend or provider.

## Architectural Rule

This prototype is evidence-producing implementation, not a new Foundation layer.

If implementation requires a decision not supported by the current Foundation, RFC, or Runtime β0.1 Design, stop and return to Design Observation rather than silently expanding the architecture.
