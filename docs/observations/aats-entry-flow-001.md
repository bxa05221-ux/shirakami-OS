# AATS Entry Flow 001

## Purpose

Establish the first implementation boundary for the user-facing path:

`AATS → Thread RPG → viewpoint collection → human-facing re-expression → current-state mapping → Small Step`

AATS is treated as the original implementation lineage of Thread RPG, not as a
renderer added after Thread RPG.

## Boundary

- AATS owns transient Thread/Participant/Post state.
- Participant persona/IP data is opaque and optional. Editing that data is deferred.
- Renzan collects observable viewpoints without deciding their meaning.
- Kasen re-expresses collected viewpoints without producing a dry participant transcript.
- Small Step selection is an external policy boundary. The current module accepts a selector; it does not implement cognitive truth or decision authority.
- The current state is passed through as observable Landscape data.

## Non-goals

- No new Kernel semantics.
- No automatic truth/meaning inference.
- No fixed participant roles.
- No participant IP/persona editor yet.
- No claim that the current Kasen fallback is the final narrative renderer.

## Lineage

`AATS → Thread RPG → later applications such as 旅とも`

The implementation preserves this lineage while keeping the runtime boundary generic.
