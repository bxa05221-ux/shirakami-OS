"""Minimal executable entry point for Shirakami OS.

This is intentionally small. It exposes one concrete boot path:
Landscape -> Protocol -> Runtime -> Transition -> Evidence -> Landscape -> Navigation -> Result.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.evidence import EvidenceRecord, capture_evidence
from runtime.landscape import LandscapeState
from runtime.navigation import NavigationState
from runtime.navigation_history import DirectionTrend, NavigationHistory
from runtime.navigation_observer import NavigationObserver
from runtime.navigation_scenario import NavigationScenario
from runtime.prototype import ExecutionContext, Runtime, Transition


@dataclass(frozen=True)
class OSResult:
    """Human-inspectable result of one Shirakami OS execution."""

    protocol_id: str
    status: str
    transition: Transition
    evidence: EvidenceRecord
    landscape: Mapping[str, Any]
    navigation: Mapping[str, Any]
    direction_trend: DirectionTrend


class ShirakamiOS:
    """Smallest usable Shirakami OS boundary."""

    def __init__(self) -> None:
        self.runtime = Runtime()
        self.landscape = LandscapeState.empty()
        self.navigation = NavigationState()
        self.navigation_observer = NavigationObserver(self.navigation)
        self.navigation_history = NavigationHistory()
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
        """Execute one Protocol and feed its observable transition into Landscape and Navigation."""
        if not self.booted:
            self.boot()

        result = self.runtime.execute(protocol_id, protocol, input_data)
        evidence = capture_evidence(result)
        self.landscape.apply_evidence(evidence)
        self.navigation_observer.observe(evidence)
        self.navigation_history.record(self.navigation.snapshot())

        return OSResult(
            protocol_id=result.protocol_id,
            status=result.status,
            transition=result.transition,
            evidence=evidence,
            landscape=self.landscape.snapshot(),
            navigation=self.navigation.snapshot(),
            direction_trend=self.navigation_history.direction_trend(),
        )

    def simulate_navigation(self, steps: int = 3) -> NavigationScenario:
        """Project the latest observed navigation state without steering or prediction."""
        latest = self.navigation_history.latest() or self.navigation.snapshot()
        return NavigationScenario.continue_observed_state(latest, steps=steps)


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
    print(f"navigation: {dict(result.navigation)}")
    print(f"direction_trend: {result.direction_trend}")
    print(f"scenario: {os.simulate_navigation().steps}")


if __name__ == "__main__":
    main()
