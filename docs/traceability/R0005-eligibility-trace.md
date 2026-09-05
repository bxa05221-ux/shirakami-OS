# R0005 Eligibility Trace

Status: trace recorded
Trace type: research → gate → implementation → verification → evidence
Scope: R0005 / R0005 Test 01

## 1. Research source

- Research ref: `bxa05221-ux/shirakami-research:research/architecture/R0005-protocol-declared-eligibility.md`
- Status: `experimental_contract`
- Research conclusion: Protocol may declare eligibility requirements, permitted transitions, verification rules, and semantic effects; Runtime evaluates the declared contract without embedding domain-specific semantic truth.
- Boundary: Runtime must not silently redefine immutable Evidence.
- Non-claim: the research artifact does not establish a finalized YAML schema.

## 2. Research test source

- Research ref: `bxa05221-ux/shirakami-research:research/architecture/R0005-test-01-eligibility-rejection.md`
- Status: `experimental_contract`
- Test distinction:
  - `accepted` for verification
  - `rejected` at eligibility
  - `verified` without semantic effect
  - `verified` with semantic effect
- Required negative behavior: rejection is observable with reason and applicable Protocol reference.
- Non-claim: final error model and API response format are not established.

## 3. Implementation gate

Gate decision: **BLOCKED for Rich Protocol Semantics implementation**.

Reason:

1. R0005 is explicitly an `experimental_contract` rather than a finalized schema.
2. The current Runtime β0.1 boundary deliberately defers executable Rich Protocol Semantics.
3. Therefore R0005 may be traced and used as an implementation target, but its semantic eligibility DSL must not be implemented as Runtime core behavior yet.

This is a traceability record, not a promotion of R0005 into Foundation or normative Runtime semantics.

## 4. Current implementation correspondence

Existing implementation correspondence is narrower than R0005:

- `runtime/current_protocol.py` checks lifecycle eligibility through `ProtocolRegistry.select_current()` before loading a current Protocol.
- This is **not** the R0005 semantic eligibility contract.
- No claim is made that current Runtime β0.1 implements `eligibility.require`, semantic-effect selection, or the full R0005 transition model.

## 5. Verification correspondence

Existing verified Runtime boundaries provide supporting evidence but do not verify R0005 itself:

- Landscape projection chain verification
- multi-stage Evidence history preservation
- Evidence immutability across stages
- failed transition does not propagate to Landscape
- deterministic Evidence replay reconstructs Landscape

These verify the surrounding β0.1 Evidence/Landscape boundaries. They must not be labeled as proof that R0005 Rich Protocol Semantics has been implemented.

## 6. Evidence boundary

Current Evidence implementation records observable execution transitions and preserves them immutably.

Trace implication:

```text
R0005 research
    ↓
R0005 Test 01
    ↓
Implementation Gate: BLOCKED
    ↓
Current β0.1 Runtime boundary
    ↓
Existing Evidence / Landscape verification
```

No Evidence record is synthesized here to claim a semantic R0005 implementation that has not occurred.

## 7. Next admissible step

The next implementation step requires a separately accepted research/specification artifact that fixes the concrete Rich Protocol Semantics boundary and verification target.

Until then:

- do not add semantic eligibility logic to Runtime core;
- do not reinterpret existing β0.1 tests as R0005 verification;
- preserve this trace as the explicit reason for the implementation gate.
