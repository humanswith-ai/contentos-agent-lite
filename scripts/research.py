"""Research providers: Tavily (search) + Firecrawl (read URL) + Serper (SERP/PAA).
All keys optional; no key -> manual-paste fallback. Timeout + never-crash; cache to _work/.cache/."""
import os
import json
import hashlib
import pathlib
import time
import requests

TIMEOUT = 20
CACHE_DIR = pathlib.Path("_work/.cache")


def _cache_get(key: str):
    f = CACHE_DIR / (hashlib.sha1(key.encode()).hexdigest() + ".json")
    if f.exists() and time.time() - f.stat().st_mtime < 6 * 3600:
        return json.loads(f.read_text())
    return None


def _cache_put(key: str, val):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (CACHE_DIR / (hashlib.sha1(key.encode()).hexdigest() + ".json")).write_text(json.dumps(val))


def _tavily(topic: str) -> list[dict]:
    key = os.environ.get("TAVILY_API_KEY")
    if not key:
        return []
    try:
        resp = requests.post("https://api.tavily.com/search",
                             json={"api_key": key, "query": topic, "max_results": 5}, timeout=TIMEOUT)
        resp.raise_for_status()
        return [{"title": x.get("title"), "url": x.get("url"), "content": x.get("content", ""), "date": ""}
                for x in resp.json().get("results", [])]
    except requests.RequestException:
        return []


def _serper(topic: str) -> list[dict]:
    key = os.environ.get("SERPER_API_KEY")
    if not key:
        return []
    try:
        resp = requests.post("https://google.serper.dev/search",
                             headers={"X-API-KEY": key, "Content-Type": "application/json"},
                             json={"q": topic}, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        out = [{"title": o.get("title"), "url": o.get("link"), "content": o.get("snippet", ""), "date": ""}
               for o in data.get("organic", [])[:5]]
        paa = [{"title": q.get("question"), "url": "", "content": q.get("snippet", ""), "date": "", "kind": "paa"}
               for q in data.get("peopleAlsoAsk", [])]
        return out + paa
    except requests.RequestException:
        return []


def _firecrawl(url: str) -> list[dict]:
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        return []
    try:
        resp = requests.post("https://api.firecrawl.dev/v1/scrape",
                             headers={"Authorization": f"Bearer {key}"},
                             json={"url": url, "formats": ["markdown"]}, timeout=TIMEOUT)
        resp.raise_for_status()
        d = resp.json().get("data", {})
        return [{"title": d.get("metadata", {}).get("title", url), "url": url,
                 "content": d.get("markdown", "")[:4000], "date": ""}]
    except requests.RequestException:
        return []


_MANUAL = ("No research keys set. Paste 3-5 sources manually into source_pack.md "
           "(each: fact — URL (date)). Get free keys: Tavily app.tavily.com, "
           "Firecrawl firecrawl.dev, Serper serper.dev (no card).")


def gather(topic: str, urls: list[str] | None = None) -> dict:
    cache_key = f"{topic}|{urls}"
    cached = _cache_get(cache_key)
    if cached:
        return cached
    sources, used = [], []
    t = _tavily(topic)
    if t:
        sources += t
        used.append("tavily")
    s = _serper(topic)
    if s:
        sources += s
        used.append("serper")
    for u in (urls or []):
        f = _firecrawl(u)
        if f:
            sources += f
            if "firecrawl" not in used:
                used.append("firecrawl")
    result = {"sources": sources, "providers_used": used,
              "manual_fallback": None if sources else _MANUAL}
    if sources:
        _cache_put(cache_key, result)
    return result


def to_source_pack_md(result: dict, topic: str) -> str:
    facts, questions = [], []
    for s in result.get("sources", []):
        if s.get("kind") == "paa":
            questions.append(f"- {s['title']}")
        elif s.get("url"):
            snippet = (s.get("content") or "").strip().replace("\n", " ")[:160]
            facts.append(f"- {snippet} — {s['url']} ({s.get('date') or 'n.d.'})")
    return (f"# Source pack — {topic}\n\n## Facts\n" + ("\n".join(facts) or "- (add facts)") +
            "\n\n## Numbers\n- (extract numbers from facts)\n\n## Audience questions\n" +
            ("\n".join(questions) or "- (add audience questions)") +
            "\n\n## Competitor gaps\n- (what competitors miss)\n\n## Founder angle\n- (your unique POV)\n")
