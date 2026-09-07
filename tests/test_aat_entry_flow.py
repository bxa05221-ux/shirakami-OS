from runtime.aats import Participant, Post, Thread
from runtime.way import Kasen, Renzan, SmallStep, map_and_reexpress


class Selector:
    def select(self, landscape):
        return SmallStep(action="write one sentence", reason="reduce the next action to one observable step")


def test_aats_preserves_thread_and_future_persona_extension_point():
    thread = Thread("t1").with_participant(
        Participant("名無し001", persona={"future": "opaque"})
    ).with_post(Post("名無し001", "まず現在地を見よう", "( ˘ω˘ )"))

    snapshot = thread.snapshot()

    assert snapshot["participants"] == ["名無し001"]
    assert snapshot["posts"][0]["aa"] == "( ˘ω˘ )"
    assert thread.participants[0].persona == {"future": "opaque"}


def test_renzan_collects_viewpoints_without_interpreting_them():
    thread = (
        Thread("t1")
        .with_participant(Participant("名無し001"))
        .with_participant(Participant("名無し002"))
        .with_post(Post("名無し001", "休んだほうがいい"))
        .with_post(Post("名無し002", "でも期限もある"))
    )

    viewpoints = Renzan().collect(thread)

    assert [v.text for v in viewpoints] == ["休んだほうがいい", "でも期限もある"]
    assert [v.participant_id for v in viewpoints] == ["名無し001", "名無し002"]


def test_kasen_reexpresses_viewpoints_as_flow_not_a_transcript():
    thread = (
        Thread("t1")
        .with_participant(Participant("名無し001"))
        .with_participant(Participant("名無し002"))
        .with_post(Post("名無し001", "休んだほうがいい"))
        .with_post(Post("名無し002", "でも期限もある"))
    )

    narrative = Kasen().compose(Renzan().collect(thread))

    assert narrative == "休んだほうがいい 見方によっては、でも期限もあるとも考えられるかもしれません。"
    assert "名無し001" not in narrative
    assert "名無し002" not in narrative


def test_entry_path_maps_landscape_before_small_step():
    thread = Thread("t1").with_participant(Participant("名無し001")).with_post(
        Post("名無し001", "今は何から手を付ける？")
    )

    result = map_and_reexpress({"urgency": "medium", "importance": "high"}, thread, selector=Selector())

    assert result.landscape == {"urgency": "medium", "importance": "high"}
    assert result.narrative == "今は何から手を付ける？"
    assert result.small_step.action == "write one sentence"
