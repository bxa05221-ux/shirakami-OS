# Copilot Provider Observation Boundary v0.2

## Purpose

This experiment verifies that a replaceable external model provider can cross the Shirakami HTTP boundary without acquiring decision authority.

The observation path is:

External Provider → HTTP API → Runtime → Evidence → Trace → AIwitness → Traceability verification

## Current verification

The provider-neutral fixture path is CI-verified.

The live path is conditional on a deployment-provided Copilot credential. No credential is committed to the repository and no credential is copied into Evidence.

## Assertions

A successful live observation must establish all of the following:

1. A real provider response was received.
2. The opaque provider output crossed the HTTP execution boundary.
3. The exact provider output was stored in Evidence.
4. The resulting Evidence ID is referenced by Trace.
5. The same Evidence ID is referenced by AIwitness.
6. Traceability validation returns valid=true.
7. execution_authorized remains false.
8. publish_authorized remains false.
9. merge_authorized remains false.
10. human_gate_required remains true.

## Authentication boundary

Provider credentials belong to the deployment/provider transport layer.

They MUST NOT be committed to source, embedded in protocol data, stored in Evidence, or used to manufacture authority state.

The experiment uses COPILOT_GITHUB_TOKEN, with GH_TOKEN and GITHUB_TOKEN accepted by the harness as compatible environment fallbacks.

## API MVP status

This experiment does not by itself mark API MVP items 9 or 10 complete.

Those items become complete only after an actual external provider execution has been observed through the HTTP → Runtime → Evidence/Trace path and the result has been verified.

Until then:

- 1–8: verified
- 9–10: provider-neutral boundary verified; real external execution pending