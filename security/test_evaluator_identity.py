import pytest
from security.evaluator_identity import EvaluatorAuthDenied, EvaluatorIdentityRegistry

TOKEN_A = "a" * 40
TOKEN_B = "b" * 40

def test_authentication_requires_registered_credential_and_project():
    registry = EvaluatorIdentityRegistry()
    registry.provision(TOKEN_A, "evaluator-a", {"project-a"})
    assert registry.authenticate(TOKEN_A, "project-a").evaluator_id == "evaluator-a"
    with pytest.raises(EvaluatorAuthDenied):
        registry.authenticate(TOKEN_A, "project-b")
    with pytest.raises(EvaluatorAuthDenied):
        registry.authenticate(TOKEN_B, "project-a")
    with pytest.raises(EvaluatorAuthDenied):
        registry.authenticate(None, "project-a")

def test_revocation_is_immediate():
    registry = EvaluatorIdentityRegistry()
    registry.provision(TOKEN_A, "evaluator-a", {"project-a"})
    registry.revoke(TOKEN_A)
    with pytest.raises(EvaluatorAuthDenied):
        registry.authenticate(TOKEN_A, "project-a")

def test_invalid_and_duplicate_provisioning_is_rejected():
    registry = EvaluatorIdentityRegistry()
    with pytest.raises(ValueError):
        registry.provision("weak", "evaluator-a", {"project-a"})
    with pytest.raises(ValueError):
        registry.provision(TOKEN_A, "evaluator-a", set())
    registry.provision(TOKEN_A, "evaluator-a", {"project-a"})
    with pytest.raises(ValueError):
        registry.provision(TOKEN_A, "evaluator-b", {"project-b"})

def test_one_evaluator_cannot_impersonate_another_with_claimed_identity():
    registry = EvaluatorIdentityRegistry()
    registry.provision(TOKEN_A, "evaluator-a", {"project-a"})
    registry.provision(TOKEN_B, "evaluator-b", {"project-a", "project-b"})
    # Identity is derived from the provisioned credential, never caller-supplied labels.
    principal = registry.authenticate(TOKEN_A, "project-a")
    assert principal.evaluator_id == "evaluator-a"
    assert principal.evaluator_id != "evaluator-b"
    with pytest.raises(EvaluatorAuthDenied):
        registry.authenticate(TOKEN_A, "project-b")


def test_project_grants_are_copied_not_aliased():
    registry = EvaluatorIdentityRegistry()
    grants = {"project-a"}
    registry.provision(TOKEN_A, "evaluator-a", grants)
    grants.add("project-b")
    with pytest.raises(EvaluatorAuthDenied):
        registry.authenticate(TOKEN_A, "project-b")
