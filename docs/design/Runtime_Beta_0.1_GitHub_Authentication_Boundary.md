# Runtime β0.1 GitHub Authentication Boundary

Status: Implementation Preparation
Version: 0.1
Date: 2026-08-11

## Purpose

Provide a replaceable authentication boundary for the GitHub transport without placing credentials in Runtime, Landscape, Evidence, or repository content.

## Boundary

```text
Execution Environment
        ↓
    TokenProvider
        ↓
    GitHub Client
        ↓
    GitHub API
```

Runtime core does not own credentials.

## Initial Provider

`EnvironmentTokenProvider` reads a token from an environment variable at request time.

Default variable:

`GITHUB_TOKEN`

A different provider may be injected for another deployment environment.

## Security Rules

- Never commit a token.
- Never write a token to Landscape State.
- Never write a token to Evidence.
- Never include a token in logs or observations.
- Missing credentials must fail closed.

## Verification

The first verification proves only credential acquisition and fail-closed behavior. A live API call requires a token supplied by the execution environment; no credential is embedded in this repository.

## Controlled Write Gate

A live GitHub write remains blocked until the execution environment explicitly provides a credential and the target path is confirmed as a non-Foundation observation artifact.

The authentication layer must not alter Protocol semantics.
