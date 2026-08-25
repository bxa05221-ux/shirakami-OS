"""Generic bridge from validated Matome Protocol IR to the Runtime boundary.

The bridge interprets only the generic Protocol IR shape. It does not branch on
or implement domain-specific actions; those remain data carried by the IR.
"""

from .protocol_loader import ProtocolIR
from .prototype import ExecutionContext, Transition


def protocol_from_ir(protocol_ir: ProtocolIR):
    """Return a Runtime-compatible Protocol callable for a validated ProtocolIR."""

    def execute(context: ExecutionContext) -> Transition:
        return Transition(
            kind="matome.protocol.transition",
            data={
                "protocol_id": context.protocol_id,
                "protocol_title": protocol_ir.title,
                "protocol_version": protocol_ir.version,
                "statement": protocol_ir.statement,
                "pipeline": [dict(item) for item in protocol_ir.pipeline],
                "input": dict(context.input),
                "changed": True,
            },
        )

    return execute
