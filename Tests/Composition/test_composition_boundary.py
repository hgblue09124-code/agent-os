from __future__ import annotations

import Composition
import Composition.Graph
import Composition.Program
from Kernel.foundation import COMPOSITION_STAGES


def test_composition_program_is_a_primitive() -> None:
    assert Composition.PRIMITIVE == "Composition Program"


def test_composition_stages_match_architecture() -> None:
    assert Composition.Program.STAGES == COMPOSITION_STAGES
    assert Composition.Program.STAGES[0] == "select_modules"
    assert Composition.Program.STAGES[-1] == "construct_composed_module"


def test_composition_is_reserved() -> None:
    assert Composition.Program.IMPLEMENTED is False
    assert Composition.Graph.IMPLEMENTED is False
