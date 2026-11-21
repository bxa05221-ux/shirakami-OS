"""Experimental declarative progress-state boundary, not a new execution engine.

This module does not execute a Protocol, authorize an action, or create Runtime
Evidence. Its snapshots are observation metadata for a separately approved
Runtime path.
"""
from dataclasses import dataclass, replace


class ProgressError(ValueError):
    """Invalid or unauthorized progress-state transition."""


@dataclass(frozen=True)
class ProgressProfile:
    profile_id: str
    stages: tuple[str, ...]
    wait_at: frozenset[str] = frozenset()
    resume_signal: str = "human_resume"

    def __post_init__(self):
        if not self.profile_id or not self.stages:
            raise ProgressError("profile ID and stages are required")
        if any(not stage for stage in self.stages) or len(set(self.stages)) != len(self.stages):
            raise ProgressError("stages must be unique and non-empty")
        if not self.wait_at.issubset(self.stages):
            raise ProgressError("wait_at must contain defined stages")
        if not self.resume_signal:
            raise ProgressError("resume_signal is required")

    def start(self) -> "ProgressState":
        return ProgressState(self.profile_id, self.stages[0], 0, "ready")


@dataclass(frozen=True)
class ProgressState:
    profile_id: str
    stage: str
    index: int
    status: str

    def snapshot(self) -> dict[str, object]:
        return dict(profile_id=self.profile_id, stage=self.stage,
                    index=self.index, status=self.status)


def _validate(profile: ProgressProfile, state: ProgressState) -> None:
    if (state.profile_id != profile.profile_id
            or state.index not in range(len(profile.stages))
            or profile.stages[state.index] != state.stage
            or state.status not in {"ready", "waiting", "stopped", "completed"}):
        raise ProgressError("state does not match profile")


def advance(profile: ProgressProfile, state: ProgressState) -> ProgressState:
    """Advance metadata only; no Runtime execution or approval is implied."""
    _validate(profile, state)
    if state.status != "ready":
        raise ProgressError("only a ready profile can advance")
    if state.stage in profile.wait_at:
        return replace(state, status="waiting")
    if state.index == len(profile.stages) - 1:
        return replace(state, status="completed")
    return ProgressState(profile.profile_id, profile.stages[state.index + 1],
                         state.index + 1, "ready")


def resume(profile: ProgressProfile, state: ProgressState, *, signal: str) -> ProgressState:
    _validate(profile, state)
    if state.status != "waiting" or signal != profile.resume_signal:
        raise ProgressError("explicit resume signal required")
    if state.index == len(profile.stages) - 1:
        return replace(state, status="completed")
    return ProgressState(profile.profile_id, profile.stages[state.index + 1],
                         state.index + 1, "ready")


def stop(profile: ProgressProfile, state: ProgressState) -> ProgressState:
    _validate(profile, state)
    if state.status in {"completed", "stopped"}:
        raise ProgressError("cannot stop a finished profile")
    return replace(state, status="stopped")


def restore(profile: ProgressProfile, snapshot: dict[str, object]) -> ProgressState:
    """Restore state as data, never as approval or executable authority."""
    try:
        state = ProgressState(snapshot["profile_id"], snapshot["stage"],
                              snapshot["index"], snapshot["status"])
    except (KeyError, TypeError) as exc:
        raise ProgressError("invalid snapshot") from exc
    _validate(profile, state)
    return state
