# Shirakami OS — Contest Prototype Submission Pack v0.1

## Purpose

This pack defines a small, reproducible demonstration of Shirakami OS for a contest or independent technical review. It prioritizes observable behavior and explicit limits over broad claims.

**Status:** public prototype / beta-stage Runtime work. This pack is not a certification or a production-readiness claim.

## One-sentence description

Shirakami OS is a model-independent Runtime architecture for preserving observable context and keeping model output separate from canonical state and execution authority.

## What to demonstrate

The primary demonstration is deterministic and does not require an external AI API key.

From a clean checkout, run these commands from the repository root:

```bash
python -m pip install pytest pyyaml fastapi pydantic httpx
python scripts/contest_demo.py
```

The one-command runner executes these checks in order and stops at the first failure:

1. `python shirakami_os.py` — minimal executable entry point.
2. `python examples/evidence_route_demo.py` — deterministic Evidence-to-Route demonstration.
3. `python -m pytest runtime tests -q` — Runtime and regression test suite.

For a step-by-step live presentation, run the three commands above individually after installing dependencies. The runner does not call an external AI provider and does not require an API key.

The repository's fixed GitHub Actions acceptance workflow independently runs the same three core checks:
- minimal executable entry point;
- deterministic Evidence-to-Route demonstration;
- Runtime and test suite.

See [Contest Prototype Acceptance workflow](../.github/workflows/contest-prototype-acceptance.yml).

## Expected conceptual path

```text
Evidence
   ↓
Route Candidate
   ↓
HUMAN_REVIEW
   ↓
Explicit Human Gate
   ↓
READY
   ↓
Runtime
   ↓
Verification
   ↓
Evidence
```

A candidate is a proposal, not authorization. Evidence does not independently authorize execution. The demonstration should show the explicit approval boundary and the verification result.

## Live-provider evidence

A separate GitHub Actions run exercised the OpenAI provider through Shirakami's in-process FastAPI HTTP TestClient path:

- [Live-provider verification run 38228522882](https://github.com/bxa05221-ux/shirakami-OS/actions/runs/38228522882)

The recorded acceptance markers were:
- `LIVE_PROVIDER_OBSERVED=true`
- `BOUNDARY_OBSERVED=true`
- `TRACEABILITY_VALID=true`
- `VERIFICATION_STATUS=pass`
- `UNAPPROVED_EXECUTION_BLOCKED=true`

This is separate from the deterministic acceptance workflow and may incur provider API cost when deliberately run. Do not run it repeatedly just to demonstrate the credential-free baseline.

## What the evidence supports

The current evidence supports a bounded statement that:
- the minimal entry point and deterministic route demo are runnable;
- the repository has an automated acceptance workflow;
- a live OpenAI HTTP-path observation has been recorded;
- the tested execution path checks approval boundaries and records traceable verification results.

## What is not established

Do not claim that this repository evidence alone establishes:
- a publicly deployed production API or service;
- production operator identity verification or an interactive approval UI;
- multi-user isolation or durable external persistence;
- correctness of arbitrary models, prompts, or Protocols;
- a guarantee that AI output is true or safe;
- certification or general production readiness.

The live-provider run used an in-process FastAPI TestClient. It did not prove behavior of a deployed public server.

## Suggested contest demo sequence

1. State the problem: AI models and providers change, while human context and decision authority should remain inspectable.
2. Run `python shirakami_os.py`.
3. Run `python examples/evidence_route_demo.py`.
4. Explain the Candidate → Human Gate → Runtime → Verification sequence.
5. Run `python -m pytest runtime tests -q` or show the corresponding GitHub Actions acceptance result.
6. Show the separate live-provider evidence and explicitly state its TestClient limitation.
7. Invite reviewers to attempt to identify any route where a candidate or model output can bypass explicit approval.

## Acceptance checklist

- [ ] Minimal entry point runs.
- [ ] Evidence-to-Route demo runs.
- [ ] Runtime and test suite pass.
- [ ] Human Gate is visible in the demo and implementation.
- [ ] Verification output is observable.
- [ ] Live-provider evidence is clearly separated from deterministic tests.
- [ ] Limitations are disclosed.
- [ ] No API key or other secret is included in the submission package.

## Completion rule

The prototype is ready for a first technical submission when the fixed acceptance workflow passes on the submitted commit, the deterministic demo can be reproduced from a clean checkout, and the submission describes both the demonstrated behavior and the limitations above. Further features are not prerequisites unless a contest's rules explicitly require them.
