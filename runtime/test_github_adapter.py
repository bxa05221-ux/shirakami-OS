from github_adapter import GitHubAdapter


def test_github_adapter_preserves_protocol_source_and_provenance():
    source = GitHubAdapter().load_source(
        repository="bxa05221-ux/shirakami-OS",
        path="spec/protocol-registry.yaml",
        ref="main",
        content="matome:\n  title: Example\n",
    )

    assert source.repository == "bxa05221-ux/shirakami-OS"
    assert source.path == "spec/protocol-registry.yaml"
    assert source.ref == "main"
    assert source.content == "matome:\n  title: Example\n"
