# Guide AI Consistency Audit v0.1

## Scope

Documentation-only audit of `docs/protocols/Guide_AI_Protocol_v0.1.md` against the current repository structure, registry, application protocol, runtime, and tests.

No runtime semantics are changed. No implementation, authorization, or semantic verification is claimed.

## Evidence inspected

- `docs/protocols/Guide_AI_Protocol_v0.1.md`
- `protocols/registry.yaml`
- `protocols/tsugaru-guide-highschool.yaml`
- `runtime/aat_thread_wayfinding.py`
- `runtime/way.py`
- `tests/test_aat_entry_flow.py`

## Findings

### G-01 — Protocol boundary is explicit

The Guide AI protocol clearly defines orientation and navigation as distinct from decision, authorization, execution, verification, and responsibility. It also requires human selection or review for route progression.

**Status:** Documented / structurally consistent.

### G-02 — Registry promotion boundary is consistent

The registry lists `guide_ai` as a candidate and states that its local knowledge Landscape connection remains pending. The protocol itself also identifies runtime implementation and API contract as non-goals.

**Status:** Consistent; runtime promotion remains pending.

### G-03 — No dedicated Guide AI runtime implementation was confirmed

The inspected runtime path contains Rensan, Kasen, Landscape observation, Small Step selection, transition application, and Evidence capture, but no dedicated Guide AI navigation object or output contract was confirmed.

**Status:** Unverified implementation / not integrated as a dedicated runtime layer.

### G-04 — Human Gate is documented, not encoded in the inspected path

The protocol requires human choice, review, consent, authorization, and execution boundaries. The inspected AATS wayfinding function selects and applies a Small Step through supplied interfaces, but does not expose a Guide AI-specific human decision record or approval state.

**Status:** Gap requiring future implementation and tests; no semantic fix made here.

### G-05 — Provenance and alternative routes are specified but not runtime-verified

The protocol requires provenance, open issues, route alternatives, boundary notices, and explicit uncertainty. Existing tests verify AATS, Rensan, Kasen, and basic entry flow behavior, but do not verify a Guide AI output schema, provenance propagation, alternative-route preservation, or stop-condition behavior.

**Status:** Runtime and semantic verification pending.

### G-06 — Application-level alignment exists

The Tsugaru Guide High School protocol includes student agency, observation before evaluation, evidence before assertion, restrictions against fabricated observations, and Guide AI roles before/during/after fieldwork. These principles align with the general Guide AI boundary, but their integration into a shared runtime contract is not established.

**Status:** Conceptual alignment confirmed; integration unverified.

## Summary matrix

| Area | Status | Note |
|---|---|---|
| Human final judgment | Documented | Runtime gate not confirmed |
| Evidence boundary | Documented | Guide-specific provenance propagation unverified |
| Uncertainty handling | Documented | Stop-condition tests absent |
| Responsibility boundary | Documented | No dedicated Guide runtime contract confirmed |
| Composability | Conceptual | Protocol routing described; integration unverified |
| Runtime implementation | Not confirmed | Existing wayfinding path is not Guide AI implementation |
| Tests | Partial | No dedicated Guide AI contract tests confirmed |

## Follow-up candidates

1. Define a minimal Guide AI output schema before implementation.
2. Add tests for provenance, alternative routes, boundary notices, and human selection.
3. Separate route suggestion from any Small Step application boundary.
4. Define how Guide AI records guidance and the subsequent human decision as separate Evidence.
5. Connect local knowledge Landscape references without promoting the registry entry directly into a Runtime Contract.

## Conclusion

Guide AI is currently a well-defined documentation-level candidate with clear human-agency and provenance boundaries. Its relationship to existing application protocols is conceptually visible, but a dedicated runtime contract, human-gate representation, provenance propagation, and semantic test coverage remain unverified.