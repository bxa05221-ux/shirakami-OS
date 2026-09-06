# R0024 — Live GitHub Read Verification

## Purpose

Verify one real execution path in which the Shirakami Runtime operational entrypoint obtains a process-local credential and reads the repository root through the GitHub adapter boundary.

## Path

`GitHub Actions runtime → operational_github_read → live GitHub probe → Repository Landscape Adapter → GitHub API → JSON observation`

## Verification target

The workflow explicitly enables live execution and supplies the Actions-provided read-only `GITHUB_TOKEN` to the existing Runtime entrypoint. Success requires the Runtime process itself to complete the read and emit the repository-root observation.

## Non-goals

- no GitHub write
- no credential persistence or discovery
- no semantic interpretation of repository contents
- no Protocol IR, Evidence, or Landscape schema changes
- no continuity or identity claim

## Acceptance rule

Only a successful workflow execution of the Runtime entrypoint counts as a live-read observation. Checkout success alone does not count.
