"""Minimal reversible Evidence propagation boundary for flow verification."""

from typing import Protocol, Sequence

from evidence import EvidenceRecord


class EvidenceConsumer(Protocol):
    """A Landscape-side consumer of immutable Evidence."""

    def apply_transition(self, evidence: EvidenceRecord) -> None: ...


class EvidencePropagator:
    """Propagate one Evidence record to multiple consumers without rewriting it."""

    def __init__(self, consumers: Sequence[EvidenceConsumer]) -> None:
        self._consumers = tuple(consumers)

    def propagate(self, evidence: EvidenceRecord) -> None:
        """Deliver the same Evidence object to every registered consumer."""

        for consumer in self._consumers:
            consumer.apply_transition(evidence)
