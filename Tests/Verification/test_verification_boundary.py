from __future__ import annotations

import Verification
import Verification.Composition
import Verification.Contract


def test_verification_has_local_and_compositional_boundaries() -> None:
    assert Verification.VERIFICATION_KINDS == ("contract", "composition")
    assert Verification.Contract.IMPLEMENTED is False
    assert Verification.Composition.IMPLEMENTED is False
