# Shirakami Radio Protocol v0.1

## 1. Purpose

Shirakami Radio is a conversational audio format that introduces Shirakami's ideas and observations without turning the host, AI, or listener into an authority hierarchy.

The radio is a **guided listening space**, not an automated decision or persuasion system.

## 2. Core Principles

- Human editorial responsibility remains explicit.
- AI may assist with drafting, variation, structure, and consistency checks, but does not decide the final message.
- Observation, interpretation, speculation, and fiction must be distinguishable.
- The tone should preserve room for hesitation, silence, humor, and disagreement.
- A calm presentation must not disguise uncertainty or manufacture credibility.
- Personal information, quotations, and third-party claims require provenance and appropriate handling.

## 3. Production Flow

```text
Theme / Source
  -> Context and Intent Extraction
  -> Segment Planning
  -> Script Draft
  -> Voice / Sound Direction
  -> Fact and Attribution Check
  -> Human Editorial Review
  -> Recording or Synthesis
  -> Listening Review
  -> Release Package
  -> Evidence and Revision Record
```

No stage implies automatic publication.

## 4. Segment Types

- **Opening**: establishes the topic, atmosphere, and listening frame.
- **Observation**: reports an experience, event, or source with clear boundaries.
- **Reflection**: develops an interpretation while marking it as interpretation.
- **Conversation**: presents multiple perspectives without forcing a conclusion.
- **Protocol Corner**: explains a Shirakami concept through an example or small experiment.
- **Pause / Transition**: gives listeners time to process and prevents excessive information density.
- **Closing**: summarizes open questions and identifies what remains unresolved.

## 5. Required Metadata

Each segment should retain:

- segment_id and version
- source references and provenance
- intended audience and duration
- authorial intent
- factual claims and verification status
- generated suggestions and human edits
- uncertainty, alternatives, and unresolved questions
- music, sound, image, quotation, and rights notes
- approval status and reviewer identity or role

## 6. Role Boundaries

### Human editor / host

- determines purpose, audience, tone, and final wording
- accepts, revises, or rejects AI suggestions
- confirms publication authorization and rights
- decides how uncertainty is communicated

### AI assistant

- proposes outlines, scripts, transitions, questions, and alternative phrasings
- identifies possible contradictions, unsupported claims, and missing context
- must not impersonate a real person or fabricate testimony
- must not silently remove uncertainty or convert speculation into fact
- must not treat polished language as evidence of correctness

### Listener

- remains an interpreter and participant, not a passive recipient of an official answer
- may be invited to submit questions, corrections, and alternative perspectives

## 7. Review Gates

Release must pause when any of the following applies:

- the speaker's intent is ambiguous
- a factual claim lacks adequate provenance
- fiction and reality could be confused
- a quotation, music, voice, or image has unresolved rights issues
- a generated revision materially changes meaning
- a personal story requires consent or privacy review
- the host cannot explain what was generated, changed, or verified

## 8. Evidence Record

The release package should preserve a compact record of:

- original brief and source set
- script versions and meaningful revisions
- verification results and unresolved limitations
- human acceptance decision
- recording / rendering version
- post-release corrections and listener feedback

Evidence records document the production process; they do not prove that every statement is objectively true.

## 9. Shirakami Connections

- **Anmon Layer**: asks what should remain unspoken, uncertain, or deferred.
- **3D Eisenhower Matrix**: organizes urgency, importance, and phase before production.
- **ThreadRPG**: supports multi-voice exploration and meaning-oriented conversation.
- **Rensan**: connects separate observations into a traceable chain without erasing differences.
- **Kasen**: compresses and redistributes meaning while preserving context.
- **Guide AI**: assists navigation and questioning without becoming the final authority.
- **Manga Pipeline**: shares provenance, review gates, and separation between drafting and approval.

## 10. Illustrative Record

```yaml
radio_segment:
  segment_id: radio-001
  version: 0.1
  status: REVIEW_REQUIRED
  theme: "AIが脇役の世界"
  duration_target: "8-12m"
  intent: "問いを残し、判断を聴き手へ返す"
  sources:
    - type: personal_observation
      provenance: required
  claims:
    - text: "例示される主張"
      status: unverified
  ai_contribution:
    allowed: true
    role: drafting_and_consistency_check
  human_decision:
    required: true
    publication_authorized: false
  unresolved_questions: []
```

## 11. Version Boundary

Version 0.1 defines the documentation-level production and review protocol only. It does not implement autonomous broadcasting, automatic publication, synthetic identity, audience profiling, or automated editorial authority.
