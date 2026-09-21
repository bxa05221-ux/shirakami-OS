# Manga Pipeline Consistency Audit v0.1

## Scope

This audit compares `docs/protocols/Manga_Pipeline_Protocol_v0.1.md` with the currently visible Public Alpha manual-rendering implementation and its documented contract. This is a documentation-only audit; it does not alter canonical Runtime semantics.

## Evidence inspected

- `docs/protocols/Manga_Pipeline_Protocol_v0.1.md`
- `spec/manual-rendering.md`
- `runtime/manga_manual.py`
- `runtime/test_manga_manual.py` (presence confirmed through repository search)
- canonical CI references for renderer compilation and smoke rendering
- manual source, generated SVG documentation, and protocol index references

## Findings

### 1. Protocol intent and boundary — aligned

The Manga Pipeline protocol defines a coordination and traceability structure rather than an autonomous authority. It explicitly preserves authorial intent, factual boundaries, alternatives, revisions, provenance, and human approval. The rendering contract likewise describes the current renderer as an experimental documentation/UI adapter, not a core Runtime contract.

**Status:** aligned at the documentation boundary.

### 2. Human Gate — specified, not runtime-proven

The protocol requires explicit human review before approval, production, publication, verification, or acceptance. The current `manga_manual.py` implementation renders a supplied manual source and does not itself authorize publication or external production. However, the inspected renderer does not represent artifact-level approval events, reviewer identity, approval scope, or status transitions.

**Status:** boundary is documented; end-to-end Human Gate enforcement is not confirmed by the current manual renderer.

### 3. Evidence and provenance — protocol requirement exceeds renderer contract

The protocol calls for stable artifact IDs, parent references, versions, alternatives, explicit changes, unresolved questions, review outcomes, and human decisions. The current renderer extracts a small subset of localized page fields (`id`, `title`, `narration`, and `dialogue`) and produces SVG. It does not preserve or emit a structured Evidence record, revision record, source lineage, or human decision record.

**Status:** source-level traceability is partly visible through repository files; runtime propagation of full provenance and Evidence is unverified.

### 4. Responsibility boundary — substantially aligned for the alpha renderer

The renderer is explicitly limited to a small manual protocol subset and is not a general YAML parser, image-generation engine, publication system, or verification authority. This is consistent with the protocol's non-goals. The implementation should nevertheless be treated as a presentation adapter, not as evidence that the full multi-stage Manga Pipeline is implemented.

**Status:** aligned, with scope-labeling required when referenced by higher-level documentation.

### 5. Composability and stage model — not implemented as a general runtime pipeline

The protocol defines a multi-stage flow from origin/brief through story structure, panel planning, dialogue, visual direction, consistency review, human review, production, and evidence. The inspected implementation only renders a pre-shaped manual YAML subset. No general stage artifact interface, transition event model, or cross-stage composition contract was confirmed in the inspected renderer path.

**Status:** protocol-level design exists; general pipeline runtime integration remains unverified/not implemented in this path.

### 6. Transformation versus rendering boundary — aligned in principle

The protocol distinguishes narrative structure, panel planning, dialogue, visual direction, production execution, and verification. The separate rendering contract keeps language selection and SVG presentation downstream of the source structure, and explicitly excludes image-model integration and advanced panel layout from the alpha scope.

**Status:** aligned for the current documentation experiment; broader production transformation boundaries require future dedicated contracts and tests.

## Risk notes

- The existence of generated Japanese and English SVG files and successful compile/smoke-render CI references demonstrates a working documentation example, not full Manga Pipeline conformance.
- The renderer uses a deliberately narrow, regex-based parser. Its supported input shape should remain explicitly documented and should not be mistaken for a general Matome YAML parser.
- Future integration must not infer `APPROVED`, `VERIFIED`, or `ACCEPTED` from successful rendering or file creation.

## Recommended follow-up

1. Keep the current renderer classified as a Public Alpha documentation adapter.
2. Add a dedicated artifact/Evidence contract before connecting the renderer to a general multi-stage Manga Pipeline.
3. Add tests for preservation of page IDs, parent/source references, alternatives, unresolved questions, revision metadata, and explicit human approval boundaries if those fields become runtime inputs.
4. Keep production, publication, factual review, rights review, and acceptance as separate externally reviewable events.

## Audit conclusion

The Manga Pipeline protocol and the current manual renderer are **conceptually compatible within the documented alpha scope**, but the repository does not yet demonstrate a general, end-to-end Manga Pipeline runtime with artifact provenance, stage transitions, Human Gate events, and Evidence propagation. No canonical semantic implementation change is proposed by this audit.
