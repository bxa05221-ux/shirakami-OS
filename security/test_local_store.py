import pytest
from cryptography.fernet import Fernet
from security.local_store import AccessDenied, EncryptedEvaluationStore, EncryptionError, RotatingKeyring
def store(): return EncryptedEvaluationStore(RotatingKeyring({"v1": Fernet.generate_key()}, "v1"))
def test_private_evaluator_record_is_isolated_until_explicitly_shared():
    records = store(); records.register_project_members("project-a", {"evaluator-a", "evaluator-b"}); records.put_private("r1", "project-a", "evaluator-a", b"private judgment")
    with pytest.raises(AccessDenied): records.read("r1", "project-a", "evaluator-b")
    with pytest.raises(AccessDenied): records.read("r1", "project-b", "evaluator-a")
    records.share_for_consensus("r1", "evaluator-a", {"evaluator-b"})
    assert records.read("r1", "project-a", "evaluator-b") == b"private judgment"
    assert [event.action for event in records.audit_events()] == ["write", "denied", "denied", "share_for_consensus", "read"]
def test_invalid_key_or_ciphertext_is_rejected():
    with pytest.raises(EncryptionError): RotatingKeyring({"v1": b"not-a-key"}, "v1")
    keyring = RotatingKeyring({"v1": Fernet.generate_key()}, "v1")
    with pytest.raises(EncryptionError): keyring.decrypt("v1", b"corrupt")

def test_unregistered_writer_and_cross_project_share_are_denied():
    records = store()
    records.register_project_members("project-a", {"owner", "peer"})
    records.register_project_members("project-b", {"outsider"})
    with pytest.raises(AccessDenied):
        records.put_private("r0", "project-a", "outsider", b"not allowed")
    records.put_private("r1", "project-a", "owner", b"secret")
    with pytest.raises(AccessDenied):
        records.share_for_consensus("r1", "owner", {"outsider"})
    with pytest.raises(AccessDenied):
        records.read("r1", "project-a", "outsider")

def test_duplicate_record_id_is_rejected_across_projects():
    records = store()
    records.register_project_members("project-a", {"a"})
    records.register_project_members("project-b", {"b"})
    records.put_private("same-id", "project-a", "a", b"original")
    with pytest.raises(AccessDenied):
        records.put_private("same-id", "project-b", "b", b"overwrite")
    assert records.read("same-id", "project-a", "a") == b"original"

def test_revocation_removes_consensus_access():
    records = store()
    records.register_project_members("project-a", {"owner", "peer"})
    records.put_private("r1", "project-a", "owner", b"secret")
    records.share_for_consensus("r1", "owner", {"peer"})
    assert records.read("r1", "project-a", "peer") == b"secret"
    records.revoke_consensus("r1", "owner")
    with pytest.raises(AccessDenied):
        records.read("r1", "project-a", "peer")
    assert records.read("r1", "project-a", "owner") == b"secret"

def test_removed_member_cannot_read_previously_shared_record():
    records = store()
    records.register_project_members("project-a", {"owner", "peer"})
    records.put_private("r1", "project-a", "owner", b"secret")
    records.share_for_consensus("r1", "owner", {"peer"})
    records.register_project_members("project-a", {"owner"})
    with pytest.raises(AccessDenied):
        records.read("r1", "project-a", "peer")

def test_store_operations_automatically_append_verifiable_audit_chain():
    from security.audit_chain import LocalAuditChain
    records = store()
    records.register_project_members("project-a", {"owner", "peer"})
    records.put_private("r1", "project-a", "owner", b"synthetic")
    with pytest.raises(AccessDenied):
        records.read("r1", "project-a", "peer")
    records.share_for_consensus("r1", "owner", {"peer"})
    assert records.read("r1", "project-a", "peer") == b"synthetic"
    records.revoke_consensus("r1", "owner")
    events = records.audit_events()
    chain = records.audit_chain_snapshot()
    assert [e.action for e in events] == [e.action for e in chain]
    assert records.verify_audit_chain(expected_head=records.audit_chain_head())
    assert not LocalAuditChain.verify(chain[:-1], expected_head=records.audit_chain_head())
    assert "synthetic" not in repr(chain)

def test_same_owner_cannot_mutate_record_through_another_project():
    records = store()
    records.register_project_members("project-a", {"owner", "peer"})
    records.register_project_members("project-b", {"owner", "peer"})
    records.put_private("r1", "project-a", "owner", b"synthetic")
    with pytest.raises(AccessDenied):
        records.share_for_consensus("r1", "owner", {"peer"}, project_id="project-b")
    with pytest.raises(AccessDenied):
        records.revoke_consensus("r1", "owner", project_id="project-b")
    with pytest.raises(AccessDenied):
        records.read("r1", "project-a", "peer")
    assert [event.action for event in records.audit_events()].count("denied_project_mismatch") == 2
    assert records.verify_audit_chain(expected_head=records.audit_chain_head())
