# Shirakami OS — 30-Minute External Review Guide

## Purpose

This guide is the practical companion to the Public Verification Pack.

It is designed for a reviewer who has approximately 30 minutes and no prior knowledge of Shirakami OS.

The goal is not to decide whether Shirakami is "good" or "bad". The goal is to determine, from the public repository:

- what the current Runtime actually executes;
- where authorization enters the flow;
- what Evidence records;
- what remains structural, experimental, or unverified.

This guide is a review route, not a certification procedure.

## Review Route

```text
00:00  Read the one-sentence definition
       ↓
05:00  Inspect repository roles and boundaries
       ↓
10:00  Run the minimal Runtime/tests
       ↓
15:00  Run the Evidence → Route demo
       ↓
20:00  Inspect Human Gate + candidate generation
       ↓
25:00  Compare implementation with specification
       ↓
30:00  Record observations / disagreements
```

## 0–5 min — Establish the claim

Read:

1. [README](../README.md)
2. [Repository Map](architecture/REPOSITORY_MAP.md)

Identify the current architectural statement:

```text
Landscape → Evidence → Protocol → Runtime → Adapter
```

Do not infer additional capabilities from the project name.

### Reviewer checkpoint

Write down, in your own words:

> What problem does the Runtime claim to solve?

If your interpretation differs from the README, keep both interpretations. Do not silently reconcile them.

## 5–10 min — Locate the authority boundaries

Read:

- [Reviewer Entry Point](architecture/REVIEWER_ENTRY_POINT.md)
- [Public Verification Pack](PUBLIC_VERIFICATION_PACK.md)

Then locate:

- `runtime/evolution_loop.py`
- `runtime/evolution_pipeline.py`
- `runtime/one_stroke_route_pipeline.py`
- `tools/protocol_route_candidates.py`

Look specifically for the transition:

```text
HUMAN_REVIEW → Human Gate → READY
```

### Reviewer checkpoint

Answer these questions from code:

1. Can a generated Candidate execute without explicit approval?
2. Can Evidence itself authorize execution?
3. What state is required before execution?
4. What happens when a required Protocol implementation is missing?

Do not answer from terminology. Follow the actual control flow.

## 10–15 min — Reproduce the baseline

From the repository root:

```bash
python shirakami_os.py
python -m pip install pytest
python -m pytest runtime tests -q
```

Record the observed result and environment.

### This establishes

- whether the minimal entry point runs;
- whether the current Runtime/test boundary is executable;
- what the repository's automated tests report at review time.

### This does not establish

- production readiness;
- semantic correctness of arbitrary Protocols;
- correctness of an external AI provider;
- safety of an arbitrary deployment.

## 15–20 min — Run the Evidence route

Run:

```bash
python examples/evidence_route_demo.py
```

Inspect the source as well as the output.

The intended sequence is:

```text
Evidence
   ↓
structural Candidate
   ↓
HUMAN_REVIEW
   ↓
explicit Human Gate
   ↓
READY
   ↓
One-Stroke Runtime
   ↓
Verification
   ↓
Evidence
```

Find the explicit approval call:

```python
pipeline.approve_candidate(approved=True)
```

### Reviewer checkpoint

Verify that candidate generation and authorization are separate operations.

If a reviewer can identify an execution path that bypasses the Human Gate, record it as an observation and verify it against the tests before drawing a conclusion.

## 20–25 min — Inspect the narrow implementation boundary

Read:

- `tools/protocol_route_candidates.py`
- `runtime/one_stroke_route_pipeline.py`
- `runtime/test_one_stroke_route_pipeline.py`

Pay particular attention to:

### Candidate generation

The current route generator is structural.

It uses explicit Protocol artifact boundaries and structural input/output relationships. It does not establish semantic compatibility merely because two Protocols can be connected structurally.

### Execution

The one-stroke pipeline executes only the selected route after the Human Gate.

Missing implementations are expected to fail closed.

### Verification

A successful expected transition can reach `ACCEPTED`.

A mismatch reaches `DIFF`; it is not silently converted into acceptance.

### Evidence

Evidence records the observed execution boundary. It is not itself an authorization mechanism.

## 25–30 min — Compare specification and implementation

Inspect the normative repository:

- [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification)

For the current route work, compare:

- One-Stroke Route Pipeline α0.2
- Evolution Loop One-Stroke Route α0.3

Use this distinction:

```text
Normative Specification
        ≠
Implementation
        ≠
Evidence
        ≠
Research Hypothesis
```

### Final review record

A useful review can end with four short lists:

#### Reproduced

What did you personally run or inspect successfully?

#### Verified

What invariant is supported by code + tests + specification?

#### Unverified

What remains outside the current evidence boundary?

#### Disputed

Where does your interpretation differ from the project's documented interpretation?

A disagreement is valuable only if it remains traceable to an observation, code path, test, or specification.

## Minimum Review Output

A reviewer should be able to answer these three questions after 30 minutes:

1. **What does Shirakami OS actually do today?**
2. **Where is execution authority granted?**
3. **What important claims remain unverified?**

If those questions cannot be answered from the repository, the review route itself needs improvement.

## Review Principle

> **Do not ask the repository to prove more than its Evidence can support.**

The purpose of this guide is therefore not to make Shirakami look complete.

It is to make the boundary between **implemented, observed, specified, and still unknown** easy to see.
