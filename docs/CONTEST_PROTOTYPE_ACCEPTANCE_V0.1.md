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

**Updated evidence:** the live OpenAI HTTP observation passed in workflow run [38228522882](https://github.com/bxa05221-ux/shirakami-OS/actions/runs/38228522882), tested commit `4a803ebaf3cce4202ff7c39679d31fdcafc60603`. It emitted `LIVE_PROVIDER_OBSERVED=true`, `BOUNDARY_OBSERVED=true`, `TRACEABILITY_VALID=true`, and `VERIFICATION_STATUS=pass`. The harness used FastAPI TestClient; this is HTTP-boundary evidence, not proof of a deployed public server.

- [x] Select one provider for the demonstration: OpenAI Responses API.
- [x] Supply credentials through repository Actions secrets, outside source control.
- [x] Run the real provider through the HTTP/API → adapter → runtime → Evidence/Trace path.
- [x] Exercise `/v1/observe` → `/v1/analyze` → explicit `/v1/approve` → `/v1/execute` → `/v1/executions/{id}/verify`.
- [x] Confirm an execution attempt before approval is rejected with HTTP 409.
- [x] Confirm `execution_authorized=false`, `publish_authorized=false`, `merge_authorized=false`, and `human_gate_required=true` remain in the response.
- [x] Save a redacted run record: [workflow run 38228522882](https://github.com/bxa05221-ux/shirakami-OS/actions/runs/38228522882), tested commit `4a803ebaf3cce4202ff7c39679d31fdcafc60603`.
- [x] Verify that model output does not itself grant authority.
- [x] Keep API keys and sensitive provider payloads out of source control and logs.

**Scope note:** the harness approval is a test action, not production operator identity verification or an interactive approval UI. The successful run uses FastAPI TestClient and does not claim public-server deployment.

## 4. Submission package

The prototype is ready for contest packaging when:

- [ ] One canonical commit is selected.
- [ ] The baseline demo and required test suite pass on that commit.
- [ ] At least one invalid/rejected authority path is shown.
- [x] Live-provider HTTP harness is verified; production deployment and interactive operator identity assurance remain explicit limitations.
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

The prototype is considered **contest-demonstrable** when sections 2, 3A, 3B, 3C, and the submission package have evidence on one fixed commit. The live-provider HTTP harness gate in 3D has passed. The submission must still describe the in-process TestClient scope and avoid claiming production deployment or operator identity assurance.

No percentage is used as a substitute for this checklist. Once the gate is met, stop expanding scope and prepare the actual contest application.

## 7. Current evidence at document creation

- An existing deterministic five-minute demo is present at `examples/evidence_route_demo.py`.
- An MVP quickstart is present at `docs/architecture/MVP_QUICKSTART.md`.
- `docs/api/API_MVP_VERIFICATION_STATUS.md` records the live OpenAI HTTP harness result and its limits.
- The live-provider result is recorded at [workflow run 38228522882](https://github.com/bxa05221-ux/shirakami-OS/actions/runs/38228522882). The deterministic baseline and full submission package must still be checked against one final candidate commit.
