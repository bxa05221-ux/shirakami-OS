"""Minimal re-observation boundary for Shirakami OS.

A concern does not become a diagnosis. A lens does not become an answer.
This module keeps re-observation separate from Landscape mutation and Evidence.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ObservationRequest:
    """A human-readable request to inspect the current Landscape differently."""

    concern: str
    lens: str
    parameters: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ObservationView:
    """A non-mutating view produced by an explicit observation request."""

    concern: str
    lens: str
    observed: Mapping[str, Any]
    uncertainty: tuple[Any, ...] = ()
    source_revision: Any = None


def reobserve(
    landscape: Mapping[str, Any],
    request: ObservationRequest,
) -> ObservationView:
    """Return an alternate view without changing the Landscape.

    The caller supplies the explicitly observed fields. This boundary does not
    diagnose the concern, score success, choose a destination, or create
    Evidence. Only an actual Landscape transition should enter the Evidence
    path elsewhere in the Runtime.
    """
    parameters = dict(request.parameters or {})
    observed = parameters.get("observed", {})
    if not isinstance(observed, Mapping):
        raise TypeError("parameters['observed'] must be a mapping")

    uncertainty = parameters.get("uncertainty", ())
    if isinstance(uncertainty, str):
        uncertainty = (uncertainty,)
    else:
        uncertainty = tuple(uncertainty or ())

    return ObservationView(
        concern=request.concern,
        lens=request.lens,
        observed=dict(observed),
        uncertainty=uncertainty,
        source_revision=landscape.get("revision"),
    )
