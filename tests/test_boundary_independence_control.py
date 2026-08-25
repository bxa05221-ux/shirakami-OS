"""Control test for Boundary Independence Test 001.

The control deliberately introduces semantic branching into a fake Runtime.
The test must observe that the transition contract changes with semantic
meaning. This demonstrates that BIT-001 is falsifiable rather than a test
that can only produce PASS results.
"""

from runtime.prototype import ExecutionContext, Transition


SEMANTIC_DOMAINS = ("cognitive_observation", "game_state")


class MeaningDependentControlRuntime:
    """Intentionally bad Runtime: semantic domain changes execution."""

    def execute(self, protocol_id: str, protocol, input_data=None):
        context = ExecutionContext(protocol_id=protocol_id, input=dict(input_data or {}))
        transition = protocol(context)
        domain = transition.data["domain"]
        kind = f"meaning-dependent.{domain}"
        return Transition(kind=kind, data={"domain": domain})


def make_protocol(domain: str):
    def protocol(context: ExecutionContext) -> Transition:
        return Transition(
            kind="boundary.independence.observed",
            data={"domain": domain},
        )

    return protocol


def test_control_detects_semantic_runtime_coupling():
    runtime = MeaningDependentControlRuntime()
    results = [
        runtime.execute(
            f"control.{domain}",
            make_protocol(domain),
            {},
        )
        for domain in SEMANTIC_DOMAINS
    ]

    # A semantically coupled Runtime must NOT preserve one generic transition.
    assert [result.kind for result in results] == [
        "meaning-dependent.cognitive_observation",
        "meaning-dependent.game_state",
    ]
    assert len({result.kind for result in results}) == len(SEMANTIC_DOMAINS)
