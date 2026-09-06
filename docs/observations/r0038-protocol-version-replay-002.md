# R0038 Protocol Version Replay — Current Main Reconstruction

## Purpose

Verify the existing boundary that preserves a Protocol version observed at execution time when Evidence is replayed later.

## Boundary

Historical Evidence → `transition_data.protocol_version` → deterministic replay

## Observation

The current generic Protocol bridge places `ProtocolIR.version` into `transition_data.protocol_version`. Evidence captures the transition data without rewriting it. R0038 therefore reads the historical version directly from the immutable observed Evidence record.

Replay compares that historical value with an independently supplied current version. A current version does not replace the historical value carried by Evidence.

The experiment also makes the missing-version case explicit: if an Evidence transition has no `protocol_version`, extraction returns `None` rather than substituting a current version.

## Boundary discipline

This experiment does not add a Protocol artifact store, artifact hash, provenance mechanism, continuity claim, identity claim, inheritance claim, semantic interpretation, truth determination, Memory Manager behavior, backend semantics, credential behavior, or GitHub write behavior.

No Evidence schema change is introduced.

## Next observation

Determine whether a historical Protocol artifact can be identified and compared by a stable content reference or hash, without allowing the current artifact to substitute for the historical one.
