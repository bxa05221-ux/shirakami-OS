# Runtime β0.1 GitHub Client Implementation

Status: Implementation
Version: 0.1
Date: 2026-08-11

## Purpose

Provide the first real GitHub transport behind the existing `GitHubClient` boundary.

## Transport

The implementation uses the GitHub Contents API through Python's standard-library HTTP client.

No GitHub credentials are stored in source. Authentication is supplied through an injected token provider.

## Landscape Representation

For this first concrete implementation, the configured Landscape is a JSON object stored at a configured repository path.

This is an implementation representation for β0.1, not a Foundation-level Landscape schema.

## Operations

### Read

`read_landscape()` reads the configured file from the configured branch and parses its JSON object.

### Write

`write_landscape()` reads the current file, applies the supplied transition, and updates the file through the GitHub Contents API using the current blob SHA.

The update therefore uses GitHub's content version boundary rather than blind overwrite.

## Security Boundary

The client requires a token provider. A missing token fails before any network request.

Tokens must be supplied by the runtime environment or an external secret manager.

No token may be committed to the repository.

## Scope Limitations

This implementation does not yet solve:

- permission policy;
- authentication lifecycle;
- concurrent writes;
- conflict resolution beyond GitHub's blob SHA requirement;
- repository event synchronization;
- GitHub webhook handling;
- multi-file Landscape transactions.

These remain separate architectural concerns.

## Integration

The concrete connection is:

Runtime
→ GitHubLandscapeAdapter
→ GitHubContentsClient
→ GitHub Contents API
→ repository Landscape file

Runtime core remains GitHub-independent.
