# Repository Chat Explorer

## Purpose

Repository Chat Explorer is an exploratory interface for understanding an unfamiliar GitHub repository.

The central UX is:

Search -> Select -> Ask the repository

"Repository Voice" means that generated answers are grounded in repository-observable material. It does not imply consciousness, intention, or private maintainer knowledge.

## Evidence boundary

The MVP imports repository metadata, README, repository tree, and recent commits. Later versions can add selected files, issues, pull requests, releases, tests, workflow results, and commit diffs.

The context is deliberately bounded. A chat answer must not silently imply that every file was inspected.

## Evidence states

- Documented: directly supported by retrieved material.
- Observed / inferred: cautious interpretation of retrieved material.
- Unknown: not established by the current evidence set.

## Next steps

1. Add a small web UI.
2. Add clickable evidence references.
3. Add targeted file retrieval when a question requires it.
4. Add commit and diff inspection.
5. Add a provider-neutral Runtime adapter.
6. Add Semantic Handoff / Matome YAML for session transfer.
