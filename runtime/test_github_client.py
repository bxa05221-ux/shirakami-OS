from github_client import GitHubContentsClient, GitHubTransportError


def test_github_client_requires_injected_token():
    client = GitHubContentsClient(
        owner="example",
        repo="landscape",
        landscape_path="landscape.json",
        token_provider=lambda: "",
    )

    try:
        client.read_landscape()
    except GitHubTransportError as exc:
        assert "token" in str(exc).lower()
    else:
        raise AssertionError("missing token must fail before transport")
