# Protocol Canonical Path Audit

Status: verification note for the β1.0 Runtime baseline.

## Finding

The repository currently contains two distinct Protocol loading shapes:

1. `runtime/protocol_loader.py`
   - accepts the β0.1 `matome:` YAML subset;
   - produces the frozen `ProtocolIR`;
   - is consumed by the Runtime-facing Protocol bridge and Protocol API.

2. `runtime/protocol_loader_v2.py`
   - accepts the repository's newer `protocol:` YAML shape;
   - produces `CurrentProtocol`;
   - is used by `tests/test_current_protocol_loader.py` for the current Tsugaru guide protocol.

These are not currently interchangeable loaders. The v2 loader does not produce `ProtocolIR`, and existing repository observations explicitly state that `protocol_loader_v2.py` is not canonical for the Runtime Protocol path.

## Canonical Runtime path

For the β1.0 Runtime boundary, the verified canonical path is:

`Matome YAML → protocol_loader.parse_matome() → ProtocolIR → ProtocolRegistry / Protocol API → Runtime`

`protocol_loader_v2.py` is therefore treated as a separate current-protocol document loader, not as a replacement for the Runtime Protocol Loader.

## Boundary rule

- Do not silently substitute `protocol_loader_v2.py` for `protocol_loader.py`.
- Do not merge the `CurrentProtocol` and `ProtocolIR` models without a separate specification decision.
- Do not expose either loader directly as a new HTTP endpoint as part of this audit.
- Existing `POST /observe` remains the only frozen external API boundary.

## Verification basis

`runtime/protocol_loader.py` explicitly describes itself as the small β0.1 Matome subset loader and defines `ProtocolIR`.

`runtime/protocol_registry.py` manages Protocol lifecycle and selection without interpreting Protocol meaning.

`runtime/protocol_api.py` consumes registry entries and builds `ProtocolRequest`; its temporary Matome registration path delegates to `parse_matome()`.

`runtime/current_protocol.py` also delegates current file loading to `parse_matome()` and checks the loaded Protocol ID against the Registry entry.

`runtime/protocol_loader_v2.py` is separately exercised by `tests/test_current_protocol_loader.py` against the `protocol:` document shape.

## Decision

No Runtime behavior is changed by this audit. The current split is recorded explicitly so that future cleanup does not accidentally turn the newer document loader into an implicit replacement for the verified Runtime Protocol boundary.

Any future unification requires a separate change with an explicit specification, tests, and verification of the affected Runtime path.
