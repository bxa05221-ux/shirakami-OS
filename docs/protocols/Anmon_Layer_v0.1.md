# Anmon Layer v0.1

## 1. Purpose

Anmon Layer is a pre-execution inquiry boundary for Shirakami Protocol generation.
It does not decide, authorize, execute, or verify. Its role is to expose ambiguity,
assumptions, missing context, and decision points before a Protocol Candidate is
reviewed by a human.

> Anmon does not produce the answer first. It makes the question and its conditions visible.

## 2. Position in the architecture

```text
Human context / Origin
        ↓
Anmon Layer
  - observations
  - interpretations
  - uncertainties
  - assumptions
  - questions
  - stop conditions
        ↓
Protocol Candidate
        ↓
Human review / authorization
        ↓
Execution
        ↓
Evidence / evaluation
```

Anmon is a boundary between intention and implementation. It must not be treated
as an execution authority or as a substitute for human judgment.

## 3. Mandatory separations

Anmon must keep the following elements distinct:

1. **Observation** — what is explicitly available or recorded.
2. **Interpretation** — a provisional reading of the observation.
3. **Uncertainty** — what is unknown, ambiguous, or not verified.
4. **Assumption** — a condition temporarily introduced to proceed.
5. **Question** — what requires clarification or human response.
6. **Constraint** — a boundary that must be respected.
7. **Stop condition** — a condition under which generation or execution must pause.
8. **Decision gate** — the point where human authorization is required.

An interpretation must not be presented as an observation. An assumption must not
be silently promoted to a fact. Confidence must not be used as proof of truth,
safety, consent, or authorization.

## 4. Minimal output contract

A conforming Anmon result should expose the following structure:

```yaml
anmon:
  id: anmon-<unique-id>
  version: "0.1"
  origin: "<source of the request>"
  intent: "<stated human intent>"
  observations:
    - id: obs-001
      content: "<explicitly available information>"
      source: "<source or context>"
  interpretations:
    - id: int-001
      content: "<provisional reading>"
      based_on: [obs-001]
      confidence: "unstated|low|medium|high"
  uncertainties:
    - id: unc-001
      content: "<unknown or ambiguous point>"
      impact: "<why it matters>"
  assumptions:
    - id: asm-001
      content: "<temporary assumption>"
      owner: "human|system|unspecified"
      reversible: true
  questions:
    - id: q-001
      question: "<clarifying question>"
      required: true
      target: "human|source|environment"
  constraints:
    - "<boundary that must be preserved>"
  stop_conditions:
    - "<condition requiring pause>"
  decision_gates:
    - id: gate-001
      reason: "<why human authorization is required>"
      status: "pending"
  next_action: "candidate_generation|clarification|stop"
```

This YAML is an illustrative contract, not an authorization mechanism. Field
presence alone does not establish validity or semantic correctness.

## 5. Operating rules

- Begin with the smallest useful set of questions.
- Preserve the user's stated intent without silently expanding it.
- Surface missing information instead of inventing it.
- Preserve alternative interpretations when ambiguity remains.
- Mark assumptions explicitly and make them reversible where possible.
- Identify conditions that require clarification before Protocol generation.
- Do not infer consent, authority, safety, truth, or priority from language confidence.
- Do not automatically execute a generated Protocol.
- Do not convert an unresolved question into a hidden default.
- Keep domain-specific judgment outside the Anmon boundary unless explicitly supplied by a human or a verified external source.
- Record interruption, refusal, mismatch, and unanswered-question paths.

## 6. Human control boundary

Anmon may recommend that clarification is needed, but it cannot answer on behalf
of the human when the answer changes intent, authorization, consent, risk, or
responsibility.

The human may:

- answer or reject a question;
- revise the stated intent;
- accept, replace, or remove an assumption;
- authorize Protocol Candidate generation;
- stop the process.

The system must preserve the distinction between a human response and a system
inference.

## 7. Review checklist

A reviewer should be able to confirm:

- [ ] Observations are traceable to available context.
- [ ] Interpretations are labeled as provisional.
- [ ] Uncertainties and assumptions are visible.
- [ ] Questions are specific enough to answer or reject.
- [ ] Constraints and stop conditions are explicit.
- [ ] Human decision gates are identified.
- [ ] No execution authority is implied.
- [ ] No unresolved ambiguity is silently converted into a default.
- [ ] The output can be handed to Protocol Generation Policy v0.1.

## 8. Non-goals

Anmon Layer v0.1 does not attempt to:

- make final decisions;
- determine domain truth automatically;
- infer consent or authorization;
- replace professional or human judgment;
- guarantee safety through confidence scores;
- execute or verify Protocols;
- eliminate ambiguity from human contexts;
- impose a single interpretation when alternatives remain.

## 9. Relationship to Protocol Generation Policy

Anmon is a preparation and boundary layer. Its output may become an input to
Protocol Generation Policy v0.1, but it does not itself create an executable
Protocol. The generated Protocol remains a candidate for human inspection and
authorization.
