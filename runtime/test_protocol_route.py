from pathlib import Path

import pytest

from api import ShirakamiAPI
from evolution_pipeline import EvidenceDrivenRuntime
from evolution_bridge import ContextSnapshot
from prototype import Transition
from protocol_route import compose_route


def _step(context):
    return Transition(
        kind=f"step.{context.protocol_id}",
        data={"value": context.input.get("value", 0) + 1, "changed": True},
    )


def _api() -> ShirakamiAPI:
    return ShirakamiAPI(EvidenceDrivenRuntime())


def test_one_stroke_route_executes_as_one_runtime_handle() -> None:
    api = _api()
    route_id = "route.a-b-c"
    api.observe(
        {"value": 0},
        ContextSnapshot(
            protocol_id=route_id,
            landscape={"route": ["a", "b", "c"]},
            metadata={"source": "route-test"},
        ),
    )
    api.analyze(route_id, protocol_exists=False, diff_ref="candidate:a-b-c")
    approved = api.approve(
        approved=True,
        reviewer="human",
        human_authorized=True,
    )
    assert approved["accepted"] is True

    route = compose_route(
        route_id,
        [("a", _step), ("b", _step), ("c", _step)],
    )
    result = api.execute(route, route_id, {"value": 0}, handoff_id="SH-HO-ROUTE-001")

    assert result["status"] == "completed"
    assert result["transition"]["kind"] == f"route.{route_id}"
    assert result["transition"]["data"]["route"] == ["a", "b", "c"]
    assert [item["protocol_id"] for item in result["transition"]["data"]["trace"]] == ["a", "b", "c"]

    verification = api.verify_execution(
        result["execution_id"],
        expected_transition_kind=f"route.{route_id}",
        diff_ref="candidate:a-b-c",
    )
    assert verification is not None
    assert verification.status == "pass"

    evidence = api.query_evidence(protocol_id=route_id)
    assert evidence


def test_route_rejects_protocol_reuse() -> None:
    with pytest.raises(ValueError):
        compose_route("route.invalid", [("a", _step), ("a", _step)])


def test_route_requires_at_least_two_protocols() -> None:
    with pytest.raises(ValueError):
        compose_route("route.invalid", [("a", _step)])
