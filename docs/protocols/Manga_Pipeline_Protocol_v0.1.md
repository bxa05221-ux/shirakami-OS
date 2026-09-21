# Manga Pipeline Protocol v0.1

## Status

Documentation-first protocol definition. This document does not introduce autonomous generation, publication, authorization, or verification behavior.

## Purpose

The Manga Pipeline Protocol organizes creative work from an originating idea to a reviewable manga production plan while preserving authorial intent, factual boundaries, creative changes, provenance, and human approval.

The pipeline is a **coordination and traceability structure**, not an automatic authority.

## Core Pipeline

```text
Origin / Brief
  → Context and Intent Extraction
  → Story Structure
  → Page and Panel Planning
  → Dialogue and Caption Draft
  → Visual Direction
  → Consistency Review
  → Human Review
  → Approved Production Package
  → Rendering / External Production
  → Evidence and Revision Record
```

Each stage produces a candidate artifact. A later stage must not silently overwrite the intent, constraints, or uncertainty of an earlier stage.

## Required Separations

The protocol MUST distinguish:

- source material from generated interpretation;
- real-world facts from fictional additions;
- author instruction from model suggestion;
- narrative structure from visual execution;
- draft content from approved content;
- production execution from quality or factual verification;
- revision from silent correction;
- observation from evaluation.

## Inputs

- originating brief or source;
- intended audience and format;
- authorial intent and non-negotiable elements;
- factual constraints and fictionalization policy;
- character, setting, timeline, and continuity information;
- safety, consent, privacy, and rights constraints;
- review criteria and stop conditions.

## Stage Outputs

Every stage SHOULD record:

- stable artifact ID and version;
- source and parent artifact references;
- current stage and status;
- generated contribution;
- preserved uncertainties and alternatives;
- explicit changes from the previous artifact;
- review questions and unresolved conflicts;
- human approval boundary.

## Stage Guidance

### 1. Origin / Brief

Capture the source, purpose, audience, intended effect, and author-defined boundaries without expanding the brief by assumption.

### 2. Context and Intent Extraction

Separate observed source information from interpretation. Ask questions when intent, setting, chronology, or rights are unclear.

### 3. Story Structure

Propose premise, beats, scene order, character roles, and pacing. Alternatives remain visible until human selection.

### 4. Page and Panel Planning

Translate the selected structure into pages, panels, visual focus, transitions, and reading direction. Do not treat panel plans as final artwork.

### 5. Dialogue and Caption Draft

Draft speech, narration, sound effects, and captions while preserving speaker identity, tone, and uncertainty. Do not invent quotations or attribute invented statements to real people.

### 6. Visual Direction

Describe composition, perspective, expressions, setting, lighting, continuity, and exclusions. Visual instructions remain subordinate to approved story intent.

### 7. Consistency Review

Surface contradictions, missing transitions, continuity breaks, unsupported factual claims, rights concerns, and mismatches between text and visual direction. Review does not itself authorize publication.

### 8. Human Review

The human author or designated reviewer decides whether to accept, revise, reject, or suspend each artifact. No generated confidence score substitutes for this decision.

### 9. Production and Evidence

Rendering or external production is executed only after explicit authorization. Record the selected artifact versions, tool or backend identity when available, revisions, observations, and review outcomes.

## Status Vocabulary

```text
IDEA
→ BRIEFED
→ STRUCTURED
→ BOARDED
→ SCRIPTED
→ VISUALLY_SPECIFIED
→ REVIEW_REQUIRED
→ APPROVED
→ IN_PRODUCTION
→ OBSERVED
→ VERIFIED (external review)
→ ACCEPTED
```

Additional terminal or interrupt states:

- `REJECTED`
- `REVISED`
- `SUSPENDED`
- `SUPERSEDED`

Status transitions require an explicit event or human review record. The pipeline MUST NOT infer approval from completion alone.

## Stop Conditions

Pause the pipeline when:

- source intent is ambiguous in a consequential way;
- factual and fictional material cannot be distinguished;
- continuity conflicts remain unresolved;
- consent, privacy, copyright, or other rights are uncertain;
- a generated change materially alters the author's intended meaning;
- the system cannot preserve provenance or revision history;
- a reviewer requests suspension or further clarification.

## Role Boundaries

The pipeline may organize, compare, draft, visualize, and surface inconsistencies. It must not independently:

- decide the author's intent;
- declare factual truth or legal permission;
- authorize publication or external action;
- erase conflicting drafts or uncertainty;
- represent generated dialogue as a real person's statement;
- convert production completion into verification or acceptance.

## Illustrative YAML

```yaml
manga_pipeline:
  id: manga-pipeline-example-001
  version: "0.1"
  status: REVIEW_REQUIRED
  origin:
    source_ref: brief-001
    author_intent: "Preserve the emotional turning point"
  constraints:
    factual_boundary: "Separate documented events from fiction"
    approval_required: true
  stages:
    - id: structure-001
      type: story_structure
      status: CANDIDATE
      parent_refs: [brief-001]
      alternatives: [structure-a, structure-b]
    - id: board-001
      type: panel_plan
      status: REVIEW_REQUIRED
      parent_refs: [structure-001]
      unresolved_questions:
        - "Does the transition preserve the intended meaning?"
  evidence_plan:
    record_artifact_versions: true
    record_revisions: true
    record_human_decisions: true
  human_boundary:
    approval_authority: human
    publication_authority: human
    verification_authority: external_review
```

## Relationship to Other Shirakami Protocols

- **Anmon** exposes ambiguity, assumptions, and questions before production.
- **3D Eisenhower Matrix** supports phase-aware handling of production tasks without granting priority authority.
- **ThreadRPG** may render alternative viewpoints or creative discussions without impersonation or decision authority.
- **Rensan** connects related story, character, source, and revision contexts while preserving their identities.
- **Kasen** supports sequential contributions with provenance and divergence retained.
- **Guide AI** may orient users among stages, artifacts, questions, and routes without approving or executing production.

## Non-Goals

This version does not define:

- an image-generation backend;
- automatic story or panel selection;
- autonomous publication;
- legal or factual certification;
- a universal artistic style;
- replacement of authorial judgment.

## Acceptance Boundary

A Manga Pipeline artifact is accepted only through an explicit human decision supported by traceable source references, revision history, unresolved-question handling, and—where relevant—external factual, rights, or quality review.
