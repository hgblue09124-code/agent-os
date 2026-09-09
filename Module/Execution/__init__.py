"""Module execution boundary facet."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Mapping, Protocol, runtime_checkable

from Module.Identity import ModuleIdentity

if TYPE_CHECKING:
    from Module import Module

BOUNDARY = "module.execution"
IMPLEMENTED = True


class FailureType(str, Enum):
    INVALID_REQUEST = "invalid_request"
    MODULE_FAILURE = "module_failure"
    CONTRACT_VIOLATION = "contract_violation"


@dataclass(frozen=True)
class ExecutionFailure:
    failure_type: FailureType
    message: str
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.failure_type, str) and not isinstance(self.failure_type, FailureType):
            try:
                object.__setattr__(self, "failure_type", FailureType(self.failure_type))
            except ValueError:
                raise ValueError(f"Invalid failure_type: '{self.failure_type}'.")
        elif not isinstance(self.failure_type, FailureType):
            raise ValueError(f"Invalid failure_type: '{self.failure_type}'.")

        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("Failure message must be a non-empty string.")

        if not isinstance(self.details, (dict, MappingProxyType)):
            raise ValueError("Failure details must be a dictionary/mapping.")

        details_dict = dict(self.details)
        for key in details_dict:
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Failure detail keys must be non-empty strings.")
        object.__setattr__(self, "details", MappingProxyType(details_dict))


@dataclass(frozen=True)
class ExecutionRequest:
    target_identity: ModuleIdentity
    input_payload: Mapping[str, Any] = field(default_factory=dict)
    request_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target_identity, ModuleIdentity):
            raise ValueError("target_identity must be a valid ModuleIdentity instance.")

        if self.request_id is not None:
            if not isinstance(self.request_id, str) or not self.request_id.strip():
                raise ValueError("request_id, if provided, must be a non-empty string.")

        if not isinstance(self.input_payload, (dict, MappingProxyType)):
            raise ValueError("input_payload must be a dictionary/mapping.")

        payload_dict = dict(self.input_payload)
        for key in payload_dict:
            if not isinstance(key, str) or not key.strip():
                raise ValueError("input_payload keys must be non-empty strings.")
        object.__setattr__(self, "input_payload", MappingProxyType(payload_dict))


@dataclass(frozen=True)
class ExecutionResult:
    is_success: bool
    output_payload: Mapping[str, Any] | None = None
    failure: ExecutionFailure | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.is_success, bool):
            raise ValueError("is_success must be a boolean.")

        if self.is_success:
            if self.failure is not None:
                raise ValueError("Successful ExecutionResult cannot contain a failure object.")
            if self.output_payload is None:
                object.__setattr__(self, "output_payload", MappingProxyType({}))
            elif not isinstance(self.output_payload, (dict, MappingProxyType)):
                raise ValueError("output_payload must be a dictionary/mapping.")
            else:
                out_dict = dict(self.output_payload)
                for key in out_dict:
                    if not isinstance(key, str) or not key.strip():
                        raise ValueError("output_payload keys must be non-empty strings.")
                object.__setattr__(self, "output_payload", MappingProxyType(out_dict))
        else:
            if self.failure is None or not isinstance(self.failure, ExecutionFailure):
                raise ValueError("Failed ExecutionResult must contain a valid ExecutionFailure instance.")
            if self.output_payload is not None:
                raise ValueError("Failed ExecutionResult cannot contain an output_payload.")


@runtime_checkable
class ModuleExecutor(Protocol):
    """Execution protocol defining the Module execution boundary."""

    def execute(self, module: Module, request: ExecutionRequest) -> ExecutionResult:
        ...


class MinimalModuleExecutor:
    """Minimal concrete implementation of ModuleExecutor Protocol."""

    def execute(self, module: Module, request: ExecutionRequest) -> ExecutionResult:
        # Step 1: Validate request structure
        if not isinstance(request, ExecutionRequest):
            return ExecutionResult(
                is_success=False,
                failure=ExecutionFailure(
                    failure_type=FailureType.INVALID_REQUEST,
                    message="Request must be an instance of ExecutionRequest.",
                ),
            )

        # Step 2: Validate target identity
        mod_identity = module.contract.identity
        req_identity = request.target_identity

        if req_identity != mod_identity:
            return ExecutionResult(
                is_success=False,
                failure=ExecutionFailure(
                    failure_type=FailureType.CONTRACT_VIOLATION,
                    message=(
                        f"Target identity mismatch: request specified '{req_identity.name}' "
                        f"v{req_identity.version} ({req_identity.kind}), but target module is "
                        f"'{mod_identity.name}' v{mod_identity.version} ({mod_identity.kind})."
                    ),
                ),
            )

        # Step 3: Invoke explicit execution capability directly
        try:
            raw_output = module.execute(request.input_payload)

            # Step 4: Normalize result
            if isinstance(raw_output, ExecutionResult):
                return raw_output

            if isinstance(raw_output, (dict, MappingProxyType)):
                return ExecutionResult(
                    is_success=True,
                    output_payload=raw_output,
                )

            return ExecutionResult(
                is_success=True,
                output_payload={"result": raw_output},
            )

        # Step 5: Handle module failure
        except Exception as exc:
            return ExecutionResult(
                is_success=False,
                failure=ExecutionFailure(
                    failure_type=FailureType.MODULE_FAILURE,
                    message=f"Module execution failed: {exc}",
                    details={"exception": type(exc).__name__},
                ),
            )


__all__ = [
    "BOUNDARY",
    "IMPLEMENTED",
    "ExecutionFailure",
    "ExecutionRequest",
    "ExecutionResult",
    "FailureType",
    "MinimalModuleExecutor",
    "ModuleExecutor",
]
