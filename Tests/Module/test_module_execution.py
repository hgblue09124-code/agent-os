from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
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


def test_valid_execution_request_construction() -> None:
    identity = ModuleIdentity(name="text_cleaner", version="1.0.0", kind="atomic")
    req = ExecutionRequest(
        target_identity=identity,
        input_payload={"raw_text": "  hello world  "},
        request_id="req-12345",
    )

    assert req.target_identity == identity
    assert req.input_payload["raw_text"] == "  hello world  "
    assert req.request_id == "req-12345"


def test_valid_successful_execution_result() -> None:
    res = ExecutionResult(
        is_success=True,
        output_payload={"clean_text": "hello world"},
    )

    assert res.is_success is True
    assert res.output_payload["clean_text"] == "hello world"
    assert res.failure is None


def test_valid_failed_execution_result() -> None:
    failure = ExecutionFailure(
        failure_type=FailureType.MODULE_FAILURE,
        message="An internal error occurred during module execution.",
        details={"code": 500},
    )
    res = ExecutionResult(
        is_success=False,
        failure=failure,
    )

    assert res.is_success is False
    assert res.output_payload is None
    assert res.failure == failure
    assert res.failure.failure_type == FailureType.MODULE_FAILURE
    assert res.failure.message == "An internal error occurred during module execution."
    assert res.failure.details["code"] == 500


def test_execution_failure_type_string_coercion() -> None:
    failure = ExecutionFailure(
        failure_type="invalid_request",
        message="Payload schema violation.",
    )
    assert failure.failure_type == FailureType.INVALID_REQUEST


def test_invalid_execution_primitives_are_rejected_deterministically() -> None:
    identity = ModuleIdentity(name="mod", version="1.0.0")

    # Invalid request target identity
    with pytest.raises(ValueError, match="target_identity must be a valid ModuleIdentity instance."):
        ExecutionRequest(target_identity="invalid_id")  # type: ignore[arg-type]

    # Invalid request_id
    with pytest.raises(ValueError, match="request_id, if provided, must be a non-empty string."):
        ExecutionRequest(target_identity=identity, request_id="  ")

    # Invalid input_payload key
    with pytest.raises(ValueError, match="input_payload keys must be non-empty strings."):
        ExecutionRequest(target_identity=identity, input_payload={"": "val"})

    # Invalid failure_type
    with pytest.raises(ValueError, match="Invalid failure_type"):
        ExecutionFailure(failure_type="non_existent_type", message="msg")  # type: ignore[arg-type]

    # Invalid failure message
    with pytest.raises(ValueError, match="Failure message must be a non-empty string."):
        ExecutionFailure(failure_type=FailureType.CONTRACT_VIOLATION, message="  ")

    # Invalid failure detail key
    with pytest.raises(ValueError, match="Failure detail keys must be non-empty strings."):
        ExecutionFailure(failure_type=FailureType.CONTRACT_VIOLATION, message="msg", details={"": 1})

    # Success result containing failure object
    failure = ExecutionFailure(failure_type=FailureType.CONTRACT_VIOLATION, message="msg")
    with pytest.raises(ValueError, match="Successful ExecutionResult cannot contain a failure object."):
        ExecutionResult(is_success=True, failure=failure)

    # Failed result without failure object
    with pytest.raises(ValueError, match="Failed ExecutionResult must contain a valid ExecutionFailure instance."):
        ExecutionResult(is_success=False)

    # Failed result containing output_payload
    with pytest.raises(ValueError, match="Failed ExecutionResult cannot contain an output_payload."):
        ExecutionResult(is_success=False, output_payload={"out": 1}, failure=failure)


def test_execution_primitives_are_immutable() -> None:
    identity = ModuleIdentity(name="mod", version="1.0.0")
    req = ExecutionRequest(
        target_identity=identity,
        input_payload={"key": "val"},
    )

    with pytest.raises(FrozenInstanceError):
        req.target_identity = identity  # type: ignore[misc]

    with pytest.raises(TypeError):
        req.input_payload["key"] = "new_val"  # type: ignore[index]

    res = ExecutionResult(is_success=True, output_payload={"key": "val"})

    with pytest.raises(FrozenInstanceError):
        res.is_success = False  # type: ignore[misc]

    with pytest.raises(TypeError):
        res.output_payload["key"] = "new_val"  # type: ignore[index]

    failure = ExecutionFailure(
        failure_type=FailureType.CONTRACT_VIOLATION,
        message="msg",
        details={"det": "val"},
    )

    with pytest.raises(FrozenInstanceError):
        failure.message = "new_msg"  # type: ignore[misc]

    with pytest.raises(TypeError):
        failure.details["det"] = "new_val"  # type: ignore[index]


def test_minimal_module_executor_protocol_compatibility() -> None:
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

    # Request with different module name
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


def test_minimal_module_executor_unimplemented_module_failure() -> None:
    executor = MinimalModuleExecutor()

    identity = ModuleIdentity(name="unhandled_mod", version="1.0.0", kind="atomic")
    contract = ModuleContract(
        identity=identity,
        capability=ModuleCapability(responsibility="No handler"),
        input_boundary=InputBoundary(),
        output_boundary=OutputBoundary(),
    )

    atomic_mod = AtomicModule(contract=contract)  # No handler
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

    # Pass non-ExecutionRequest
    res = executor.execute(atomic_mod, "invalid_request_object")  # type: ignore[arg-type]

    assert res.is_success is False
    assert res.failure is not None
    assert res.failure.failure_type == FailureType.INVALID_REQUEST


def test_boundary_no_forbidden_companion_imports() -> None:
    forbidden_modules = ("agent-core", "agent-core-next", "living-data-ocean", "underworld")
    for loaded_mod in sys.modules:
        for forbidden in forbidden_modules:
            assert forbidden not in loaded_mod, f"Forbidden module {forbidden} found in sys.modules!"
