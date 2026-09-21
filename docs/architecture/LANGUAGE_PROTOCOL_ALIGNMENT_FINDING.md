# Language / Protocol Alignment Finding

Status: implementation finding for the β1.0 Runtime baseline.

## Purpose

This note records an implementation-level finding about the relationship between natural-language input, OPPAI preprocessing, generated or selected Protocol representations, and the Runtime boundary.

It does not introduce a new Protocol semantic, change the Runtime contract, or establish a theory claim.

## Observed structure

The repository currently represents at least two qualitatively different information paths:

```text
Human natural language
        ↓
     OPPAI
        ↓
canonical_prompt / observation
        ↓
   Runtime adapter
```

and:

```text
Matome YAML
    ↓
protocol_loader.parse_matome()
    ↓
 ProtocolIR
    ↓
Protocol Registry / Protocol API / bridge
    ↓
 Runtime
```

A separate current-protocol document path also exists:

```text
protocol: YAML
    ↓
protocol_loader_v2.py
    ↓
CurrentProtocol
```

The existing canonical-path audit records that `ProtocolIR` and `CurrentProtocol` are not interchangeable and must not be silently merged.

## Alignment finding

The current implementation makes a useful separation between the user's language input and the Protocol supplied to Runtime.

`runtime/oppai_runtime_flow.py` accepts `text` and `protocol` as separate inputs. OPPAI produces an observable `OppaiObservation`; its `canonical_prompt` is passed as the Runtime input while the Protocol remains a separate value.

Therefore, the repository does not currently justify treating:

```text
user prompt == Protocol
```

as an implementation invariant.

The same applies to:

```text
Matome YAML == Protocol YAML
```

The existing loader audit already records these as distinct representations with different consumers and boundaries.

## Potential failure boundary

If a future implementation generates or selects a Protocol from natural-language interaction, an additional alignment boundary is required between the language-side representation and the generated/selected Protocol.

Conceptually:

```text
Natural language
      ↓
OPPAI / language observation
      ↓
Prompt / interaction representation
      ↓
Generated or selected Protocol
      ↓
ProtocolIR / Runtime representation
      ↓
Runtime
```

The risk is not limited to syntactic validation. A Protocol can be structurally valid while no longer preserving the relevant constraints, target, or unresolved state represented on the language side.

This is therefore an alignment concern, not merely a loader-validation concern.

## What is currently verified

- OPPAI preserves raw input and exposes structured observations without claiming hidden-intent resolution.
- `canonical_prompt` and `protocol` are separate values in the OPPAI Runtime flow.
- The β1.0 canonical Runtime Protocol path is `Matome YAML → ProtocolIR → Registry/API → Runtime`.
- `protocol_loader_v2.py` produces `CurrentProtocol` from a separate `protocol:` document shape.
- Existing implementation audits explicitly prohibit silently substituting the v2 loader or merging `CurrentProtocol` and `ProtocolIR` without a separate specification decision.

## What is not yet verified

- No canonical implementation contract currently defines how a naturally generated Protocol is derived from a language-side representation.
- No canonical alignment check currently establishes semantic correspondence between language input and a generated Protocol.
- No claim is made that such a generated Protocol currently exists as an autonomous Runtime mechanism.
- No Runtime behavior is changed by this finding.

## Boundary rule

Until a separate specification is adopted:

- do not equate Prompt with Protocol;
- do not equate Matome YAML with Protocol YAML;
- do not merge `CurrentProtocol` and `ProtocolIR` implicitly;
- do not add an alignment endpoint merely from this finding;
- do not infer hidden intent as a prerequisite for Protocol generation;
- preserve the existing `POST /observe` external API boundary.

## Recommended next investigation

If this finding is taken forward, investigate an explicit **Language–Protocol Alignment Boundary** before implementing any automatic Protocol generation.

The investigation should establish:

1. which language-side fields constitute the alignment input;
2. which Protocol fields must remain traceable to those inputs;
3. how unresolved or uncertain language elements are represented;
4. what constitutes an alignment failure;
5. what Evidence is recorded when alignment succeeds or fails;
6. whether the alignment is a Runtime concern, a Research concern, or a handoff between them.

Any implementation should follow the existing one-change/one-verification rule and require a separate specification decision before changing Runtime behavior.
