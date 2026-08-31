from runtime.protocol_runtime_bridge import execute_protocol
from runtime.prototype import Transition


TSUGARU_GUIDE_PROTOCOL = {
    "matome": {
        "title": "TSUGARU GUIDE HIGH SCHOOL COLLABORATION PROTOCOL",
        "version": "0.1",
        "purpose": "student landscape observation and regional continuity",
        "principles": [
            "student_as_observer",
            "student_as_co_creator",
            "landscape_first",
            "evidence_before_assertion",
            "intergenerational_continuity",
        ],
    }
}


def test_tsugaru_guide_protocol_executes_without_runtime_domain_semantics():
    def transition(value):
        return Transition(
            kind="student.observation",
            data={
                "observation": value["observation"],
                "student_question": value["student_question"],
                "source": value["source"],
            },
        )

    execution = execute_protocol(
        TSUGARU_GUIDE_PROTOCOL,
        transition,
        input_value={
            "observation": "The bus stop has no route information visible from the road.",
            "student_question": "Would a first-time visitor know where to wait?",
            "source": "student.fieldwalk",
        },
    )

    assert execution.protocol_title == "TSUGARU GUIDE HIGH SCHOOL COLLABORATION PROTOCOL"
    assert execution.protocol_version == "0.1"
    assert execution.result.status == "completed"
    assert execution.result.transition.kind == "student.observation"
    assert execution.result.transition.data == {
        "observation": "The bus stop has no route information visible from the road.",
        "student_question": "Would a first-time visitor know where to wait?",
        "source": "student.fieldwalk",
    }


def test_tsugaru_guide_domain_meaning_remains_outside_runtime_contract():
    def transition(value):
        return Transition(
            kind="student.discovery",
            data={
                "location": value["location"],
                "discovery": value["discovery"],
                "verification_status": value["verification_status"],
            },
        )

    execution = execute_protocol(
        TSUGARU_GUIDE_PROTOCOL,
        transition,
        input_value={
            "location": "local-history-site",
            "discovery": "A previously undocumented local story was reported by a resident.",
            "verification_status": "unverified",
        },
    )

    result = execution.result
    assert result.status == "completed"
    assert result.transition.kind == "student.discovery"
    assert result.transition.data["verification_status"] == "unverified"
    assert "student_as_observer" in TSUGARU_GUIDE_PROTOCOL["matome"]["principles"]
    assert "student_as_observer" not in result.signals
    assert "landscape_first" not in result.signals
