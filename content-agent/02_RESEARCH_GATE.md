# 02 · Research Gate — gather real sources

Goal: collect enough real material that the piece can be **grounded and citable**, then judge
whether it's strong enough to write from. No sources → no draft.

## How to gather (pick what's available)

**A. With a free key (deterministic):**
```
python -m scripts.cli research --topic "<your topic>"
```
This uses whichever of Tavily / Firecrawl / Serper keys you set (`.env`) and prints a
`source_pack` draft (URLs + snippets + People-Also-Ask). Paste it into `_work/source_pack.md`.

**B. Zero keys (agent does it):** the agent searches/reads with its own tools, or you paste the
5-10 links + notes you prepared. The workshop homework — *your site, your best content on the
topic, 1-2 authoritative sources, one audience observation, one topic (a competitor or two
optional)* — is exactly this input.

## Score each source (credibility)

For every source, note: **first-party / reputable / weak**. A piece resting only on weak sources
(SEO blogspam, undated claims, your own marketing) is a P0 — get at least some first-party or
reputable material.

## Extract while you research
- **Audience questions** the piece should answer (aim for 5).
- **Competitor gaps** *(optional)* — what competitors all say vs what they all miss (a bonus angle).
- **Numbers with a source** — these become your citable backbone.

---

```
GATE 02 — Research
Score:   <0-100>   (coverage + source credibility)
Status:  READY | REVISE | STOP
Blockers:
  - [P0] Everything rests on weak/undated sources, or there is no real material.
Next step: if READY → assemble 03_SOURCE_PACK_GATE.md
```

**STOP condition:** if you cannot point to at least a few credible, dated sources, stop. Writing
on top of weak sources just produces confident, wrong text.
