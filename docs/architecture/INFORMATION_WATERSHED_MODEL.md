# Information Watershed Model

## Purpose

This document records an architectural interpretation that has emerged from the existing Shirakami implementation: **information can be divided into different Protocol routes and reused for different needs while remaining within a common Landscape / Evidence / Runtime boundary**.

This is a descriptive architecture model, not a new normative Protocol specification.

## 1. Water-system analogy

Shirakami can be understood as an information water system.

```text
                    Information source
                           │
                       Landscape
                           │
                      ── diversion ──
                     /       |        \
                    /        |         \
             Protocol A  Protocol B  Protocol C
                  │          │           │
               need A      need B      need C
                  │          │           │
                  └────── observation ───┘
                             │
                          Evidence
                             │
                      re-observation
                             │
                         Landscape
```

The important point is not that every application shares one identical sequence. The existing implementation already demonstrates that different routes can use different intermediate components while preserving common boundaries.

## 2. Protocols as a gearbox

The water-system view describes the flow. The **gearbox** view describes the mechanism that changes the route.

A Protocol is not valuable only because it exists as a reusable component. Its architectural value also comes from being composable with other Protocols and Runtime boundaries.

Conceptually:

```text
Route A:  A → B → C → Evidence
Route B:  A → C → D → Evidence
Route C:  B → D → C → Evidence
```

These are illustrative compositions, not claims that all such permutations are currently executable.

The current repository already contains explicit route observation and a generic Protocol dispatch surface. `PROTOCOL_ROUTE_FOUNDATION.md` defines declared and observed Protocol routes, while the Runtime boundary keeps execution semantics separate from route observation.

## 3. Existing evidence

The repository provides several concrete observations supporting this model:

- The AATS Wayfinding implementation exposes the route `AATS → Thread → Renzan → Kasen → Landscape → Small Step → Evidence → Re-observation`.
- The generic Protocol route foundation represents Protocol relationships as declared or observed routes rather than hard-coding one application-specific endpoint.
- Runtime execution produces observable transitions and Evidence without requiring the route map to reinterpret those transitions.
- The Landscape Adapter boundary allows external systems to be connected without putting external-system behavior into Runtime core.
- The manga manual is an experimental rendering path in which the same underlying manual structure can be rendered through a different human-facing adapter.

These observations support **reconfigurable routing** as an architectural direction. They do not, by themselves, prove unrestricted arbitrary Protocol permutation.

## 4. n-gram and the one-stroke route

The gearbox model becomes more precise when Protocol connections are treated as local transitions.

If Protocol A produces a state that Protocol B can accept, the connection can be represented as:

```text
A.output → B.input
```

A sequence of such local connections forms a candidate route:

```text
2-gram:  A → B
3-gram:  A → B → C
4-gram:  A → B → C → D
```

Here, **n-gram is a route-candidate mechanism, not an authority or a semantic truth engine**. It can propose a next compatible Protocol from the recent sequence, while Protocol contracts and verification determine whether the transition is actually admissible.

The resulting route can be understood as a **one-stroke route**: a continuous sequence of locally compatible Protocol transitions from a starting state toward a defined destination or stopping condition.

```text
Landscape
   ↓
Protocol A
   ↓  compatible transition
Protocol B
   ↓  compatible transition
Protocol D
   ↓
Runtime
   ↓
Evidence
   ↓
Landscape
```

The term "one-stroke" is architectural shorthand here, not a claim that every route is an Eulerian path or that Protocols may be reused without constraints.

The intended separation is:

- **n-gram** — generates candidate local connections
- **Protocol boundary** — constrains admissible connections
- **Runtime** — executes the selected route
- **Evidence** — records what actually happened
- **Human / system policy** — retains control over destination and acceptance

This gives the water-system analogy an executable interpretation: **the water flows through a network of verified-compatible gates, while route construction determines where the flow is diverted.**

## 5. What is actually reused

The reusable unit is not only code.

The repository separates:

- Landscape — the environment/context being observed
- Protocol — meaning and execution structure
- Runtime — execution boundary
- Evidence — observable transition record
- Adapter — external-system boundary
- Renderer / surface — human-facing representation

Because these boundaries are explicit, a new use case does not necessarily require a new AI model or a new Runtime core. It may instead be expressible by selecting, composing, or reordering existing Protocol and adapter components.

The actual compatibility of a composition still has to be verified from its input/output contracts and tests.

## 6. Information is not consumed once

The water metaphor also clarifies the role of Evidence.

Information can be diverted to one need, produce an observable transition, and return as Evidence to the broader Landscape. The result can then participate in another route.

This is not a claim that Evidence is automatically converted into domain truth. The existing design explicitly preserves the distinction between observable Evidence and interpretation.

> **Shirakami does not treat information as a one-way answer pipeline. It provides boundaries through which information can flow, branch, be observed, and flow again.**

## 7. Human control

The water does not choose where the canal is built.

In Shirakami, route composition remains a human/system design concern. AI may operate inside a route, but it is not the authority that decides the destination of the information system.

This is consistent with the existing principle that Runtime does not own domain truth and that human final judgment remains outside AI authority.

## 8. Verification boundary

The next verification target is not to prove the metaphor. It is to test the architectural claim directly.

For selected existing Protocols, record:

1. input state
2. transformation
3. output state
4. Evidence produced
5. predecessor compatibility
6. successor compatibility
7. preservation of Landscape identity

Then execute at least two different compositions using overlapping Protocol components and verify that both remain observable and replayable through the existing Evidence boundary.

This keeps the model grounded in **one change, one verification** rather than turning the metaphor into unverified theory.

## Status

**Status: Architecture interpretation / verification target**

This document does not promote a new Protocol to the Registry and does not change the Runtime contract.