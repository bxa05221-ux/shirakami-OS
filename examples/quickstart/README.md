# Shirakami OS Quickstart

This example is intentionally small. It is a runnable-shaped introduction to the β0.1 architecture.

## What it demonstrates

```text
Protocol YAML
    ↓
Execution
    ↓
Observation
    ↓
Transition
    ↓
Evidence
    ↓
Landscape State
```

The example does not require GitHub credentials and does not write to a repository.

## Files

- `protocol.yaml` — minimal 的目yaml Protocol
- `input.yaml` — example input

## Intended execution

The β0.1 Runtime prototype should load the Protocol and input, execute the observation flow, capture Evidence, and expose the resulting Landscape State.

The repository's current Runtime modules are the implementation reference. This example is deliberately kept independent of GitHub so a reviewer can first understand and test the Runtime boundary locally.

## Expected result

```text
Protocol loaded
Observation captured
Transition created
Evidence captured
Landscape State exposed

SUCCESS
```

## Important

This Quickstart is a local architecture demonstration. It does not claim that the complete Live GitHub API path is executable without supplying a token-bearing environment.
