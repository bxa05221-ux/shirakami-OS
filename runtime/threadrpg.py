"""ThreadRPG reference-form state engine.

This module implements the protocol boundary, not an AI persona system.
It preserves observations over time, holds unresolved questions, supports
revisit/rainwater transitions, and leaves Catch authority with the human.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True)
class ThreadObservation:
    observation_id: str
    viewpoint: int
    content: str
    created_at: str
    context: Mapping[str, Any] = field(default_factory=dict)
    revisit_of: str | None = None


@dataclass(frozen=True)
class UnresolvedQuestion:
    question_id: str
    text: str
    source_observation_id: str
    created_at: str
    resolved: bool = False


@dataclass(frozen=True)
class HumanCatch:
    catch_id: str
    question_id: str | None
    observation_ids: tuple[str, ...]
    declaration: str
    created_at: str
    authority: str = "human"


class ThreadRPG:
    """Provider-neutral executable state boundary for ThreadRPG."""

    VIEWPOINT_COUNT = 7

    def __init__(self, landscape: Mapping[str, Any] | None = None) -> None:
        self.landscape: dict[str, Any] = dict(landscape or {})
        self.observations: list[ThreadObservation] = []
        self.unresolved_questions: list[UnresolvedQuestion] = []
        self.rainwater_mode: bool = False
        self.catches: list[HumanCatch] = []

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _id(prefix: str) -> str:
        return f"{prefix}_{uuid4().hex}"

    def observe(
        self,
        viewpoint: int,
        content: str,
        *,
        context: Mapping[str, Any] | None = None,
        revisit_of: str | None = None,
    ) -> ThreadObservation:
        if not isinstance(viewpoint, int) or not 1 <= viewpoint <= self.VIEWPOINT_COUNT:
            raise ValueError("viewpoint must be an integer from 1 to 7")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("content must be a non-empty string")
        if revisit_of is not None and not any(
            item.observation_id == revisit_of for item in self.observations
        ):
            raise ValueError("revisit_of must reference an existing observation")

        observation = ThreadObservation(
            observation_id=self._id("obs"),
            viewpoint=viewpoint,
            content=content,
            created_at=self._now(),
            context=dict(context or {}),
            revisit_of=revisit_of,
        )
        self.observations.append(observation)
        return observation

    def hold_question(
        self,
        text: str,
        *,
        source_observation_id: str,
    ) -> UnresolvedQuestion:
        if not any(
            item.observation_id == source_observation_id
            for item in self.observations
        ):
            raise ValueError("source_observation_id must reference an observation")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")

        question = UnresolvedQuestion(
            question_id=self._id("q"),
            text=text,
            source_observation_id=source_observation_id,
            created_at=self._now(),
        )
        self.unresolved_questions.append(question)
        return question

    def revisit(
        self,
        question_id: str,
        *,
        viewpoint: int,
        content: str,
        context: Mapping[str, Any] | None = None,
    ) -> ThreadObservation:
        question = self._get_question(question_id)
        if question.resolved:
            raise ValueError("resolved questions cannot be revisited")
        return self.observe(
            viewpoint,
            content,
            context=context,
            revisit_of=question.source_observation_id,
        )

    def enable_rainwater_mode(self) -> None:
        self.rainwater_mode = True

    def disable_rainwater_mode(self) -> None:
        self.rainwater_mode = False

    def rainwater_targets(self) -> tuple[str, ...]:
        """Return unresolved questions that rainwater mode puts back into circulation."""
        if not self.rainwater_mode:
            return ()
        return tuple(
            question.question_id
            for question in self.unresolved_questions
            if not question.resolved
        )

    def observation_connections(self, question_id: str) -> tuple[str, ...]:
        """Return observations connected to a held question without resolving it."""
        question = self._get_question(question_id)
        return tuple(
            observation.observation_id
            for observation in self.observations
            if observation.observation_id == question.source_observation_id
            or observation.revisit_of == question.source_observation_id
        )

    def declare_catch(
        self,
        declaration: str,
        *,
        question_id: str | None = None,
        observation_ids: tuple[str, ...] | list[str] = (),
        authority: str = "human",
    ) -> HumanCatch:
        if authority != "human":
            raise PermissionError("Catch authority is human-only")
        if not isinstance(declaration, str) or not declaration.strip():
            raise ValueError("declaration must be a non-empty string")
        known = {item.observation_id for item in self.observations}
        if any(item not in known for item in observation_ids):
            raise ValueError("observation_ids must reference existing observations")
        if question_id is not None:
            self._get_question(question_id)

        catch = HumanCatch(
            catch_id=self._id("catch"),
            question_id=question_id,
            observation_ids=tuple(observation_ids),
            declaration=declaration,
            created_at=self._now(),
        )
        self.catches.append(catch)
        return catch

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "landscape": dict(self.landscape),
            "observations": [
                {
                    "observation_id": item.observation_id,
                    "viewpoint": item.viewpoint,
                    "content": item.content,
                    "created_at": item.created_at,
                    "context": dict(item.context),
                    "revisit_of": item.revisit_of,
                }
                for item in self.observations
            ],
            "unresolved_questions": [
                {
                    "question_id": item.question_id,
                    "text": item.text,
                    "source_observation_id": item.source_observation_id,
                    "created_at": item.created_at,
                    "resolved": item.resolved,
                }
                for item in self.unresolved_questions
            ],
            "rainwater_mode": self.rainwater_mode,
            "catches": [
                {
                    "catch_id": item.catch_id,
                    "question_id": item.question_id,
                    "observation_ids": list(item.observation_ids),
                    "declaration": item.declaration,
                    "created_at": item.created_at,
                    "authority": item.authority,
                }
                for item in self.catches
            ],
        }

    def _get_question(self, question_id: str) -> UnresolvedQuestion:
        for question in self.unresolved_questions:
            if question.question_id == question_id:
                return question
        raise ValueError("unknown question_id")
