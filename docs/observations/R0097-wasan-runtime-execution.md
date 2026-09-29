# R0097 — Wasan Runtime Execution

## Purpose

Verify that the Wasan Protocol candidate can pass through the existing ProtocolRequest → invoke_protocol → Runtime → Evidence → Landscape path without adding domain semantics to the Runtime.

## Input

Problem: 鶴と亀が合わせて5匹、足は合わせて14本。鶴と亀はそれぞれ何匹か。

## Execution

The calculation backend was treated as replaceable application logic. The execution preserved seven explicit calculation steps and a separate verification expression.

## Observed result

- status: completed
- protocol_id: wasan
- cranes: 3
- turtles: 2
- verification: 2*3 + 4*2 = 14 and 3+2 = 5

## Evidence boundary

The result was captured as immutable EvidenceRecord data and projected into LandscapeState. The Runtime did not define the mathematical meaning of the problem or certify the result as mathematical truth.

## Important implementation observation

The first Wasan candidate artifact used a richer custom top-level shape. The current repository loader expects the `protocol:` artifact shape. R0097 aligned the Wasan artifact with that existing loader contract rather than adding a new loader or Runtime semantic path.

## Status

Observed execution success for the existing generic Runtime boundary.

This does not establish historical authenticity of the example problem, mathematical authority, product-market fit, or promotion of Wasan from candidate to protocolized Runtime semantics.
