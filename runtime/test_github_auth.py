import pytest

from github_auth import EnvironmentTokenProvider, authorization_header


def test_token_is_read_from_environment(monkeypatch):
    monkeypatch.setenv("TEST_GITHUB_TOKEN", "test-token")
    provider = EnvironmentTokenProvider("TEST_GITHUB_TOKEN")
    assert authorization_header(provider) == {
        "Authorization": "Bearer test-token"
    }


def test_missing_token_fails_closed(monkeypatch):
    monkeypatch.delenv("TEST_GITHUB_TOKEN", raising=False)
    provider = EnvironmentTokenProvider("TEST_GITHUB_TOKEN")
    with pytest.raises(RuntimeError):
        provider.get_token()
