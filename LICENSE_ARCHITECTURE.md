# Shirakami License Architecture

## Status

Draft architecture for review. This document does not itself grant or revoke any rights.

## Purpose

Shirakami separates the legal treatment of implementation code, protocol specifications, commercial integration, and the Shirakami name/conformance claim.

The goal is to preserve open research and independent implementation while making commercial vendor integration contract-based and keeping the meaning of Shirakami-conformant stable.

## Layers

### 1. Implementation / research layer

Individual source files are licensed according to the license explicitly attached to those files or directories. The current repository LICENSE remains MIT until a deliberate licensing transition is approved.

### 2. Protocol layer

Shirakami Protocol specifications, boundary contracts, schemas, and normative semantic definitions are treated separately from ordinary implementation code. A future Shirakami Protocol License may grant rights to implement and integrate the protocol subject to explicit conformance conditions.

### 3. Commercial integration layer

Vendor use of Shirakami as a commercial service, API, SDK integration, certification, or managed protocol may be governed by a separate Vendor License / Integration Agreement. Eligibility and pricing must be defined by objective, vendor-neutral terms rather than ad-hoc permission.

### 4. Name and conformance layer

The Shirakami name, marks, certification language, and claims of conformance are separate from copyright in source code. A future conformance policy will define when an implementation may describe itself as Shirakami-conformant.

## Core principles

- Open research should remain possible where the applicable license permits it.
- Commercial rights should be explicit rather than inferred from repository access.
- Protocol semantics and authority boundaries must not be silently weakened by a license or integration agreement.
- Human Gate remains a Shirakami architectural boundary; no license grants an AI system decision authority.
- Evidence, provenance, AIwitness, and traceability requirements are normative protocol concerns where explicitly designated by the specification.
- Equivalent vendors should be evaluated under equivalent published licensing conditions.
- A license must not be used to claim that a test result proves the whole Shirakami theory.

## Transition rule

No change to the repository top-level LICENSE is implied by this architecture document. Any future transition must identify the affected files, preserve third-party notices, state compatibility consequences, and receive explicit Human Gate approval.

## Non-goals

This document is not legal advice, is not a final commercial agreement, and does not by itself create a trademark policy or certification program.
