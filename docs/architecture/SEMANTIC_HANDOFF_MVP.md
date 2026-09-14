# Shirakami GitHub Semantic Handoff — MVP v0.1

## Purpose

GitHub users often need an AI to inspect a repository for one specific question. The MVP prevents the repository from being treated as undifferentiated context.

The system selects the smallest useful evidence set, records why each resource was selected, preserves the source revision, and hands the resulting evidence to an AI runtime through Matome YAML.

## Core Rule

> Do not give the AI the repository. Give the AI the repository evidence required for the question.

## Flow

```text
Human Request
      ↓
Semantic Selection
      ↓
GitHub Retrieval
      ↓
Evidence Preservation
      ↓
Anmon Check
      ↓
Matome YAML Handoff
      ↓
AI Runtime
      ↓
Human Review
```

## MVP Scope

### Included

- GitHub repository and ref as source
- Question/purpose driven selection
- Explicit include/exclude scope
- Reviewer Entry Point as the default discovery boundary
- Commit SHA preservation where available
- Retrieval reason for each selected resource
- Evidence classification: fact / interpretation / hypothesis / unresolved / protocol
- Matome YAML handoff
- Human final judgment

### Not included yet

- Automatic whole-repository crawling
- Automatic code execution
- AI-provider-specific invocation
- Repository mutation
- Autonomous scope expansion
- Semantic claims presented as authoritative facts

## Selection Policy

Selection is incremental.

1. Start with the smallest entry-point evidence set.
2. Determine whether it answers the user's question.
3. If not, place the missing requirement in Anmon.
4. Expand selection explicitly.
5. Record the newly retrieved evidence.

A retrieval step must never silently expand its scope.

## Initial Entry Point

For this repository, the first architectural entry point is:

- `README.md`
- `docs/architecture/REVIEWER_ENTRY_POINT.md`

The reviewer entry point already defines a recommended route through the repository and distinguishes normative specifications from implementation and observation material.

## Example

Question:

> Can Shirakami be represented as a model-independent reference architecture?

Initial selection:

```text
README.md
 docs/architecture/REVIEWER_ENTRY_POINT.md
```

If architectural evidence is insufficient, expand to the architecture documents and normative specification boundary. Do not begin by loading `runtime/` or the entire repository.

## Authority Boundary

```text
GitHub Repository
      = source evidence

Semantic Handoff
      = selection / preservation / transfer

AI
      = interpretation / proposal

Human
      = final authority
```

The Semantic Handoff layer does not decide what is true. It makes the evidence path observable and reproducible.

## Relation to Shirakami

This MVP is an application of the Shirakami architecture rather than a replacement for it.

It exercises the following boundaries:

- Landscape: the user's question and constraints
- Evidence: selected repository resources
- Anmon: unresolved evidence requirements
- Protocol: selection and handoff rules
- Runtime: execution of the handoff process
- Adapter: GitHub as the source-system adapter
- Renderer: Matome YAML as the semantic handoff representation

## Success Condition

The MVP succeeds when two independent AI reviews can receive the same question, the same repository revision, and the same selected Evidence set, and can inspect the selection path without requiring the entire repository as context.

## Status

Experimental implementation candidate.

Version: `0.1`

Target user: GitHub user working with AI-assisted repository inspection.
