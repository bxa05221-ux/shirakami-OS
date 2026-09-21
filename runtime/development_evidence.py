"""Import repository development notes into a deterministic evidence boundary.

This module intentionally keeps imported development evidence separate from the
transition-oriented ``EvidenceRecord`` used by the Runtime.
"""

from dataclasses import dataclass, field
import re
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class DevelopmentEvidence:
    """Canonical, immutable representation of a development evidence document."""

    evidence_id: str
    source_type: str
    source_ref: str
    observed_at: str
    protocol_id: str
    status: str
    summary: str
    claims: tuple[str, ...] = ()
    verification: tuple[str, ...] = ()
    human_gate: str = "unknown"
    limitations: tuple[str, ...] = ()
    provenance: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))

    def as_dict(self) -> dict[str, object]:
        """Return a deterministic, JSON-compatible representation."""
        return {
            "evidence_id": self.evidence_id,
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "observed_at": self.observed_at,
            "protocol_id": self.protocol_id,
            "status": self.status,
            "summary": self.summary,
            "claims": list(self.claims),
            "verification": list(self.verification),
            "human_gate": self.human_gate,
            "limitations": list(self.limitations),
            "provenance": dict(sorted(self.provenance.items())),
        }


_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
_META_RE = re.compile(r"^-\s*([^:]+):\s*(.*?)\s*$")


def _section_lines(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        match = _SECTION_RE.match(line)
        if match:
            current = match.group(1).strip().lower()
            sections.setdefault(current, [])
        elif current:
            stripped = line.strip()
            if stripped and stripped != "---":
                sections[current].append(stripped)
    return sections


def _metadata(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        match = _META_RE.match(line.strip())
        if match:
            result[match.group(1).strip().lower().replace(" ", "_")] = match.group(2).strip()
    return result


def _items(sections: dict[str, list[str]], *names: str) -> tuple[str, ...]:
    for name in names:
        values = sections.get(name)
        if values:
            return tuple(v[2:].strip() if v.startswith("- ") else v for v in values)
    return ()


def parse_development_evidence(
    text: str,
    *,
    source_ref: str,
    evidence_id: str | None = None,
) -> DevelopmentEvidence:
    """Parse the repository's development-evidence Markdown format.

    Missing values remain explicit as ``unknown`` rather than being inferred.
    """
    if not text.strip():
        raise ValueError("development evidence document is empty")

    metadata = _metadata(text)
    sections = _section_lines(text)
    source_type = metadata.get("source_type", "repository_development_document")
    observed_at = metadata.get("date", metadata.get("observed_at", "unknown"))
    protocol_id = metadata.get("protocol_id", "unknown")
    status = metadata.get("status", "unknown")
    observation_values = _items(sections, "observation", "summary")
    summary = " ".join(observation_values) if observation_values else "unknown"
    claims = observation_values
    verification = _items(sections, "verification evidence", "verification")
    limitations = _items(sections, "boundary", "limitations")
    human_gate = metadata.get("human_gate", "unknown")
    record_id = evidence_id or metadata.get("evidence_id") or source_ref

    return DevelopmentEvidence(
        evidence_id=record_id,
        source_type=source_type,
        source_ref=source_ref,
        observed_at=observed_at,
        protocol_id=protocol_id,
        status=status,
        summary=summary,
        claims=claims,
        verification=verification,
        human_gate=human_gate,
        limitations=limitations,
        provenance=MappingProxyType({"source_ref": source_ref, "parser": "alpha-0.1"}),
    )
