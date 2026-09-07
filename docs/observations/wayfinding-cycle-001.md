# Wayfinding Cycle 001

## Purpose

Connect the current observable Landscape to one externally selected Small Step and a subsequent re-observation.

## Boundary

`Landscape → external Small Step policy → StepApplier → re-observation`

The runtime provides only the cycle boundary. Cognitive echo-location and 3D-PRUIM remain external policies.

## Contract

- `LandscapeObserver` supplies the observable current state.
- `SmallStepSelector` supplies one next action from outside the Kernel.
- `StepApplier` performs that action at the application/service boundary.
- The cycle records the before snapshot, selected Small Step, and after snapshot.
- The same observer is used before and after the step so the result remains directly observable.

## Non-goals

- No cognitive interpretation in Kernel.
- No implementation of cognitive echo-location.
- No implementation of 3D-PRUIM.
- No claim that the selected step is universally correct.
- No vendor-specific AI dependency.
