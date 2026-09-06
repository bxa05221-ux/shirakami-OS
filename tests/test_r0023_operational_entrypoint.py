from __future__ import annotations

import os

from runtime.operational_github_read import main


def test_operational_entrypoint_requires_explicit_enable(monkeypatch, capsys):
    monkeypatch.delenv("SHIRAKAMI_LIVE_GITHUB_TEST", raising=False)
    monkeypatch.delenv("SHIRAKAMI_GITHUB_TOKEN", raising=False)

    assert main() == 2
    captured = capsys.readouterr()
    assert "live GitHub read is disabled" in captured.err


def test_operational_entrypoint_requires_token(monkeypatch, capsys):
    monkeypatch.setenv("SHIRAKAMI_LIVE_GITHUB_TEST", "1")
    monkeypatch.delenv("SHIRAKAMI_GITHUB_TOKEN", raising=False)

    assert main() == 2
    captured = capsys.readouterr()
    assert "SHIRAKAMI_GITHUB_TOKEN is required" in captured.err
