"""Immutable Landscape Observation boundary for Runtime β0.1."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


def _immutable_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class LandscapeObservation:
    """A non-authoritative observation of current Landscape state.

    Observation records what was observed. It does not interpret domain truth,
    mutate Landscape, create authorization, or become executable by itself.
    """

    observation_identity: str
    source_landscape_context: Mapping[str, Any]
    observed_state: Mapping[str, Any]
    provenance: Mapping[str, Any]
    uncertainty: str
    timestamp_or_run_context: Mapping[str, Any]
    authority: bool = False
    executable: bool = False

    def __post_init__(self) -> None:
        if not self.observation_identity:
            raise ValueError("observation_identity is required")
        if self.authority:
            raise ValueError("LandscapeObservation cannot carry authority")
        if self.executable:
            raise ValueError("LandscapeObservation cannot be executable")

        object.__setattr__(
            self,
            "source_landscape_context",
            _immutable_mapping(self.source_landscape_context),
        )
        object.__setattr__(
            self,
            "observed_state",
            _immutable_mapping(self.observed_state),
        )
        object.__setattr__(self, "provenance", _immutable_mapping(self.provenance))
        object.__setattr__(
            self,
            "timestamp_or_run_context",
            _immutable_mapping(self.timestamp_or_run_context),
        )

    @classmethod
    def from_landscape(
        cls,
        landscape: Any,
        *,
        observation_identity: str,
        provenance: Mapping[str, Any],
        uncertainty: str,
        timestamp_or_run_context: Mapping[str, Any],
        source_landscape_context: Mapping[str, Any] | None = None,
    ) -> "LandscapeObservation":
        """Capture a Landscape snapshot without applying any mutation."""
        if not hasattr(landscape, "snapshot"):
            raise TypeError("landscape must expose snapshot()")

        observed_state = landscape.snapshot()
        context = (
            dict(source_landscape_context)
            if source_landscape_context is not None
            else {}
        )
        return cls(
            observation_identity=observation_identity,
            source_landscape_context=context,
            observed_state=observed_state,
            provenance=provenance,
            uncertainty=uncertainty,
            timestamp_or_run_context=timestamp_or_run_context,
        )
