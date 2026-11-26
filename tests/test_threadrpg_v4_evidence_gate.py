from runtime.aats import Post, Thread
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_observation import observe_post, record_observation
from runtime.threadrpg_v4_evidence_gate import observation_evidence_matches


def test_existing_observation_evidence_matches():
    thread = Thread("t").with_post(Post("icchi", "hello"))
    observation = observe_post(thread, 0, origin="human_post")
    store = record_observation(thread, observation, EvidenceStore())
    evidence_id = store.all()[0].evidence_id

    assert observation_evidence_matches(store, thread, 0, evidence_id)


def test_unknown_evidence_is_rejected():
    thread = Thread("t").with_post(Post("icchi", "hello"))
    assert not observation_evidence_matches(
        EvidenceStore(), thread, 0, "unknown"
    )


def test_mismatched_post_is_rejected():
    thread = Thread("t").with_post(Post("icchi", "hello"))
    observation = observe_post(thread, 0, origin="human_post")
    store = record_observation(thread, observation, EvidenceStore())
    evidence_id = store.all()[0].evidence_id

    modified = Thread("t").with_post(Post("icchi", "changed"))
    assert not observation_evidence_matches(
        store, modified, 0, evidence_id
    )


def test_mismatched_thread_is_rejected():
    thread = Thread("t").with_post(Post("icchi", "hello"))
    observation = observe_post(thread, 0, origin="human_post")
    store = record_observation(thread, observation, EvidenceStore())
    evidence_id = store.all()[0].evidence_id

    other = Thread("other").with_post(Post("icchi", "hello"))
    assert not observation_evidence_matches(
        store, other, 0, evidence_id
    )
