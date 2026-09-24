# CLP-R2R-01 Approval Boundary

## Purpose

Record the verified boundary between the CLP-09~20 Research-to-Runtime handoff and the existing Runtime `HumanGate` / `ApprovalEnvelope` implementation.

## Finding

The repository already contains `runtime/human_gate.py` and `runtime/approval_envelope.py`.
The existing `ApprovalEnvelope` is an execution/publication authorization envelope with `candidate_id`, `protocol_id`, provenance, evidence references, reviewer, scope, and authorization flags.

The CLP-R2R-01 minimum model uses `ApprovalEnvelope` as a meaning-side handoff after a human decision about an `InterpretationRecord`.

These are related but not identical boundaries.

## Decision

Do not replace or overload the existing `ApprovalEnvelope` in this slice.
Do not infer semantic approval from execution authorization.
Do not add interpretation-specific fields to the existing envelope merely to force the two models together.

The minimum Runtime chain remains:

```text
EvidenceRecord
  -> InterpretationRecord
  -> DecisionRecord
  -> DecisionLineage
  -> HumanGate
```

The existing execution/publication `ApprovalEnvelope` remains a separate downstream authorization boundary.

## Required future adapter

If a later Runtime slice connects the two boundaries, it must explicitly carry:

- decision_id
- target_interpretation_id
- human actor identity
- timestamp
- approval scope

without implying that semantic approval automatically grants execution or publication authority.

## Verification rule

A semantic Decision is not an execution authorization.
An execution ApprovalEnvelope is not evidence that an Interpretation is true.

This document is an implementation finding, not a new Research hypothesis.
