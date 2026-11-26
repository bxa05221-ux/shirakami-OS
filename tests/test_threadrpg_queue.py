import pytest

from runtime.threadrpg_queue import ImaginaryTerm, SemanticConnection, ThreadRPGQueue


def test_only_new_declared_connections_become_growth_history_and_turns_are_bounded():
    queue = ThreadRPGQueue()
    link = SemanticConnection("対義語遊び", "で？", "research_return")

    first = queue.ingest([str(index) for index in range(7)], [link])
    second = queue.ingest(["latest"], [link])

    assert first.recent_turns == ("2", "3", "4", "5", "6")
    assert first.new_connections == (link,)
    assert second.new_connections == ()
    assert second.growth_history == (link,)


def test_user_wish_requires_evidence_to_leave_active_set_and_schedules_reobservation():
    queue = ThreadRPGQueue()
    queue.add_terms([ImaginaryTerm("wish-1", "user", "行きたい")])

    with pytest.raises(ValueError, match="subject confirmation"):
        queue.resolve_term("wish-1")

    queue.resolve_term("wish-1", "EVID-1", subject_confirmed=True)
    context = queue.ingest([], [])
    assert context.unresolved_terms == ()
    assert context.queued_items[-1].kind == "reobserve"


def test_ai_terms_are_explicitly_hypothetical_not_claimed_as_emotion():
    with pytest.raises(ValueError, match="hypothetical"):
        ImaginaryTerm.from_mapping({"term_id": "ai-1", "subject": "ai", "text": "want"})

    term = ImaginaryTerm.from_mapping(
        {"term_id": "ai-1", "subject": "ai", "text": "仮の次の問い", "hypothetical": True}
    )
    assert term.represents_real_emotion is False
