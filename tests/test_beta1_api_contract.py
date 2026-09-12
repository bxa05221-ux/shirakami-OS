"""Contract tests for the Shirakami OS β1.0 Public API boundary.

These tests intentionally validate the public boundary, not backend-specific
implementation details.
"""


def test_beta1_api_contract_document_exists():
    from pathlib import Path

    path = Path(__file__).parents[1] / "spec" / "api-beta-1.0.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "# Shirakami OS β1.0 Public API" in text
    assert "POST /v1/execute" in text
    assert "POST /v1/landscape/observe" in text
    assert "POST /v1/evidence/observe" in text
    assert "POST /v1/adapter/invoke" in text
