from runtime.experimental_semantic_handoff import (
    SEMANTIC_HANDOFF_V02_EXPERIMENT,
    experimental_semantic_handoff_registration,
)


def test_experimental_semantic_handoff_registration_is_pinned_and_nonexecuting():
    registration = experimental_semantic_handoff_registration()

    assert registration["status"] == "experimental"
    assert registration["upstream"]["repository"] == "bxa05221-ux/github-context-bridge"
    assert registration["upstream"]["commit"] == "e5442dffb3451766d5ed15ee1e208d420c6321ef"
    assert registration["upstream"]["source_commit"] == "ed3a13c2a48426b16dffab1666fca745a83de21f"
    assert registration["upstream"]["entry_point"] == "validate_semantic_handoff_v02"
    assert registration["boundary"] == "external_adapter_only"
    assert registration["authority"]["execution_permitted"] is False
    assert registration["preservation"] == {
        "human_gate_required": True,
        "evidence_is_immutable": True,
        "reality_mutation": False,
    }
    assert "cross-AI semantic preservation" in registration["unverified"]
    assert registration is not SEMANTIC_HANDOFF_V02_EXPERIMENT
