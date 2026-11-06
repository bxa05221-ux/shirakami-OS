"""Synthetic-only HTTP authorization tests for the isolated evaluation API."""
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

from api.evaluation_records import create_evaluation_records_app
from security.evaluator_identity import EvaluatorIdentityRegistry
from security.local_store import EncryptedEvaluationStore, RotatingKeyring

A, B, C = "a" * 40, "b" * 40, "c" * 40

def fixture_client():
    identities = EvaluatorIdentityRegistry()
    identities.provision(A, "alice", {"p1"})
    identities.provision(B, "bob", {"p1"})
    identities.provision(C, "carol", {"p2"})
    store = EncryptedEvaluationStore(RotatingKeyring({"v1": Fernet.generate_key()}, "v1"))
    store.register_project_members("p1", {"alice", "bob"})
    store.register_project_members("p2", {"carol"})
    return TestClient(create_evaluation_records_app(identities, store)), identities

def hdr(token):
    return {"X-Evaluator-Token": token}

def test_identity_bound_to_credential_and_private_records():
    client, _ = fixture_client()
    url = "/evaluation/projects/p1/records"
    assert client.post(url, json={"record_id": "r1", "content": "synthetic"}, headers=hdr(A)).status_code == 201
    assert client.get(url + "/r1", headers=hdr(A)).json()["content"] == "synthetic"
    assert client.get(url + "/r1", headers=hdr(B)).status_code == 403
    assert client.get(url + "/r1", headers=hdr(C)).status_code == 403
    assert client.get(url + "/r1").status_code == 403
    assert client.post(url, json={"record_id": "r2", "content": "x"}, headers=hdr(C)).status_code == 403

def test_consensus_share_and_revoke_are_owner_controlled():
    client, _ = fixture_client()
    url = "/evaluation/projects/p1/records"
    client.post(url, json={"record_id": "r1", "content": "synthetic"}, headers=hdr(A))
    share = url + "/r1/share"
    assert client.post(share, json={"recipients": ["bob"]}, headers=hdr(B)).status_code == 403
    assert client.post(share, json={"recipients": ["carol"]}, headers=hdr(A)).status_code == 403
    assert client.post(share, json={"recipients": ["bob"]}, headers=hdr(A)).status_code == 200
    assert client.get(url + "/r1", headers=hdr(B)).status_code == 200
    assert client.post(url + "/r1/revoke", headers=hdr(A)).status_code == 200
    assert client.get(url + "/r1", headers=hdr(B)).status_code == 403

def test_revoked_token_denied_without_client_supplied_identity():
    client, identities = fixture_client()
    url = "/evaluation/projects/p1/records"
    client.post(url, json={"record_id": "r1", "content": "synthetic"}, headers=hdr(A))
    identities.revoke(A)
    assert client.get(url + "/r1", headers=hdr(A)).status_code == 403

def test_cross_project_record_id_cannot_be_shared_or_revoked():
    client, _ = fixture_client()
    p1 = "/evaluation/projects/p1/records"
    p2 = "/evaluation/projects/p2/records"
    client.post(p1, json={"record_id": "r1", "content": "synthetic"}, headers=hdr(A))
    assert client.post(p2 + "/r1/share", json={"recipients": ["carol"]}, headers=hdr(C)).status_code == 403
    assert client.post(p2 + "/r1/revoke", headers=hdr(C)).status_code == 403
