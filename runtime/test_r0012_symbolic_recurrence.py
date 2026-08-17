"""R0012: symbolic recurrence with lineage and Human Authority.

This test intentionally keeps domain meaning outside Runtime. The Runtime only
executes a protocol that returns an observable Transition; Evidence preserves
that transition; Landscape applies the resulting transition.
"""

from evidence import capture_evidence
from landscape import LandscapeState
from prototype import ExecutionContext, Runtime, Transition


def test_r0012_symbolic_recurrence_requires_human_authority() -> None:
    historical_evidence = {
        "symbol": "grandfather_said",
        "lineage": {
            "source": "historical_evidence",
            "relation": "grandfather",
            "context": "family_memory",
        },
    }

    current_landscape = {
        "context": "present_decision",
        "recurrence_candidate": "grandfather_said",
        "human_authority": False,
    }

    def recurrence_protocol(context: ExecutionContext) -> Transition:
        data = dict(context.input)
        if not data["human_authority"]:
            return Transition(
                kind="symbolic.recurrence.blocked",
                data={
                    "changed": False,
                    "symbol": data["recurrence_candidate"],
                    "reason": "human_authority_required",
                },
            )

        return Transition(
            kind="symbolic.recurrence.accepted",
            data={
                "changed": True,
                "symbol": data["recurrence_candidate"],
                "lineage": data["historical_evidence"]["lineage"],
                "recurrence_context": data["context"],
                "authority": "human",
            },
        )

    runtime = Runtime()

    blocked = runtime.execute(
        "r0012.symbolic_recurrence",
        recurrence_protocol,
        {**current_landscape, "historical_evidence": historical_evidence},
    )
    blocked_evidence = capture_evidence(blocked)

    landscape = LandscapeState.empty()
    landscape.apply_evidence(blocked_evidence)

    assert blocked.status == "completed"
    assert blocked.transition.kind == "symbolic.recurrence.blocked"
    assert landscape.snapshot() == {}

    authorized_input = {
        **current_landscape,
        "historical_evidence": historical_evidence,
        "human_authority": True,
    }
    accepted = runtime.execute(
        "r0012.symbolic_recurrence",
        recurrence_protocol,
        authorized_input,
    )
    accepted_evidence = capture_evidence(accepted)
    landscape.apply_evidence(accepted_evidence)

    assert accepted.transition.kind == "symbolic.recurrence.accepted"
    assert accepted_evidence.transition_data["symbol"] == "grandfather_said"
    assert accepted_evidence.transition_data["lineage"]["relation"] == "grandfather"
    assert accepted_evidence.transition_data["authority"] == "human"
    assert landscape.snapshot()["symbol"] == "grandfather_said"
    assert landscape.snapshot()["recurrence_context"] == "present_decision"
