# Anmon Layer Consistency Audit v0.1

- **Scope:** Anmon Layer v0.1 and its registry/mapping references
- **Audit mode:** Documentation and repository evidence review
- **Status:** Partial audit — follow-up required
- **Date:** 2026-09-22

## 1. Confirmed alignment

The Anmon Layer document is aligned with the shared Shirakami boundary principles in the following respects:

- It is a pre-execution inquiry boundary.
- It does not decide, authorize, execute, or verify.
- It separates observations, interpretations, uncertainties, assumptions, questions, constraints, stop conditions, and decision gates.
- It preserves human review and authorization before Protocol Candidate execution.
- It prohibits silent defaults and requires uncertainty and interruption paths to remain visible.

Primary source: `docs/protocols/Anmon_Layer_v0.1.md`.

## 2. Human Gate finding

**Status: Confirmed in protocol text.**

The protocol explicitly identifies human review/authorization as a boundary after Protocol Candidate generation and permits the human to revise intent, accept or reject assumptions, authorize candidate generation, or stop the process.

This confirms the intended responsibility boundary at the documentation level. Runtime enforcement and dedicated automated tests were not established by this audit entry.

## 3. Evidence finding

**Status: Requires verification.**

The protocol places Evidence/evaluation after execution in its architecture diagram and requires interruption, refusal, mismatch, and unanswered-question paths to be recorded. However, this audit did not establish that Anmon outputs and those exceptional paths are currently persisted in a traceable Evidence structure through implementation and tests.

No semantic change is proposed in this audit document.

## 4. Five-turn observation boundary discrepancy

**Status: Mismatch / unresolved.**

Repository registry and mapping references describe the Anmon Layer as preserving a “five-turn observation boundary.” The current Anmon Layer v0.1 protocol document does not define:

- what constitutes a turn;
- the exact five-turn procedure or limit;
- how the boundary behaves when clarification remains unresolved;
- an implementation mechanism; or
- an automated test demonstrating the boundary.

Therefore, the registry claim cannot currently be treated as a verified protocol requirement. It must remain an audit finding until the canonical source, implementation, and test evidence are connected.

**Required follow-up:** either document the five-turn boundary as a normative rule with examples and tests, or qualify/remove the registry note through an explicitly reviewed change. This audit does not make that semantic decision.

## 5. Responsibility boundary

**Status: Confirmed in protocol text; runtime status unconfirmed.**

The document clearly states that Anmon is not an execution authority and cannot infer consent, authorization, safety, truth, or priority from confidence or language. Repository-level implementation and test coverage still require separate verification.

## 6. Audit conclusion

Anmon Layer v0.1 is conceptually clear regarding inquiry, uncertainty exposure, and human control. Its principal consistency issue is the unsubstantiated “five-turn observation boundary” claim in repository metadata. The next audit step is to locate or add implementation and test evidence without silently redefining the protocol.
