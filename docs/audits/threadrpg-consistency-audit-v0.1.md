# ThreadRPG Consistency Audit v0.1

Status: Initial audit record / documentation only
Date: 2026-09-22

## Scope

This audit compares:

- `docs/protocols/ThreadRPG_Protocol_Generation_Policy_v0.1.md`
- `docs/threadrpg-reintegration-draft-0.1.md`
- existing AATS-related runtime and tests
- `protocols/thread-rpg-v1.2.1.yaml`

No normative Foundation or Runtime semantics are changed by this record.

## Findings

| Area | Status | Finding |
|---|---|---|
| Shared principles | Partial alignment | The policy and reintegration draft preserve uncertainty, alternatives, human judgment, and non-authoritative viewpoints. |
| Human Gate | Unconfirmed in ThreadRPG path | The policy requires human review before accepting a Protocol Candidate, but the inspected AATS wayfinding cycle does not expose a dedicated approval gate. |
| Evidence | Implemented in AATS path | The wayfinding runtime captures Evidence after a selected small step and applies it to Landscape. |
| Responsibility boundary | Partial alignment | The policy prohibits automatic authorization and execution; the existing wayfinding function directly invokes a selector and applier in one cycle. Its authorization semantics require explicit confirmation. |
| Composability | Partial / draft-level | The reintegration draft identifies Independent Observation, Conference, Matome, Evidence, and Landscape transition as candidate protocol stages, but these are not yet established as concrete normative artifacts. |
| Matome API relationship | Unconfirmed | The draft describes Matome API v3.2 as experimental; no confirmed Runtime contract connection was established in this audit. |
| Renderer boundary | Clear in documents | Renderer presentation is separated from Thread/Perspective semantics in the reintegration draft. |

## Existing implementation evidence

The inspected AATS path includes:

```text
Thread
  -> Renzan.collect
  -> Kasen.compose
  -> Landscape observation
  -> SmallStep selection
  -> Step application
  -> Evidence capture
  -> re-observation
```

The existing test verifies viewpoint collection, narrative composition, before/after observations, Evidence capture, and Landscape Evidence storage.

## Primary mismatch

The existing AATS wayfinding cycle is an observable Thread-to-Evidence-to-reobservation path. It should not yet be declared equivalent to the proposed ThreadRPG reintegration cycle:

```text
Independent Observation
  -> Conference
  -> Matome
  -> Evidence
  -> Landscape
```

The relationship between discussion/proposal generation and execution authorization remains insufficiently explicit in the inspected ThreadRPG-specific path.

## Recommended next verification

1. Identify whether a Human Gate exists upstream of `SmallStepSelector` or `StepApplier`.
2. Add a focused test or documentation contract for approval, rejection, interruption, and unresolved-authority paths before any semantic Runtime change.
3. Specify the minimum Evidence fields needed for subsequent independent observation.
4. Decide whether the AATS wayfinding cycle is a legacy application path, a ThreadRPG implementation path, or an adapter between them.
5. Keep the Matome API experimental until its required operations and contract are explicitly established.

## Non-goals

This audit does not:

- change ThreadRPG semantics;
- add a new Runtime layer;
- declare the reintegration draft implemented;
- authorize autonomous execution;
- convert the experimental Matome API into a normative specification.
