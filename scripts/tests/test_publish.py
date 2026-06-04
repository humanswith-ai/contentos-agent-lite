"""Gate 08 — Publish & Distribute. TDD: these are written before scripts/publish.py
is implemented (verify-red), then the implementation is made to satisfy them."""
import json as _json
from scripts import publish, cli

GOOD_HTML = """<!doctype html><html><head>
<title>Best payment stack for SaaS</title>
<meta name="description" content="A 2026 comparison of payment stacks for SaaS founders.">
<link rel="canonical" href="https://example.com/blog/payment-stack/">
<meta property="og:title" content="Best payment stack for SaaS">
<meta property="og:description" content="A 2026 comparison.">
<meta property="og:url" content="https://example.com/blog/payment-stack/">
<meta property="og:image" content="https://example.com/og/payment.png">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BlogPosting","headline":"Best payment stack for SaaS"}</script>
</head><body><h1>Best payment stack for SaaS</h1><p>Stripe leads...</p></body></html>"""

NO_CANONICAL_HTML = """<!doctype html><html><head>
<title>Untitled</title><meta property="og:title" content="x"></head>
<body><h1>One</h1></body></html>"""

DUP_H1_HTML = GOOD_HTML.replace("<p>Stripe leads...</p>", "<h1>Second heading</h1><p>x</p>")

BAD_JSONLD_HTML = GOOD_HTML.replace('"@type":"BlogPosting"', '"@type":"WebSite"')

GOOD_MD = """---
title: Best payment stack for SaaS
description: A 2026 comparison.
canonical: https://example.com/blog/payment-stack/
---
# Best payment stack for SaaS

Stripe leads...
"""

NO_CANONICAL_MD = """---
title: Best payment stack
---
# Best payment stack

Body.
"""

CANON = "https://example.com/blog/payment-stack/"


# ---------- lint: canonical (the load-bearing publishing-hygiene check) ----------
def test_lint_good_html_passes_no_p0():
    r = publish.lint_publish(GOOD_HTML)
    assert r["format"] == "html"
    assert r["passed"] is True
    assert not [b for b in r["blockers"] if b["severity"] == "P0"]


def test_lint_missing_canonical_html_is_p0():
    r = publish.lint_publish(NO_CANONICAL_HTML)
    assert r["passed"] is False
    p0 = [b for b in r["blockers"] if b["severity"] == "P0"]
    assert any(b["check"] == "canonical_present" for b in p0)


def test_lint_missing_canonical_markdown_is_p0():
    r = publish.lint_publish(NO_CANONICAL_MD)
    assert r["format"] == "markdown"
    assert r["passed"] is False
    assert any(b["check"] == "canonical_present" for b in r["blockers"])


def test_lint_good_markdown_passes():
    r = publish.lint_publish(GOOD_MD)
    assert r["format"] == "markdown"
    assert r["passed"] is True
    assert r["checks"]["canonical_present"] is True


def test_lint_duplicate_h1_blocks():
    r = publish.lint_publish(DUP_H1_HTML)
    assert r["checks"]["single_h1"] is False
    assert any(b["check"] == "single_h1" for b in r["blockers"])


def test_lint_jsonld_must_be_article_type():
    assert publish.lint_publish(GOOD_HTML)["checks"]["jsonld_article"] is True
    assert publish.lint_publish(BAD_JSONLD_HTML)["checks"]["jsonld_article"] is False


def test_lint_canonical_mismatch_when_expected_given():
    r = publish.lint_publish(GOOD_HTML, canonical_url="https://example.com/OTHER/")
    assert r["checks"].get("canonical_matches") is False
    assert any(b["check"] == "canonical_matches" for b in r["blockers"])


def test_lint_canonical_match_ignores_trailing_slash_and_www():
    r = publish.lint_publish(GOOD_HTML, canonical_url="https://www.example.com/blog/payment-stack")
    assert r["checks"].get("canonical_matches") is True


# ---------- distribution: canonical-first, backlink-always ----------
def test_distribution_returns_all_platforms_by_default():
    d = publish.distribution_drafts(CANON, "Title", "Summary.")
    for p in ("linkedin", "medium", "devto", "vcru", "dzen", "telegram", "x"):
        assert p in d and d[p].strip()


def test_every_draft_backlinks_the_canonical():
    d = publish.distribution_drafts(CANON, "Title", "Summary.")
    for platform, body in d.items():
        assert CANON in body, f"{platform} draft is missing the canonical backlink"


def test_drafts_include_title_and_summary():
    d = publish.distribution_drafts(CANON, "My Unique Title", "My unique summary text.")
    for body in d.values():
        assert "My Unique Title" in body
        assert "My unique summary text." in body


def test_distribution_requires_canonical():
    try:
        publish.distribution_drafts("", "T", "S")
        raised = False
    except ValueError:
        raised = True
    assert raised, "distribution_drafts must refuse an empty canonical (canonical-first rule)"


def test_distribution_respects_platform_subset():
    d = publish.distribution_drafts(CANON, "T", "S", platforms=["linkedin", "x"])
    assert set(d.keys()) == {"linkedin", "x"}


# ---------- CLI glue ----------
def test_cli_publish_lint_good_html(tmp_path, capsys):
    f = tmp_path / "page.html"
    f.write_text(GOOD_HTML)
    rc = cli.main(["publish", "--file", str(f), "--json"])
    out = _json.loads(capsys.readouterr().out)
    assert rc == 0 and out["lint"]["passed"] is True


def test_cli_publish_bad_returns_1(tmp_path):
    f = tmp_path / "bad.html"
    f.write_text(NO_CANONICAL_HTML)
    assert cli.main(["publish", "--file", str(f), "--json"]) == 1


def test_cli_publish_distribute_subset(tmp_path, capsys):
    f = tmp_path / "page.html"
    f.write_text(GOOD_HTML)
    rc = cli.main(["publish", "--file", str(f), "--canonical", CANON,
                   "--distribute", "--title", "T", "--summary", "S",
                   "--platforms", "linkedin,x", "--json"])
    out = _json.loads(capsys.readouterr().out)
    assert rc == 0
    assert set(out["distribution"].keys()) == {"linkedin", "x"}
    assert all(CANON in v for v in out["distribution"].values())
