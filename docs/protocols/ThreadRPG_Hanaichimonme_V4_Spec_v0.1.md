# 花いちもんめ方式 V4 — 実装仕様 v0.1

Status: draft / renderer boundary  
Date: 2026-11-27

## Source ledger

| Source | Status | What this document uses |
| --- | --- | --- |
| Continuing user's explicit definition (2026-11-27) | normative for this draft | Dynamic speaker/order/relation selection; no fixed role, mandatory participation, equal turns, forced conclusion, Reality mutation, or replacement of Human Gate. |
| Retrieved repository history, 2026-11-12–13 | implementation evidence only | V4 turn adapter, injected model bridge, reply provenance, observation boundary, and an earlier reaction-field experiment. It does not prove a 2026-11-16 Worker deployment or 86-response trial. |
| `ThreadRPG_Protocol_Generation_Policy_v0.1.md` | existing boundary | Synthetic viewpoints remain non-authoritative; uncertainty and human final decision remain visible. |

The original 11/16 Worker/protocol text and the claimed 86-response test were
not retrieved in this checkout. They are recorded as unverified history, not
as proof that this implementation reproduces them.

## Contract

`HanaichimonmeSession.generate()` is the actual generated-reply path:

`caller input → dynamic plan → injected generator → selected anonymous posts → semantic links → next session turn`

The input generator is injected. No provider, paid API, merge, deployment, or
Reality mutation is selected by this contract. `execute_hanaichimonme_request`
exposes the same path to a caller that owns a `HanaichimonmeSessionStore`.
The store is process-local; durable cross-process persistence is deliberately
not claimed.

## Dynamic selection

- Anonymous IDs are renderer labels, not fixed personalities or fixed roles.
- The planner considers recent posts and transparent semantic links, then picks
  a variable subset. A person may speak repeatedly; any candidate may be silent.
- A generated reply may cite an earlier post (`>>N`) or a prior reply in its
  batch. These are preserved as provenance, so horizontal replies are not
  flattened into answers to Icchi.
- Correction markers (`訂正`, `違う`, `いや`, `修正`) and research-return cues
  (`研究へ戻る`, `調べ直す`, `検証`, `続き`) are extractable links with the exact
  trigger and post index. This is transparent pattern extraction, not a claim
  to understand hidden intent or determine truth.
- Cue is an activation signal for a changed candidate subset. It is not queue,
  priority, command execution, or a guarantee of a response.

## Separate mechanisms

Hanaichimonme chooses rendering participants, sequence, and visible response
relations. The pre-existing reaction field is retained as a separate,
non-authoritative flow/strength experiment; it neither fixes V4 participants
nor selects replies. Queue remains a work queue and is not cue. Five recent
turns are a planner window, not a Matome-style layered compression.

## Subject-owned unresolved terms

An unresolved wish is not removed merely because an implementation demands an
Evidence ID. Resolution now requires explicit subject/caller confirmation;
optional Evidence can be retained as provenance. Neither the renderer nor a
semantic link decides that a wish has disappeared.

## Verification coverage

`tests/test_threadrpg_v4_hanaichimonme_flow.py` covers dynamic selection on
the generated-post path, a silent anonymous candidate, repeated anonymous
participation, horizontal reply/correction/cue links, session continuity, and
the transport helper. Tests using injected generators are mocks and do not
claim real-model behavior. Existing model-bridge tests remain offline fixtures.

## Deliberately unresolved

- Exact Worker deployment and the 86-response historical trial;
- durable session storage and cross-process recovery;
- a production model/provider contract and live-model evaluation;
- semantic relations beyond the documented transparent patterns;
- whether any generated material should become accepted Evidence or a fact.
