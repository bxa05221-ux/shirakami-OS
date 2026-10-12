# Shirakami OS — Contest Prototype Acceptance v0.1

Status: Working acceptance contract  
Base: current `main` at branch creation  
Purpose: define the smallest demonstrable prototype that can be submitted to a technical or innovation contest.

This document is a delivery boundary, not a new kernel milestone. It must not reopen completed milestones merely because more tests or features are possible.

## 1. Prototype claim

Shirakami OS is not a new LLM. It is a runtime architecture that structures context, protocol execution, evidence, verification, and human authority around replaceable AI runtimes.

Core claim for the demonstration:

> AI may propose or simulate; it does not gain decision authority. Execution that requires human approval must pass an explicit Human Gate, and the result must be inspectable.

## 2. Primary demonstration

Use the existing five-minute route-loop demo as the deterministic baseline:

```bash
python examples/evidence_route_demo.py
```

Expected observable sequence:

1. Evidence is used to generate a structural candidate.
2. Candidate enters `HUMAN_REVIEW`.
3. Explicit approval moves the runtime to `READY`.
4. The selected route executes.
5. Verification produces an observable result.
6. Evidence is retained for inspection.

The demo must run from a clean checkout without provider credentials. It demonstrates the protocol and authority boundary, not the behavior of a real external model.

## 3. Required acceptance checks

### A. Reproducible baseline

- [ ] A new reviewer can follow `docs/architecture/MVP_QUICKSTART.md`.
- [ ] `python shirakami_os.py` completes.
- [ ] `python examples/evidence_route_demo.py` completes and displays the sequence above.
- [ ] `python -m pytest runtime tests -q` passes on the stated Python version.
- [ ] Commands and actual observed output are recorded for the candidate commit.

### B. Human Gate behavior

- [ ] Candidate generation alone does not authorize execution.
- [ ] The explicit approval point is visible in the demo.
- [ ] A rejection or invalid authority path is demonstrated or covered by a focused test.
- [ ] Runtime/model output cannot directly mutate canonical state or bypass the Human Gate.
- [ ] Any claim is limited to the boundary actually tested; do not imply production identity assurance without evidence.

### C. Evidence and verification

- [ ] The demo shows the result and verification status.
- [ ] Evidence/trace references or records can be inspected after execution.
- [ ] Verified observations are distinguished from interpretation and unverified assumptions.
- [ ] A failed or rejected path is observable rather than silently treated as success.

### D. External AI provider path

The current API MVP status records items 1–8 as verified, while items 9–10 remain pending until a real external provider executes through the HTTP path and the resulting output is verified through Evidence/Trace.

- [ ] Choose one provider/model only for the demo; do not make the kernel provider-specific.
- [ ] Supply credentials through environment/configuration outside source control.
- [ ] Run the real provider through the HTTP/API → adapter → runtime → Evidence/Trace path.
- [ ] Exercise the API as a stateful sequence: `/v1/observe` → `/v1/analyze` → explicit `/v1/approve` with `human_authorized=true` → `/v1/execute` → `/v1/executions/{id}/verify`.
- [ ] Confirm an execution attempt before approval is rejected, and a rejected approval does not permit execution.
- [ ] Confirm response metadata continues to report `execution_authorized=false`, `publish_authorized=false`, `merge_authorized=false`, and `human_gate_required=true`; do not confuse a completed Runtime operation with transfer of decision authority.
- [ ] Save a redacted run record with commit, command, outcome, and verification evidence.
- [ ] Verify that model output does not itself grant authority.
- [ ] Never commit API keys, personal data, or sensitive request/response content.

This is the strongest contest demonstration, but it must not block preparing the deterministic baseline and its evidence.

## 4. Submission package

The prototype is ready for contest packaging when:

- [ ] One canonical commit is selected.
- [ ] The baseline demo and required test suite pass on that commit.
- [ ] At least one invalid/rejected authority path is shown.
- [ ] Real-provider HTTP E2E is either verified, or explicitly identified as a limitation if the target contest permits a provider-neutral prototype.
- [ ] A reviewer can reproduce the demonstration using the documented commands.
- [ ] The submission states what is implemented, what was tested, what remains unverified, and the exact environment.
- [ ] A short architecture diagram and a 2–3 minute demo script use only claims supported by evidence.

## 5. Explicit non-goals for this delivery

Do not require the following to package this prototype:

- a polished commercial UI;
- production deployment or multi-user operations;
- support for multiple AI providers in the demo;
- integration of Anka (currently frozen);
- a ThreadRPG-specific runtime;
- new kernel invariants without a demonstrated gap;
- an ever-growing test count as a proxy for completion.

## 6. Delivery gate

The prototype is considered **contest-demonstrable** when sections 2, 3A, 3B, 3C, and the submission package have evidence on one fixed commit. The real-provider path in 3D is a preferred strengthening gate; if not completed, the submission must describe the limitation accurately.

No percentage is used as a substitute for this checklist. Once the gate is met, stop expanding scope and prepare the actual contest application.

## 7. Current evidence at document creation

- An existing deterministic five-minute demo is present at `examples/evidence_route_demo.py`.
- An MVP quickstart is present at `docs/architecture/MVP_QUICKSTART.md`.
- `docs/api/API_MVP_VERIFICATION_STATUS.md` explicitly distinguishes the verified provider-neutral boundary from pending real-provider execution through the HTTP path.
- These source files establish a starting point, not a claim that all acceptance checks have been rerun on this branch.
