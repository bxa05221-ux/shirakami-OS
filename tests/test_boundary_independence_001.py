"""Boundary Independence Test 001.

This test does not prove that Shirakami OS is a new computational model.
It checks a narrower, falsifiable property at the current Runtime boundary:
semantically different Protocols can be executed by the same Runtime without
changing the Runtime implementation or transition contract.
"""

from runtime.prototype import ExecutionContext, Runtime, Transition


SEMANTIC_DOMAINS = (
    "cognitive_observation",
    "conversation",
    "care_observation",
    "game_state",
    "repository_observation",
    "organization_workflow",
)


def make_protocol(domain: str):
    """Create a Protocol whose semantic domain is local to the Protocol."""

    def protocol(context: ExecutionContext) -> Transition:
        return Transition(
            kind="boundary.independence.observed",
            data={
                "domain": domain,
                "payload": dict(context.input),
            },
        )

    return protocol


def test_different_semantic_domains_share_the_same_runtime_boundary():
    runtime = Runtime()
    results = []

    for domain in SEMANTIC_DOMAINS:
        result = runtime.execute(
            f"bit001.{domain}",
            make_protocol(domain),
            {"probe": "BIT-001"},
        )
        results.append(result)

    assert all(result.status == "completed" for result in results)
    assert all(result.steps == 1 for result in results)
    assert all(result.transition.kind == "boundary.independence.observed" for result in results)
    assert [result.protocol_id for result in results] == [
        f"bit001.{domain}" for domain in SEMANTIC_DOMAINS
    ]


def test_semantic_density_does_not_change_runtime_transition_contract():
    runtime = Runtime()
    densities = (
        {},
        {"context": "basic"},
        {"context": "basic", "history": ["e1", "e2"]},
        {
            "context": "basic",
            "history": ["e1", "e2", "e3"],
            "relations": ["r1", "r2", "r3"],
            "observations": ["o1", "o2", "o3"],
        },
    )

    results = [
        runtime.execute(
            f"bit001.density.{index}",
            make_protocol("density_probe"),
            payload,
        )
        for index, payload in enumerate(densities)
    ]

    assert all(result.status == "completed" for result in results)
    assert all(result.steps == 1 for result in results)
    assert all(result.transition.kind == "boundary.independence.observed" for result in results)
