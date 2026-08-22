"""Minimal executable entry point for Shirakami OS.

This is intentionally small. It exposes one concrete boot path:
Landscape -> Protocol -> Runtime -> Transition -> Evidence -> Landscape -> Result.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.evidence import EvidenceRecord, capture_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import ExecutionContext, Runtime, Transition


@dataclass(frozen=True)
class OSResult:
    """Human-inspectable result of one Shirakami OS execution."""

    protocol_id: str
    status: str
    transition: Transition
    evidence: EvidenceRecord
    landscape: Mapping[str, Any]


class ShirakamiOS:
    """Smallest usable Shirakami OS boundary."""

    def __init__(self) -> None:
        self.runtime = Runtime()
        self.landscape = LandscapeState.empty()
        self.booted = False

    def boot(self, landscape: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
        """Start the OS with an initial observable Landscape."""
        self.landscape = LandscapeState(_state=dict(landscape or {}))
        self.booted = True
        return self.landscape.snapshot()

    def execute(
        self,
        protocol_id: str,
        protocol,
        input_data: Mapping[str, Any] | None = None,
    ) -> OSResult:
        """Execute one Protocol and feed its observable transition back to Landscape."""
        if not self.booted:
            self.boot()

        result = self.runtime.execute(protocol_id, protocol, input_data)
        evidence = capture_evidence(result)
        self.landscape.apply_evidence(evidence)

        return OSResult(
            protocol_id=result.protocol_id,
            status=result.status,
            transition=result.transition,
            evidence=evidence,
            landscape=self.landscape.snapshot(),
        )


def example_protocol(context: ExecutionContext) -> Transition:
    """Small protocol used only to demonstrate the executable OS boundary."""
    return Transition(
        kind="landscape.message.received",
        data={
            "changed": True,
            "message": context.input.get("message", ""),
        },
    )


def main() -> None:
    os = ShirakamiOS()
    initial = os.boot({"owner": "human", "state": "ready"})
    result = os.execute(
        "example.landscape.message",
        example_protocol,
        {"message": "hello landscape"},
    )

    print("Shirakami OS")
    print("============")
    print(f"booted: {os.booted}")
    print(f"initial_landscape: {dict(initial)}")
    print(f"protocol: {result.protocol_id}")
    print(f"status: {result.status}")
    print(f"transition: {result.transition.kind}")
    print(f"evidence: {dict(result.evidence.transition_data)}")
    print(f"landscape: {dict(result.landscape)}")


if __name__ == "__main__":
    main()
