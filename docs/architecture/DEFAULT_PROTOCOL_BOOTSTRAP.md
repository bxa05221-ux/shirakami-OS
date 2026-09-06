# Default Protocol Bootstrap

The Shirakami OS Registry has two Protocol lifecycles:

- **Default Protocol** — the permanent OS footing. It must exist before an OS-level default request can be built.
- **Temporary Protocol** — a user-authored Matome YAML flow that can be registered, replaced, and removed.

## Bootstrap boundary

`bootstrap_default_protocol(registry)` provides the permanent default artifact when the registry is empty. Repeated bootstrap calls reuse the already registered default.

The bootstrap does not interpret Protocol phases and does not add domain semantics to the Kernel. The default artifact is still represented through the same Matome Protocol machinery used by temporary Protocols.

This establishes the operational lifecycle:

```text
OS startup
  ↓
default Protocol bootstrap
  ↓
Protocol Registry
  ↓
normal Protocol request / Runtime path
```

Temporary Protocol creation remains separate:

```text
natural interaction
  ↓
flow stabilizes
  ↓
Matome YAML
  ↓
Temporary Protocol
```
