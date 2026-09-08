from runtime.credential_provider import EnvironmentCredentialProvider


def test_environment_credential_provider_reads_value_without_persistence(monkeypatch):
    monkeypatch.setenv("SHIRAKAMI_TEST_TOKEN", "test-only-token")

    provider = EnvironmentCredentialProvider("SHIRAKAMI_TEST_TOKEN")

    assert provider.get() == "test-only-token"
    assert provider.variable_name == "SHIRAKAMI_TEST_TOKEN"


def test_environment_credential_provider_fails_closed_when_missing(monkeypatch):
    monkeypatch.delenv("SHIRAKAMI_TEST_TOKEN", raising=False)

    provider = EnvironmentCredentialProvider("SHIRAKAMI_TEST_TOKEN")

    assert provider.get() == ""


def test_provider_re_reads_environment_value(monkeypatch):
    monkeypatch.setenv("SHIRAKAMI_TEST_TOKEN", "first")
    provider = EnvironmentCredentialProvider("SHIRAKAMI_TEST_TOKEN")

    assert provider.get() == "first"

    monkeypatch.setenv("SHIRAKAMI_TEST_TOKEN", "second")
    assert provider.get() == "second"
