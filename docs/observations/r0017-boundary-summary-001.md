# R0017 — Boundary Summary

R0017 extends R0015 by moving the re-observation through the explicit Projection boundary rather than calling `LandscapeState.apply_evidence()` directly.

The experiment observes:

1. Evidence records can be projected into independent Landscape states.
2. The same ordered Evidence produces the same observable snapshot.
3. Evidence ordering remains inspectable.
4. No continuity or semantic identity field is introduced.

The result is limited to current Projection behavior.
