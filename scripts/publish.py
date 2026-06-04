"""Gate 08 — Publish & Distribute (the open skeleton).

Two transparent, offline, zero-key helpers for the moment AFTER gate 07 says a
piece is ready:

1. `lint_publish(text, canonical_url=None)` — a pre-publish hygiene check on the
   page you're about to publish (HTML or markdown-with-frontmatter): one canonical
   URL, one H1, Open-Graph tags, Article/BlogPosting JSON-LD, a meta description.
   These are the publishing-side signals that decide whether an AI answer engine
   can fetch + attribute a citation to YOUR url.

2. `distribution_drafts(canonical_url, ...)` — canonical-first adaptation drafts
   for LinkedIn / Medium / dev.to / VC.ru / Dzen / Telegram / X. EVERY draft links
   back to the canonical so the authority compounds on the URL you own, not on a
   silo you rent.

The hosted Humanswith.ai Workspace does the guarded rebuild, the automatic
post-publish re-scan (Hermes), and the Workspace Files sync. This file is the
transparent skeleton — no network, no keys, no Workspace logic.
"""
import re

PLATFORMS = ("linkedin", "medium", "devto", "vcru", "dzen", "telegram", "x")


def _norm_url(u: str) -> str:
    u = (u or "").strip().split("#")[0].split("?")[0]
    u = re.sub(r"^https?://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return u.rstrip("/").lower()


def _same_url(a: str, b: str) -> bool:
    return _norm_url(a) == _norm_url(b)


def _frontmatter(text: str) -> dict:
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def lint_publish(text: str, canonical_url: str | None = None) -> dict:
    """Lint a to-be-published page. Returns
    {format, checks{name: bool|None}, blockers[{severity, check, message}], passed}.
    `passed` is True iff there are no P0 blockers (a P0 = the page can't be reliably
    cited as yours)."""
    is_html = bool(re.search(r"<\s*(html|head|body|link|meta|script|h1)\b", text, re.I))
    checks: dict = {}
    blockers: list = []

    def add(name, ok, sev, msg):
        checks[name] = ok
        if ok is False:
            blockers.append({"severity": sev, "check": name, "message": msg})

    # 1) canonical — the load-bearing publishing-hygiene check
    if is_html:
        m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', text, re.I)
        href = None
        if m:
            h = re.search(r'href=["\']([^"\']+)["\']', m.group(0), re.I)
            href = h.group(1) if h else None
        add("canonical_present", href is not None, "P0",
            'No <link rel="canonical">. An AI engine attributes a citation to one '
            "canonical URL — without it your distributed copies compete with you.")
        if href and canonical_url:
            add("canonical_matches", _same_url(href, canonical_url), "P1",
                f'canonical "{href}" does not match the expected "{canonical_url}".')
    else:
        fm = _frontmatter(text)
        add("canonical_present", "canonical" in fm, "P0",
            "No `canonical:` in frontmatter. Set the one canonical URL before you distribute.")
        if canonical_url and fm.get("canonical"):
            add("canonical_matches", _same_url(fm["canonical"], canonical_url), "P1",
                f'frontmatter canonical "{fm["canonical"]}" does not match the expected '
                f'"{canonical_url}".')

    # 2) exactly one H1
    if is_html:
        n_h1 = len(re.findall(r"<h1\b", text, re.I))
    else:
        n_h1 = len(re.findall(r"^#\s+\S", text, re.M))
    add("single_h1", n_h1 == 1, "P1",
        f"Found {n_h1} H1 heading(s); a citable page needs exactly one "
        "(zero or duplicate H1s confuse answer extraction).")

    # 3) Open Graph tags (control the share card)
    og = ["og:title", "og:description", "og:url"]
    if is_html:
        present = [t for t in og
                   if re.search(rf'(?:property|name)=["\']{re.escape(t)}["\']', text, re.I)]
    else:
        fm = _frontmatter(text)
        present = [t for t in og if fm.get(t.split(":", 1)[1]) or fm.get(t.replace(":", "_"))]
    add("og_tags", len(present) == len(og), "P1",
        f"Missing Open Graph tag(s): {sorted(set(og) - set(present))} — they control "
        "how the social/share card renders.")

    # 4) Article/BlogPosting JSON-LD (strongest AI-citability signal)
    if is_html:
        ld = re.search(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', text, re.I | re.S)
        has_article = bool(ld and re.search(
            r'"@type"\s*:\s*"(Article|BlogPosting|NewsArticle|TechArticle)"', ld.group(1)))
        add("jsonld_article", has_article, "P1",
            "No Article/BlogPosting JSON-LD. Structured data is the single strongest "
            "AI-citability signal.")
    else:
        checks["jsonld_article"] = None  # n/a for raw markdown (usually injected at build)

    # 5) meta description (HTML, soft)
    if is_html:
        add("meta_description",
            bool(re.search(r'<meta[^>]+name=["\']description["\']', text, re.I)), "P2",
            "No meta description — engines fall back to a random page snippet.")

    passed = not any(b["severity"] == "P0" for b in blockers)
    return {"format": "html" if is_html else "markdown",
            "checks": checks, "blockers": blockers, "passed": passed}


def _template(platform: str, url: str, title: str, summary: str) -> str:
    t, s, u = title, summary, url
    if platform == "linkedin":
        return (f"{t}\n\n{s}\n\n"
                "I broke down the full reasoning — data, examples, the decision table — "
                "in the original post.\n\n"
                f"Read it here (original, canonical source): {u}\n\n"
                "#SaaS #AEO #GEO")
    if platform == "medium":
        return (f"# {t}\n\n"
                f"*Originally published at {u} — that page is the canonical version.*\n\n"
                f"{s}\n\n"
                "> Tip: use Medium's “Import a story” with the original URL so Medium "
                "sets rel=canonical back to your site.\n\n"
                f"Full version on the source site: {u}")
    if platform == "devto":
        return ("---\n"
                f"title: {t}\n"
                "published: true\n"
                f"canonical_url: {u}\n"
                "---\n\n"
                f"{s}\n\n"
                f"*Originally published at {u}.*")
    if platform == "vcru":
        return (f"{t}\n\n{s}\n\n"
                f"Полная версия (оригинал, канонический источник): {u}")
    if platform == "dzen":
        return (f"{t}\n\n{s}\n\n"
                f"Источник и полная версия: {u}")
    if platform == "telegram":
        return (f"**{t}**\n\n{s}\n\n"
                f"Полностью → {u}")
    if platform == "x":
        return (f"{t}\n\n{s}\n\n"
                f"🧵 full write-up (original): {u}")
    return f"{t}\n\n{s}\n\nOriginal: {u}"


def distribution_drafts(canonical_url: str, title: str, summary: str,
                        platforms=None) -> dict:
    """Return {platform: draft} canonical-first adaptations. Every draft links back
    to `canonical_url` so the AI-citation authority compounds on the URL you own."""
    if not canonical_url or not str(canonical_url).strip():
        raise ValueError("canonical_url is required — always distribute canonical-first.")
    plats = tuple(platforms) if platforms else PLATFORMS
    return {p: _template(p, canonical_url, title, summary) for p in plats}
