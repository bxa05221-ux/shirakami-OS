from runtime.constellation_candidates import ConstellationCandidateStore


store = ConstellationCandidateStore()

first = store.hold(("star-001", "star-002"), confidence=None, reversible=True)
second = store.hold(("star-002", "star-003"), confidence=None, reversible=True)

assert first.star_ids == ("star-001", "star-002")
assert second.star_ids == ("star-002", "star-003")
assert first.confidence is None
assert second.confidence is None
assert first.reversible is True
assert second.reversible is True
assert store.candidates() == (first, second)

# Boundary rule: candidate relations remain candidates; no constellation is produced.
assert not hasattr(store, "constellations")

print("DISTORTED_CELESTIAL_SPHERE_CONSTELLATION CANDIDATE VERIFIED")
