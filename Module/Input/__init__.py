"""Module input facet."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

BOUNDARY = "module.input"
IMPLEMENTED = True


@dataclass(frozen=True)
class InputBoundary:
    schema: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.schema, dict):
            raise ValueError("Input schema must be a dictionary.")
        for key in self.schema:
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Input schema keys must be non-empty strings.")
