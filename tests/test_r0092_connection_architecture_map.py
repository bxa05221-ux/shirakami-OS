from runtime.oppai_runtime_flow import execute, prepare
from runtime.protocol_api import ProtocolRequest, build_default_protocol_request, invoke_protocol


def test_r0092_records_existing_boundary_roles_without_claiming_connection():
    prepared = prepare("hello r0092", protocol="default")
    assert prepared.protocol == "default"
    assert prepared.input_for_runtime == "hello r0092"
    assert callable(execute)
    assert callable(build_default_protocol_request)
    assert callable(invoke_protocol)


def test_r0092_protocol_request_remains_the_existing_protocol_boundary():
    request = ProtocolRequest(
        protocol_id="r0092.protocol",
        version="0.1",
        input={"input": "hello"},
    )
    assert request.protocol_id == "r0092.protocol"
    assert request.version == "0.1"
    assert request.input == {"input": "hello"}


def test_r0092_does_not_treat_oppai_preparation_as_evidence_record():
    prepared = prepare("hello r0092", protocol="default")
    assert isinstance(prepared.evidence, dict)
    assert prepared.evidence.get("schema") == "OPPAI"
    assert "protocol_id" not in prepared.evidence
    assert "transition_kind" not in prepared.evidence
    assert "transition_data" not in prepared.evidence
