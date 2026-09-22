# Local Repository Runtime Boundary v0.1

This observation records the first local-repository execution boundary for the
GitHub-to-Shirakami hypothesis.

## Boundary

```
GitHub Repository
      ↓ sync / checkout
Local Repository
      ↓
Protocol Loader
      ↓
ProtocolIR
      ↓
Shirakami Runtime
```

The Local Repository is a storage/execution boundary, not a second protocol
authority. Both the GitHub-backed loader and the local loader delegate
interpretation to the existing `parse_matome` implementation.

## Verification

The same Matome YAML is supplied through:

1. a deterministic GitHub Contents client; and
2. a local repository checkout.

Both paths must produce the same `ProtocolIR`.

This verifies portability of the protocol artifact after checkout without
introducing new protocol semantics or requiring a live GitHub request during
Runtime execution.

## Scope

This is a boundary verification only. It does not implement Git synchronization,
authentication, commit policy, repository mutation, or model evaluation.
