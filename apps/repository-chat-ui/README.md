# Repository Chat Explorer UI

Local web UI for Repository Chat Explorer.

## Run

    python apps/repository-chat-ui/server.py

Then open http://localhost:8787

The API key remains on the local server and is not sent to the browser.

## Flow

Search GitHub → select repository → talk to the repository → inspect evidence categories.

Current MVP evidence: repository metadata, README, repository tree, recent commits.

Next: targeted file retrieval and clickable file/commit evidence.