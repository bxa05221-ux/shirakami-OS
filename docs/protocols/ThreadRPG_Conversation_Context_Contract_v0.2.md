# ThreadRPG Conversation Context Contract v0.2

Status: proposed protocol contract / review required

## Purpose

This contract adds a minimal conversation-level constraint to the existing
ThreadRPG policy.  It does not introduce a persistent character system, a new
Runtime service, or decision authority.

ThreadRPG continuity belongs to the conversation context: its prior claims,
corrections, unresolved questions, references, and changes in wording.  It
does not belong to an anonymous participant's stable personality.

## Required rendering properties

### Context, not persona, persists

- A later post MAY refer to earlier posts, corrections, and unresolved matters.
- An anonymous viewpoint MAY appear, disappear, or be replaced between turns.
- The renderer MUST NOT represent an anonymous participant as a stable person
  merely to create continuity.
- Conversation context MUST remain distinguishable from generated persona-like
  presentation.

### Productive incompleteness

The renderer MAY include a mistaken reading, a repeated question, a late
participant, a disagreement, a digression, or an unanswered question when it
is connected to the available context.

Such contributions are not evidence, diagnosis, consent, or authority.  They
must remain visibly revisable by the user and by subsequent viewpoints.

### Room for the user's own words

- The renderer MUST preserve a route for the user to correct a viewpoint.
- It MUST NOT state an unprovided inner state, motive, feeling, or life history
  as though it were established fact.
- It MUST NOT force every turn into empathy, reassurance, summary, or a final
  lesson.
- It MAY ask, disagree, or leave an issue open rather than completing an
  interpretation on the user's behalf.

## Safety and authority boundary

This contract does not weaken the existing policy to stop or request
clarification when safety, intent, authority, consent, or responsibility is
unclear.  Contextual ambiguity is not authorization to make a safety or
decision claim.

## Conformance scenarios

An implementation claiming this contract must demonstrate all of the following
without asserting that synthetic viewpoints are real people:

1. A correction changes the available context for a later post.
2. A later post can participate without a stable anonymous identity.
3. Repetition or disagreement leaves the user's interpretation open.
4. A generated post does not assert an unprovided inner state as fact.

## Non-goals

This contract does not define a clinical, crisis-response, or therapeutic
protocol; it does not authorize autonomous action; and it does not make a
ThreadRPG output a decision or an Evidence record by itself.
