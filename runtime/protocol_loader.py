"""Minimal dependency-free loader for the β0.1 Matome YAML subset.

This is intentionally a small, explicit loader for the Quickstart contract.
It does not attempt to implement the full YAML specification.
"""

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Mapping


class ProtocolLoadError(ValueError):
    """Raised when a Matome Protocol cannot be loaded or validated."""


@dataclass(frozen=True)
class ProtocolIR:
    """Validated Protocol representation consumed by the Runtime bridge."""

    protocol_id: str
    title: str
    version: str
    statement: str
    pipeline: tuple[Mapping[str, str], ...]


def load_matome(path: str | Path) -> ProtocolIR:
    text = Path(path).read_text(encoding="utf-8")
    return parse_matome(text)


def parse_matome(text: str) -> ProtocolIR:
    """Parse the small Matome YAML subset used by the β0.1 Quickstart."""
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines or lines[0].strip() != "matome:":
        raise ProtocolLoadError("root key must be 'matome'")

    title = _scalar(lines, "title")
    version = _scalar(lines, "version")
    statement = _block_scalar(lines, "statement")
    pipeline = _pipeline(lines)

    if not title or not version or not pipeline:
        raise ProtocolLoadError("Protocol requires title, version, and pipeline")

    return ProtocolIR(
        protocol_id=_slug(title),
        title=title,
        version=version,
        statement=statement,
        pipeline=tuple(pipeline),
    )


def _scalar(lines: list[str], key: str) -> str:
    prefix = f"  {key}:"
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix):].strip().strip('"\'')
    raise ProtocolLoadError(f"missing matome.{key}")


def _block_scalar(lines: list[str], key: str) -> str:
    prefix = f"  {key}: >"
    for index, line in enumerate(lines):
        if line == prefix:
            parts: list[str] = []
            for following in lines[index + 1 :]:
                if len(following) - len(following.lstrip()) < 4:
                    break
                parts.append(following.strip())
            if not parts:
                raise ProtocolLoadError(f"empty matome.{key}")
            return " ".join(parts)
    raise ProtocolLoadError(f"missing matome.{key}")


def _pipeline(lines: list[str]) -> list[Mapping[str, str]]:
    items: list[dict[str, str]] = []
    phase: str | None = None
    action: str | None = None
    for line in lines:
        match = re.match(r"\s*-\s*phase:\s*(.+)$", line)
        if match:
            if phase is not None and action is None:
                raise ProtocolLoadError("pipeline item is missing action")
            if phase is not None:
                items.append({"phase": phase, "action": action or ""})
            phase = match.group(1).strip().strip('"\'')
            action = None
            continue
        match = re.match(r"\s+action:\s*(.+)$", line)
        if match and phase is not None:
            action = match.group(1).strip().strip('"\'')
    if phase is not None:
        if action is None:
            raise ProtocolLoadError("pipeline item is missing action")
        items.append({"phase": phase, "action": action})
    if not items:
        raise ProtocolLoadError("pipeline must contain at least one item")
    return items


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", ".", value.lower()).strip(".")
    return slug or "matome.protocol"
