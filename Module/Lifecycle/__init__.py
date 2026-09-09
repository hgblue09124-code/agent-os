"""Module lifecycle facet."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

BOUNDARY = "module.lifecycle"
IMPLEMENTED = True


class LifecycleState(str, Enum):
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(frozen=True)
class ModuleLifecycle:
    state: LifecycleState = LifecycleState.CREATED

    def __post_init__(self) -> None:
        if isinstance(self.state, str) and not isinstance(self.state, LifecycleState):
            try:
                object.__setattr__(self, "state", LifecycleState(self.state))
            except ValueError:
                raise ValueError(f"Invalid lifecycle state: '{self.state}'.")
        elif not isinstance(self.state, LifecycleState):
            raise ValueError(f"Invalid lifecycle state: '{self.state}'.")

    def with_state(self, new_state: LifecycleState | str) -> ModuleLifecycle:
        """Returns a new ModuleLifecycle instance with the updated state (value-oriented)."""
        return ModuleLifecycle(state=new_state)
