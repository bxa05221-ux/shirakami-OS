# Local Repository → Replaceable LLM Boundary v0.1

This observation extends the Local Repository boundary by verifying that the
same local Protocol can be executed through two replaceable backend adapters.

## Verified path

```
Local Repository
      ↓
Protocol Loader
      ↓
ProtocolIR
      ↓
PipelinePlan
      ↓
PipelineAdapter
   ↙         ↘
LLM-A       LLM-B
```

The test uses deterministic backend functions rather than external model APIs.
The backend is therefore a stand-in for an LLM adapter boundary, not a model
quality evaluation.

## Invariants

- The ProtocolIR remains identical.
- Pipeline identity, version, phase, and action remain identical.
- Backend identity changes only at the Adapter boundary.
- Human Gate input remains explicit and is not converted into an AI decision.
- No provider-specific behavior is added to Protocol or Runtime.

## Meaning

This establishes the next part of the GitHub-to-Shirakami hypothesis:

> A Local Repository can provide a stable Shirakami environment while the
> execution backend is replaceable.

This is a boundary observation, not evidence that arbitrary production LLMs are
already interchangeable. Provider-specific adapters and real model verification
remain separate work.
