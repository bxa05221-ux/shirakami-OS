# Shirakami Landscape Observer

## Status

Prototype application definition / not yet production-ready.

## Purpose

Provide a focused application for observing how a user's Landscape changes over time while preserving the distinction between Observation, Evidence, Projection, and Interpretation.

This is the first candidate specialized application for validating Shirakami OS as a practical user-facing system.

## Core loop

```text
User interaction
      ↓
Observation
      ↓
Evidence
      ↓
Landscape projection
      ↓
Re-observation
      ↓
New Evidence
```

## Product boundary

The application does not attempt to be a general AI assistant.

Its job is to make Landscape change visible and traceable.

### MVP capabilities

- show current Landscape state;
- record observable transitions;
- preserve Evidence identity and history;
- show propagation from Evidence to one or more projections;
- distinguish Observation from Interpretation;
- allow the user to inspect how a later Evidence relates to an earlier projection;
- support model replacement without changing the user's Landscape representation.

## Non-goals

- no new Foundation theory;
- no `WaterVein` abstraction at application level;
- no automatic psychological diagnosis;
- no requirement for a specific LLM vendor;
- no assumption that Evidence is permanently frozen;
- no automatic rewriting of historical Evidence.

## Why this application

This application exercises the parts of Shirakami OS that are currently under direct architectural investigation:

- Landscape-centered runtime;
- Evidence lifecycle;
- propagation;
- re-observation;
- model-independent Context preservation.

The application therefore serves as both a useful tool and an architectural verification surface.

## First milestone

Do not implement the full UI yet.

First demonstrate the following executable scenario:

1. create one observable Landscape transition;
2. capture `Evidence₁`;
3. project it into a Landscape state;
4. observe the resulting state;
5. capture distinct `Evidence₂`;
6. preserve the relation between the two without mutating `Evidence₁`.

If this scenario cannot be implemented cleanly using the existing Runtime boundaries, record the architectural limitation before expanding the application.
