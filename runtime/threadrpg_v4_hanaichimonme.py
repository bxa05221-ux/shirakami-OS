"""Deterministic Hanaichimonme reaction field and dormant ROM population.

This module plans *who might respond*, not what is true or what Icchi should do.
No model calls, Reality mutation, or human decision authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256


def _unit(seed: str) -> float:
    return int(sha256(seed.encode("utf-8")).hexdigest()[:12], 16) / (16 ** 12 - 1)


@dataclass(frozen=True)
class Axis:
    center: int = 50
    dispersion: int = 30

    def __post_init__(self):
        if any(type(v) is not int or not 0 <= v <= 100 for v in (self.center, self.dispersion)):
            raise ValueError("center and dispersion must be integers in [0, 100]")

    def sample(self, seed: str) -> int:
        # Dispersion is a bounded deviation, not a forced disagreement.
        return round(max(0, min(100, self.center + (2 * _unit(seed) - 1) * self.dispersion)))


@dataclass(frozen=True)
class Field:
    content: Axis = Axis()
    personality: Axis = Axis()
    crowd: Axis = Axis()


@dataclass(frozen=True)
class Resident:
    participant_id: str
    interest: str
    persistent: bool = True


@dataclass(frozen=True)
class Reaction:
    participant_id: str
    content: int
    personality: int
    participation: int
    speaks: bool


@dataclass(frozen=True)
class ReactionField:
    thread_id: str
    post_index: int
    residents: tuple[Reaction, ...]
    rom_population: int
    rom_visitors: tuple[str, ...]


def plan_reactions(
    thread_id: str,
    post_index: int,
    field: Field = Field(),
    dormant: tuple[Resident, ...] = (),
) -> ReactionField:
    """Generate seven distinct response tendencies and optional ROM arrivals.

    Dormant residents are kept distinct from seven core speakers. ROM arrivals
    are only candidates; no synthetic speech or authority is created here.
    """
    if not thread_id or type(post_index) is not int or post_index < 0:
        raise ValueError("thread_id and nonnegative post_index required")
    if not isinstance(field, Field):
        raise TypeError("field must be Field")
    if len({r.participant_id for r in dormant}) != len(dormant):
        raise ValueError("ROM participant IDs must be unique")
    seed = f"{thread_id}:{post_index}"
    reactions = []
    for i in range(7):
        pid = f"nanashi-{i + 1}"
        key = f"{seed}:{pid}"
        participation = field.crowd.sample(key + ":crowd")
        reactions.append(Reaction(
            participant_id=pid,
            content=field.content.sample(key + ":content"),
            personality=field.personality.sample(key + ":personality"),
            participation=participation,
            speaks=_unit(key + ":speak") * 100 < participation,
        ))
    # Crowd size is virtual and does not create posts or impersonate people.
    rom_population = round(field.crowd.center * 2)
    visitors = tuple(
        r.participant_id for r in dormant
        if _unit(f"{seed}:{r.participant_id}:arrival") * 100 < field.crowd.center / 5
    )
    return ReactionField(thread_id, post_index, tuple(reactions), rom_population, visitors)
