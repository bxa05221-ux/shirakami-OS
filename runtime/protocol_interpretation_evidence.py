"""Explicit, non-authoritative records of suspected Protocol misinterpretations.

This boundary preserves source and observed output without granting semantic
authority to a model, a validator, or an Evidence record. A reviewer may label
the observed mismatch, but no label edits the source Protocol or authorizes a
Runtime transition.
"""
from dataclasses import dataclass, replace
from typing import Literal

CandidateStatus = Literal["candidate_only", "reviewed", "rejected"]
MISINTERPRETATION_CATEGORIES = frozenset({
    "forced_conclusion",
    "isolated_perspectives",
    "lost_unresolved_question",
    "observation_as_fact",
    "unapproved_protocol_promotion",
    "other",
})


class InterpretationEvidenceError(ValueError):
    """A candidate lacks an explicit observable reference or valid lineage."""


@dataclass(frozen=True)
class InterpretationEvidence:
    evidence_id: str
    protocol_ref: str
    protocol_revision: str
    input_ref: str
    original_output: str
    observed_output: str
    claimed_difference: str
    category: str
    observer: str
    status: CandidateStatus = "candidate_only"
    reviewer: str | None = None
    review_note: str | None = None

    def __post_init__(self) -> None:
        required = (
            self.evidence_id, self.protocol_ref, self.protocol_revision,
            self.input_ref, self.original_output, self.observed_output,
            self.claimed_difference, self.category, self.observer,
        )
        if any(not isinstance(x, str) or not x.strip() for x in required):
            raise InterpretationEvidenceError("explicit provenance and both outputs are required")
        if self.category not in MISINTERPRETATION_CATEGORIES:
            raise InterpretationEvidenceError("unknown category")
        if self.status not in ("candidate_only", "reviewed", "rejected"):
            raise InterpretationEvidenceError("invalid status")
        if self.status == "candidate_only" and (self.reviewer or self.review_note):
            raise InterpretationEvidenceError("unreviewed candidates cannot carry a review")
        if self.status != "candidate_only" and (
            not self.reviewer or not self.reviewer.strip()
            or not self.review_note or not self.review_note.strip()
        ):
            raise InterpretationEvidenceError("review requires explicit identity and rationale")

    def as_record(self) -> dict[str, object]:
        """A plain record; explicitly not Runtime Evidence or a verified fact."""
        return {
            "kind": "protocol_interpretation_candidate",
            "evidence_id": self.evidence_id,
            "protocol_ref": self.protocol_ref,
            "protocol_revision": self.protocol_revision,
            "input_ref": self.input_ref,
            "original_output": self.original_output,
            "observed_output": self.observed_output,
            "claimed_difference": self.claimed_difference,
            "category": self.category,
            "observer": self.observer,
            "status": self.status,
            "reviewer": self.reviewer,
            "review_note": self.review_note,
            "runtime_evidence": False,
            "authorizes_execution": False,
            "changes_canonical_protocol": False,
        }


def review_interpretation(
    candidate: InterpretationEvidence, *, reviewer: str,
    review_note: str, accepted_as_observation: bool,
) -> InterpretationEvidence:
    """Review the *observation*, never certify a Protocol's semantic truth."""
    if candidate.status != "candidate_only":
        raise InterpretationEvidenceError("candidate already reviewed")
    if not reviewer.strip() or not review_note.strip():
        raise InterpretationEvidenceError("reviewer and rationale are required")
    return replace(
        candidate,
        status="reviewed" if accepted_as_observation else "rejected",
        reviewer=reviewer,
        review_note=review_note,
    )
