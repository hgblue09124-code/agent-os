"""Module Contract facet."""

from __future__ import annotations

from dataclasses import dataclass, field

from Module.Capability import ModuleCapability
from Module.Identity import ModuleIdentity
from Module.Input import InputBoundary
from Module.Lifecycle import ModuleLifecycle
from Module.Output import OutputBoundary

BOUNDARY = "module.contract"
IMPLEMENTED = True

CONTRACT_QUESTIONS: tuple[str, ...] = (
    "what_is_the_module",
    "identity",
    "capability",
    "input",
    "output",
    "lifecycle",
    "dependencies",
    "verification",
)


@dataclass(frozen=True)
class ModuleContract:
    identity: ModuleIdentity
    capability: ModuleCapability
    input_boundary: InputBoundary
    output_boundary: OutputBoundary
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    lifecycle: ModuleLifecycle = field(default_factory=ModuleLifecycle)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, ModuleIdentity):
            raise ValueError("identity must be a valid ModuleIdentity instance.")
        if not isinstance(self.capability, ModuleCapability):
            raise ValueError("capability must be a valid ModuleCapability instance.")
        if not isinstance(self.input_boundary, InputBoundary):
            raise ValueError("input_boundary must be a valid InputBoundary instance.")
        if not isinstance(self.output_boundary, OutputBoundary):
            raise ValueError("output_boundary must be a valid OutputBoundary instance.")
        if not isinstance(self.dependencies, (tuple, list)):
            raise ValueError("dependencies must be a tuple or list of strings.")
        if isinstance(self.dependencies, list):
            object.__setattr__(self, "dependencies", tuple(self.dependencies))
        for dep in self.dependencies:
            if not isinstance(dep, str) or not dep.strip():
                raise ValueError("Dependency names must be non-empty strings.")
        if not isinstance(self.lifecycle, ModuleLifecycle):
            raise ValueError("lifecycle must be a valid ModuleLifecycle instance.")
