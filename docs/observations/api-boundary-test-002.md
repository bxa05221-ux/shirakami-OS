# API Boundary Test 002: OPPAI Normalize

Status: implementation verification

## Purpose

Verify the existing `/v0.1/oppai/normalize` HTTP boundary against the current OPPAI normalization contract without changing Runtime semantics.

## Contract under test

- Input field: `text` (required string)
- Optional input: `context`
- Event: `oppai.observed`
- Schema: `OPPAI`
- Version: `0.1`
- `canonical_prompt` preserves the complete user-authored input
- correction markers and unresolved questions remain observable
- confidence is `provisional` when corrections or unresolved questions are present, otherwise `observed`

## Verification

The E2E test sends a correction and a question so that the boundary exposes the non-destructive normalization fields without requiring an LLM.

This document records the test target only. It does not introduce new semantics.
