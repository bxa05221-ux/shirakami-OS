# Protocol Composition Detection Report

Generated from structural inspection of Protocol artifacts on the `main` branch. The detector is now available at `tools/protocol_composition_detector.py`.

## Detected route signals

| Protocol/artifact | Input | Output | Route / phases | Evidence signal | Landscape signal |
|---|---:|---:|---|---:|---:|
| Thread RPG v1.2.1 | — | — | multi-voice capabilities (no explicit executable pipeline in artifact) | — | yes |
| Manga User Manual | — | — | observe → evidence | yes | yes |
| Wasan v0.1 | yes | yes | problem_solving execution | yes | — |
| Tsugaru Guide High School | — | — | question → fieldwalk → observation → investigation → interpretation → proposal → feedback → inheritance | yes | yes |
| Sequential Verification Multi-Agent | role inputs/outputs | role inputs/outputs | OBSERVE → AUDIT → CHANGE → VERIFY → CONFIRM | yes | — |
| Sequential Verification Efficiency Metrics | yes | yes | measurement/record | yes | — |

## Automatically detected architectural signals

1. **Explicit input/output boundaries exist in multiple Protocol artifacts.**
2. **Explicit route/phase sequences exist in multiple artifacts.**
3. **Evidence and Landscape are recurring boundary concepts rather than application-specific one-offs.**
4. **The Runtime already exposes generic Protocol invocation and RouteMap transition recording.**
5. **Therefore the repository contains enough structural information to begin automatic composition analysis.**

## What the detector does not claim

The detector does **not** infer that any two Protocols are semantically compatible. A matching field name or route step is not sufficient evidence of compatibility.

Compatibility must be checked against:

- input state
- output state
- transition semantics
- Evidence requirements
- Landscape requirements
- predecessor/successor constraints
- Runtime tests

## Next automatic step

The next implementation step is to convert the detected fields into a compatibility matrix:

```text
Protocol A output ──compatible?──> Protocol B input
Protocol B output ──compatible?──> Protocol C input
                              ↓
                         Evidence boundary
                              ↓
                           Landscape
```

This turns the water/gearbox model into a measurable repository property rather than a metaphor.

**Status: structural detector verified / selected Runtime→Evidence composition verified**

### Selected executable verification

The repository now contains an executable boundary test at
`runtime/test_protocol_composition_evidence.py`.

It verifies one limited composition:

```text
Protocol A output
      ↓
Protocol B input
      ↓
Runtime execution
      ↓
EvidenceRecord
```

The test deliberately does **not** claim that matching field names prove semantic
compatibility. The detector reports structural overlap separately and marks
semantic compatibility as `unknown` unless a stronger Protocol contract
establishes it.

This is a verification of one selected composition, not unrestricted Protocol
permutation.