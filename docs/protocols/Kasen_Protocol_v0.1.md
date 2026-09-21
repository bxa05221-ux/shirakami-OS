# Kasen Protocol v0.1

## 1. Purpose

Kasen（歌仙）は、複数の文脈・視点・記録を、連歌のように段階的に接続しながら、意味の展開と差異の保持を支援する documentation-level protocol である。

Kasen does not produce a single authoritative conclusion. It supports human inspection of how one contribution responds to, extends, questions, or redirects another.

## 2. Core Principles

- Each contribution retains its origin, context, provenance, and uncertainty.
- A response may connect to a prior contribution without being treated as proof of it.
- Continuity and divergence are both valid outcomes.
- Generated text is a proposed contribution, not an authorized decision.
- Interpretation must remain distinguishable from observation and quotation.
- Human judgment remains the boundary for acceptance, execution, and responsibility.

## 3. Contribution Model

Each Kasen contribution should record, where applicable:

- `id`: stable contribution identifier
- `origin`: person, system, document, or process that produced it
- `context`: relevant situation and scope
- `preceding_refs`: contributions being answered or extended
- `observation`: directly available material
- `interpretation`: meaning assigned to that material
- `intent`: purpose of the contribution
- `relation`: extend, respond, question, contrast, redirect, summarize, or unknown
- `uncertainty`: unresolved ambiguity or limitation
- `evidence_refs`: supporting records
- `status`: IDEA, CANDIDATE, REVIEWED, ACCEPTED, REJECTED, or SUPERSEDED
- `human_boundary`: pending human review, decision, or approval

## 4. Operating Procedure

1. Identify the contribution and its source.
2. Record the preceding context without rewriting it silently.
3. Separate observation, quotation, and interpretation.
4. Generate or register the next contribution as a candidate.
5. Identify continuity, divergence, unanswered questions, and new assumptions.
6. Preserve alternative routes rather than forcing convergence.
7. Present the sequence and its relations for human inspection.
8. Promote, accept, execute, or archive only through an explicit human-controlled boundary.

## 5. Prohibited Behavior

Kasen must not:

- silently alter or overwrite prior contributions;
- convert sequence into causality, agreement, truth, or authority;
- treat repetition as verification;
- fabricate provenance, quotations, consent, or evidence;
- collapse conflicting viewpoints into an artificial consensus;
- authorize execution or external action automatically;
- present generated contributions as statements from real people;
- hide uncertainty, missing context, or unresolved branches.

## 6. Illustrative Structure

```yaml
kasen:
  id: kasen-session-001
  contributions:
    - id: c001
      origin: human
      context: initial inquiry
      observation: "available source material"
      interpretation: null
      intent: propose
      relation: initial
      uncertainty: []
      evidence_refs: []
      status: CANDIDATE
      human_boundary: review_required
    - id: c002
      origin: ai
      context: response to c001
      preceding_refs: [c001]
      observation: "c001 as received"
      interpretation: "explicitly marked interpretation"
      intent: extend
      relation: extend
      uncertainty: ["interpretation requires human confirmation"]
      evidence_refs: []
      status: CANDIDATE
      human_boundary: review_required
```

## 7. Stop Conditions

The process must pause when:

- provenance cannot be established;
- the preceding context is ambiguous;
- an interpretation is being mistaken for an observation;
- conflicting contributions are being silently reconciled;
- a request would require authorization, consent, or execution;
- evidence is insufficient for the proposed claim;
- the human decision boundary is unclear.

## 8. Non-goals

Kasen is not:

- an autonomous deliberation authority;
- a truth, safety, or consent evaluator;
- a replacement for Evidence or verification;
- a mechanism for automated authorization;
- a method for manufacturing consensus;
- a personality simulation of contributors.

## 9. Status

Documentation-only protocol definition. No runtime behavior is introduced by this document.
