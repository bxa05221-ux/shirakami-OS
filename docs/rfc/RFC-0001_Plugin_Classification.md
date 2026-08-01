# RFC-0001 Plugin Classification

## Purpose

This RFC defines an architectural classification for plugins in Shirakami OS. Plugins provide orthogonal, optional capabilities that extend the Runtime without altering Foundation artifacts.

## Principles

- Foundation is immutable.
- Plugins extend Runtime.
- Plugins are independent capabilities.
- Plugins never modify Foundation.

## Initial Plugin Categories

- Observation Plugin

  Architectural description: Captures data from external sources or the runtime environment (telemetry, logs, input streams). Observation plugins are responsible for collecting and normalizing signals for downstream processing.

- Analysis Plugin

  Architectural description: Consumes observations and produces interpretations, inferences, or enriched datasets. Analysis plugins implement domain- or task-specific processing (e.g., classification, summarization, feature extraction) and remain stateless with respect to Foundation.

- Integration Plugin

  Architectural description: Bridges Shirakami OS with external systems and services (datastores, message buses, third-party APIs). Integration plugins manage connectivity and translate between external protocols and the Runtime's internal data models.

- Rendering Plugin

  Architectural description: Transforms runtime outputs into presentation formats or artifacts (visualizations, reports, export formats). Rendering plugins focus on presentation concerns and do not change core runtime behavior.

## Out of Scope

This RFC does not define or prescribe:

- APIs
- Loaders
- Registration
- Security
- Configuration
- Marketplace
- Runtime implementation

Classification precedes implementation.
