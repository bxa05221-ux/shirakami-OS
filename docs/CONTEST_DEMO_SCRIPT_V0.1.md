# Shirakami OS — Contest Demo Script v0.1

Purpose: give a reviewer a reproducible 2–3 minute walkthrough of the current provider-neutral prototype.

## Before the demo

Use a clean checkout of the exact candidate commit. Record the commit SHA and Python version. From the repository root run:

```bash
python shirakami_os.py
python examples/evidence_route_demo.py
python -m pytest runtime tests -q
```

Do not claim these commands passed unless they were run on the candidate commit being submitted. The CI result is useful supporting evidence, but it does not replace checking the exact commit.

## Spoken walkthrough (2–3 minutes)

**0:00–0:25 — What Shirakami is**

“Shirakami OS is not a new language model. It is a model-independent runtime architecture that separates context and protocol handling, evidence, verification, and human decision authority. Its core rule is: AI may propose or simulate, but the decision authority does not move to the AI.”

**0:25–0:55 — Evidence produces a candidate**

Run `python examples/evidence_route_demo.py`. Point to the first output section: observed protocol evidence is used to derive a structural candidate. This is a deterministic demonstration, not a claim that an external model made the decision.

**0:55–1:25 — Human Gate**

Point to `HUMAN_REVIEW`, then the explicit approval step and transition to `READY`. Explain that candidate generation itself is not authorization. The HTTP boundary test also checks that execution before explicit approval is rejected with HTTP 409.

**1:25–1:55 — Runtime and verification**

Point to the selected route, result, verification status, and retained Evidence records. Explain that the execution result is checked and left inspectable rather than treated as self-authorizing.

**1:55–2:25 — What is and is not proven**

“The deterministic demo and CI tests verify the prototype's tested control-flow and traceability boundaries. In addition, the live OpenAI HTTP harness passed: [workflow run 38228522882](https://github.com/bxa05221-ux/shirakami-OS/actions/runs/38228522882) recorded `LIVE_PROVIDER_OBSERVED=true`, `BOUNDARY_OBSERVED=true`, `TRACEABILITY_VALID=true`, and `VERIFICATION_STATUS=pass`. This uses FastAPI TestClient; it does not claim a deployed public server or production operator identity verification.”

**2:25–2:45 — Close**

“The prototype is intentionally bounded. This submission does not claim production identity assurance, a polished commercial UI, or that the model itself is trustworthy. It demonstrates a testable separation between AI output, execution control, evidence, and human approval.”

## Evidence to capture for the submission

- Candidate commit SHA and Python version.
- Terminal output from the three commands above.
- CI links and outcomes tied to the same commit.
- A screenshot or short recording showing `HUMAN_REVIEW`, explicit approval, execution result, verification status, and retained Evidence.
- Include the live OpenAI HTTP workflow result and its exact commit in the evidence pack. State plainly that this is an in-process HTTP harness, not a deployed public server; never relabel fixture mode as a live model run.

## Submission guardrails

- Do not include secrets, personal data, or sensitive prompts/responses in the recording or logs.
- Do not claim “production-ready”, “unbypassable”, “world-first”, or similar absolute statements without independent evidence.
- Do not use test count as a completion percentage. The acceptance contract in `docs/CONTEST_PROTOTYPE_ACCEPTANCE_V0.1.md` is the delivery gate.
