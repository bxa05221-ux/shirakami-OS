"""Experimental, non-executing Semantic Handoff v0.2 bridge registration.

This module records one immutable upstream implementation reference for review
and fixture-level integration.  It never downloads, imports, authenticates to,
or dispatches through that repository.  Runtime authority remains with the
existing Human Gate and Evidence boundaries.
"""

from __future__ import annotations

from typing import Final

SEMANTIC_HANDOFF_V02_EXPERIMENT: Final = {
    "status": "experimental",
    "upstream": {
        "repository": "bxa05221-ux/github-context-bridge",
        "commit": "e5442dffb3451766d5ed15ee1e208d420c6321ef",
        "source_commit": "ed3a13c2a48426b16dffab1666fca745a83de21f",
        "path": "src/semantic_handoff_adapter.py",
        "entry_point": "validate_semantic_handoff_v02",
    },
    "boundary": "external_adapter_only",
    "authority": {"execution_permitted": False},
    "preservation": {
        "human_gate_required": True,
        "evidence_is_immutable": True,
        "reality_mutation": False,
    },
    "unverified": (
        "cross-AI semantic preservation",
        "human identity or approval authenticity",
        "external communication",
    ),
}


def experimental_semantic_handoff_registration() -> dict:
    """Return a copy of the reviewable, non-executing integration record."""

    return {
        **SEMANTIC_HANDOFF_V02_EXPERIMENT,
        "upstream": dict(SEMANTIC_HANDOFF_V02_EXPERIMENT["upstream"]),
        "authority": dict(SEMANTIC_HANDOFF_V02_EXPERIMENT["authority"]),
        "preservation": dict(SEMANTIC_HANDOFF_V02_EXPERIMENT["preservation"]),
    }
