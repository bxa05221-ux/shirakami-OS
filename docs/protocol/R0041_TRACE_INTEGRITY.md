# R0041 — Trace Integrity Failure Classification

## Purpose

R0040 verifies that adversarially broken traces are rejected or remain observable.
R0041 adds a deterministic classification layer so an observed integrity failure
has a machine-readable code.

The classification layer does not repair a trace, infer missing facts, or make a
human decision.

## Failure codes

| Code | Meaning |
| --- | --- |
| `EVIDENCE_MISSING` | Required Evidence is unavailable and routing is blocked |
| `PROMPT_SIMULATION_MISMATCH` | Prompt and Simulation identifiers differ |
| `PROTOCOL_SIMULATION_MISMATCH` | Protocol and Simulation identifiers differ |
| `WITNESS_SIMULATION_MISMATCH` | AIwitness and Simulation identifiers differ |
| `DECISION_SIMULATION_MISMATCH` | HumanDecision and Simulation identifiers differ |
| `HUMAN_APPROVAL_MISSING` | Explicit human approval is absent |
| `DECISION_OPERATION_MISMATCH` | HumanDecision and Operation identifiers differ |
| `CONTEXT_TAMPERED` | Observed Context version differs from the expected version |
| `RUNTIME_FAILURE` | Simulation Runtime returned an observable failure |
| `RESULT_EVIDENCE_MISSING` | Reality change is reported without resulting Evidence |

## Evidence preservation

Findings can be serialized as an Evidence-shaped record:

`kind: trace_integrity_findings`

The record contains the classification code, severity, and observable detail.
It does not claim why the failure happened beyond the available identifiers and
state.

## Verification boundary

R0041 verifies classification, not system correctness. A passing run means the
known adversarial cases receive deterministic classifications.

The intended loop is now:

Evidence → Context → Matrix → Protocol → Prompt → Simulation → AIwitness
→ Human Decision → Operation → Evidence
→ **Integrity Classification**

Thus, when the chain is broken, Shirakami can not only reject or expose the break;
it can preserve a machine-readable account of the observed failure.
