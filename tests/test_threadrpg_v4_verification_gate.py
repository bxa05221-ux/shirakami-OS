from runtime.aats import Post, Thread
from runtime.threadrpg_v4_landscape import ConversationLandscape, Delta


def classify(**kwargs):
    thread = Thread("verification-gate").with_post(
        Post("nanashi", "unverified claim")
    )
    landscape = ConversationLandscape().record_generation_turn(
        thread,
        (
            Delta(
                "observation",
                "unverified claim",
                (0,),
                origin="anonymous_generated",
                **kwargs,
            ),
        ),
    )
    return landscape.to_matome_draft()


def test_verified_flag_alone_cannot_promote_fact():
    result = classify(verified=True)
    assert result["facts"] == []
    assert result["unverified"] == ["unverified claim"]


def test_evidence_id_without_approval_cannot_promote_fact():
    result = classify(
        verified=True,
        verification_evidence_id="evidence-001",
    )
    assert result["facts"] == []


def test_approval_without_evidence_cannot_promote_fact():
    result = classify(
        verified=True,
        human_approved=True,
    )
    assert result["facts"] == []


def test_all_explicit_conditions_allow_fact_candidate():
    result = classify(
        verified=True,
        human_approved=True,
        verification_evidence_id="evidence-001",
    )
    assert result["facts"] == ["unverified claim"]
