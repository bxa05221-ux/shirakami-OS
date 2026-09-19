# Full Trace Reconstruction Protocol

Status: MVP v0.1

## Purpose

This protocol closes the first executable Shirakami trace loop:

Evidence → Context → Matrix → Protocol → Prompt → Simulation → AIwitness → Human Decision → Operation → Evidence

The reconstruction layer does not execute actions and does not infer missing facts. It only links explicitly supplied records.

## Trace requirements

A reconstruction trace records:

- input Evidence references
- Context version
- Protocol and Prompt identifiers
- Simulation identifier
- AIwitness identifier
- Human Decision identifier and status
- Operation identifier and status
- whether the Operation reported a Reality change
- resulting Evidence references, when supplied
- uncertainty carried from AIwitness

The trace must reject crossed records. A Human Decision or Operation belonging to another Simulation cannot be attached to the witness.

## Evidence boundary

The reconstruction layer does not store or require raw external data.

If an Operation changes Reality, the resulting Evidence reference should be supplied by the responsible external system or Adapter. If no resulting Evidence reference exists, the trace explicitly records an empty set rather than inventing one.

## Human boundary

The reconstruction layer does not decide whether an Operation was appropriate.

It records the supplied Human Decision and its status. The existing Operation boundary still requires an explicit approved HumanDecision before execution.

## Serialization

The trace can be exposed as an Evidence-shaped record containing:

- kind: reconstruction_trace
- witness_id
- prompt_id
- protocol_id
- simulation_id
- decision_id
- operation_id
- decision_status
- operation_status
- reality_changed
- input_evidence_refs
- resulting_evidence_refs
- context_version
- uncertainty

## Verification target

Given the same explicit records, the reconstruction chain is deterministic.

The protocol therefore makes it possible to ask:

> What Evidence entered the AI, which Context and Protocol were involved, what was simulated, who made the decision, what Operation followed, and what Evidence resulted?

That is the MVP meaning of AIwitness as a traceable witness function.
