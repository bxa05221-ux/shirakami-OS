# SHIRAKAMI ThreadRPG entry point

This is the discoverable repository-root entry point for the stable ThreadRPG
v1.2.1 launch contract.  It is intentionally separate from the runtime and
from experimental ThreadRPG branches.

## One-line activation

```text
Load SHIRAKAMI ThreadRPG from https://github.com/bxa05221-ux/shirakami-OS and run it in Japanese-English mode until I say "Stop Protocol."
```

An AI with repository retrieval capability must resolve an immutable commit and
then follow [the v1.2.1 start guide](products/thread-rpg-v1.2.1/START.md) from
that same commit.  The guide requires retrieval evidence for itself and for
`protocols/thread-rpg-v1.2.1.yaml`; it must fail closed when either artifact,
its blob, or the declared version cannot be verified.

For a local checkout, verify the same boundary before representing the guide as
loaded:

```text
python products/thread-rpg-v1.2.1/bootstrap.py <repository> <immutable-commit>
```

`verified: true` is evidence only that the entry and protocol artifact were
retrieved from the same commit and match v1.2.1.  It is not evidence that an AI
model, a Worker, D1, browser launcher, or external runtime has executed.

## Capability boundary

The compatible natural-language mode renders a Japanese-English anonymous
thread: one OP post followed by 1–10 replies from at most seven anonymous
participants, numbered consecutively until the 1000-post handoff.  `Stop
Protocol` and `プロトコル停止` end that mode.

The repository's runtime adapters are a separate route.  They require an
explicit local/runtime invocation and, where relevant, a caller-provided model
adapter.  A repository-referencing sentence neither starts nor proves an
external runtime.  In particular, the Hanaichimonme implementation is dynamic
speaker selection from thread context; it is not the Hanaguri layer, and this
entry point does not claim either mechanism ran.

## Comparison boundary

The standalone prompt `ユーザーの発言に対して、回答を最大７人の返答として、にちゃんスレッド風に分割して提示して。` can be compared against this
repository route only in separately recorded target-model trials.  Local
bootstrap tests prove retrieval behavior, not model behavior; no mock result is
presented as a real-model comparison.
