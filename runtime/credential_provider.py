"""Credential provider boundary for Runtime integrations.

The Runtime receives credentials from an injected provider.  This module does
not persist, log, discover, or interpret secrets; it only defines the boundary
between Runtime code and the operational credential source.
"""

from __future__ import annotations

import os
from typing import Protocol


class CredentialProvider(Protocol):
    """Return a credential for an integration, or an empty string if absent."""

    def get(self) -> str:
        ...


class EnvironmentCredentialProvider:
    """Read a credential from a process environment variable.

    The value is read on demand and is never written to repository files or
    emitted by this module.  The environment is only one implementation of the
    generic CredentialProvider boundary; Runtime code must not depend on it.
    """

    def __init__(self, variable_name: str) -> None:
        if not variable_name:
            raise ValueError("variable_name must not be empty")
        self.variable_name = variable_name

    def get(self) -> str:
        return os.environ.get(self.variable_name, "")


def environment_credential_provider(variable_name: str) -> CredentialProvider:
    """Construct an environment-backed credential provider."""

    return EnvironmentCredentialProvider(variable_name)
