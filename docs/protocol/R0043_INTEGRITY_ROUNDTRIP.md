# R0043 — Integrity Round Trip

R0043 closes the adversarial verification loop.

A clean trace must produce no integrity findings.
A deliberately tampered trace must produce deterministic findings.
Those findings must be reconstructable against the original trace identity.

The loop is:

Trace → Adversarial disturbance → Classification → Integrity Reconstruction

This is a verification of observability, not a claim that every possible failure
mode has been modeled.

## Acceptance conditions

1. Clean trace yields zero findings.
2. Tampered identity yields the expected classification codes.
3. Findings retain the trace identity.
4. No hidden cause is invented.
5. The integrity reconstruction remains Evidence-shaped.

The important property is symmetry:

Normal operation is reconstructable.
Abnormal operation is also reconstructable.

Thus the trace does not disappear merely because the system failed.
