"""Epic G Phase 1 reviewer queue MVP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


REASON_CODES = {
    "policy_risk",
    "ambiguity",
    "too_easy_or_too_hard",
    "poor_localization",
    "unfunny_or_low_quality",
    "duplicate",
}


@dataclass
class QueueItem:
    entry_id: str
    language: str
    word: str
    clue_text: str
    auto_flags: List[str]
    score_summary: Dict[str, float]
    source_trace: Dict[str, str]
    status: str = "reviewed"


@dataclass
class ReviewDecision:
    action: str
    reason_code: str | None = None
    note: str = ""


def apply_decision(item: QueueItem, decision: ReviewDecision) -> QueueItem:
    action_to_status = {
        "approve": "approved",
        "request_edit": "draft",
        "escalate": "reviewed",
        "reject": "deprecated",
        "deprecate": "deprecated",
    }

    new_status = action_to_status.get(decision.action)
    if new_status is None:
        raise ValueError("invalid_action")

    if decision.action != "approve":
        if decision.reason_code is None or decision.reason_code not in REASON_CODES:
            raise ValueError("A valid reason_code is required for non-approve actions")

    item.status = new_status
    return item
