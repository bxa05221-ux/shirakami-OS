# R0007 Protocol Migration Trace

Status: trace recorded
Trace type: research → gate → implementation → verification → evidence
Scope: R0007 / R0007 Test 01 / current R0010 boundary

## 1. Research source

- Research ref: `bxa05221-ux/shirakami-research:research/architecture/R0007-protocol-migration-contract.md`
- Status: `experimental_contract`
- Requirement: Protocol migration is itself a new transition; historical Evidence identity, provenance, original Protocol version, lineage, migration source/target, rationale, verification state, and semantic effect remain recoverable.
- Boundary: migration must not rewrite historical Evidence.
- Non-claim: automatic migration algorithms are not established.

## 2. Research test source

- Research ref: `bxa05221-ux/shirakami-research:research/architecture/R0007-test-01-semantic-protocol-migration.md`
- Status: `experimental_contract`
- Test finding: semantic Protocol change requires re-evaluation, not textual conversion.
- Required negative behavior: when v2 information is insufficient, migration is incomplete and missing information is not fabricated.
- Required lineage: historical v1 interpretation remains recoverable and new v2 evaluation is a new transition.

## 3. Implementation gate

Gate decision: **BLOCKED for automatic Protocol migration implementation**.

Reason:

1. R0007 is an `experimental_contract`.
2. Its non-claim explicitly excludes automatic migration algorithms.
3. Current R0010 Runtime boundary requires accepted Protocol/Research artifacts before semantic expansion.

This trace records the boundary; it does not promote R0007 into Runtime core semantics.

## 4. Current Runtime correspondence

Current β0.1 Runtime already preserves the surrounding invariants:

- Execution produces immutable EvidenceRecord.
- Evidence is projected into LandscapeState rather than rewritten.
- Landscape can be replayed from preserved Evidence.
- Replay order is observable when later Evidence overwrites projected keys.

These are supporting boundaries only. They do not constitute implementation of Protocol migration.

## 5. Verification correspondence

Relevant existing verification:

- multi-stage Evidence history preservation;
- Evidence immutability across stages;
- failed transition does not propagate to Landscape;
- deterministic Evidence replay reconstructs Landscape;
- replay order dependence is explicitly recorded in R0010.

The existing tests verify Evidence/Landscape preservation properties that R0007 depends on, but they do not verify semantic migration itself.

## 6. Evidence boundary

```text
R0007 research
    ↓
R0007 Test 01
    ↓
Implementation Gate: BLOCKED
    ↓
Current R0010 β0.1 Evidence/Landscape boundary
    ↓
Existing verification evidence
```

No synthetic Evidence is created to claim a migration that has not occurred.

## 7. Next admissible step

A future migration implementation requires a separately accepted research/specification artifact defining the concrete migration execution boundary and verification target.

Until then:

- do not add automatic migration algorithms to Runtime core;
- do not rewrite historical Evidence;
- do not label existing β0.1 replay tests as R0007 migration verification.
