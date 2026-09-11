from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.protocol_api import build_protocol_request, invoke_protocol
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Runtime, Transition
from runtime.protocol_loader_v2 import parse_protocol


def test_r0097_wasan_protocol_loads_and_executes_with_traceable_steps():
    registry = ProtocolRegistry()
    registry.register(
        "wasan",
        {"version": "0.1", "title": "和算Protocol"},
        state="experimental",
    )

    request = build_protocol_request(
        registry,
        "wasan",
        {
            "problem": "鶴と亀が合わせて5匹、足は合わせて14本。鶴と亀はそれぞれ何匹か。",
            "known": ["animals=5", "legs=14", "crane_legs=2", "turtle_legs=4"],
            "unknown": ["cranes", "turtles"],
        },
    )

    def wasan_executor(protocol_request):
        data = protocol_request.input
        cranes = 3
        turtles = 2
        steps = [
            "cranes + turtles = 5",
            "2*cranes + 4*turtles = 14",
            "cranes = 5 - turtles",
            "2*(5-turtles) + 4*turtles = 14",
            "10 + 2*turtles = 14",
            "turtles = 2",
            "cranes = 3",
        ]
        return Runtime().execute(
            protocol_request.protocol_id,
            lambda _context: Transition(
                kind="wasan.problem.solved",
                data={
                    "changed": True,
                    "problem": data["problem"],
                    "steps": steps,
                    "result": {"cranes": cranes, "turtles": turtles},
                    "verification": "2*3 + 4*2 = 14 and 3+2 = 5",
                },
            ),
            data,
        )

    result = invoke_protocol(request, wasan_executor)
    evidence = capture_evidence(result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert result.status == "completed"
    assert evidence.protocol_id == "wasan"
    assert evidence.transition_kind == "wasan.problem.solved"
    assert evidence.transition_data["result"] == {"cranes": 3, "turtles": 2}
    assert len(evidence.transition_data["steps"]) == 7
    assert landscape.snapshot()["verification"] == "2*3 + 4*2 = 14 and 3+2 = 5"


def test_r0097_wasan_artifact_uses_current_protocol_loader_shape():
    from pathlib import Path

    protocol = parse_protocol(Path("protocols/wasan-v0.1.yaml").read_text(encoding="utf-8"))

    assert protocol.protocol_id == "wasan"
    assert protocol.version == "0.1"
    assert protocol.name == "和算Protocol"
    assert protocol.status == "candidate"
    assert protocol.purpose
