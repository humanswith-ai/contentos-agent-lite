import responses
from scripts import research


def test_no_keys_returns_manual_fallback(monkeypatch):
    for k in ("TAVILY_API_KEY", "FIRECRAWL_API_KEY", "SERPER_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    r = research.gather("payment stacks for founders")
    assert r["providers_used"] == []
    assert r["manual_fallback"] is not None
    assert "paste" in r["manual_fallback"].lower()


@responses.activate
def test_tavily_used_when_key_present(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    monkeypatch.delenv("SERPER_API_KEY", raising=False)
    responses.add(
        responses.POST, "https://api.tavily.com/search",
        json={"results": [{"title": "Stripe", "url": "https://stripe.com", "content": "fees"}]}, status=200)
    r = research.gather("payments")
    assert "tavily" in r["providers_used"]
    assert r["sources"][0]["url"] == "https://stripe.com"


def test_to_source_pack_md_shape():
    md = research.to_source_pack_md(
        {"sources": [{"title": "Stripe", "url": "https://stripe.com", "content": "Stripe processed $1.4T", "date": "2024"}],
         "manual_fallback": None, "providers_used": ["tavily"]}, "payments")
    assert "## Facts" in md and "https://stripe.com" in md and "## Audience questions" in md


def test_intent_block_includes_paa_and_related():
    md = research.to_source_pack_md({
        "sources": [
            {"title": "How do founders pick a stack?", "url": "", "content": "", "kind": "paa"},
            {"title": "best payment processor for startups", "url": "", "content": "", "kind": "related"},
        ], "manual_fallback": None, "providers_used": ["serper"]}, "payments")
    assert "## Intent / queries" in md
    assert "best payment processor for startups" in md  # related search surfaced
    assert "How do founders pick a stack?" in md         # PAA surfaced as intent too


@responses.activate
def test_serper_captures_related_searches(monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test")
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    responses.add(
        responses.POST, "https://google.serper.dev/search",
        json={"organic": [{"title": "S", "link": "https://s.com", "snippet": "x"}],
              "peopleAlsoAsk": [{"question": "Why Stripe?", "snippet": "api"}],
              "relatedSearches": [{"query": "stripe vs adyen"}]}, status=200)
    r = research.gather("payments")
    kinds = [s.get("kind") for s in r["sources"]]
    assert "related" in kinds
    assert any(s.get("title") == "stripe vs adyen" for s in r["sources"])
