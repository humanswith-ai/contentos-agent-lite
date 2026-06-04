# 08 · Publish & Distribute Gate — canonical-first, backlink-always

Gate 07 said the *words* are ready. This gate is about publishing them so an AI answer
engine can **fetch and attribute the citation to a URL you own** — and distributing them
without your rented silos out-ranking your own page.

Two moves, in order.

## A. Publish on your own site first (the canonical)

Before you press publish, lint the page. With the `scripts/` layer:

```
python -m scripts.cli publish --file dist/your-post/index.html --canonical https://you.com/your-post/
```

(or do it by hand from this checklist):

```
[ ] exactly ONE <link rel="canonical"> → your own URL          (P0 — without it, copies compete with you)
[ ] exactly ONE <h1>                                            (P1 — zero/duplicate H1 breaks extraction)
[ ] Open Graph: og:title, og:description, og:url                (P1 — controls the share card)
[ ] Article / BlogPosting JSON-LD                               (P1 — the strongest AI-citability signal)
[ ] meta description                                            (P2 — else the engine picks a random snippet)
[ ] the page is in sitemap.xml and not blocked by robots/noindex
```

**P0 fails block publish.** Publish the canonical, confirm it returns 200 and renders, then —
and only then — distribute.

## B. Distribute canonical-first (every copy backlinks the original)

Generate adaptation drafts that all point back to the canonical:

```
python -m scripts.cli publish --canonical https://you.com/your-post/ \
  --distribute --title "Your headline" --summary "One-line summary." \
  --file dist/your-post/index.html
```

You get a canonical-first draft per platform — **LinkedIn, Medium, dev.to, VC.ru, Dzen,
Telegram, X** — each ending in a link to the original. The rule never changes:

- **Publish on your domain first.** The canonical accrues the authority and the citations.
- **Every silo copy links back** to the canonical. On Medium use *Import a story* (sets
  rel=canonical); on dev.to set `canonical_url`. A copy with no backlink cannibalises you.
- **Adapt, don't paste.** Re-hook for each audience; keep the claim/number set identical to
  the canonical (no new unsourced facts — that would reopen gate 02/03).

## What this gate does NOT do

It does not publish for you, it does not rebuild your site, and it does not re-measure
whether AI engines started citing you. It gives you a clean pre-publish lint + canonical-first
drafts — the manual skeleton.

---

```
GATE 08 — Publish & Distribute
Lint:    PASS | FAIL   (FAIL = an unresolved P0, e.g. missing canonical)
Canonical: <your owned URL>
Distribution: drafts generated, every copy backlinks the canonical
Next step:
  - PASS → publish the canonical (your call — the agent never auto-publishes), then post the
           backlinked adaptations.
  - FAIL → fix the P0 (usually: add the canonical), re-lint.
```

**The agent never publishes for you.** It hands you a linted page + canonical-first drafts;
you press the button. The hosted version does the **guarded rebuild**, the **automatic
post-publish re-scan** (did AI engines start citing you?), and the **Workspace Files** sync —
see the repo README → https://humanswith.ai/platform/content-publisher/.
