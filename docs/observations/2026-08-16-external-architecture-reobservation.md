# External Architecture Re-observation — 2026-08-16

## Status

Observation recorded as an external review artifact.

This document preserves the external AI observation as an observation/evidence record. It does not redefine the Foundation or silently reconcile differences between the externally observed GitHub landscape and development-side work.

## Observed facts

- The `main` branch currently contains RFC-0001 through RFC-0006; no `R0009` or `R0009.1` artifact was found by repository search.
- The root-level `Shirakami-OS` file is identified by the external reviewer as the Foundation Revision α2.2 base-point document.
- `runtime/test_prototype.py` provides six Runtime boundary tests covering success, failure observability, invalid protocol ID, invalid protocol, invalid context input, and invalid protocol result.
- `apps/landscape-observer/README.md` explicitly distinguishes Observation, Evidence, Projection, and Interpretation and describes a milestone involving Evidence₁ → Projection₁ → LandscapeState₁ → re-observation → Evidence₂.
- The external reviewer reports that the current `LandscapeState.apply_evidence()` implementation still directly merges evidence transition data into state, so the Projection boundary is not yet fully represented in code.
- The external reviewer reports that `WaterVein` is referenced by the landscape-observer design but is not defined in this repository.
- `.github/workflows/runtime-beta-0.1.yml` exists and defines Runtime tests, renderer compilation, and manga smoke rendering.

## Important distinction

The absence of R0009/R0009.1 from `main` is an observation about the GitHub landscape at observation time. It does not establish that development-side R0009/R0009.1 work does not exist elsewhere.

Therefore this record intentionally does not classify the discrepancy as a defect until the development landscape, branches, and other repositories are reconciled.

## Architectural reading

The re-observation strengthens the following interpretation of the current repository:

- Foundation is intentionally kept small and stable.
- Runtime boundary behavior is already tested at code level.
- Projection is recognized as a distinct architectural boundary, but remains an implementation gap.
- Evidence is intended to preserve observable transitions rather than encode domain interpretation.
- External AI reviews themselves can function as development evidence without becoming Foundation authority.

## Next verification targets

1. Reconcile the development-side R0009/R0009.1 landscape with the GitHub landscape.
2. Verify the Projection boundary with an Evidence₁ → Projection₁ → LandscapeState₁ → Evidence₂ vertical slice.
3. Verify whether GitHub-specific implementation remains inside Runtime or has been moved behind the Adapter boundary.
4. Preserve Evidence lineage without mutating earlier Evidence records.
5. Only after the above observations are stable, decide whether a new protocol/RFC artifact should be published.

## Evidence policy

This document records what was observed. It does not promote external interpretation to architectural truth. Foundation changes remain subject to the project's existing RFC-first governance.
