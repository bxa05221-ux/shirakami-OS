# R0028: Operational Landscape Cycle

## Purpose

Verify one read-only operational cycle using the Runtime boundary already established by R0024–R0027.

## Observable path

`GitHub read → Repository Landscape observation → LandscapeState bootstrap → Runtime → Evidence → after-state → re-observation`

The cycle is intentionally operational rather than semantic. The Runtime receives the observed repository Landscape as an existing observable state, performs the existing example transition, and exposes the resulting state and Evidence through the existing observation boundary.

## Acceptance

A GitHub Actions Runtime process must successfully execute the operational entrypoint with a process-local read token and produce an inspectable JSON result containing before-state, Evidence, after-state, and re-observation.

## Non-goals

- semantic interpretation of the repository;
- continuity or identity claims;
- truth determination;
- GitHub writes;
- credential persistence or discovery;
- Evidence schema changes;
- new Kernel cognitive concepts.

## Operational lesson

The cycle deliberately uses existing boundaries instead of adding another abstraction. The observation is read, bootstrapped, executed, and re-observed without converting the external repository into domain meaning.
