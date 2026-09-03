from runtime.tulip import TULIP_PROTOCOL_ID, tulip_protocol
from runtime.prototype import Runtime


def test_tulip_starts_from_human_observation():
    result = Runtime().execute(TULIP_PROTOCOL_ID, tulip_protocol, {"subject": "チューリップ"})

    assert result.status == "completed"
    assert result.transition.kind == "landscape.observation.started"
    assert result.transition.data["subject"] == "チューリップ"
    assert result.transition.data["changed"] is True
    assert result.transition.data["projection"] == "none"


def test_tulip_does_not_invent_subject_when_explicitly_given():
    result = Runtime().execute(TULIP_PROTOCOL_ID, tulip_protocol, {"subject": "赤いチューリップ"})

    assert result.transition.data["subject"] == "赤いチューリップ"
