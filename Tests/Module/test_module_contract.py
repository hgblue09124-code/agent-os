from __future__ import annotations

import sys
import pytest

from Module import (
    AtomicModule,
    InputBoundary,
    LifecycleState,
    MesoModule,
    Module,
    ModuleCapability,
    ModuleContract,
    ModuleIdentity,
    ModuleLifecycle,
    OutputBoundary,
)
from Verification.Contract import verify_module_contract, ContractVerificationResult


def test_valid_module_contract_construction() -> None:
    identity = ModuleIdentity(name="text_cleaner", version="1.0.0", kind="atomic")
    capability = ModuleCapability(
        responsibility="Clean raw text strings by stripping whitespace and control characters.",
        tags=("text", "cleaning"),
    )
    input_b = InputBoundary(schema={"raw_text": str})
    output_b = OutputBoundary(schema={"clean_text": str})
    dependencies = ("logger_module",)
    lifecycle = ModuleLifecycle(state=LifecycleState.CREATED)

    contract = ModuleContract(
        identity=identity,
        capability=capability,
        input_boundary=input_b,
        output_boundary=output_b,
        dependencies=dependencies,
        lifecycle=lifecycle,
    )

    assert contract.identity == identity
    assert contract.capability == capability
    assert contract.input_boundary == input_b
    assert contract.output_boundary == output_b
    assert contract.dependencies == ("logger_module",)
    assert contract.lifecycle == lifecycle


def test_identity_is_explicit() -> None:
    identity = ModuleIdentity(name="data_parser", version="2.1.0", kind="atomic")
    assert identity.name == "data_parser"
    assert identity.version == "2.1.0"
    assert identity.kind == "atomic"


def test_capability_is_explicit() -> None:
    capability = ModuleCapability(
        responsibility="Parse JSON payload into structured dictionaries.",
        tags=("parser", "json"),
    )
    assert capability.responsibility == "Parse JSON payload into structured dictionaries."
    assert capability.tags == ("parser", "json")


def test_input_and_output_boundaries_are_explicit() -> None:
    in_b = InputBoundary(schema={"payload": bytes, "encoding": str})
    out_b = OutputBoundary(schema={"parsed_dict": dict})

    assert in_b.schema == {"payload": bytes, "encoding": str}
    assert out_b.schema == {"parsed_dict": dict}


def test_dependencies_are_explicit() -> None:
    deps = ("crypto_provider", "auth_verifier")
    identity = ModuleIdentity(name="secure_vault", version="1.0.0", kind="atomic")
    capability = ModuleCapability(responsibility="Store sensitive credentials safely.")
    contract = ModuleContract(
        identity=identity,
        capability=capability,
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
        dependencies=deps,
    )
    assert contract.dependencies == ("crypto_provider", "auth_verifier")


def test_lifecycle_is_explicit() -> None:
    lifecycle = ModuleLifecycle(state=LifecycleState.CREATED)
    assert lifecycle.state == LifecycleState.CREATED

    lifecycle.transition_to(LifecycleState.INITIALIZED)
    assert lifecycle.state == LifecycleState.INITIALIZED

    lifecycle.transition_to("running")
    assert lifecycle.state == LifecycleState.RUNNING

    with pytest.raises(ValueError, match="Invalid lifecycle state"):
        lifecycle.transition_to("non_existent_state")


def test_invalid_contract_state_is_rejected_deterministically() -> None:
    # Invalid identity name
    with pytest.raises(ValueError, match="Module name must be a non-empty string."):
        ModuleIdentity(name="", version="1.0.0")

    # Invalid identity version
    with pytest.raises(ValueError, match="Module version must be a non-empty string."):
        ModuleIdentity(name="valid_name", version="  ")

    # Invalid identity kind
    with pytest.raises(ValueError, match="Module kind must be one of"):
        ModuleIdentity(name="valid_name", version="1.0.0", kind="invalid_kind")

    # Invalid capability responsibility
    with pytest.raises(ValueError, match="Module responsibility must be a non-empty string."):
        ModuleCapability(responsibility="")

    # Invalid input schema key
    with pytest.raises(ValueError, match="Input schema keys must be non-empty strings."):
        InputBoundary(schema={"": str})

    # Invalid output schema key
    with pytest.raises(ValueError, match="Output schema keys must be non-empty strings."):
        OutputBoundary(schema={" ": str})

    # Invalid dependency item
    with pytest.raises(ValueError, match="Dependency names must be non-empty strings."):
        ModuleContract(
            identity=ModuleIdentity(name="mod", version="1.0.0"),
            capability=ModuleCapability(responsibility="resp"),
            input_boundary=InputBoundary(),
            output_boundary=OutputBoundary(),
            dependencies=("",),
        )


def test_atomic_module_satisfies_contract() -> None:
    identity = ModuleIdentity(name="atomic_node", version="1.0.0", kind="atomic")
    capability = ModuleCapability(responsibility="Perform single atomic operation.")
    contract = ModuleContract(
        identity=identity,
        capability=capability,
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )

    atomic_mod = AtomicModule(contract=contract)

    assert isinstance(atomic_mod, Module)
    assert atomic_mod.contract == contract

    # Reject atomic module with meso contract kind
    meso_contract = ModuleContract(
        identity=ModuleIdentity(name="meso_node", version="1.0.0", kind="meso"),
        capability=capability,
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )
    with pytest.raises(ValueError, match="AtomicModule requires an atomic contract kind"):
        AtomicModule(contract=meso_contract)


def test_meso_module_satisfies_contract() -> None:
    atomic_identity = ModuleIdentity(name="child_node", version="1.0.0", kind="atomic")
    atomic_contract = ModuleContract(
        identity=atomic_identity,
        capability=ModuleCapability(responsibility="Subtask"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )
    child_mod = AtomicModule(contract=atomic_contract)

    meso_identity = ModuleIdentity(name="composite_pipeline", version="1.0.0", kind="meso")
    meso_contract = ModuleContract(
        identity=meso_identity,
        capability=ModuleCapability(responsibility="Composed pipeline execution."),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
        dependencies=("child_node",),
    )

    meso_mod = MesoModule(contract=meso_contract, child_modules=(child_mod,))

    assert isinstance(meso_mod, Module)
    assert meso_mod.contract == meso_contract
    assert meso_mod.child_modules == (child_mod,)

    # Reject meso module with atomic contract kind
    with pytest.raises(ValueError, match="MesoModule requires a meso contract kind"):
        MesoModule(contract=atomic_contract)


def test_no_companion_repository_imported() -> None:
    forbidden_modules = ("agent-core", "agent-core-next", "living-data-ocean")
    for loaded_mod in sys.modules:
        for forbidden in forbidden_modules:
            assert forbidden not in loaded_mod, f"Forbidden module {forbidden} found in sys.modules!"


def test_local_contract_verification() -> None:
    identity = ModuleIdentity(name="verified_mod", version="1.0.0", kind="atomic")
    capability = ModuleCapability(responsibility="Valid responsibility.")
    contract = ModuleContract(
        identity=identity,
        capability=capability,
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )

    res: ContractVerificationResult = verify_module_contract(contract)
    assert res.is_valid is True
    assert res.errors == ()
