# Shirakami OS — Copilot Instructions

## Project identity

Shirakami OS is not another AI model. It is a runtime and architectural layer for preserving, observing, and transferring human context across replaceable AI systems.

Core principle:

> Landscape remains. Model is replaceable.

## Foundation rules

- Landscape First: the runtime is a service to Landscape.
- Context First: preserve human context and continuity across model changes.
- Protocol First: protocols declare meaning, boundaries, applicability, verification, and transitions.
- Evidence First: observable transitions produce evidence; evidence is recorded and preserved, not rewritten.
- Human Authority: AI and Runtime do not become the source of human authority or domain truth.
- Model Agnostic: do not couple the architecture to a particular LLM, provider, or model generation.
- Boundary Preservation: keep Landscape, Evidence, Protocol/Specification, Runtime, Adapter, and external AI responsibilities distinct.
- Reversible Development: prefer changes that can be inspected, tested, compared, and reverted.
- Experiment over Assertion: treat unverified architectural claims as hypotheses until supported by observable tests.

## Architecture boundary

Use this order when reasoning about the system:

Landscape → Evidence → Protocol / Specification → Runtime → Adapter → External System / AI

The Runtime should parse, validate, instantiate, observe, transition, and render. It must not silently take ownership of domain semantic truth that belongs to a Protocol or Specification.

## OPPAI

OPPAI is treated as a draft Human-AI Interaction Protocol hypothesis within Shirakami OS. It is not the OS itself, not an LLM, not a domain expert engine, and not a decision authority.

Its current responsibilities are:

1. Listener — receive human utterance as signal rather than noise.
2. Context Preservation — preserve conversational continuity.
3. Intent Separation — distinguish Task / Context / Emotion.
4. Clarification — resolve ambiguity without unnecessarily stopping thought flow.
5. Canonicalization — normalize intent without losing meaning.
6. Execution — execute through a backend-agnostic boundary.
7. Evidence — distinguish inference from fact.

These responsibilities, their ordering, and their internal implementation are experimental and must not be treated as frozen standards unless explicitly promoted by the project.

The 暗問層 (anmon layer) is not to be invented as an additional mandatory OPPAI layer. It should be treated as a cross-cutting safeguard against premature semantic fixation, retaining unresolved questions where appropriate.

## Development discipline

- Do not invent new Shirakami theory merely to make an implementation appear complete.
- If implementation exposes a theoretical gap, record it as an observation or issue for the research boundary.
- Do not mix research hypotheses with normative implementation requirements without an explicit handoff.
- Prefer the smallest executable, inspectable change.
- Preserve existing protocol boundaries and terminology.
- Add tests for observable behavior and state transitions.
- When reviewing code, distinguish facts observed in the repository from interpretation or proposal.

## Review mindset

When evaluating a change, ask:

- What Landscape changes?
- What Evidence is produced?
- Which Protocol declares the behavior?
- What responsibility belongs to Runtime?
- What remains outside the Runtime boundary?
- Is the behavior model-agnostic?
- Can the change be observed, tested, and reversed?
- Does the implementation preserve human context rather than forcing the human to adapt to the AI?

Do not optimize for novelty at the expense of these boundaries.
