"""Minimal reversible Reverse Landscape Flow experiment.

This module keeps Evidence immutable and models the reverse path as explicit
lineage records. It intentionally does not generate interpretations or mutate
Evidence; questions and counter-evidence are supplied by the observer.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from evidence import EvidenceRecord


@dataclass(frozen=True)
class DeltaRecord:
    """A change observed between two Landscape-facing snapshots."""

    source_evidence_id: str
    changed: Mapping[str, Any]
    removed: tuple[str, ...] = ()


@dataclass(frozen=True)
class MatomeRepresentation:
    """A representation of Delta, not a replacement for its source Evidence."""

    delta: DeltaRecord
    format: str = "yaml"


@dataclass(frozen=True)
class DarkQuestion:
    """A question directed at a Delta without asserting its hidden cause."""

    matome: MatomeRepresentation
    question: str


@dataclass(frozen=True)
class CounterEvidence:
    """Evidence gathered to test an interpretation or question."""

    question: DarkQuestion
    observation: Mapping[str, Any]


@dataclass(frozen=True)
class ReObservation:
    """A new observation linked to prior lineage without rewriting it."""

    prior_evidence_id: str
    counter_evidence: CounterEvidence
    outcome: str


def evidence_id(evidence: EvidenceRecord) -> str:
    """Return a stable, human-readable lineage key for an Evidence record."""

    return f"{evidence.protocol_id}:{evidence.transition_kind}"


def derive_delta(
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    source_evidence_id: str,
) -> DeltaRecord:
    """Extract only observable mapping differences; do not interpret them."""

    changed = {
        key: value
        for key, value in current.items()
        if previous.get(key) != value
    }
    removed = tuple(sorted(set(previous) - set(current)))
    return DeltaRecord(
        source_evidence_id=source_evidence_id,
        changed=MappingProxyType(changed),
        removed=removed,
    )


def represent_delta(delta: DeltaRecord, format: str = "yaml") -> MatomeRepresentation:
    """Wrap a Delta in a replaceable representation format."""

    return MatomeRepresentation(delta=delta, format=format)


def pose_dark_question(
    matome: MatomeRepresentation,
    question: str,
) -> DarkQuestion:
    """Attach a question without turning it into an interpretation."""

    if not question.strip():
        raise ValueError("question must be non-empty")
    return DarkQuestion(matome=matome, question=question)


def record_counter_evidence(
    question: DarkQuestion,
    observation: Mapping[str, Any],
) -> CounterEvidence:
    """Record a new observation against a Dark Question."""

    return CounterEvidence(
        question=question,
        observation=MappingProxyType(dict(observation)),
    )


def record_reobservation(
    prior_evidence_id: str,
    counter_evidence: CounterEvidence,
    outcome: str,
) -> ReObservation:
    """Create a new lineage node without changing prior Evidence."""

    if not outcome.strip():
        raise ValueError("outcome must be non-empty")
    return ReObservation(
        prior_evidence_id=prior_evidence_id,
        counter_evidence=counter_evidence,
        outcome=outcome,
    )
