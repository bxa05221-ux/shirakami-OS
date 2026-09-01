# Shirakami OS — MVP Review

This page is the practical entry point for a first external review.

## What is working

The current MVP demonstrates a minimal, inspectable path from a Protocol source to a Runtime result:

```text
Protocol Source
      ↓
Protocol Loader
      ↓
Current Selection
      ↓
MTM Compatibility
      ↓
Runtime Execution
      ↓
Inspectable Result
```

The implementation intentionally does **not** invoke an AI provider yet. The purpose of this MVP is to prove the Runtime boundary, not to build another AI model.

## Verify locally

```bash
python -m pytest runtime tests -q
```

## Review focus

A reviewer does not need to understand the entire Shirakami project first. The useful questions at this stage are:

1. Can a Protocol be loaded without embedding domain-specific meaning in the Runtime?
2. Can current Protocol selection be separated from historical artifacts?
3. Can the Runtime boundary remain independent of a particular AI provider?
4. Is the execution result inspectable and testable?

## What is deliberately deferred

- AI-provider integration
- production storage
- full UI
- advanced migration policy
- richer semantic execution

These are post-MVP concerns. They should not be used to obscure whether the current Runtime boundary works.

## Position

Shirakami OS is an implementation/runtime layer. Protocols and specifications define what may be executed; the Runtime provides the stable execution boundary; adapters connect external systems and AI providers.
