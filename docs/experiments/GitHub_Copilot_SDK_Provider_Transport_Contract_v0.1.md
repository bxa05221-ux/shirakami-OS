# GitHub Copilot SDK Provider Transport Contract v0.1

Status: candidate provider transport / not API MVP completion

## Purpose

This document defines how Shirakami may connect to GitHub Copilot SDK without making
GitHub Copilot part of the Shirakami Runtime's semantic or authority layer.

The provider boundary remains replaceable:

```
External HTTP
    ↓
Shirakami API
    ↓
RealModelAdapter
    ↓
Provider Transport
    ↓
GitHub Copilot SDK
    ↓
Model
```

The Runtime, Evidence, Trace, AIwitness, and Human Gate layers remain unchanged.

## Current external status

GitHub Models is retired as of July 30, 2026. Its former inference API is therefore
not a viable new provider path.

GitHub Copilot now provides a programmatic Copilot SDK. The SDK can be used by
server-side applications and supports authentication suitable for backend
deployments. It can route a prompt/session to models exposed by Copilot.

This document treats Copilot SDK as a candidate transport only. It does not claim
that Shirakami has executed a real Copilot request.

## Contract

A provider transport MUST:

1. receive only the canonical model request crossing the RealModelAdapter boundary;
2. return opaque model output to Shirakami;
3. keep credentials outside source control and outside Evidence content;
4. avoid rewriting observations, Evidence, Trace, or authority state;
5. be replaceable without changing Runtime semantics;
6. expose provider/model identity only as metadata, not as decision authority.

A provider transport MUST NOT:

- approve execution;
- set `execution_authorized`;
- set `publish_authorized`;
- set `merge_authorized`;
- bypass Human Gate;
- manufacture Evidence on behalf of the Runtime.

## Authentication boundary

Authentication belongs to the provider transport/deployment layer.

No provider credential is stored in this repository for this experiment.

For GitHub Actions, GitHub documents `GITHUB_TOKEN` as the built-in workflow
credential for GitHub API access. Copilot SDK authentication has its own supported
server-side mechanisms; the actual credential choice must be made at integration
time.

## Verification gate

The first real-provider experiment must prove only this path:

```
External HTTP
    ↓
RealModelAdapter
    ↓
Provider Transport
    ↓
Real model
    ↓
RuntimeResult
    ↓
Evidence
    ↓
Trace
    ↓
AIwitness
```

Required assertions:

- model output reaches RuntimeResult;
- the exact model output is bound to Evidence;
- Evidence ID changes when model output changes;
- Trace references the resulting Evidence ID;
- AIwitness references the same Evidence ID;
- `execution_authorized == false`;
- `human_gate_required == true`;
- no provider credential appears in source control or Evidence.

## MVP denominator

This experiment does not change the fixed ten-item API MVP denominator.

Items 9 and 10 remain pending until an external provider has actually executed
through the public HTTP path and the complete Evidence/Trace path has been verified.

## Decision

Do not revive the retired GitHub Models API path.

Keep `RealModelAdapter` provider-neutral and treat GitHub Copilot SDK as one
replaceable provider transport candidate alongside other providers.
