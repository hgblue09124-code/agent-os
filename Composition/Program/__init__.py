"""Composition Program boundary.

Stages are declared for later implementation (PR-04).
No composer is implemented in PR-01.
"""

BOUNDARY = "composition.program"
IMPLEMENTED = False

STAGES: tuple[str, ...] = (
    "select_modules",
    "validate_contracts",
    "connect_inputs_outputs",
    "validate_dependencies",
    "construct_composed_module",
)
