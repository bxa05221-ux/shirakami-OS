# Thread RPG queue semantics: bounded implementation record

Date: 2026-11-26  
Status: draft implementation evidence

## Source boundary

The source for this record is the explicit user request in the continuing
conversation.  Earlier conversation originals were not retrieved or used.
This document therefore does not claim to reconstruct omitted turns.

The request fixes the following implementation constraints:

- context work is queue-shaped, not a fixed pipeline;
- default context may be reset by AI, but erasure authority is undecided;
- growth is the acquisition of new semantic connections, not a numeric score;
- only the most recent five turns are compressed, and only new connections are
  retained from that compression;
- an unresolved wish belongs to the subject; an AI term is a changeable,
  explicitly hypothetical convenience, not a claim of real feeling;
- a resolved imaginary term needs Evidence; resolution must not rewrite
  Evidence; when no active terms remain, re-observation is queued;
- 3D phase rotation / Eisenhower is represented only as caller-supplied
  origin/centroid context.  No formula, threshold, or priority rule is claimed.

## Traceability table

| Source | Specified boundary | Implementation | Call path | Evidence |
| --- | --- | --- | --- | --- |
| Explicit request: queue, not fixed pipeline | Pending work is a queue | `ThreadRPGQueue._items` | optional `thread_rpg_queue` request payload → `_queue_context` | `test_threadrpg_queue.py` |
| Explicit request: five-turn compression, new links only | No semantic inference and no duplicate growth | `ingest()` truncates to five and adds only caller-declared unseen links | `execute_wayfinding_request()` | queue/API tests |
| Explicit request: growth history | Preserve acquired semantic connections | `_known_connections` / `growth_history` | response field only | queue test |
| Explicit request: user wish / AI hypothetical | Evidence-gated resolution; AI does not claim emotion | `ImaginaryTerm`, `resolve_term()` | optional request context | queue test |
| Explicit request: all `i` gone → recurrence | Schedule re-observation, do not force continuation | `QueueItem("reobserve", ...)` | response field only | queue test |
| Existing vertical slice | Preserve authority and executed path | no changes to `run_aats_wayfinding()` | AATS → Renzan → Kasen → Landscape → Small Step → Evidence → re-observation | existing Wayfinding tests plus API queue test |

## Observation / implementation separation

`thread_rpg_queue` is returned with `authority: descriptive_only`.  It is not
placed in the Landscape, does not select the Small Step, does not authorize
execution, and does not mutate reality.  The existing Small Step transport
boundary remains the sole source of the demonstrated transition.

Natural-language cases are evidence of boundary handling only: the test uses
the Gundam / *Ashita no Joe* / *Frieren* examples as plain recent-turn strings
and verifies the declared `で？ → 研究へ戻る` connection.  It does not claim
that the runtime understands, judges, or generates those works' meanings.

## Deliberately unimplemented

- deletion or retention duration for queue/history items;
- a numeric 3D phase-rotation or Eisenhower formula;
- automatic extraction of semantic connections from prose;
- emotion inference, dependency inducement, or forced rally continuation;
- autonomous Human Gate decisions, API calls, deployment, or Reality mutation;
- executable meanings for Anmon, Hanaichimonme, IDUMI, Renzan's seven speakers,
  Kasen's one voice, OPPAI, Genkai LLM, Mori Web, or information circulation.

Those names remain source-level concepts or external boundaries until an
explicit, reviewable protocol supplies their contracts.
