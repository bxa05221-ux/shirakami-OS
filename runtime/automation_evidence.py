"""R0087 Operation automation -> Evidence boundary.

Implementation-only bridge. Converts already observable automation step
results into immutable EvidenceRecord instances without assigning semantic
meaning or changing the Evidence contract.
"""

from typing import Iterable, Tuple

from .evidence import EvidenceRecord
from .operation_automation import AutomationStepResult


def capture_automation_evidence(
    protocol_id: str,
    results: Iterable[AutomationStepResult],
) -> Tuple[EvidenceRecord, ...]:
    """Capture one immutable EvidenceRecord for each automation step result."""
    if not protocol_id:
        raise ValueError("protocol_id is required")

    captured = []
    for result in results:
        if not isinstance(result, AutomationStepResult):
            raise TypeError("AutomationStepResult is required")
        captured.append(
            EvidenceRecord(
                protocol_id=protocol_id,
                status="observed",
                transition_kind="operation_automation_step",
                transition_data={
                    "step": result.step,
                    "outcome": result.outcome,
                },
                signals=("operation_automation",),
            )
        )
    return tuple(captured)
