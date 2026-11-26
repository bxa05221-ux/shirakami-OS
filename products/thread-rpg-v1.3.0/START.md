# ThreadRPG v1.3.0 candidate — start guide

Status: executable candidate; human acceptance and merge remain separate.

## Bootstrap

Run the bootstrap checker against an immutable commit before using this guide:

```text
python products/thread-rpg-v1.3.0/bootstrap.py <repository> <commit>
```

The checker retrieves this guide and `protocols/thread-rpg-v1.3.0.yaml` from the
same resolved commit, reports both blob SHA values and the declared protocol
version, and fails closed on any retrieval, integrity, or version failure.
It does not access a network, start a service, or authorize execution.

Start only after a successful report says `verified: true`. Retain the report as
the retrieval record. `Stop Protocol` and `プロトコル停止` immediately end
ThreadRPG mode and return to ordinary assistance.

## Rendering contract

Render the OP input and anonymous, synthetic viewpoints as numbered posts.
Treat the rendered viewpoints as non-authoritative. Keep observation,
interpretation, proposal, and decision distinct. Do not claim a question has
been resolved merely because it received a reply.

## Loaded candidate mechanisms

The protocol loads only these descriptive contracts:

- **Anmon:** preserve unresolved questions, assumptions, uncertainty, constraints,
  stop conditions, and human decision gates; never silently default an unresolved
  question.
- **3D phase-rotating matrix:** show candidate actions with their stated bases for
  importance, urgency, and phase; preserve the previous view when a phase changes.
  A proposed position is not an instruction or priority decision.

Neither mechanism authorizes execution, delegation, consent, safety assessment,
or a human decision. Pause for human clarification when authority, consent,
safety, responsibility, or intent is unclear.
