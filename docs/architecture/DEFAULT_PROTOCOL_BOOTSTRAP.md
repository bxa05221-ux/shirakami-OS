# Default Protocol Bootstrap

The OS has one mandatory Default Protocol. It is a permanent runtime footing,
not a domain-specific behavior definition.

At the operational boundary, startup ensures that the Default Protocol is
registered before a Default Protocol request is resolved. Temporary Protocols
remain ordinary user-authored Matome YAML artifacts and use the same generic
request and execution machinery.

```text
OS startup
    ↓
bootstrap Default Protocol
    ↓
Protocol Registry
    ↓
Default / Temporary Protocol Request
    ↓
Runtime executor
```

Bootstrap is idempotent: if the Default Protocol is already registered, the
existing registry entry is returned. The Runtime does not infer semantic
meaning from the Default Protocol artifact.
