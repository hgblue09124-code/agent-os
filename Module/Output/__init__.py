"""Module output facet."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

BOUNDARY = "module.output"
IMPLEMENTED = True


@dataclass(frozen=True)
class OutputBoundary:
    schema: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.schema, dict):
            raise ValueError("Output schema must be a dictionary.")
        for key in self.schema:
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Output schema keys must be non-empty strings.")
