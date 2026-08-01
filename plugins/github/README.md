# GitHub Adapter

Status:
Prototype

Purpose

The GitHub Adapter enables Shirakami OS to understand
GitHub repositories as architectural knowledge.

Current Scope

- Repository Discovery
- README Navigation
- RFC Discovery
- Documentation Reading

Future Scope

- Issue Navigation
- Pull Request Support
- Repository Synchronization

Architecture Notes

The GitHub Adapter is not a Git client.

The adapter treats a GitHub repository as a structured architectural knowledge source.

Its responsibility is to discover,
read,
and navigate repository knowledge.

Repository ownership always remains outside the adapter.

The adapter never owns project knowledge.
It only provides access to it.
