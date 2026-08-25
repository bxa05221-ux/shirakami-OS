# Usage Evidence Protocol α0.1

## Purpose

This protocol defines the minimum observable evidence produced when a third party uses a Shirakami OS artifact.

The purpose is **verification through use**, not surveillance and not mandatory collection of user data.

The protocol connects external usage to the existing Shirakami OS evidence flow:

```text
Usage
  ↓
Observable Transition
  ↓
Evidence
  ↓
Observation
  ↓
Landscape Delta
```

## Design principles

- The object of observation is the **observable transition**, not the identity of the user.
- Evidence records facts produced by execution; interpretation remains separate.
- Original evidence is preserved and must not be silently rewritten.
- Participation in reporting is optional unless a specific artifact explicitly states otherwise.
- No unnecessary personal data is required.
- Usage telemetry must not be introduced merely because this protocol exists.
- Local execution should remain useful without transmitting usage data.
- Aggregation must not be presented as proof of correctness; it is evidence for further observation and review.

## Minimum evidence

When an implementation emits a usage evidence record, the minimum useful fields are:

```yaml
usage_evidence:
  protocol_version: "alpha0.1"
  artifact: "..."
  artifact_version: "..."
  execution_id: "..."
  timestamp: "..."
  action: "..."
  result:
    status: "success | failure"
  transition:
    before: "..."
    after: "..."
  error:
    type: null
    message: null
```

Implementations may add fields when they are necessary for reproducibility or diagnosis, but additions should not silently turn the record into user tracking.

## What may be observed

Examples include:

- successful execution
- failed execution
- validation failure
- runtime error
- protocol loading failure
- unexpected input
- API boundary failure
- test result
- reproducible user-reported behavior
- externally contributed Issue or Pull Request

## What is not automatically collected

This protocol does not authorize automatic collection of:

- names or account identities
- conversation contents
- unrelated filesystem contents
- credentials or tokens
- private repository contents
- precise location
- unrelated telemetry

If an implementation needs any such information for a separate purpose, that purpose and its collection rules must be specified independently.

## Reporting modes

### Local mode

The runtime records evidence locally. Nothing is transmitted automatically.

### Explicit export

A user may explicitly export evidence for an Issue, Pull Request, support request, or other review channel.

### CI mode

A CI workflow may produce execution evidence as a build artifact or test output. The workflow should expose only information appropriate to the repository and execution environment.

### Service mode

A hosted service may collect operational evidence only when its own service-level documentation and consent/usage terms explicitly define that collection.

## Observation boundary

A usage evidence record is not itself an interpretation.

For example:

```text
Evidence:
  runtime returned validation_error

Observation:
  users may be encountering an unclear input contract

Interpretation:
  documentation or schema may need improvement
```

These layers must remain distinguishable.

## Review loop

Usage evidence should feed the existing review process rather than automatically changing the system:

```text
Third-party use
      ↓
Observable transition
      ↓
Evidence
      ↓
Observation
      ↓
Human / reviewer interpretation
      ↓
Issue / proposal
      ↓
Protocol or Runtime change
      ↓
CI verification
```

The protocol therefore creates a **verification loop**, not an autonomous self-modifying loop.

## Constraints

1. Do not treat usage volume as a quality score.
2. Do not infer user intent from execution traces alone.
3. Do not convert an error into a design conclusion without observation/review.
4. Do not require telemetry for local use unless a separately documented service requires it.
5. Preserve provenance of exported evidence.
6. Keep personal data out of evidence whenever it is not necessary for the stated verification purpose.
7. Do not use this protocol to expand the theoretical Shirakami Model; it is an implementation-side observation contract.

## Status

**α0.1 — implementation-side draft**

This document is a supporting protocol for external usage verification. It does not replace the existing Evidence Contract, Observation Review Protocol, Repository Event Contract, or normative specifications.
