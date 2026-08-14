from protocol_bridge import protocol_from_ir
from protocol_loader import parse_matome
from prototype import Runtime


ALPHA_MATOME = """matome:
  title: Alpha Domain Protocol
  version: 0.1
  statement: >
    Alpha defines its own transition vocabulary.
  pipeline:
    - phase: alpha
      action: increment_value
"""


BETA_MATOME = """matome:
  title: Beta Domain Protocol
  version: 0.1
  statement: >
    Beta defines a different transition vocabulary.
  pipeline:
    - phase: beta
      action: multiply_value
    - phase: beta.audit
      action: record_reason
"""


def test_r0009_same_runtime_executes_two_domain_protocols():
    """The same Runtime executes different Matome Protocol IR instances."""
    runtime = Runtime()
    alpha_ir = parse_matome(ALPHA_MATOME)
    beta_ir = parse_matome(BETA_MATOME)

    alpha = runtime.execute(
        alpha_ir.protocol_id,
        protocol_from_ir(alpha_ir),
        {"value": 10},
    )
    beta = runtime.execute(
        beta_ir.protocol_id,
        protocol_from_ir(beta_ir),
        {"value": 10},
    )

    assert alpha.status == "completed"
    assert beta.status == "completed"
    assert alpha.transition.kind == "matome.protocol.transition"
    assert beta.transition.kind == "matome.protocol.transition"
    assert alpha.transition.data["protocol_title"] == "Alpha Domain Protocol"
    assert beta.transition.data["protocol_title"] == "Beta Domain Protocol"
    assert alpha.transition.data["pipeline"] == [
        {"phase": "alpha", "action": "increment_value"}
    ]
    assert beta.transition.data["pipeline"] == [
        {"phase": "beta", "action": "multiply_value"},
        {"phase": "beta.audit", "action": "record_reason"},
    ]


def test_r0009_runtime_has_no_domain_specific_protocol_branching():
    """Domain-specific vocabulary remains data in Protocol IR, not Runtime code."""
    runtime = Runtime()
    alpha_ir = parse_matome(ALPHA_MATOME)
    beta_ir = parse_matome(BETA_MATOME)

    alpha = runtime.execute(alpha_ir.protocol_id, protocol_from_ir(alpha_ir), {})
    beta = runtime.execute(beta_ir.protocol_id, protocol_from_ir(beta_ir), {})

    assert alpha.transition.data["pipeline"][0]["action"] == "increment_value"
    assert beta.transition.data["pipeline"][0]["action"] == "multiply_value"
    assert beta.transition.data["pipeline"][1]["action"] == "record_reason"


def test_r0009_protocol_ir_can_carry_domain_semantic_marker_without_runtime_branch():
    """A Protocol-defined marker can cross the generic boundary as data."""
    runtime = Runtime()
    protocol_ir = parse_matome(
        """matome:
  title: Semantic Marker Protocol
  version: 0.1
  statement: >
    A protocol may carry a semantic marker as part of its declared data.
  pipeline:
    - phase: domain
      action: emit_marker
"""
    )

    result = runtime.execute(
        protocol_ir.protocol_id,
        protocol_from_ir(protocol_ir),
        {"semantic_marker": "domain-defined"},
    )

    assert result.status == "completed"
    assert result.transition.kind == "matome.protocol.transition"
    assert result.transition.data["pipeline"][0]["action"] == "emit_marker"
    assert result.transition.data["input"]["semantic_marker"] == "domain-defined"
