"""Minimal Project Source Registry boundary for Shirakami OS."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

ACTIVE_STATUSES = frozenset({"active", "implementation_handoff", "implemented", "verified"})
SOURCE_TYPE_ORDER = (
    "matome_yaml",
    "design",
    "blueprint",
    "constitution",
    "vision",
    "implementation",
    "experiment",
    "evidence",
)
REQUIRED_FIELDS = frozenset({"id", "type", "path", "status", "authority"})


@dataclass(frozen=True)
class SourceRef:
    id: str
    type: str
    path: str
    status: str
    authority: str
    requested_context: object | None = None


def parse_source_ref(raw: Mapping[str, object]) -> SourceRef:
    missing = REQUIRED_FIELDS.difference(raw)
    if missing:
        raise ValueError(f"missing source fields: {', '.join(sorted(missing))}")
    return SourceRef(
        id=str(raw["id"]),
        type=str(raw["type"]),
        path=str(raw["path"]),
        status=str(raw["status"]),
        authority=str(raw["authority"]),
        requested_context=raw.get("requested_context"),
    )


def build_registry(raw_sources: Iterable[Mapping[str, object]]) -> tuple[SourceRef, ...]:
    """Validate and order declared source references without resolving conflicts."""
    refs = tuple(parse_source_ref(item) for item in raw_sources)
    ids = [ref.id for ref in refs]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        raise ValueError(f"duplicate source ids: {', '.join(duplicates)}")
    order = {kind: index for index, kind in enumerate(SOURCE_TYPE_ORDER)}
    return tuple(sorted(refs, key=lambda ref: (order.get(ref.type, len(order)), ref.id)))
