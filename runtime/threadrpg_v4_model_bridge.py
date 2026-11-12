"""ThreadRPG v4 provider-neutral reply generation bridge.

No implicit network calls, authority changes, or Reality mutation.
"""
import json

from runtime.threadrpg_v4_minimal_flow import AnonymousReply, ReplyProposal


class ModelReplyGenerator:
    def __init__(self, model_adapter):
        if not callable(model_adapter):
            raise TypeError("model_adapter must be callable")
        self.model_adapter = model_adapter

    def __call__(self, thread, event):
        prompt = json.dumps(
            {
                "task": "Generate 1-8 anonymous VIP-style thread replies",
                "rules": [
                    "Allow replies to other anonymous posters",
                    "Allow jokes, disagreement and digressions",
                    "Do not force a conclusion or summary",
                    "Never invent an Icchi post",
                    "Return JSON with a replies array",
                    "Each reply has text, source_post_indices and batch_reply_indices",
                    "Indices are zero-based; batch references must point backward"
                ],
                "event": event.kind,
                "posts": thread.snapshot()["posts"],
            },
            ensure_ascii=False,
        )
        result = self.model_adapter(prompt, "threadrpg.v4")
        if not isinstance(result, dict):
            raise ValueError("provider response must be a mapping")
        output = result.get("output")
        if not isinstance(output, str):
            raise ValueError("provider output must be a JSON string")

        data = json.loads(output)
        if not isinstance(data, dict) or not isinstance(data.get("replies"), list):
            raise ValueError("provider output must contain replies array")

        replies = tuple(
            AnonymousReply(
                text=item["text"],
                source_post_indices=tuple(item.get("source_post_indices", [])),
                batch_reply_indices=tuple(item.get("batch_reply_indices", [])),
            )
            for item in data["replies"]
        )
        return ReplyProposal(replies=replies)