# OPPAI Verification Status v0.1

**Status:** Verification record  
**Scope:** OPPAI input boundary / semantic preservation  
**Target branch:** `verification/v04-deep-immutability`

## Purpose

This document records the verification scope currently implemented for the OPPAI input boundary.

The goal is not to prove that OPPAI understands human intent correctly. The goal is narrower:

- preserve the user-authored source text;
- keep observational signals separate from source text and factual certainty;
- preserve unresolved state rather than silently resolving it;
- keep the OPPAI boundary replaceable and observable.

## Verified test scope

The current OPPAI workflow runs these test modules:

```text
tests/test_oppai_schema.py
tests/test_oppai_runtime_flow.py
tests/test_input_boundary_contract.py
```

The input-boundary contract specifically checks:

1. Japanese Unicode and newlines survive the boundary unchanged.
2. `raw_input` and `canonical_prompt` remain the same source value in the current bounded implementation.
3. Interaction observations remain separate from the source text.
4. Unresolved questions remain unresolved rather than being converted into facts.
5. Empty, whitespace-only, `None`, and non-string input are rejected.

## CI execution

The OPPAI workflow is configured for:

- push events affecting the relevant runtime/tests/docs/workflow paths;
- pull requests affecting those paths;
- manual `workflow_dispatch` execution;
- a weekly scheduled execution (`17 2 * * 1`).

The workflow has `contents: read` permission and runs the three test modules above.

**Operational note:** GitHub Actions scheduled workflows run from the repository's default branch. Therefore, the schedule definition on this verification branch should not be interpreted as an already-active weekly job until the workflow is present on the default branch.

## Current evidence

For commit `0e59cf36e8ca180a43242620188a9b9e84d2fe80`, the repository's available GitHub Actions verification reported successful completion for the OPPAI Runtime workflow and the other verification workflows associated with that commit.

This confirms CI execution for that commit; it does not establish broader semantic correctness beyond the tests actually executed.

## Non-goals

This verification does **not** establish:

- reliable hidden-intent inference;
- complete prompt-injection detection;
- psychological-state inference;
- factual truth of arbitrary user input;
- safety of arbitrary downstream protocols or backends;
- correctness of a future full Protocol specification.

## Boundary principle

OPPAI is an observation and normalization boundary, not an authority layer.

A warning, interaction signal, or parser observation must not silently become a Protocol command, a factual assertion, or a replacement for the user's judgment.
