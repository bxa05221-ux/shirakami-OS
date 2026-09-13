"""Verify temporal history lookup for one observed star.

Implementation-boundary experiment only: history is keyed by explicit star id
and returned in observation order without semantic interpretation.
"""

from runtime.star_history import StarObservationHistory


def main() -> None:
    history = StarObservationHistory()

    history.record({
        "id": "star-001",
        "content": "星が見えにくい",
        "distance": None,
        "brightness": 0.4,
        "phase": "quiet",
    })
    history.record({
        "id": "star-001",
        "content": "さっきの星が少し見えてきた",
        "distance": None,
        "brightness": 0.7,
        "phase": "emerging",
    })
    history.record({
        "id": "star-001",
        "content": "また少し見えにくくなった",
        "distance": None,
        "brightness": 0.5,
        "phase": "fading",
    })

    observations = history.history("star-001")
    assert len(observations) == 3
    assert [item.brightness for item in observations] == [0.4, 0.7, 0.5]
    assert [item.phase for item in observations] == ["quiet", "emerging", "fading"]
    assert [item.content for item in observations] == [
        "星が見えにくい",
        "さっきの星が少し見えてきた",
        "また少し見えにくくなった",
    ]
    assert history.history("unknown") == ()
    assert history.star_ids() == ("star-001",)

    print("DISTORTED_CELESTIAL_SPHERE_STAR HISTORY VERIFIED")


if __name__ == "__main__":
    main()
