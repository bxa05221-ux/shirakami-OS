# Protocol Candidate Lifecycle

## Purpose

This document defines the boundary between an idea, a protocol candidate, an approved protocol, and executable runtime behavior.

Generation and structural validation may be automated, but promotion to an approved executable protocol requires explicit human review and Human Gate approval.

## Lifecycle

    Discovery / Observation
            ↓
    Idea / Hypothesis
            ↓
    Matome (handoff/specification artifact)
            ↓
    Protocol Candidate
            ↓
    Structural Validation
            ↓
    HUMAN_REVIEW
            ↓
    Approval Envelope
            ↓
    Human Gate
            ↓
    Approved Protocol
            ↓
    Runtime
            ↓
    Verification
            ↓
    Evidence
            ↺

## Boundary Rules

### 1. Idea is not a Protocol

An idea or observation records what was noticed or conceived. It does not authorize execution.

### 2. Matome is not automatically a Protocol

Matome YAML may preserve context, rationale, constraints, and implementation intent. It is a handoff/specification artifact unless explicitly promoted through the lifecycle.

### 3. Candidate is not Approved

A generated or manually assembled Protocol Candidate remains non-executable as an approved protocol until structural validation and human approval are complete.

### 4. Structural Validation is not Human Judgment

Automated validation may check schema, required fields, references, boundary consistency, and other mechanical constraints. It must not be treated as semantic or ethical approval.

### 5. Human Gate is the promotion boundary

Only the human approval path may promote a candidate to Approved Protocol status.

### 6. Runtime does not grant authority

Runtime executes an approved definition within its declared boundaries. Successful execution does not prove that the underlying model, interpretation, or real-world effect is valid.

### 7. Evidence returns to the Landscape

Execution and verification produce Evidence. Evidence may inform later discovery and candidate generation, but it does not silently rewrite an approved Protocol.

## Candidate State Model

Recommended states:

- IDEA
- MATOME
- CANDIDATE
- STRUCTURALLY_VALIDATED
- HUMAN_REVIEW
- APPROVED
- EXECUTING
- VERIFIED
- REJECTED
- SUPERSEDED

State transitions must be explicit and reconstructable.

## Separation of Concern

The lifecycle separates four questions:

1. Why did this idea arise? — discovery / rationale
2. What is being proposed? — candidate protocol
3. Who authorized promotion? — human approval / Human Gate
4. What actually happened? — Runtime / Evidence

This separation prevents an implementation artifact from silently becoming an authority-bearing specification.

## Relationship to Activation Pump and Background Runner

Activation Pump and Background Runner are downstream execution-control concepts.

They should consume an already approved protocol or an explicitly authorized execution candidate. They must not become implicit approval mechanisms.

Therefore:

- Candidate lifecycle defines promotion authority.
- Activation Pump defines activation mechanics.
- Background Runner defines background execution mechanics.
- Runtime defines execution semantics.
- Evidence defines what was observed.

## Implementation Status

This document is a current-main architectural contract.

It does not claim that every state transition is already implemented. Missing transitions should be implemented as small, independently verifiable boundaries rather than by importing an old PR wholesale.

## Design Principle

> Generation may be automated. Promotion remains human-authorized. Execution remains observable.
