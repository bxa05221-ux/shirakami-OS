from prototype import Runtime, Transition


def test_r0009_same_runtime_executes_two_domain_protocols():
    runtime = Runtime()

    def protocol_alpha(context):
        return Transition(
            kind="alpha.applied",
            data={"domain": "alpha", "value": context.input["value"] + 1, "changed": True},
        )

    def protocol_beta(context):
        return Transition(
            kind="beta.applied",
            data={"domain": "beta", "value": context.input["value"] * 2, "changed": True},
        )

    alpha = runtime.execute("alpha.protocol", protocol_alpha, {"value": 10})
    beta = runtime.execute("beta.protocol", protocol_beta, {"value": 10})

    assert alpha.status == "completed"
    assert beta.status == "completed"
    assert alpha.transition.kind == "alpha.applied"
    assert beta.transition.kind == "beta.applied"
    assert alpha.transition.data["value"] == 11
    assert beta.transition.data["value"] == 20
    assert alpha.transition.data["domain"] == "alpha"
    assert beta.transition.data["domain"] == "beta"


def test_r0009_runtime_accepts_domain_defined_semantic_effect():
    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="custom.semantic.effect",
            data={"changed": True, "semantic_marker": context.input["marker"]},
        )

    result = runtime.execute("custom.protocol", protocol, {"marker": "domain-defined"})

    assert result.status == "completed"
    assert result.transition.kind == "custom.semantic.effect"
    assert result.transition.data["semantic_marker"] == "domain-defined"
