"""Radio and nursery-resilience experiments for metadata-only ProgressProfile."""
import pytest

from runtime.progress_profile import (
    ProgressError, ProgressProfile, advance, restore, resume, stop,
)


RADIO = ProgressProfile(
    "radio-experimental",
    ("listener", "host", "review", "publish"),
    wait_at=frozenset({"listener", "review"}),
    resume_signal="human_resume",
)
RESILIENCE = ProgressProfile(
    "resilience-experimental",
    ("observe", "dialogue", "record", "reobserve", "evidence"),
    wait_at=frozenset({"observe", "reobserve"}),
    resume_signal="human_resume",
)


@pytest.mark.parametrize("profile", [RADIO, RESILIENCE])
def test_wait_resume_and_snapshot_roundtrip(profile):
    initial = profile.start()
    waiting = advance(profile, initial)
    assert waiting.status == "waiting"
    assert restore(profile, waiting.snapshot()) == waiting
    with pytest.raises(ProgressError, match="only a ready"):
        advance(profile, waiting)
    with pytest.raises(ProgressError, match="explicit resume"):
        resume(profile, waiting, signal="ai_approval")
    resumed = resume(profile, waiting, signal="human_resume")
    assert resumed.index == 1
    assert resumed.status == "ready"
    assert restore(profile, resumed.snapshot()) == resumed


@pytest.mark.parametrize("profile", [RADIO, RESILIENCE])
def test_stop_prevents_automatic_restart(profile):
    stopped = stop(profile, profile.start())
    assert stopped.status == "stopped"
    with pytest.raises(ProgressError):
        advance(profile, stopped)
    with pytest.raises(ProgressError):
        resume(profile, stopped, signal="human_resume")


def test_radio_requires_second_human_pause_and_finishes():
    s = resume(RADIO, advance(RADIO, RADIO.start()), signal="human_resume")
    s = advance(RADIO, s)  # host -> review
    assert s.stage == "review"
    s = advance(RADIO, s)
    assert s.status == "waiting"
    s = resume(RADIO, s, signal="human_resume")
    assert s.stage == "publish"
    assert advance(RADIO, s).status == "completed"


def test_resilience_reobserve_wait_and_completion():
    s = resume(RESILIENCE, advance(RESILIENCE, RESILIENCE.start()),
               signal="human_resume")
    s = advance(RESILIENCE, s)  # dialogue -> record
    s = advance(RESILIENCE, s)  # record -> reobserve
    s = advance(RESILIENCE, s)  # wait at reobserve
    assert s.stage == "reobserve" and s.status == "waiting"
    s = resume(RESILIENCE, s, signal="human_resume")
    assert s.stage == "evidence"
    assert advance(RESILIENCE, s).status == "completed"


def test_invalid_profile_and_tampered_snapshot_are_rejected():
    with pytest.raises(ProgressError):
        ProgressProfile("bad", ("a", "a"))
    with pytest.raises(ProgressError):
        ProgressProfile("bad", ("a",), wait_at=frozenset({"nonexistent"}))
    snapshot = RADIO.start().snapshot()
    snapshot["stage"] = "publish"
    with pytest.raises(ProgressError):
        restore(RADIO, snapshot)


def test_progress_snapshot_never_claims_authorization_or_evidence():
    snapshot = advance(RADIO, RADIO.start()).snapshot()
    assert set(snapshot) == {"profile_id", "stage", "index", "status"}
    assert "approved" not in snapshot
    assert "evidence" not in snapshot
