# Activation Boundary Experiment 001

Status: prepared for execution

## Purpose

Verify whether the current main branch contains a connected, executable boundary from human text input to Protocol selection and Runtime execution.

This experiment uses "pump" only as an implementation metaphor. No new Shirakami theory is introduced.

## Question

Can one start from human text and, through an existing canonical entry point, reach:

`human input → activation/entry boundary → protocol selection → Protocol IR → Runtime execution`

without manually constructing the downstream objects in the experiment itself?

## Observed implementation

- `runtime/oppai_runtime_flow.py` provides `prepare()` and `execute()`. `execute()` requires a caller-supplied `runtime_adapter`; it does not select a Protocol from the registry. 
- `api/runtime_api.py` exposes `/v0.1/oppai/normalize` and `/v0.1/execute` as separate endpoints. The OPPAI endpoint normalizes text; the execute endpoint requires a Protocol object in its payload.
- `runtime/protocol_runtime_bridge.py` executes supplied Protocol IR through `Runtime`; it does not perform human-input-to-Protocol selection.
- `runtime/prototype.py` executes a supplied callable Protocol. Its `example_protocol` directly returns `changed=True`.
- `examples/oppai_adapter_demo.py` calls `run_oppai_flow()`, but the current `runtime/oppai_runtime_flow.py` exposes `prepare()` and `execute()` instead. This is an implementation mismatch requiring direct verification, not silent repair.
- The separate Shirakami Radio UI is on PR #233 rather than main, and its default mode is Demo mode; its Runtime endpoint is the OPPAI normalization boundary rather than a complete conversation backend.

## Falsification / confirmation criteria

### Connected pump confirmed

A single executable path starts from human text, selects or resolves a Protocol, constructs/loads the required Protocol IR, invokes Runtime, and produces an observable execution result without the experiment manually supplying the missing connection.

### Pump not confirmed

Human text can be normalized, and Runtime can execute a supplied Protocol, but no existing executable boundary connects those steps. In that case record:

`OPPAI input boundary exists; Runtime execution boundary exists; canonical activation/pump boundary is unverified.`

## Important distinction

This experiment does not determine whether a Shirakami-specific model effect exists. That is the subsequent "battery/model-effect" experiment.

## Rule

File existence is not execution evidence. A passing static check is not evidence of model effect. Do not mark the activation boundary verified until an executable run demonstrates the connected path.
