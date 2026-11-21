"""Student controls; the supplied core and data layer are unchanged."""
import re
from statistics import median

TEXT_FIELDS = ("name", "university", "program")
INSTRUCTION = re.compile(
    r"\b(?:ignore|disregard|override)\b.{0,100}\b(?:instructions?|prompts?|system|rules?)\b"
    r"|\b(?:output|reply|respond)\s*:\s*(?:shortlist|reject)\b"
    r"|<\|(?:im_start|im_end|system)\|>", re.IGNORECASE,
)


def my_extra_refusal(profile, purpose):
    """Reject malformed free-text fields or explicit instruction-like content before rendering."""
    for field in TEXT_FIELDS:
        value = getattr(profile, field, None)
        if not isinstance(value, str) or not value.strip() or len(value) > 200:
            return "invalid_text_field"
        if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
            return "multiline_or_control_text"
        if INSTRUCTION.search(value):
            return "instruction_in_profile"
    return None


def my_extra_escalation(profile, decision):
    """A refusal of the highest-need bracket receives a human merits check."""
    if decision.decision == "reject" and profile.household_income_bracket == 1:
        return "highest_need_rejection_review"
    return None


def choose_band(scores, target=0.20):
    """Observed-score band near the two decision medians, closest to the review target.

    This calibrates workload, not predictive uncertainty or correctness. Ties can prevent
    reaching the target. The same declared rule is used before and after blinding.
    """
    values = sorted(scores["reject"] + scores["shortlist"])
    if not values:
        raise ValueError("No scored replies for band calibration")
    available = sorted(set(values))
    centres = [median(v) for v in scores.values() if v]
    anchor = sum(centres) / len(centres)
    candidates = []
    for lo in available:
        for hi in available:
            if lo <= anchor <= hi:
                inside = sum(lo <= x <= hi for x in values)
                candidates.append((abs(inside / len(values) - target), hi-lo,
                                   abs((lo+hi)/2-anchor), lo, hi))
    best = min(candidates)
    return (int(best[-2]), int(best[-1]))
