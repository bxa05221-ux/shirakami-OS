# Wayfinding API boundary

Status: implementation candidate

The completed AATS Wayfinding cycle is exposed through a framework-independent HTTP boundary at `/v1/wayfinding`.

Flow:
`HTTP → AATS Thread → Renzan → Kasen → Landscape → Small Step → Transition → Evidence → Landscape re-observation → JSON`

The API does not implement cognitive echo-location, 3D-PRUIM semantics, truth inference, or persona/IP editing. Semantic selection remains outside the transport boundary.

The endpoint is a transport adapter, not a new Protocol. LLM/backend choice remains replaceable.
