from __future__ import annotations

from pathlib import Path

from Kernel.foundation import INVARIANTS


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_PATHS = (
    "README.md",
    "pyproject.toml",
    ".gitignore",
    "Kernel/__init__.py",
    "Kernel/Runtime/__init__.py",
    "Module/__init__.py",
    "Module/Contract/__init__.py",
    "Module/Identity/__init__.py",
    "Module/Capability/__init__.py",
    "Module/Input/__init__.py",
    "Module/Output/__init__.py",
    "Module/Lifecycle/__init__.py",
    "Composition/__init__.py",
    "Composition/Program/__init__.py",
    "Composition/Graph/__init__.py",
    "Verification/__init__.py",
    "Verification/Contract/__init__.py",
    "Verification/Composition/__init__.py",
    "Tests/Kernel/test_foundation.py",
    "Tests/Module/test_module_boundary.py",
    "Tests/Composition/test_composition_boundary.py",
    "Tests/Verification/test_verification_boundary.py",
    "Documentation/Architecture/ARCHITECTURE.md",
    "Documentation/Architecture/INVARIANTS.md",
    "Documentation/Architecture/DEPENDENCY.md",
    "Documentation/Contracts/CONTRACT_BOUNDARY.md",
    "Documentation/Roadmap/ROADMAP.md",
    "Documentation/Research/RESEARCH_DIRECTION.md",
)


def test_required_foundation_paths_exist() -> None:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    assert missing == []


def test_readme_states_canonical_role_and_companions() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "canonical Agent OS architecture" in text.lower() or "Canonical Agent OS" in text
    assert "agent-core" in text
    assert "agent-core-next" in text
    assert "living-data-ocean" in text
    assert "no required runtime dependency" in text.lower()


def test_invariants_are_enumerated() -> None:
    assert len(INVARIANTS) == 18
    document = (ROOT / "Documentation/Architecture/INVARIANTS.md").read_text(encoding="utf-8")
    for index in range(1, 19):
        assert f"I{index}." in document
