# Repository Chat Explorer UI

Local web UI for Repository Chat Explorer.

## Run

    python apps/repository-chat-ui/server.py

Then open http://localhost:8787

The API key remains on the local server and is not sent to the browser.

## Flow

Search GitHub → select repository → talk to the repository → inspect evidence.

## Current MVP

The chat context is built from:

- repository metadata
- README.md
- recursive repository tree sample
- recent commits

The response now exposes clickable evidence links for the selected repository, README, tree, and recent commits.

## Boundary

Repository Voice is an interface, not a claim that the repository is conscious or that generated text represents maintainer intent.

The system is designed to distinguish documented facts, observations/inferences, and unknowns. It does not rank or score repositories.

## Next

- targeted file retrieval when a question requires implementation detail
- clickable evidence for specific files referenced by an answer
- commit/diff inspection
- issues, pull requests, releases, tests, and workflow evidence
