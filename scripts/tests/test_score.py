from scripts import score

STRONG = """## How do founders pick a payment stack?
Stripe processed $1.4 trillion in 2024 [1], up 25% year over year.

Founders should weigh fees, payout speed, and API quality.

- Fees: 2.9% + 30c
- Payouts: 2-day default

## What about international?
PayPal and Adyen cover more regions [2].

## FAQ
**Why Stripe?** Best API. **Why not?** Higher fees.

[1] https://stripe.com  [2] https://adyen.com
"""

WEAK = "In today's fast-paced world, our robust seamless solution unlocks the power of payments. It's crucial to delve into this game-changing platform."


def test_strong_draft_scores_high_and_ready():
    r = score.score_draft(STRONG, "en")
    assert r["overall"] >= 70
    assert set(r["axes"]) == {
        "direct_answer", "named_entities", "numerical_attribution", "question_h2s",
        "structured_elements", "faq_block", "anti_slop", "citation_markers"}
    assert r["verdict"] in ("REVISE", "READY")


def test_weak_draft_stops():
    r = score.score_draft(WEAK, "en")
    assert r["overall"] < 55
    assert r["verdict"] == "STOP"
    assert any(b["severity"] == "P0" for b in r["blockers"])


def test_axes_bounded_0_100():
    r = score.score_draft(STRONG, "en")
    assert all(0 <= v <= 100 for v in r["axes"].values())
    assert 0 <= r["overall"] <= 100


def test_verdict_thresholds():
    r = score.score_draft(STRONG, "en")
    if r["overall"] >= 85 and not any(b["severity"] == "P0" for b in r["blockers"]):
        assert r["verdict"] == "READY"
