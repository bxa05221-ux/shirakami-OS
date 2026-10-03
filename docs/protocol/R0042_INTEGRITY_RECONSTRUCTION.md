# R0042 — Integrity Reconstruction

R0040 detects adversarial trace breaks.
R0041 classifies observable failure modes.
R0042 reconstructs the relationship between the trace and those findings.

The purpose is not to determine a hidden cause. It is to preserve what was
observably inconsistent, where it occurred in the trace, and which Context
version was involved.

## Boundary

R0042 does not:
- repair the trace;
- infer intent or hidden causes;
- decide whether a human decision was correct;
- rewrite missing Evidence.

## Flow

Evidence → Context → Matrix → Protocol → Prompt → Simulation → AIwitness
→ Human Decision → Operation → Evidence
→ Integrity Classification → Integrity Reconstruction

## Result

An IntegrityReconstruction preserves:
- reconstruction ID;
- linked witness/prompt/protocol/simulation/decision/operation IDs;
- Context version;
- deterministic failure classifications.

The reconstruction itself can be serialized as an Evidence-shaped record.

This establishes a closed forensic loop for observable integrity failures.
