from runtime.aats import Thread, Post
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_observation import observe_post, record_observation
from runtime.threadrpg_v4_landscape import ConversationLandscape, Delta


def test_evidence_landscape_connection():
    thread = Thread("t").with_post(Post("icchi", "hello"))
    store = record_observation(
        thread,
        observe_post(thread, 0, origin="human_post"),
        EvidenceStore(),
    )
    delta = Delta(
        "observation", "hello", (0,),
        origin="human_post",
        verified=True,
        human_approved=True,
        verification_evidence_id=store.all()[0].evidence_id,
    )
    landscape = ConversationLandscape().record_generation_turn(thread, (delta,))
    assert landscape.observed_evidence_draft(thread, store) == {
        "evidence_matched": ["hello"],
        "unverified": [],
        "facts": [],
    }
