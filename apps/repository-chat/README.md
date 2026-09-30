# Repository Chat Explorer

Search GitHub repositories and talk to a selected repository as a conversational subject.

## MVP

1. Search repositories by name or description.
2. Select a repository.
3. Import bounded repository context: metadata, README, tree, recent commits.
4. Build a Repository Identity prompt.
5. Ask questions in Repository Voice.
6. Keep evidence and uncertainty visible.

Usage:

    python apps/repository-chat/repository_chat.py search "context ai protocol"
    python apps/repository-chat/repository_chat.py chat owner/name "お前は何者？"

Set OPENAI_API_KEY for model-backed answers. OPENAI_MODEL may override the model name.

Without an API key, chat prints the assembled prompt and repository context so the boundary can be inspected without a model call.

## Boundary

Repository Chat does not claim that a repository has consciousness, intentions, or undocumented knowledge.

Repository evidence -> Context -> Repository Identity -> AI Runtime -> Answer

## Non-goals

- ranking repositories
- inventing maintainer intentions
- treating generated answers as maintainer-authoritative statements
- requiring one AI provider
