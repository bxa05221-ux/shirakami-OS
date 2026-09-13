# Protocol Responsibility Classification α0.1

## Purpose

Establish the responsibility boundary for protocols used by the Shirakami Launch Model without introducing new theory or automatic protocol selection.

## Classification

| Class | Responsibility | Examples | Selection / activation |
|---|---|---|---|
| Background Protocol | Maintain or observe the cognitive/contextual background around the Landscape | 暗問層逆算プロトコル / 3D位相回転アイゼンハワーマトリクス / 歪天球 | Intended to operate in the background; not selected as an application gear by the AI |
| Application Protocol | Provide an explicit method of interaction, expression, or task handling | ThreadRPG and other application protocols | Explicitly presented/selected by the human; optional |
| Runtime / Governance | Provide the execution, validation, exchange, evidence, and boundary mechanisms for protocols | OPPAI / Protocol Registry / Protocol IR / Runtime / Adapter / Evidence | Infrastructure; does not select semantic protocols autonomously |

## Responsibility Boundary

- Background Protocols are not equivalent to Application Protocols.
- Background operation does not mean that a protocol autonomously decides human intent or semantic truth.
- Application Protocol selection remains a human-controlled operation.
- ThreadRPG is optional and is not a prerequisite for Shirakami Runtime operation.
- Runtime / Governance components execute and validate declared protocol operations; they do not invent domain meaning or replace human judgment.
- External AI remains an execution backend/adapter target and has no semantic authority.

## Operational Model

The Launch Model distinguishes two paths:

1. Background support:
   `Landscape ↔ Background Protocols`

2. Human-selected application execution:
   `User → Protocol Presentation/Selection → OPPAI → Protocol Registry → Protocol IR → Runtime → Adapter → External AI`

These paths may coexist. The presence of Background Protocols does not imply automatic selection of an Application Protocol.

## Current Background Set

The following are classified as Background Protocols for the current Launch Model boundary:

- 暗問層逆算プロトコル
- 3D位相回転アイゼンハワーマトリクス
- 歪天球

Their detailed theoretical definitions remain governed by their respective research handoffs. This document does not redefine them.

## Verification Boundary

This document establishes classification and responsibility only. It does not claim that every Background Protocol is currently implemented as a continuously executing runtime component.

Implementation of continuous background execution is a separate verification task.
