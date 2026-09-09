"""Module primitive.

Atomic Module and Meso Module are both Modules. Meso is a Module
produced by composition, not a separate architectural tier.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, Protocol, runtime_checkable

from Module.Capability import ModuleCapability
from Module.Contract import ModuleContract
from Module.Execution import (
    ExecutionFailure,
    ExecutionRequest,
    ExecutionResult,
    FailureType,
    MinimalModuleExecutor,
    ModuleExecutor,
)
from Module.Identity import ModuleIdentity
from Module.Input import InputBoundary
from Module.Lifecycle import LifecycleState, ModuleLifecycle
from Module.Output import OutputBoundary

MODULE_KINDS = ("atomic", "meso")
FIRST_CLASS_PRIMITIVE = "Module"


@runtime_checkable
class Module(Protocol):
    """Module contract protocol satisfied by both Atomic and Meso modules."""

    @property
    def contract(self) -> ModuleContract:
        ...

    def execute(self, input_payload: Mapping[str, Any]) -> Mapping[str, Any] | ExecutionResult:
        """Explicit single entry point for module execution capability."""
        ...


class AtomicModule:
    """Atomic Module implementation fulfilling ModuleContract."""

    def __init__(
        self,
        contract: ModuleContract,
        handler: Callable[[Mapping[str, Any]], Any] | None = None,
    ) -> None:
        if contract.identity.kind != "atomic":
            raise ValueError(f"AtomicModule requires an atomic contract kind, got '{contract.identity.kind}'.")
        self._contract = contract
        self._handler = handler

    @property
    def contract(self) -> ModuleContract:
        return self._contract

    @property
    def handler(self) -> Callable[[Mapping[str, Any]], Any] | None:
        return self._handler

    def execute(self, input_payload: Mapping[str, Any]) -> Mapping[str, Any] | ExecutionResult:
        if self._handler is None:
            raise NotImplementedError(f"AtomicModule '{self._contract.identity.name}' has no handler defined.")
        return self._handler(input_payload)


class MesoModule:
    """Meso Module (composed module) fulfilling ModuleContract."""

    def __init__(
        self,
        contract: ModuleContract,
        child_modules: tuple[Module, ...] = (),
        handler: Callable[[Mapping[str, Any]], Any] | None = None,
    ) -> None:
        if contract.identity.kind != "meso":
            raise ValueError(f"MesoModule requires a meso contract kind, got '{contract.identity.kind}'.")
        self._contract = contract
        self._child_modules = tuple(child_modules)
        self._handler = handler

    @property
    def contract(self) -> ModuleContract:
        return self._contract

    @property
    def child_modules(self) -> tuple[Module, ...]:
        return self._child_modules

    @property
    def handler(self) -> Callable[[Mapping[str, Any]], Any] | None:
        return self._handler

    def execute(self, input_payload: Mapping[str, Any]) -> Mapping[str, Any] | ExecutionResult:
        if self._handler is None:
            raise NotImplementedError(f"MesoModule '{self._contract.identity.name}' has no execution handler defined.")
        return self._handler(input_payload)


__all__ = [
    "FIRST_CLASS_PRIMITIVE",
    "MODULE_KINDS",
    "AtomicModule",
    "ExecutionFailure",
    "ExecutionRequest",
    "ExecutionResult",
    "FailureType",
    "InputBoundary",
    "LifecycleState",
    "MesoModule",
    "MinimalModuleExecutor",
    "Module",
    "ModuleCapability",
    "ModuleContract",
    "ModuleExecutor",
    "ModuleIdentity",
    "ModuleLifecycle",
    "OutputBoundary",
]
