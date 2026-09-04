from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition


def outcome_protocol(context):
    return Transition(
        kind="tabitomo.outcome.observed",
        data={
            "traveler_choice": context.input["traveler_choice"],
            "observed_outcome": context.input["observed_outcome"],
            "changed": True,
        },
    )


def test_tabitomo_observed_outcome_projects_into_existing_landscape():
    runtime = Runtime()
    result = runtime.execute(
        "tabitomo.outcome",
        outcome_protocol,
        {
            "traveler_choice": "scenic_route",
            "observed_outcome": "arrived_at_viewpoint",
        },
    )

    evidence = capture_evidence(result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert landscape.snapshot() == {
        "traveler_choice": "scenic_route",
        "observed_outcome": "arrived_at_viewpoint",
        "changed": True,
    }
    assert landscape.evidence == [evidence]
