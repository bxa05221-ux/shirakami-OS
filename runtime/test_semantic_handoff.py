from runtime.semantic_handoff import SemanticHandoff

def test_semantic_handoff_preserves_context_without_authority():
    handoff = SemanticHandoff(
        observation_id="0123456789abcdef",
        landscape={"text": "x"},
        protocol_id="protocol.example.v1",
        runtime_state="observed",
        evidence_ids=("evidence-1",),
        metadata={"source": "api"},
    )
    payload = handoff.as_mapping()
    assert payload["observation_id"] == "0123456789abcdef"
    assert payload["protocol_id"] == "protocol.example.v1"
    assert payload["evidence_ids"] == ("evidence-1",)
    assert "approval" not in payload
    assert "execution_authorized" not in payload

def test_semantic_handoff_is_frozen():
    handoff = SemanticHandoff("0123456789abcdef")
    try:
        handoff.protocol_id = "changed"
    except Exception:
        pass
    else:
        raise AssertionError("SemanticHandoff must be immutable")

def test_semantic_handoff_does_not_mutate_source_context():
    landscape = {"text": "x"}
    metadata = {"source": "api"}
    handoff = SemanticHandoff("0123456789abcdef", landscape=landscape, metadata=metadata)
    payload = handoff.as_mapping()
    payload["landscape"]["text"] = "changed"
    payload["metadata"]["source"] = "changed"
    assert landscape["text"] == "x"
    assert metadata["source"] == "api"
