# R0037 implementation correction

The first R0037 workflow run exposed an adapter-boundary mismatch: `MemoryAdapter` provides `read()`, while Landscape observation is exposed by the module-level `adapt_landscape_observation()` function. The implementation was corrected to use that existing boundary.

No adapter interface or Kernel semantics were changed.
