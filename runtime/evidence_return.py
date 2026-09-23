"""Compatibility facade for the Runtime Evidence return boundary.

The canonical backend conversion lives in ``evidence_return_backend``.
This module preserves the historical import path while keeping the
Backend -> Evidence responsibility unchanged.
"""

from .evidence_return_backend import evidence_from_backend_response

__all__ = ["evidence_from_backend_response"]
