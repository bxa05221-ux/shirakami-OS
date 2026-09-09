# Shirakami OS β1.0 — Operation Start

Status: implementation observation

## Purpose

Record the transition from β1.0 verification into continuous operation.

This document does not introduce new theory, Protocol semantics, Landscape schema, or Renderer/Adapter contracts.

## Verified Preceding State

- R0057 Adapter Exchange — merged
- R0058 Renderer Exchange — merged
- R0059 Renderer Boundary Continuity — merged
- R0060 Adapter / Renderer End-to-End Continuity — merged
- Canonical `test-runtime` — success for R0060
- Default branch `main` — protected
- Required status check — `test-runtime`

## β1.0 Operation Definition

β1.0 operation means that the existing Runtime can continue to observe and verify Landscape and Evidence continuity while external AI, Adapter, and Renderer components may be exchanged.

The operation state is not defined by AI/model quality or by universal interchangeability.

## Operational Boundaries

Canonical flow:

`Landscape → Evidence → Protocol → Runtime → Adapter → Backend`

Presentation boundary:

`Landscape → Runtime → Renderer`

The Runtime serves Landscape. Adapter and Renderer remain boundaries rather than semantic authorities.

## Operational Rules

- One Change / One Verification
- Do not treat file existence as experiment success
- Do not mark unverified results as success
- Preserve Evidence without rewriting it
- Do not equate Landscape state reconstruction with Evidence lineage reconstruction
- Do not resolve Artifact mismatch by guesswork
- Do not introduce new theory from the Runtime side
- Return unresolved theoretical questions to the research side

## Operation Start Observation

R0060 provides the immediate verified baseline for operation. The next work should operate from the protected `main` state and keep operational observations explicit and addressable.

## Non-goals

- New theory
- New Protocol semantics
- Landscape schema redesign
- AI/model quality evaluation
- Universal Adapter interchangeability
- Renderer output quality evaluation
- Evidence lineage reconstruction

## Next

Proceed with β1.0 operational loop work using the protected `main` branch and canonical `test-runtime` verification gate.
