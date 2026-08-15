# Third-Party Evaluation Support Prototype α0.1

Prototype application specification for supporting third-party evaluators during an evaluation period.

## Purpose

Support evaluators who cannot always meet at the same time by preserving each evaluator's current recognition and making it available through the Shiraz Presenter nonlinear meeting model.

The application does not delegate evaluation judgment to AI.

## Core flow

Evaluation Landscape
→ Evaluator Landscape
→ Observation
→ Recognition
→ Matome Snapshot
→ Presenter
→ Recognition Difference
→ Evidence
→ Resilience Observation
→ Re-observation

## Prototype boundary

The first prototype focuses on:

- Evaluation workspace
- Individual evaluator landscape
- Observation and recognition records
- Matome YAML snapshots
- Presenter / nonlinear meeting
- Evidence lineage
- Resilience observations
- Permission boundary
- Audit trail

External adapters such as Calendar, Document Storage, and GitHub are integration targets, not prerequisites for the first executable slice.

## Design rule

Do not silently extend Shirakami OS Foundation semantics. If implementation requires a new Foundation decision, stop and return to Design Observation.
