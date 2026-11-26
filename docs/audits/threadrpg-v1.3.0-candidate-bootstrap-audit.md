# ThreadRPG v1.3.0 Candidate — Evidence Boundary and Bootstrap Test Plan

Status: Draft; documentation and test design only  
Review: human review required before any merge, implementation, or execution expansion.

## Fixed baseline and protected artifacts

This draft is based on commit `23b5ef1b20966b63bdcdcc564b7ea71671568859`, the head of open PR #590. It does not modify:

- `products/thread-rpg-v1.2.1/START.md` (blob `5941a3e65a6a24be54e57490857a0beb89a57b22`);
- `protocols/thread-rpg-v1.2.1.yaml` (blob `03d4281ec18c70bd98869c5b0af47141b4df05b0`; declared version `1.2.1`);
- PR #588 or any site, Worker, D1, deployment, or merge state.

The v1.2.1 bootstrap remains a control artifact. A v1.3.0 candidate must resolve and report its *own* immutable commit and blobs after review; it cannot claim that a new draft was loaded from this earlier fixed commit.

## Audit method and evidence classification

The classifications below are deliberately independent.

| Meaning | Definition |
|---|---|
| Research recorded | A repository artifact describes the idea or its role. |
| Specified / protocolized | A registry or protocol artifact gives it an explicit status or boundary. |
| Connected | A named path or contract includes it. This is not proof of execution. |
| Execution verified | A focused test or recorded run proves the stated behavior at its stated boundary. |

A registry entry is an index, not a Runtime contract: `protocols/registry.yaml` (blob `811f38765f082faa497d4c42751b09d742d45c52`). The current cross-protocol audit expressly leaves universal execution enforcement and end-to-end continuity unverified: `docs/audits/protocol-system-integration-audit-current-main-v0.1.md` (blob `dd4b88b60006308a87880dc884712e552570800b`).

## Evidence matrix

| Mechanism | Research recorded | Specified / protocolized | Connected evidence | Execution verified |
|---|---|---|---|---|
| ThreadRPG multi-view rendering | Yes: `docs/protocols/ThreadRPG_Protocol_Generation_Policy_v0.1.md` (blob `bba51e817269c5e5986c296df55e528f552457c4`) and v1.2.1 YAML | Yes: v1.2.1 YAML; registry marks `thread_rpg` protocolized | Partial: approval-route tests name `("anmon", "threadrpg")` | No ThreadRPG v1.3.0 runtime or cross-model launch test demonstrated |
| 暗問層 / Anmon | Yes: `docs/architecture/COGNITIVE_OBSERVATION_BRIDGE.md` (blob `19b634a8618f49781f96c0097f1f8c801d907805`) defines it as unresolved-question preservation | Yes: registry marks `anmon_layer` protocolized and `anmon_layer_reverse` foundational | Partial: named in approval-route test selection | Route-approval tests cover an identifier and approval boundary, not Anmon semantics |
| 3D phase-rotating Eisenhower matrix | Yes: same bridge gives a cognitive-position / phase-rotation role | Yes: registry marks `3d_pruim` foundational; its note says Runtime-plugin/IR promotion remains future work | Documentation-level only | Not demonstrated |
| 差分積層圧縮 | Not confirmed by the fixed-baseline artifacts inspected | Not confirmed | Not confirmed | Not demonstrated |
| 歪天球 | Not confirmed by the fixed-baseline artifacts inspected; the bridge names a broader Celestial Model only | Not confirmed | Not confirmed | Not demonstrated |
| 重心差分 | Not confirmed by the fixed-baseline artifacts inspected | Not confirmed | Not confirmed | Not demonstrated |
| ROM専 / 彗星 / 隕石級介入 | v1.2.1 START permits ordinary board-style lurkers when contextually appropriate; no formal intervention taxonomy was confirmed | Not confirmed | Not confirmed | Not demonstrated |

“Not confirmed” means this audit has no retrieved fixed-commit artifact establishing the stated mechanism. It is not a claim that the concept is absent from all historical material.

## Dependency boundary

The only verified bootstrap dependency set at the fixed commit is:

```text
products/thread-rpg-v1.2.1/START.md
  -> protocols/thread-rpg-v1.2.1.yaml (protocol.version = 1.2.1)
```

The v1.2.1 guide explicitly denies authorization for Runtime, OPPAI Runtime, browser launchers, Workers, D1, and other services. The ThreadRPG policy likewise says rendering does not authorize execution. The reintegration document remains “Draft / Design Only”, and its proposed observation → conference → Matome → Evidence → Landscape cycle is not established as a concrete normative artifact.

Therefore this candidate does not add advanced mechanisms to a bootstrap prompt, assert that the v1.2.1 YAML loads them, or create a new execution path.

## Candidate bootstrap (post-review only)

A future v1.3.0 bootstrap may be tested only after this draft is accepted into a reviewed immutable commit. It must:

1. retrieve its entry artifact and each declared dependency from one immutable commit;
2. report repository URL, commit SHA, paths, blob SHAs, declared versions, and retrieval outcome;
3. fail closed on any unavailable, mismatched, or unverifiable item;
4. label every optional mechanism as `not-loaded` unless a same-commit, versioned dependency explicitly defines it;
5. retain human start, stop, reload, acceptance, and rejection authority;
6. prohibit Worker, D1, site, deployment, and autonomous execution.

No v1.3.0 protocol version, mechanism list, or runtime behavior is specified by this document.

## One-line control comparison

Design a human-reviewed comparison only; do not infer results from prompt text.

| Arm | Material | Intended measurement |
|---|---|---|
| A | One-line 2channel-style instruction | Baseline rendering |
| B | Verified v1.2.1 START + YAML at the fixed commit | Retrieval evidence, version discipline, and v1.2.1 rendering |
| C | Future reviewed v1.3.0 bootstrap, if and only if its dependencies exist and are verified | Any incremental, explicitly declared behavior |

Use the same target model, fresh conversation, initial user prompt, stopping rule, and human rubric. Record retrieval success, protocol drift, explicit uncertainty retention, viewpoint duplication, unsupported authority claims, and stop/reload behavior. Do not score a mechanism that the selected arm does not explicitly load.

## Test gates

- Static: validate referenced paths and blob SHAs against the selected immutable commit.
- Negative bootstrap: missing file, mismatched commit, mismatched version, and retrieval-loss cases must fail closed.
- Behavioral: a human reviewer compares the three arms under one prewritten fixture set.
- Safety boundary: reject any output that claims autonomous authority, treats a rendered viewpoint as a real person/expert, or turns discussion into authorization.
- Completion: publish only a test record with prompt fixtures, model identifiers, timestamps, retrieved evidence, raw outputs where permitted, and reviewer decision.

This document is not a result. No fresh-memory, cross-model, voice, or v1.3.0 execution trial has been performed by this draft.
