# Shirakami Navigation α0.1

## Purpose

Shirakami Navigation is a navigation-support layer for Landscape observation.
It is not an autonomous life-control or autopilot system.

## Instrument stack

- **Distorted Celestial Sphere**: navigation map / long-range relational map.
- **Cognitive Echolocation**: observes current position and direction from Landscape changes.
- **Reference Frame**: a human-selected measurement standard such as a faith, ideal, belief, or professional ethic.
- **Gyro Reference**: conceptual attitude/reference-axis observation. A multi-link Foucault pendulum is retained as a conceptual model, not a physical implementation requirement.
- **Course Adjustment**: existing 3D phase rotation × Eisenhower mechanisms may present course/risk considerations; they do not autonomously steer the person.
- **Evidence**: immutable record of observable transitions.

## Navigation State

The minimum state is:

```yaml
navigation_state:
  position: null
  direction: null
  attitude: null
  reference_frame: null
  map_id: distorted_celestial_sphere
  horizon: null
  landscape_revision: 0
  evidence_cursor: null
  uncertainty: []
```

## Human boundary

The human owns values, reference-frame selection, destination/goal selection, and final decisions.

AI may observe, calculate, compare, map, present alternatives, expose uncertainty, and preserve evidence.

AI must not choose the person's values or faith, select a life destination, autonomously change course, or make the final decision.

## Core principle

> AI does not pilot a person's life. It supports navigation by keeping current position, direction, reference, horizon, and evidence observable.

## Runtime boundary

Navigation observes the existing Runtime/Landscape flow. It does not replace the Runtime, rewrite Evidence, or assign domain truth.

```text
Landscape
  ↓
Protocol
  ↓
Runtime
  ↓
Transition
  ↓
Evidence
  ↓
Navigation Observer
  ↓
Navigation State
  ↓
Human judgment
  ↓
next observation
```

## Non-goals

- autonomous life planning
- automatic value selection
- automatic faith selection
- automatic destination selection
- autonomous course correction
- treating a reference frame as absolute truth
