# Simulation Runtime Protocol

## MVP status

Draft v0.1 — executable simulation boundary.

## Purpose

This layer receives a versioned PromptSpec and executes a bounded Simulation.
The MVP uses a supplied callable so that the Shirakami boundary can be tested
without binding the architecture to a particular AI provider.

## Flow

```
Prompt
  ↓
Runtime
  ↓
Simulation
  ↓
SimulationResult
  ↓
AIwitness / Evidence
```

## Reality boundary

Simulation output is explicitly marked as Simulation.

It must not be silently converted into Reality or ordinary observed Evidence.

A SimulationResult contains:

- Simulation ID
- Prompt ID
- Protocol ID
- status
- output
- assumptions

## Failure boundary

Simulation failures are returned as observable results rather than being
silently swallowed.

## Provider independence

The simulation callable may later be replaced by:

- a local model,
- a remote model,
- a rule-based simulator,
- a domain simulator,
- another Runtime implementation.

The Prompt and Evidence boundaries remain independent of the provider.

## Verification target

The MVP succeeds if:

1. a Prompt can be executed without a provider-specific dependency;
2. the SimulationResult points back to Prompt and Protocol;
3. Simulation remains explicitly separated from Reality;
4. failures remain observable;
5. the result can be handed to AIwitness.
