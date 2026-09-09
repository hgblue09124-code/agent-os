from __future__ import annotations

import Module
import Module.Capability
import Module.Contract
import Module.Identity
import Module.Input
import Module.Lifecycle
import Module.Output


def test_module_is_first_class_primitive() -> None:
    assert Module.FIRST_CLASS_PRIMITIVE == "Module"


def test_atomic_and_meso_are_both_modules() -> None:
    assert Module.MODULE_KINDS == ("atomic", "meso")


def test_contract_questions_are_complete() -> None:
    required = {
        "what_is_the_module",
        "identity",
        "capability",
        "input",
        "output",
        "lifecycle",
        "dependencies",
        "verification",
    }
    assert required == set(Module.Contract.CONTRACT_QUESTIONS)


def test_contract_facets_are_implemented() -> None:
    assert Module.Contract.IMPLEMENTED is True
    assert Module.Identity.IMPLEMENTED is True
    assert Module.Capability.IMPLEMENTED is True
    assert Module.Input.IMPLEMENTED is True
    assert Module.Output.IMPLEMENTED is True
    assert Module.Lifecycle.IMPLEMENTED is True
