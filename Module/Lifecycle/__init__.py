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


@dataclass
class ModuleLifecycle:
    state: LifecycleState = LifecycleState.CREATED

    def transition_to(self, new_state: LifecycleState | str) -> None:
        if isinstance(new_state, str):
            try:
                new_state = LifecycleState(new_state)
            except ValueError:
                raise ValueError(f"Invalid lifecycle state: '{new_state}'.")
        elif isinstance(new_state, LifecycleState):
            pass
        else:
            raise ValueError(f"Invalid lifecycle state: '{new_state}'.")
        self.state = new_state
