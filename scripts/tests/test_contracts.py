from scripts import contracts

GOOD_PACK = """## Facts
- Stripe processed $1.4 trillion in 2024 — https://stripe.com/annual (2025-01)
- OpenAI launched ChatGPT in 2022 — https://openai.com/blog/chatgpt (2022-11)

## Numbers
- 1.4 trillion
## Audience questions
- How do founders pick a payment stack?
## Competitor gaps
- Nobody explains fees plainly.
## Founder angle
- We migrated 3 SaaS to Stripe.
"""

BAD_PACK = """## Facts
- Stripe is the best payment processor ever.

## Numbers
## Audience questions
## Competitor gaps
## Founder angle
"""


def test_source_pack_ok():
    r = contracts.validate_source_pack(GOOD_PACK)
    assert r["ok"] is True
    assert r["missing"] == []
    assert r["facts_without_source"] == []


def test_source_pack_fact_without_source_is_flagged():
    r = contracts.validate_source_pack(BAD_PACK)
    assert r["ok"] is False
    assert "Stripe is the best payment processor ever." in r["facts_without_source"]


def test_source_pack_missing_section():
    r = contracts.validate_source_pack("## Facts\n- a — http://x (2024)\n")
    assert r["ok"] is False
    assert "Numbers" in r["missing"]


GOOD_BRIEF = """Audience: Series A founders
Goal: drive demo signups
Format: LinkedIn post
Angle: migration pain
Structure: hook / proof / CTA
Must-mention: Stripe $1.4T fact
Forbidden: hype adjectives
CTA: book a demo
Success criteria: 5 qualified replies
"""


def test_brief_ok():
    assert contracts.validate_brief(GOOD_BRIEF)["ok"] is True


def test_brief_missing_cta():
    r = contracts.validate_brief(
        "Audience: x\nGoal: y\nFormat: z\nAngle: a\nStructure: b\nMust-mention: c\nForbidden: d\nSuccess criteria: e\n"
    )
    assert r["ok"] is False
    assert "CTA" in r["missing"]
