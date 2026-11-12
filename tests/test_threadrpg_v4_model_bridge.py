"""Offline ThreadRPG v4 model boundary regression."""
import json

import pytest

from runtime.aats import Thread
from runtime.real_model_adapter import RealModelAdapter
from runtime.threadrpg_v4_minimal_flow import run_minimal_flow
from runtime.threadrpg_v4_model_bridge import ModelReplyGenerator


def test_model_bridge_generates_anonymous_cross_replies():
    requests = []

    def fixture(request):
        requests.append(request)
        return {
            "provider": "offline-fixture",
            "output": json.dumps({
                "replies": [
                    {
                        "text": "それなｗ",
                        "source_post_indices": [0],
                    },
                    {
                        "text": ">>2 いや違うだろｗ",
                        "batch_reply_indices": [0],
                    },
                ]
            }, ensure_ascii=False),
        }

    generator = ModelReplyGenerator(RealModelAdapter(fixture))
    result = run_minimal_flow(Thread("vip-1"), "相談がある", generator)

    assert len(requests) == 1
    assert requests[0].context["protocol_id"] == "threadrpg.v4"
    assert [post.participant_id for post in result.thread.posts] == [
        "icchi", "nanashi", "nanashi"
    ]
    assert result.resolved_reply_references == ((0,), (1,))
    assert result.reality_mutation_permitted is False
    assert result.llm_connected is False


def test_invalid_model_output_is_rejected_without_committing_posts():
    generator = ModelReplyGenerator(
        lambda prompt, protocol_id: {"output": '{"replies":[]}'}
    )
    original = Thread("vip-2")
    with pytest.raises(ValueError):
        run_minimal_flow(original, "相談がある", generator)
    assert original.posts == ()