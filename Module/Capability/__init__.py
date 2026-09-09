"""Module capability facet."""

from __future__ import annotations

from dataclasses import dataclass, field

BOUNDARY = "module.capability"
IMPLEMENTED = True


@dataclass(frozen=True)
class ModuleCapability:
    responsibility: str
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.responsibility, str) or not self.responsibility.strip():
            raise ValueError("Module responsibility must be a non-empty string.")
        if not isinstance(self.tags, (tuple, list)):
            raise ValueError("Module tags must be a tuple or list of strings.")
        if isinstance(self.tags, list):
            object.__setattr__(self, "tags", tuple(self.tags))
        for tag in self.tags:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError("Tag must be a non-empty string.")
