"""Module output facet."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

BOUNDARY = "module.output"
IMPLEMENTED = True


@dataclass(frozen=True)
class OutputBoundary:
    schema: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.schema, (dict, MappingProxyType)):
            raise ValueError("Output schema must be a mapping/dictionary.")
        schema_dict = dict(self.schema)
        for key in schema_dict:
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Output schema keys must be non-empty strings.")
        object.__setattr__(self, "schema", MappingProxyType(schema_dict))
