import inspect

from runtime.evidence import EvidenceRecord
from runtime.execution_request import ExecutionRequest
from runtime.oppai_runtime_flow import execute, prepare
from runtime.protocol_api import ProtocolRequest, build_default_protocol_request, invoke_protocol


def test_r0091_oppai_protocol_resolution_requires_registry_and_protocol_request():
    prepared = prepare("hello r0091", protocol="default", context={"source": "human"})

    assert prepared.protocol == "default"
    assert prepared.input_for_runtime == "hello r0091"
    assert not isinstance(prepared, ProtocolRequest)

    parameters = inspect.signature(build_default_protocol_request).parameters
    assert "registry" in parameters


def test_r0091_oppai_adapter_contract_is_not_protocol_request_executor_contract():
    execute_parameters = inspect.signature(execute).parameters
    invoke_parameters = inspect.signature(invoke_protocol).parameters

    assert list(execute_parameters)[:4] == ["text", "runtime_adapter", "protocol", "context"]
    assert list(invoke_parameters)[:2] == ["request", "executor"]

    request = ProtocolRequest(protocol_id="r0091.protocol", version="0.1", input={"input": "hello"})
    assert request.input == {"input": "hello"}


def test_r0091_oppai_evidence_shape_is_not_evidence_record_shape():
    prepared = prepare("hello r0091", protocol="default")

    evidence_keys = set(prepared.evidence)
    required_record_fields = {
        "protocol_id",
        "status",
        "transition_kind",
        "transition_data",
        "signals",
        "confidence",
    }

    assert "schema" in evidence_keys
    assert "confidence" in evidence_keys
    assert not required_record_fields.issubset(evidence_keys)
    assert list(inspect.signature(EvidenceRecord).parameters) == [
        "protocol_id",
        "status",
        "transition_kind",
        "transition_data",
        "signals",
        "confidence",
    ]


def test_r0091_execution_request_is_operation_identity_not_protocol_identity():
    request = ExecutionRequest(operation_id="r0091", execution_id="exec-1")

    assert request.identity == ("r0091", "exec-1")
    assert not hasattr(request, "protocol_id")
    assert not hasattr(request, "input")
