from __future__ import annotations

from pathlib import Path

import Kernel
from Kernel import foundation
from Kernel.Runtime import IMPLEMENTED as RUNTIME_IMPLEMENTED


ROOT = Path(__file__).resolve().parents[2]


def test_kernel_package_imports() -> None:
    assert Kernel.FOUNDATION_VERSION == "0.1.0"
    assert foundation.FOUNDATION_VERSION == Kernel.FOUNDATION_VERSION


def test_architecture_axis_order() -> None:
    assert foundation.ARCHITECTURE_AXIS[0] == "Kernel/Runtime"
    assert foundation.ARCHITECTURE_AXIS[-1] == "Agent"
    assert "Module Contract" in foundation.ARCHITECTURE_AXIS
    assert "Composition Program" in foundation.ARCHITECTURE_AXIS
    assert "Composed/Meso Module" in foundation.ARCHITECTURE_AXIS


def test_runtime_is_reserved_not_implemented() -> None:
    assert RUNTIME_IMPLEMENTED is False


def test_pr01_does_not_ship_product_subsystems() -> None:
    forbidden_filenames = {
        "llm.py",
        "memory.py",
        "planner.py",
        "tools.py",
        "agent.py",
        "runtime_engine.py",
    }
    shipped = {path.name.lower() for path in ROOT.rglob("*.py")}
    assert forbidden_filenames.isdisjoint(shipped)


def test_no_companion_runtime_dependency_declared() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for name in foundation.FORBIDDEN_RUNTIME_DEPENDENCIES:
        assert name not in pyproject
