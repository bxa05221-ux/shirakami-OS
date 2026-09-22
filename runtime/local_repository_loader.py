"""Local Repository Protocol Loader boundary.

Loads a protocol artifact from a local repository checkout and delegates
interpretation to the existing Protocol Loader. The local repository owns
storage; the protocol loader owns interpretation.
"""

from __future__ import annotations

from pathlib import Path

from .protocol_loader import ProtocolIR, parse_matome


class LocalRepositoryProtocolLoader:
    """Load a Matome YAML protocol from a local repository checkout."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def load(self, path: str) -> ProtocolIR:
        """Read a protocol path below the repository root and parse it."""
        candidate = self.root / path
        if not candidate.is_file():
            raise FileNotFoundError(path)
        return parse_matome(candidate.read_text(encoding="utf-8"))
