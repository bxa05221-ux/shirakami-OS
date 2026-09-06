from __future__ import annotations

import os

import pytest

from runtime.live_github_probe import read_live_repository_landscape


@pytest.mark.integration
def test_live_github_read_requires_explicit_operational_configuration():
    """Live access is opt-in and must receive a credential externally."""
    if os.getenv("SHIRAKAMI_LIVE_GITHUB_TEST") != "1":
        pytest.skip("live GitHub integration is explicitly disabled")

    token = os.getenv("SHIRAKAMI_GITHUB_TOKEN", "")
    if not token:
        pytest.fail("SHIRAKAMI_GITHUB_TOKEN is required for the live integration test")

    result = read_live_repository_landscape(
        "bxa05221-ux",
        "shirakami-OS",
        lambda: token,
    )

    assert set(result) == {"repository", "branch", "entries"}
    assert result["repository"] == "bxa05221-ux/shirakami-OS"
