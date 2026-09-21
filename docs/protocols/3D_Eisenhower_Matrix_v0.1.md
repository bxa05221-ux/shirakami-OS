# 3D Phase-Rotating Eisenhower Matrix v0.1

## 1. Purpose

This protocol organizes candidate actions without allowing an AI system to silently determine human priorities. It extends the familiar urgent/important distinction with contextual dimensions and explicit phase rotation.

The matrix is a **decision-support representation**, not an autonomous prioritization authority.

## 2. Position in Shirakami

```text
Human context / Anmon output
        ↓
Priority candidates
        ↓
3D phase-rotating matrix
        ↓
Human review / selection
        ↓
Protocol Candidate
```

Anmon exposes ambiguity and missing conditions. The matrix makes competing priorities visible. Human judgment remains responsible for selection, deferral, delegation, or refusal.

## 3. Three dimensions

A candidate item should be represented across three contextual dimensions:

1. **Importance** — consequence or value relative to the stated intent.
2. **Urgency** — time pressure, deadline, or deterioration risk.
3. **Phase** — the current operating context, such as preparation, response, recovery, maintenance, or learning.

Importance and urgency must be supported by explicit evidence or human statements. Phase is contextual and may change over time.

## 4. Phase rotation

A phase rotation is a deliberate re-evaluation when context changes. It must not be treated as proof that an item has objectively changed priority.

Rotation triggers may include:

- a new deadline or loss of time pressure;
- a change in available resources;
- new evidence or an unresolved contradiction;
- a change in risk, consent, authority, or human intent;
- interruption, refusal, or environmental change.

Each rotation should preserve the previous view so that changes remain traceable.

## 5. Minimal YAML representation

```yaml
priority_matrix:
  id: matrix-<unique-id>
  version: "0.1"
  intent_ref: "<human intent or Anmon reference>"
  phase:
    name: preparation
    basis: "<explicit context>"
  items:
    - id: item-001
      description: "<candidate action>"
      importance:
        value: high
        basis: "human|evidence|unspecified"
      urgency:
        value: medium
        basis: "human|evidence|unspecified"
      phase_fit: "<why this phase matters>"
      dependencies: []
      uncertainty_refs: []
      proposed_position: "do|schedule|delegate|consider|hold"
      human_decision: pending
  rotation:
    triggered_by: "<context change>"
    previous_phase: null
    current_phase: preparation
    preserved_previous_view: true
  decision_gate:
    required: true
    status: pending
```

The representation is descriptive. `proposed_position` is a candidate, not an instruction. `human_decision` must not be inferred from model confidence or item order.

## 6. Operating rules

- Do not equate urgency with importance.
- Do not treat importance as universal; bind it to the stated intent and context.
- Do not create numerical scores unless their meaning and source are explicit.
- Preserve ties, alternatives, and unresolved uncertainty.
- Never silently discard an item because it is difficult to classify.
- Re-evaluate after a phase rotation rather than mutating history.
- Keep delegation and refusal as human-controlled decisions.
- Pause when authority, consent, safety, or responsibility is unclear.
- Record the basis for every proposed position.
- Keep execution and verification outside this representation.

## 7. Review checklist

- [ ] Every item is traceable to an intent or source context.
- [ ] Importance and urgency have visible bases.
- [ ] The current phase is explicit.
- [ ] Rotation triggers are recorded.
- [ ] Previous views remain available.
- [ ] Alternatives and ties are preserved.
- [ ] Proposed positions are not treated as commands.
- [ ] Human decision gates are visible.
- [ ] Uncertainty and stop conditions remain linked.
- [ ] No execution or semantic verification is implied.

## 8. Non-goals

This version does not attempt to:

- make final decisions for humans;
- predict the objectively correct priority;
- convert contextual judgments into universal scores;
- automatically execute, delegate, or cancel actions;
- erase historical priority views;
- replace domain expertise or human responsibility.

## 9. Relationship to Anmon and Protocol Generation

Anmon provides questions, assumptions, uncertainties, constraints, and decision gates. The matrix arranges candidate actions while preserving those references. Protocol Generation Policy may use the reviewed matrix as input, but no item becomes executable without the applicable human authorization boundary.
