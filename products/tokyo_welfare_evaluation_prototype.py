"""Synthetic-only trial workflow for Tokyo welfare-service third-party evaluation.

This module deliberately contains no model adapter, network client, persistence
configuration, or automatic decision logic.  It is a small, local facilitation
tool: evaluators enter their own observations, compare disclosed grounds, make
a human-recorded consensus note, and collect trial feedback.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from cryptography.fernet import Fernet

from security.local_store import EncryptedEvaluationStore, RotatingKeyring


SYNTHETIC_ONLY_NOTICE = "架空データ限定。実在の利用者・事業所・個人情報を入力しないでください。"
HUMAN_DECISION_NOTICE = "最終判断は人間の評価者が行います。これは報告書草案です。"


class TrialBoundaryError(ValueError):
    """Raised when a caller crosses the deliberately narrow trial boundary."""


@dataclass(frozen=True)
class SyntheticCase:
    case_id: str
    title: str
    service_type: str
    scenario: str
    is_synthetic: bool = True


@dataclass(frozen=True)
class EvaluatorInput:
    evaluator_id: str
    criterion: str
    observation: str
    evidence: tuple[str, ...]
    tentative_view: str


@dataclass(frozen=True)
class ConsensusRecord:
    facilitator_id: str
    note: str
    unresolved_points: tuple[str, ...]
    human_confirmed: bool


@dataclass(frozen=True)
class TrialFeedback:
    evaluator_id: str
    ease_of_use: int
    helpful_parts: str
    problems: str
    would_use_in_work: str


@dataclass
class TokyoWelfareEvaluationTrial:
    """A local, in-memory workflow that keeps separate views until disclosure.

    The encrypted store is used for evaluator input so that private notes are
    not readable by peers before an explicit share-for-consensus step.
    """

    case: SyntheticCase
    evaluator_ids: set[str]
    _store: EncryptedEvaluationStore = field(init=False, repr=False)
    _inputs: dict[str, EvaluatorInput] = field(default_factory=dict, init=False)
    _shared: set[str] = field(default_factory=set, init=False)
    _consensus: ConsensusRecord | None = field(default=None, init=False)
    _feedback: list[TrialFeedback] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.case.is_synthetic or not self.case.case_id.startswith("synthetic-"):
            raise TrialBoundaryError("this trial accepts only an explicitly synthetic case")
        if not self.evaluator_ids or any(not value.strip() for value in self.evaluator_ids):
            raise TrialBoundaryError("at least one named trial evaluator is required")
        self._store = EncryptedEvaluationStore(
            RotatingKeyring({"trial-v1": Fernet.generate_key()}, "trial-v1")
        )
        self._store.register_project_members(self.case.case_id, self.evaluator_ids)

    def record_input(self, item: EvaluatorInput) -> str:
        """Save one evaluator's own input; it is private until explicitly shared."""
        if item.evaluator_id not in self.evaluator_ids:
            raise TrialBoundaryError("input author is not a trial evaluator")
        if not all((item.criterion.strip(), item.observation.strip(), item.tentative_view.strip())):
            raise TrialBoundaryError("criterion, observation and tentative view are required")
        if not item.evidence or any(not value.strip() for value in item.evidence):
            raise TrialBoundaryError("at least one stated evidence item is required")
        record_id = f"input-{item.evaluator_id}-{uuid4().hex}"
        # The store protects the original entry; the in-memory index intentionally
        # holds structured synthetic data only for this no-persistence trial.
        payload = "\n".join((item.criterion, item.observation, *item.evidence, item.tentative_view)).encode("utf-8")
        self._store.put_private(record_id, self.case.case_id, item.evaluator_id, payload)
        self._inputs[record_id] = item
        return record_id

    def share_for_consensus(self, record_id: str, evaluator_id: str) -> None:
        if record_id not in self._inputs:
            raise TrialBoundaryError("unknown trial input")
        self._store.share_for_consensus(
            record_id, evaluator_id, self.evaluator_ids - {evaluator_id}, project_id=self.case.case_id
        )
        self._shared.add(record_id)

    def compare_views(self) -> dict[str, object]:
        """Show disclosed views side by side; no score, winner, or decision is made."""
        disclosed = [self._inputs[record_id] for record_id in sorted(self._shared)]
        evidence_sets = [set(item.evidence) for item in disclosed]
        shared_evidence = set.intersection(*evidence_sets) if len(evidence_sets) >= 2 else set()
        all_evidence = set().union(*evidence_sets) if evidence_sets else set()
        return {
            "case_id": self.case.case_id,
            "views": [
                {
                    "evaluator_id": item.evaluator_id,
                    "criterion": item.criterion,
                    "observation": item.observation,
                    "evidence": list(item.evidence),
                    "tentative_view": item.tentative_view,
                }
                for item in disclosed
            ],
            "shared_evidence": sorted(shared_evidence),
            "divergent_evidence": sorted(all_evidence - shared_evidence),
            "decision": None,
            "human_gate_required": True,
        }

    def record_human_consensus(self, record: ConsensusRecord) -> None:
        if record.facilitator_id not in self.evaluator_ids:
            raise TrialBoundaryError("consensus facilitator is not a trial evaluator")
        if not record.human_confirmed:
            raise TrialBoundaryError("a human evaluator must explicitly confirm a consensus note")
        if not record.note.strip():
            raise TrialBoundaryError("a human consensus note is required")
        self._consensus = record

    def draft_report(self) -> dict[str, object]:
        comparison = self.compare_views()
        return {
            "status": "DRAFT - human review required",
            "synthetic_only": True,
            "notice": HUMAN_DECISION_NOTICE,
            "case": {"title": self.case.title, "service_type": self.case.service_type, "scenario": self.case.scenario},
            "comparative_views": comparison["views"],
            "shared_evidence": comparison["shared_evidence"],
            "divergent_evidence": comparison["divergent_evidence"],
            "human_consensus": None if self._consensus is None else {
                "facilitator_id": self._consensus.facilitator_id,
                "note": self._consensus.note,
                "unresolved_points": list(self._consensus.unresolved_points),
            },
            "final_decision": None,
        }

    def submit_feedback(self, feedback: TrialFeedback) -> None:
        if feedback.evaluator_id not in self.evaluator_ids:
            raise TrialBoundaryError("feedback author is not a trial evaluator")
        if not 1 <= feedback.ease_of_use <= 5:
            raise TrialBoundaryError("ease_of_use must be between 1 and 5")
        self._feedback.append(feedback)

    def feedback_summary(self) -> list[dict[str, object]]:
        return [
            {
                "evaluator_id": item.evaluator_id,
                "ease_of_use": item.ease_of_use,
                "helpful_parts": item.helpful_parts,
                "problems": item.problems,
                "would_use_in_work": item.would_use_in_work,
            }
            for item in self._feedback
        ]
