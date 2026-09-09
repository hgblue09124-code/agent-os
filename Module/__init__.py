"""Module primitive.

Atomic Module and Meso Module are both Modules. Meso is a Module
produced by composition, not a separate architectural tier.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from Module.Capability import ModuleCapability
from Module.Contract import ModuleContract
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


class AtomicModule:
    """Atomic Module implementation fulfilling ModuleContract."""

    def __init__(self, contract: ModuleContract) -> None:
        if contract.identity.kind != "atomic":
            raise ValueError(f"AtomicModule requires an atomic contract kind, got '{contract.identity.kind}'.")
        self._contract = contract

    @property
    def contract(self) -> ModuleContract:
        return self._contract


class MesoModule:
    """Meso Module (composed module) fulfilling ModuleContract."""

    def __init__(self, contract: ModuleContract, child_modules: tuple[Module, ...] = ()) -> None:
        if contract.identity.kind != "meso":
            raise ValueError(f"MesoModule requires a meso contract kind, got '{contract.identity.kind}'.")
        self._contract = contract
        self._child_modules = tuple(child_modules)

    @property
    def contract(self) -> ModuleContract:
        return self._contract

    @property
    def child_modules(self) -> tuple[Module, ...]:
        return self._child_modules


__all__ = [
    "FIRST_CLASS_PRIMITIVE",
    "MODULE_KINDS",
    "AtomicModule",
    "InputBoundary",
    "LifecycleState",
    "MesoModule",
    "Module",
    "ModuleCapability",
    "ModuleContract",
    "ModuleIdentity",
    "ModuleLifecycle",
    "OutputBoundary",
]
