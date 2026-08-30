# OPPAI Benchmark Harness v0.1

Status: implementation support

## Purpose

Provide a small, repeatable harness for comparing direct model use with the same model behind an OPPAI boundary.

## Measurement philosophy

The harness treats human operational friction as a first-class observation. It does not reduce the experiment to model quality scores.

### Primary measures

- elapsed human interaction time
- correction count
- re-explanation count
- context-recovery count
- completion rate
- voluntary continuation rate

### Qualitative measures

Each trial may also record comfort and friction notes. These are retained as observations rather than converted into an invented universal score.

## Experimental discipline

The downstream adapter should remain identical between control and experimental conditions. Only the input boundary changes.

```text
Direct:  Human → Model Adapter
OPPAI:   Human → OPPAI → Model Adapter
```

The harness can later be connected to a real adapter, but its data model is deliberately independent of vendor, model, or API.

## Evidence boundary

The harness records observations. It does not declare that OPPAI is superior. Conclusions must be made from accumulated trials and retained evidence.
