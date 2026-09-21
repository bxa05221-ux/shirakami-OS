# Protocol Compatibility Matrix

## Purpose

This artifact turns the structural signals detected by `tools/protocol_composition_detector.py` into an explicit pairwise matrix.

It is deliberately conservative:

- `structural_match=true` means only that at least one source output field overlaps a target input field.
- `semantic_compatibility=unknown` unless a stronger Protocol contract establishes semantic compatibility.
- the matrix does not alter Registry or Runtime behavior.
- the matrix does not authorize arbitrary Protocol permutation.

## Reproducible generation

Run from the repository root:

```bash
python tools/protocol_compatibility_matrix.py --root .
```

The command scans `protocols/**/*.yaml` and produces a Markdown matrix on stdout.

## Interpretation

```text
Protocol A.output
      │
      ├── structural overlap ──> Protocol B.input
      │
      └── semantic compatibility = unknown
                         │
                      verification
                         ↓
                       Runtime
                         ↓
                      Evidence
```

The matrix is therefore a candidate-generation boundary between structural detection and executable verification.

## Verification

`runtime/test_protocol_compatibility_matrix.py` verifies that:

1. a matching output/input field produces `structural_match=true`;
2. the matching field is explicitly reported;
3. semantic compatibility remains `unknown`;
4. the reverse direction is not inferred as compatible merely because the forward direction matched.

This is intentionally a narrow verification step. The next stage is selected route verification through Runtime → Evidence, not automatic semantic approval.

## Status

**Status: structural compatibility matrix implemented; semantic compatibility remains unverified.**

No Runtime contract change is introduced by this artifact.