"""Review-pass changes: publish threshold 85 -> 72; competitor gaps optional."""
from scripts import score, contracts


def test_publish_threshold_is_72():
    # Real ContentOS publishes ~72+ for most formats; a blanket 85 fails too much.
    assert getattr(score, "READY_THRESHOLD", 85) == 72


def test_verdict_honors_threshold_param():
    strong = ("## How do founders pick a stack?\nStripe did $1.4T in 2024 [1].\n\n"
              "- fees 2.9%\n\n## FAQ\n**Why?** API.\n\n[1] https://stripe.com\n")
    r = score.score_draft(strong, "en")
    assert r["verdict"] == "READY"  # default 72 bar
    strict = score.score_draft(strong, "en", ready_threshold=r["overall"] + 5)
    assert strict["verdict"] == "REVISE"  # raising the bar above its score flips it


PACK_NO_COMPETITORS = """## Facts
- Stripe processed $1.4T in 2024 — https://stripe.com (2025)
## Numbers
- 1.4 trillion
## Audience questions
- How do founders pick a payment stack?
## Founder angle
- We migrated 3 SaaS to Stripe.
"""


def test_competitor_gaps_is_optional():
    # Competitors are optional; own knowledge base + content sources are the requirement.
    r = contracts.validate_source_pack(PACK_NO_COMPETITORS)
    assert r["ok"] is True
    assert "Competitor gaps" not in r["missing"]
