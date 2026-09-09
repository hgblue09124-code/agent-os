"""Architectural constants for the Agent OS foundation.

These values are documentation encoded as data so the package structure
and invariants can be smoke-tested. They are not a runtime.
"""

from __future__ import annotations

FOUNDATION_VERSION = "0.1.0"

ARCHITECTURE_AXIS: tuple[str, ...] = (
    "Kernel/Runtime",
    "Module Contract",
    "Atomic Module",
    "Composition Program",
    "Composed/Meso Module",
    "Skill",
    "Agent",
)

DEPENDENCY_DIRECTION: tuple[str, ...] = (
    "Agent",
    "Skill",
    "Meso Module",
    "Atomic Module",
    "Module Contract",
    "Kernel",
)

MODULE_KINDS: tuple[str, ...] = ("atomic", "meso")

COMPOSITION_STAGES: tuple[str, ...] = (
    "select_modules",
    "validate_contracts",
    "connect_inputs_outputs",
    "validate_dependencies",
    "construct_composed_module",
)

FORBIDDEN_RUNTIME_DEPENDENCIES: tuple[str, ...] = (
    "agent-core",
    "agent-core-next",
    "living-data-ocean",
)

PR01_OUT_OF_SCOPE: tuple[str, ...] = (
    "runtime_engine",
    "llm",
    "memory",
    "planner",
    "tool_system",
)

INVARIANTS: tuple[str, ...] = (
    "I1_single_responsibility",
    "I2_independent_boundary",
    "I3_explicit_contract",
    "I4_determinate_io",
    "I5_explicit_dependencies",
    "I6_independently_testable",
    "I7_no_upward_business_dependency",
    "I8_composition_has_no_business_logic",
    "I9_validate_before_compose",
    "I10_meso_is_a_module",
    "I11_verification_is_part_of_composition",
    "I12_no_decorative_abstraction",
    "I13_no_premature_optimization",
    "I14_no_unneeded_distribution",
    "I15_priority_correctness_first",
    "I16_downward_dependencies_only",
    "I17_no_required_companion_runtime_dependency",
    "I18_pr01_does_not_implement_product_subsystems",
)
