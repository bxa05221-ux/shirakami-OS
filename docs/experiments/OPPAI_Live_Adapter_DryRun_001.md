# OPPAI Live Adapter Dry Run 001

Status: executed as local adapter simulation

## Purpose

Demonstrate the complete interaction boundary without coupling the repository to a commercial model API.

## Input

> いや、そうじゃない。AIを賢くするんじゃなくて、人間がAIを操作しなくても普通に話せるようにしたいんだよ。

## Expected boundary behavior

1. Preserve the exact raw input.
2. Detect the explicit correction signal.
3. Preserve the preceding conceptual context rather than deleting it.
4. Detect the operational intent expressed in the utterance.
5. Produce a canonical prompt candidate for a replaceable downstream adapter.
6. Keep the observation separate from any downstream model answer.

## Adapter

The dry run uses a deterministic mock adapter. This is intentional: the test isolates the OPPAI/Runtime boundary and does not claim model intelligence.

## Expected observable result

The Runtime receives the OPPAI canonical prompt candidate through the adapter interface and returns an adapter result while preserving the OPPAI observation separately.

## Interpretation

If this boundary behaves as designed, the next step is not to add more prompt engineering. The next step is to connect a real model adapter and compare the human repair work required with and without the OPPAI boundary.

## Limitation

This dry run does not establish that OPPAI improves downstream quality, reduces elapsed time, or achieves parity between models.
