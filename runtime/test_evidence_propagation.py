from evidence import capture_evidence
from evidence_propagation import EvidencePropagator
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, example_protocol


class RecordingConsumer:
    def __init__(self):
        self.received = []

    def apply_transition(self, evidence):
        self.received.append(evidence)


def test_one_evidence_reaches_multiple_consumers_without_rewriting():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "flow boundary"},
    )
    evidence = capture_evidence(result)

    adapter = InMemoryLandscapeAdapter()
    recorder = RecordingConsumer()

    EvidencePropagator([adapter, recorder]).propagate(evidence)

    assert adapter.read_state()["changed"] is True
    assert recorder.received == [evidence]
    assert recorder.received[0] is evidence


def test_propagation_preserves_failure_as_non_transition():
    def failing_protocol(context):
        raise RuntimeError("boom")

    result = Runtime().execute("failing.protocol", failing_protocol, {})
    evidence = capture_evidence(result)

    adapter = InMemoryLandscapeAdapter()
    recorder = RecordingConsumer()

    EvidencePropagator([adapter, recorder]).propagate(evidence)

    assert adapter.read_state() == {}
    assert recorder.received == [evidence]
    assert recorder.received[0] is evidence
