# AATS Entry Flow 001

## Purpose

Establish the first implementation boundary for:

`AATS → Thread RPG → viewpoint collection → human-facing re-expression → current-state mapping → Small Step`

AATS (ASCII Art Thread Simulator) is treated as the original implementation lineage of Thread RPG.

## Boundary

- AATS owns transient Thread / Participant / Post state.
- Participant persona/IP data is opaque and optional; editing it is deferred.
- Renzan collects observable viewpoints without interpreting them.
- Kasen re-expresses viewpoints without a dry A/B participant transcript.
- Small Step selection is an external policy boundary.
- Current Landscape data passes through as observable state.

## Non-goals

- No new Kernel semantics.
- No automatic truth or meaning inference.
- No fixed participant roles.
- No participant IP/persona editor yet.
- No claim that the fallback Kasen text is the final narrative renderer.

## Lineage

`AATS → Thread RPG → later applications such as 旅とも`
