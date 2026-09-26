"""Shirakami Thread Runtime v0.1.

Minimal dependency-free execution boundary for Shirakami Thread Protocol v0.1.
The runtime records Posts and emits observations; it does not infer psychology,
assign Evidence status, or make decisions for the user.
"""

from dataclasses import dataclass, field
from time import monotonic
from typing import Any, Mapping
from uuid import uuid4

MODES = frozenset({"Normal", "CoolDown", "Silence"})
AUTHORS = frozenset({"User", "Shirakami"})


@dataclass(frozen=True)
class ThreadPost:
    id: str
    author: str
    content: str
    mode: str = "Normal"
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ThreadObservation:
    kind: str
    data: Mapping[str, Any]


class ThreadRuntime:
    """Stateful, provider-neutral Thread Protocol runtime."""

    def __init__(self, *, max_posts: int | None = None, max_seconds: float | None = None) -> None:
        if max_posts is not None and (not isinstance(max_posts, int) or max_posts < 1):
            raise ValueError("max_posts must be an integer >= 1 or None")
        if max_seconds is not None and (not isinstance(max_seconds, (int, float)) or max_seconds < 0):
            raise ValueError("max_seconds must be >= 0 or None")
        self.max_posts = max_posts
        self.max_seconds = max_seconds
        self._started_at: float | None = None
        self._posts: list[ThreadPost] = []
        self._mode = "Normal"
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def posts(self) -> tuple[ThreadPost, ...]:
        return tuple(self._posts)

    def start(self) -> ThreadObservation:
        if self._started_at is not None:
            raise RuntimeError("thread already started")
        self._started_at = monotonic()
        return ThreadObservation(
            "thread.started",
            {"protocol": "Shirakami Thread Protocol", "version": "0.1"},
        )

    def append_post(self, author: str, content: str, *, mode: str | None = None,
                    post_id: str | None = None,
                    metadata: Mapping[str, Any] | None = None) -> ThreadObservation:
        self._ensure_started()
        if self._closed:
            raise RuntimeError("thread is closed")
        if author not in AUTHORS:
            raise ValueError("author must be User or Shirakami")
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        selected_mode = mode or self._mode
        if selected_mode not in MODES:
            raise ValueError("mode must be Normal, CoolDown, or Silence")

        post = ThreadPost(
            id=post_id or str(uuid4()),
            author=author,
            content=content,
            mode=selected_mode,
            metadata=dict(metadata or {}),
        )
        self._posts.append(post)
        self._mode = selected_mode

        observation = ThreadObservation(
            "thread.post.appended",
            {"post_id": post.id, "author": post.author, "mode": post.mode,
             "content_length": len(post.content), "post_count": len(self._posts)},
        )
        if self._should_close():
            self.close(reason="limit")
        return observation

    def transition_mode(self, mode: str) -> ThreadObservation:
        self._ensure_started()
        if self._closed:
            raise RuntimeError("thread is closed")
        if mode not in MODES:
            raise ValueError("mode must be Normal, CoolDown, or Silence")
        previous = self._mode
        self._mode = mode
        return ThreadObservation("thread.mode.transitioned", {"from": previous, "to": mode})

    def close(self, *, reason: str = "user") -> ThreadObservation:
        self._ensure_started()
        if self._closed:
            return ThreadObservation("thread.close.already_closed", {"reason": reason})
        self._closed = True
        return ThreadObservation(
            "thread.closed",
            {"reason": reason, "post_count": len(self._posts), "mode": self._mode},
        )

    def snapshot(self) -> Mapping[str, Any]:
        """Return Runtime state as an Observation-shaped, non-Evidence output."""
        self._ensure_started()
        return {
            "protocol": "Shirakami Thread Protocol",
            "version": "0.1",
            "state": "closed" if self._closed else "active",
            "mode": self._mode,
            "post_count": len(self._posts),
            "posts": [
                {"id": p.id, "author": p.author, "content": p.content,
                 "mode": p.mode, "metadata": dict(p.metadata)}
                for p in self._posts
            ],
        }

    def _ensure_started(self) -> None:
        if self._started_at is None:
            raise RuntimeError("thread has not been started")

    def _should_close(self) -> bool:
        if self.max_posts is not None and len(self._posts) >= self.max_posts:
            return True
        if self.max_seconds is not None and self._started_at is not None:
            return monotonic() - self._started_at >= self.max_seconds
        return False
