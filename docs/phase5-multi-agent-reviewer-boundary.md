# Phase 5 Multi-Agent Reviewer Boundary

## Principle

Multiple agents may provide independent observations, evidence references, Matome YAML context, and proposals. The reviewer layer must not convert those perspectives into an autonomous decision.

## Data flow

`Reviewer registration → Review submission → Comparable perspectives → Human Gate`

## Invariants

- A reviewer must be registered before submitting a review.
- Each review retains its reviewer identity and evidence IDs.
- Matome YAML is preserved as reviewer context, not authority.
- Distinct observations are retained rather than averaged into a synthetic verdict.
- `decision` remains `None` at the reviewer layer.
- `human_gate_required` remains `True`.

## Non-goals

This layer does not implement voting, ranking, confidence aggregation, autonomous approval, merge authorization, or publication authorization.
