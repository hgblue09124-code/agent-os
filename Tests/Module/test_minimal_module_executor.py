from __future__ import annotations

import sys
import pytest

from Module import (
    AtomicModule,
    ExecutionFailure,
    ExecutionRequest,
    ExecutionResult,
    FailureType,
    InputBoundary,
    MesoModule,
    MinimalModuleExecutor,
    Module,
    ModuleCapability,
    ModuleContract,
    ModuleExecutor,
    ModuleIdentity,
    OutputBoundary,
)


def test_minimal_module_executor_satisfies_protocol() -> None:
    executor = MinimalModuleExecutor()
    assert isinstance(executor, ModuleExecutor)


def test_minimal_module_executor_atomic_module_success() -> None:
    executor = MinimalModuleExecutor()

    identity = ModuleIdentity(name="stripper", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=identity,
        capability=ModuleCapability(responsibility="Strip whitespace"),
        input_boundary=InputBoundary(schema={"text": str}),
        output_boundary=OutputBoundary(schema={"clean": str}),
    )

    atomic_mod = AtomicModule(
        contract=contract,
        handler=lambda payload: {"clean": payload["text"].strip()},
    )

    req = ExecutionRequest(target_identity=identity, input_payload={"text": "  hello  "})
    res = executor.execute(atomic_mod, req)

    assert res.is_success is True
    assert res.output_payload["clean"] == "hello"
    assert res.failure is None

    # Input payload remains unmutated
    assert req.input_payload["text"] == "  hello  "


def test_minimal_module_executor_meso_module_success() -> None:
    executor = MinimalModuleExecutor()

    child_identity = ModuleIdentity(name="child", version="1.0.0", kind="atomic")
    child_mod = AtomicModule(
        contract=ModuleContract(
            identity=child_identity,
            capability=ModuleCapability(responsibility="Child task"),
            input_boundary=InputBoundary(),
            output_boundary=OutputBoundary(),
        )
    )

    meso_identity = ModuleIdentity(name="pipeline", version="1.0.0", kind="meso")
    meso_contract = ModuleContract(
        identity=meso_identity,
        capability=ModuleCapability(responsibility="Pipeline task"),
        input_boundary=InputBoundary(schema={"a": int, "b": int}),
        output_boundary=OutputBoundary(schema={"sum": int}),
        dependencies=("child",),
    )

    meso_mod = MesoModule(
        contract=meso_contract,
        child_modules=(child_mod,),
        handler=lambda payload: {"sum": payload["a"] + payload["b"]},
    )

    req = ExecutionRequest(target_identity=meso_identity, input_payload={"a": 10, "b": 20})
    res = executor.execute(meso_mod, req)

    assert res.is_success is True
    assert res.output_payload["sum"] == 30


def test_minimal_module_executor_explicit_execution_entry_point_used() -> None:
    called_execute = False

    class ExplicitCustomModule:
        def __init__(self, contract: ModuleContract) -> None:
            self._contract = contract

        @property
        def contract(self) -> ModuleContract:
            return self._contract

        def execute(self, input_payload):
            nonlocal called_execute
            called_execute = True
            return {"result": "explicit"}

    identity = ModuleIdentity(name="explicit_mod", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=identity,
        capability=ModuleCapability(responsibility="Explicit task"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )

    custom_mod = ExplicitCustomModule(contract)
    req = ExecutionRequest(target_identity=identity)
    executor = MinimalModuleExecutor()

    res = executor.execute(custom_mod, req)  # type: ignore[arg-type]
    assert res.is_success is True
    assert res.output_payload["result"] == "explicit"
    assert called_execute is True


def test_minimal_module_executor_target_identity_mismatch() -> None:
    executor = MinimalModuleExecutor()

    mod_identity = ModuleIdentity(name="target_mod", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=mod_identity,
        capability=ModuleCapability(responsibility="Task"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )
    atomic_mod = AtomicModule(contract=contract)

    wrong_identity = ModuleIdentity(name="wrong_mod", version="1.0.0", kind="atomic")
    req = ExecutionRequest(target_identity=wrong_identity)

    res = executor.execute(atomic_mod, req)

    assert res.is_success is False
    assert res.failure is not None
    assert res.failure.failure_type == FailureType.CONTRACT_VIOLATION
    assert "Target identity mismatch" in res.failure.message


def test_minimal_module_executor_module_failure_handling() -> None:
    executor = MinimalModuleExecutor()

    identity = ModuleIdentity(name="failing_mod", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=identity,
        capability=ModuleCapability(responsibility="Fail operation"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )

    def failing_handler(payload):
        raise ValueError("Computation failure inside module")

    atomic_mod = AtomicModule(contract=contract, handler=failing_handler)
    req = ExecutionRequest(target_identity=identity)

    res = executor.execute(atomic_mod, req)

    assert res.is_success is False
    assert res.failure is not None
    assert res.failure.failure_type == FailureType.MODULE_FAILURE
    assert "Computation failure inside module" in res.failure.message
    assert res.failure.details.get("exception") == "ValueError"


def test_minimal_module_executor_unimplemented_handler_failure() -> None:
    executor = MinimalModuleExecutor()

    identity = ModuleIdentity(name="unhandled_mod", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=identity,
        capability=ModuleCapability(responsibility="No handler"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )

    atomic_mod = AtomicModule(contract=contract)  # No handler -> execute() raises NotImplementedError
    req = ExecutionRequest(target_identity=identity)

    res = executor.execute(atomic_mod, req)

    assert res.is_success is False
    assert res.failure is not None
    assert res.failure.failure_type == FailureType.MODULE_FAILURE
    assert "has no handler defined" in res.failure.message


def test_minimal_module_executor_invalid_request() -> None:
    executor = MinimalModuleExecutor()

    identity = ModuleIdentity(name="mod", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=identity,
        capability=ModuleCapability(responsibility="Task"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )
    atomic_mod = AtomicModule(contract=contract)

    res = executor.execute(atomic_mod, "invalid_request_object")  # type: ignore[arg-type]

    assert res.is_success is False
    assert res.failure is not None
    assert res.failure.failure_type == FailureType.INVALID_REQUEST


def test_boundary_no_forbidden_companion_imports() -> None:
    forbidden_modules = ("agent-core", "agent-core-next", "living-data-ocean", "underworld")
    for loaded_mod in sys.modules:
        for forbidden in forbidden_modules:
            assert forbidden not in loaded_mod, f"Forbidden module {forbidden} found in sys.modules!"
