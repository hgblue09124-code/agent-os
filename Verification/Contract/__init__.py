"""Module contract local verification facet."""

from __future__ import annotations

from dataclasses import dataclass

from Module.Contract import ModuleContract

BOUNDARY = "verification.contract"
IMPLEMENTED = True


@dataclass(frozen=True)
class ContractVerificationResult:
    is_valid: bool
    errors: tuple[str, ...] = ()


def verify_module_contract(contract: ModuleContract) -> ContractVerificationResult:
    """Perform local verification on a ModuleContract."""
    if not isinstance(contract, ModuleContract):
        return ContractVerificationResult(is_valid=False, errors=("Contract is not a ModuleContract instance.",))

    errors: list[str] = []

    try:
        if not contract.identity.name or not contract.identity.version:
            errors.append("Invalid identity name or version.")
        if not contract.capability.responsibility:
            errors.append("Invalid capability responsibility.")
    except Exception as exc:
        errors.append(f"Verification error: {exc}")

    return ContractVerificationResult(
        is_valid=len(errors) == 0,
        errors=tuple(errors),
    )
