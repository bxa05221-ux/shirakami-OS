# R0040 Trace Integrity Adversarial Verification

## Purpose

R0040 deliberately presents malformed or crossed records to the executable Shirakami trace boundary.

The goal is not to prove that the system is correct in every domain. The goal is to verify that explicit identity and decision boundaries fail closed or remain observable when records are missing, crossed, rejected, or altered.

## Adversarial cases

- missing required Evidence blocks Protocol routing
- blocked routing cannot become an executable Prompt
- crossed Prompt / Simulation IDs are rejected by AIwitness
- crossed HumanDecision / Simulation IDs are rejected by Operation
- rejected HumanDecision cannot authorize Operation
- crossed Decision / Operation records are rejected by reconstruction
- missing resulting Evidence is not invented
- Context-version changes remain observable
- Runtime failures become observable failed Simulation results

## Interpretation

A passing R0040 run means these specific boundary invariants are executable and automatically checked.

It does not establish model accuracy, domain safety, completeness of Reality capture, or correctness of a human decision.
