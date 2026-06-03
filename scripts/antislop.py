"""Deterministic anti-slop scanner. EN rules ported from .claude/rules/anti-slop-v2.md;
RU calques/intensifiers from .claude/rules/ru-marketing-translation.md.
Transparent + extensible. >=1 hit in a hero/title should block; >=3 hits overall = block."""
import re

# (rule_id, lang, pattern). Highest-signal subset; extend to the full 20 EN rules
# (anti-slop-v2.md) + RU calque verbs (ru-marketing-translation.md) as a follow-up.
_RULES = [
    ("sycophantic_opening", "en", r"^(great|excellent|fantastic|wonderful|amazing)\s+(question|point|observation|insight)!?"),
    ("hedge_filler", "en", r"\bit('s| is) (important|worth|essential|crucial) to (note|mention|remember)\b"),
    ("delve", "en", r"\b(delve|delving|dive|diving)\s+(into|deep|deeper)\b"),
    ("navigate_landscape", "en", r"\b(navigate|navigating).{0,20}\blandscape\b|\b(evolving|complex|dynamic)\s+landscape\b|\btapestry of\b"),
    ("unlock_power", "en", r"\b(unlock|unleash|harness|tap into)s?\s+(the\s+)?(power|potential|magic|secret)\s+of\b"),
    ("throat_clearing_time", "en", r"\bin (today's|the|an?|this) (fast-paced|digital|modern|increasingly|competitive|ever-changing)\s+\w+\b"),
    ("empty_intensifier", "en", r"\b(crucial|vital|essential|pivotal|paramount)\b"),
    ("hype_adjective", "en", r"\b(game-?changer|game-?changing|revolutionary|groundbreaking|cutting-?edge|state-of-the-art|next-?gen(eration)?)\b"),
    ("empty_product_adj", "en", r"\b(robust|seamless|intuitive|comprehensive|holistic|world-class|best-in-class)\b"),
    # RU
    ("ru_intensifier", "ru", r"(мощн(ый|ое|ая|ые)|бесшовн\w*|холистическ\w*|революционн\w*|передов(ой|ое|ая))"),
    ("ru_filler", "ru", r"(стоит отметить|важно отметить|в современном мире|на сегодняшний день)"),
]
_COMPILED = [(rid, lang, re.compile(pat, re.IGNORECASE | re.MULTILINE)) for rid, lang, pat in _RULES]


def scan(text: str, lang: str = "en") -> dict:
    hits = []
    for rid, rlang, rx in _COMPILED:
        # apply same-language rules; EN rules also run on RU text (anglicisms leak in),
        # but RU rules are not applied to EN text.
        if rlang == "ru" and lang != "ru":
            continue
        for m in rx.finditer(text):
            hits.append({"rule": rid, "lang": rlang, "span": m.group(0).strip()})
    count = len(hits)
    verdict = "clean" if count == 0 else ("review" if count < 3 else "block")
    return {"hits": hits, "count": count, "verdict": verdict}
