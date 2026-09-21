# Human Gate Integration Audit v0.1

## Status

- Scope: existing Human Gate and selected-route execution boundary
- Result: fail-closed behavior is covered by focused tests; cross-protocol approval metadata remains unstandardized
- Runtime semantics: unchanged
- Authority: human approval remains explicit and external to candidate generation

## Verified behavior

The existing `OneStrokeRoutePipeline` separates:

1. candidate proposal;
2. human review;
3. explicit approval;
4. route execution;
5. verification and Evidence retention.

Focused tests verify that:

- selection without approval raises `PermissionError`;
- execution without an approved route is rejected;
- missing Protocol implementations stop execution;
- approved routes execute and produce verification Evidence;
- Evidence-derived candidates remain unauthorized until human review and approval.

## Boundary findings

### Candidate generation is not authorization

Structural candidates may be generated from Evidence, but generation does not mutate the Evolution Loop into an executable state.

### Approval is fail-closed

The route pipeline requires an explicit approval path before execution. An unapproved candidate cannot be executed through the selected-route boundary.

### Approval vocabulary is local

The implementation uses Evolution Loop states such as `HUMAN_REVIEW` and `READY`, but a shared approval-state envelope across OPPAI, Protocol, Pipeline, Manga, and Radio boundaries is not yet established.

### Evidence continuity

The route pipeline retains execution and verification Evidence. End-to-end propagation of reviewer identity, approval decision, provenance, uncertainty, rights notes, and revision history across every protocol transformation remains unverified.

## Decision

Do not introduce a new universal Human Gate abstraction solely for symmetry. Preserve the existing fail-closed route boundary and collect cross-protocol cases that require a shared contract.

## Next observation target

Test a single selected Protocol/Pipeline handoff carrying:

- candidate identifier;
- reviewer identity;
- approval state;
- approval timestamp or event reference;
- provenance and uncertainty;
- execution authorization scope.

The test must confirm that missing or invalid approval metadata prevents execution and that successful execution does not imply semantic approval.

## Non-goals

- no automatic approval;
- no semantic selection by OPPAI;
- no claim that CI success establishes human authorization;
- no broad Runtime rewrite;
- no replacement of domain-specific review with a universal score.
