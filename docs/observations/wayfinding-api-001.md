# Wayfinding HTTP API boundary

Status: implemented

The completed AATS Wayfinding cycle is exposed through a framework-independent HTTP boundary at `POST /v1/wayfinding`.

Flow:
`HTTP → AATS Thread → Renzan → Kasen → Landscape → Small Step → Transition → Evidence → Landscape re-observation → JSON`

The endpoint is a transport adapter, not a new Protocol. LLM/backend choice remains replaceable.
