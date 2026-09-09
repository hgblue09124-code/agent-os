"""Module identity facet."""

from __future__ import annotations

from dataclasses import dataclass

BOUNDARY = "module.identity"
IMPLEMENTED = True
VALID_KINDS = ("atomic", "meso")


@dataclass(frozen=True)
class ModuleIdentity:
    name: str
    version: str
    kind: str = "atomic"

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Module name must be a non-empty string.")
        if not isinstance(self.version, str) or not self.version.strip():
            raise ValueError("Module version must be a non-empty string.")
        if self.kind not in VALID_KINDS:
            raise ValueError(f"Module kind must be one of {VALID_KINDS}, got '{self.kind}'.")
