# Shirakami OS — Public Verification Pack

## Purpose

This document is a compact verification route for a first-time external reviewer.

It is not a certification, benchmark, or claim of production readiness. It records what a reviewer can reproduce from the public repository and what each check does — and does not — establish.

## 1. Repository orientation

Start with:

1. [README](../README.md)
2. [Reviewer Entry Point](architecture/REVIEWER_ENTRY_POINT.md)
3. [MVP Quickstart](architecture/MVP_QUICKSTART.md)
4. [Five-minute Runtime Demo](../examples/evidence_route_demo.py)

The intended review path is:

```text
Understand
   ↓
Inspect boundaries
   ↓
Run
   ↓
Observe
   ↓
Compare implementation with specification
```

## 1.5 30-minute route

For a timed first-pass review, use the [30-Minute External Review Guide](EXTERNAL_REVIEW_GUIDE_30MIN.md). It is a practical companion to this pack and does not expand the verification claims made here.

## 2. Reproduce the minimal Runtime

Requirements:

- Python 3.11+
- Git
- pytest for the verification suite

From the repository root:

```bash
python shirakami_os.py
python -m pip install pytest
python -m pytest runtime tests -q
```

### This establishes

- the minimal executable entry point can be invoked;
- the repository's Runtime and regression tests can be executed;
- the current test suite provides an executable verification boundary.

### This does not establish

- production readiness;
- semantic correctness of every Protocol;
- correctness of an external AI provider;
- correctness of arbitrary user-defined Protocols;
- safety of an arbitrary deployment environment.

## 3. Reproduce the Evidence-driven route loop

Run:

```bash
python examples/evidence_route_demo.py
```

The demonstration uses temporary Protocol artifacts and no external AI provider.

Review the output for this sequence:

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

The demo intentionally keeps the authorization step explicit in the source:

```python
pipeline.approve_candidate(approved=True)
```

Candidate generation itself does not authorize execution.

## 4. Inspect the implementation boundary

The shortest implementation path is:

- `tools/protocol_route_candidates.py`
  - derives structural n-gram candidates;
  - accepts Evidence-derived candidates only from explicit `protocol_path` fields;
  - does not infer semantic compatibility.
- `runtime/one_stroke_route_pipeline.py`
  - moves a selected candidate into `HUMAN_REVIEW`;
  - resolves the existing R0100 Human Gate;
  - executes only an approved candidate;
  - verifies the resulting route transition.
- `runtime/test_one_stroke_route_pipeline.py`
  - tests fail-closed approval;
  - tests execution and verification;
  - tests Evidence-derived proposals;
  - tests mismatch handling.

## 5. Inspect the normative boundary

Stable normative contracts live in the separate [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification) repository.

For the current route integration, inspect:

- One-Stroke Route Pipeline α0.2
- Evolution Loop One-Stroke Route α0.3

The implementation-side α0.4 bridge is documented in [Evidence → Route Candidate Bridge](EVIDENCE_ROUTE_CANDIDATE_ALPHA_0_4.md).

A reviewer should distinguish:

```text
Specification
     ≠
Implementation
     ≠
Evidence
     ≠
Research hypothesis
```

## 6. Safety boundary to verify

The central invariant is:

> A Route Candidate may be proposed by structure or Evidence, but only explicit human approval may authorize execution.

Check the implementation and tests for these properties:

- proposal does not mutate the Evolution Loop into an executable state;
- `HUMAN_REVIEW` precedes authorization;
- `READY` is required for execution;
- missing Protocol implementations fail closed;
- verification mismatch becomes `DIFF`, not silent acceptance;
- Evidence records the observed execution result.

## 7. Review questions

A useful external review does not need to agree with the project's terminology.

Ask:

1. Can the claimed Runtime boundary be reproduced?
2. Can a Candidate execute without the Human Gate?
3. Can Evidence silently authorize execution?
4. Does structural compatibility get presented as semantic correctness?
5. Can a verification mismatch silently become acceptance?
6. Can the execution result be traced back to the selected route?
7. Are normative specifications distinguishable from implementation experiments?

Record disagreements as observations and verify them against code, tests, and specifications.

## 8. Public-status interpretation

The repository should currently be described as:

**Publicly inspectable and reproducible Prototype / β-stage Runtime work.**

It should not be described solely on the basis of this pack as:

- production-ready infrastructure;
- a general-purpose autonomous agent safety system;
- a semantic Protocol reasoning engine;
- a guarantee of AI correctness;
- a universal human-context preservation solution.

The purpose of this pack is narrower: make the current implementation boundary easy for an independent person to reproduce, inspect, and challenge.

## 9. Verification checklist

- [ ] README understood
- [ ] Reviewer Entry Point inspected
- [ ] Minimal Runtime executed
- [ ] Test suite executed
- [ ] Evidence route demo executed
- [ ] Human Gate source inspected
- [ ] Evidence-derived candidate source inspected
- [ ] Verification / DIFF behavior inspected
- [ ] Normative specification compared with implementation
- [ ] Any disagreement recorded as an observation rather than silently resolved

## 10. What a successful review means

A successful review does not mean that the reviewer agrees with Shirakami.

It means the reviewer can independently answer:

> **What does this implementation actually do, where are its authority boundaries, and what remains unverified?**

That is the intended public verification boundary.
