# Phase 4 → Phase 5 Bridge

## Phase 4: AIwitness

A provenance timeline is now exposed through witness history. Each revision is numbered at the API boundary while the underlying witness store remains append-only.

`Evidence → Execution → Trace → Witness revision 1 → Witness revision 2 → ...`

Revision numbering is observational metadata; it grants no authority.

## Phase 5: Multi-Agent Reviewer Boundary

Multiple reviewers may submit independent `matome_yaml`, observations, evidence IDs, and proposals.

The reviewer boundary deliberately returns:

- comparable perspectives
- linked evidence
- proposals
- `decision: null`
- `human_gate_required: true`

It does not calculate consensus, select a winner, approve execution, publish, or merge.

The design therefore supports multi-agent coexistence without converting plurality into automated authority.
