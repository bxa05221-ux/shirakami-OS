"""Minimal API-key authentication for the HTTP transport.

Authentication is an access-control boundary only. It does not create
semantic authority and does not participate in Context/Evidence lineage.
"""

from __future__ import annotations

import hmac

from fastapi import Header, HTTPException


def require_api_key(expected_api_key: str | None):
    """Return a FastAPI dependency for an optional configured API key.

    When no key is configured, the transport remains backward-compatible for
    local/test use. Once configured, every protected request must provide the
    matching X-API-Key header.
    """

    def dependency(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
        if expected_api_key is None:
            return
        if x_api_key is None or not hmac.compare_digest(x_api_key, expected_api_key):
            raise HTTPException(status_code=401, detail="invalid or missing API key")

    return dependency
