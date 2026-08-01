# Licensing Proposal — Shirakami OS (Future Governance)

This document records a proposal for future licensing governance for the Shirakami OS project. It is a discussion and planning document only — it does not change the repository's existing license or relicense any files.

IMPORTANT: Do not modify the existing root LICENSE file in the repository. Do not change the current MIT license in this commit. This proposal only records possible directions and constraints for future work.

## Current state

- The repository currently uses the MIT License (root LICENSE).
- The repository contains multiple categories of content which may have different legal and community implications:
  - Foundation Architecture
  - RFC Documents
  - Glossary
  - Specifications
  - Examples
  - Plugins / Extensions

## Observation

- Shirakami OS is an architecture-first specification project, not only a software implementation repository. The repository therefore contains both normative specification text and executable/illustrative implementation artifacts.
- A single, repository-wide MIT license is permissive and low-friction, but it may conflate distinct expectations for normative specification text vs implementation/example code.
- A future separation of licensing between specification/documentation and implementation materials may be worth considering to improve clarity for implementers, contributors, and downstream integrators.

## Possible future direction

The following is a proposed, non-binding direction for discussion:

- Keep MIT for implementation materials (examples, plugins, runtime code, and other implementation artifacts). MIT preserves maximal freedom for implementers and experimentation.
- Consider adopting a documentation/specification license such as Creative Commons Attribution 4.0 International (CC‑BY 4.0) for normative documents, RFCs, and specifications. CC‑BY ensures attribution while remaining permissive for reuse in standards and documentation contexts.
- Add lightweight governance documents *only when the ecosystem requires them* — for example, a short Trademark/Terminology policy and a CONTRIBUTING section that clarifies licensing expectations for new contributions.
- If patent clarity is an explicit concern for future implementers, consider Apache‑2.0 for code in lieu of MIT (or dual-licensing), but take this decision only after community consultation and (optionally) legal review.

## Constraints for this proposal

- No immediate relicensing: this document does not change the root LICENSE or any existing file licensing. Historical content remains licensed under MIT unless contributors explicitly agree otherwise.
- No license migration is enacted by this proposal.
- Preserve existing contributor expectations: do not impose retroactive obligations on past contributors. New contributions may be requested to adopt the new license for new/changed files once the project community agrees.

## Principle alignment — "Architecture First"

Licensing decisions should preserve and support the project's "Architecture First" principle by ensuring:

- Specification clarity: normative text should be clearly identifiable, versioned, and labelled so readers and implementers know what is authoritative.
- Implementation freedom: example code, plugins, and runtime implementations should remain easy to reuse and experiment with.
- Ecosystem compatibility: license choices should avoid blocking adoption, standardization, and downstream implementations where possible.

## Migration impact (summary)

- Low friction path: apply new licenses only to newly added or updated files, and publish a top-level mapping (e.g., `LICENSES.md`) describing which directories are intended to be under which license. Historical files remain under MIT unless contributors consent to relicensing.
- Higher friction path: retroactive relicensing of existing files will require contacting contributors for permission or adopting procedures (e.g., DCO/CLA) that allow re-licensing in the future.

## Recommended next steps (non-actionable in this commit)

1. Publish this proposal in `docs/` (this file) so contributors can review and discuss.
2. If the community agrees, prepare a `LICENSES.md` mapping file and per-directory license files, and update CONTRIBUTING to describe licensing expectations for future contributions.
3. Perform an authorship audit for files intended to be relicensed and gather consent where needed.
4. Draft a short Trademark / Terminology Use policy if the community wants to control use of the project brand or claims of conformance.

---

This is a proposal document only. It intentionally does not change the repository root LICENSE or relicence any existing files.
