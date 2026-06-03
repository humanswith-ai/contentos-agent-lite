"""Transparent AEO/quality scorer (spec sections 8/11). 8 weighted axes, each 0-100.
Heuristic + documented — NOT the private tuned ContentOS model (moat boundary)."""
import re
from scripts import antislop

WEIGHTS = {  # sum = 100
    "direct_answer": 18, "named_entities": 15, "numerical_attribution": 15,
    "question_h2s": 12, "structured_elements": 12, "faq_block": 10,
    "anti_slop": 10, "citation_markers": 8,
}


def _first_words(text: str, n: int = 100) -> str:
    return " ".join(re.sub(r"^#.*$", "", text, flags=re.M).split()[:n])


def _axis_direct_answer(text: str) -> int:
    lead = _first_words(text, 60)
    has_number = bool(re.search(r"\b\d", lead))
    has_entity = bool(re.search(r"\b[A-Z][a-z]+\b", lead))
    declarative = len(lead.split()) >= 20
    return min(100, 34 * (has_number + has_entity + declarative))


def _axis_named_entities(text: str) -> int:
    ents = set(re.findall(r"\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?\b", text))
    return min(100, len(ents) * 20)


def _axis_numerical_attribution(text: str) -> int:
    nums = re.findall(r"\b\d[\d.,]*\s*(?:%|billion|million|trillion|x)?\b", text)
    attributed = re.findall(r"\b\d[\d.,]*\b[^.\n]{0,40}(?:\[\d+\]|\(\d{4}|https?://)", text)
    if not nums:
        return 0
    return min(100, 40 + 20 * len(attributed))


def _axis_question_h2s(text: str) -> int:
    h2s = re.findall(r"^##\s+(.+)$", text, re.M)
    if not h2s:
        return 0
    q = sum(1 for h in h2s if h.strip().endswith("?"))
    return int(100 * q / len(h2s))


def _axis_structured_elements(text: str) -> int:
    has_list = bool(re.search(r"^\s*[-*]\s+\S", text, re.M))
    has_table = bool("|" in text and re.search(r"^\s*\|.*\|", text, re.M))
    has_faq = bool(re.search(r"(?i)\bFAQ\b|\*\*[^*]+\?\*\*", text))
    return min(100, 40 * (has_list + has_table + has_faq))


def _axis_faq_block(text: str) -> int:
    return 100 if re.search(r"(?im)^##\s*FAQ|(\*\*.+\?\*\*)", text) else 0


def _axis_anti_slop(text: str, lang: str) -> int:
    hits = antislop.scan(text, lang)["count"]
    return max(0, 100 - 25 * hits)


def _axis_citation_markers(text: str) -> int:
    markers = len(re.findall(r"\[\d+\]|https?://", text))
    return min(100, markers * 25)


def score_draft(draft: str, lang: str = "en", source_pack: str | None = None) -> dict:
    axes = {
        "direct_answer": _axis_direct_answer(draft),
        "named_entities": _axis_named_entities(draft),
        "numerical_attribution": _axis_numerical_attribution(draft),
        "question_h2s": _axis_question_h2s(draft),
        "structured_elements": _axis_structured_elements(draft),
        "faq_block": _axis_faq_block(draft),
        "anti_slop": _axis_anti_slop(draft, lang),
        "citation_markers": _axis_citation_markers(draft),
    }
    overall = round(sum(axes[a] * w for a, w in WEIGHTS.items()) / 100)
    blockers = []
    if overall < 55:
        blockers.append({"severity": "P0", "axis": "overall", "message": f"overall {overall} < 55",
                         "fix_hint": "add sources, numbers, structure; cut slop"})
    if axes["anti_slop"] <= 25:
        blockers.append({"severity": "P1", "axis": "anti_slop", "message": "heavy AI-slop",
                         "fix_hint": "rewrite per anti-slop rules"})
    if axes["citation_markers"] == 0 and axes["numerical_attribution"] > 0:
        blockers.append({"severity": "P1", "axis": "citation_markers", "message": "numbers without citations",
                         "fix_hint": "anchor stats with [n] sources"})
    has_p0 = any(b["severity"] == "P0" for b in blockers)
    verdict = "STOP" if (overall < 55 or has_p0) else ("READY" if overall >= 85 else "REVISE")
    return {"overall": overall, "axes": axes, "blockers": blockers, "verdict": verdict}
