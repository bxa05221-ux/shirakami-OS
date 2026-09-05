"""Verify the Thread RPG canonical artifact against the β0.1 loader boundary."""

from pathlib import Path

import pytest

from runtime.protocol_loader import ProtocolLoadError, load_matome


ROOT = Path(__file__).resolve().parents[1]
THREAD_RPG = ROOT / "protocols" / "thread-rpg-v1.2.1.yaml"


def test_thread_rpg_is_present_as_canonical_protocol_artifact():
    text = THREAD_RPG.read_text(encoding="utf-8")

    assert "id: thread_rpg" in text
    assert "version: 1.2.1" in text
    assert "protocol_semantics_owned_by_protocol: true" in text


def test_thread_rpg_canonical_artifact_does_not_silently_enter_matome_beta01_subset():
    text = THREAD_RPG.read_text(encoding="utf-8")

    with pytest.raises(ProtocolLoadError):
        load_matome(THREAD_RPG)

    assert text.splitlines()[0].strip() == "protocol:"
