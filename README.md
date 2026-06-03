# ContentOS Agent Lite — open-source AI content agent for founders

[![CI](https://github.com/humanswith-ai/contentos-agent-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/humanswith-ai/contentos-agent-lite/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)

**ContentOS Agent Lite is an open-source AI content agent for founders that writes from a verifiable
_process, not a prompt_.** It walks your coding agent through **7 gates**: context → sources → brief →
draft → checks → uplift → publish. Every draft gets a transparent **0–100 score across 8 axes**,
locally, in your terminal. It's a free, self-hosted alternative to one-shot AI writers. It runs in
**Claude Code / Cursor / Codex** with **zero API keys**, and gets sharper with a free research key.
It scores English, Russian, and Arabic content.

> **Honest scope:** this is a _skeleton of the content process_, not a full platform. It won't
> guarantee search rankings, do multi-source fact-checking, or run a learning loop. What it gives you:
> text that is **grounded, checked, and in your voice** — and a folder you keep and reuse.

## Why it's different

- **Process, not prompt.** Seven gates (`00`–`07`). Each emits a score (0–100), a status
  (READY · REVISE · STOP), blockers (P0 · P1), and the next step.
- **No draft before the work is done.** The agent may not write until business context, research,
  the source pack, and the brief all pass. A fact without a source is a hard stop.
- **Deterministic where it counts.** A tiny optional Python layer scores the draft and flags
  AI-slop the same way every time — quality isn't the model's mood.
- **Runs with zero keys.** Inside Claude Code / Cursor / Codex the agent _is_ the model.

## Quickstart (60 seconds)

```bash
git clone https://github.com/humanswith-ai/contentos-agent-lite
cd contentos-agent-lite

# (optional) the deterministic helpers — needs only Python:
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# (optional) free research keys — each optional; Serper needs no card:
cp .env.example .env   # fill any of TAVILY_API_KEY / FIRECRAWL_API_KEY / SERPER_API_KEY
```

Then in **Claude Code / Cursor / Codex**, open the `content-agent/` folder and say:

> *"Act as my content agent. Follow gates `00`→`07`. My topic is: **\<your topic\>**."*

Drop the agent into any of your own projects with `python -m scripts.cli init --into <dir>`. It
scaffolds `content-agent/` **and teaches your project's coding agent** — a managed block in
`CLAUDE.md` / `AGENTS.md` (re-runnable, your own content preserved) — so you can just say
*"write a post about …"* and it follows the gates.

## How it works — the 7 gates

| File | Step | Hard stop (P0) |
|---|---|---|
| `00_FOUNDER_CONTENT_AGENT.md` | operating contract | writes a draft before 01–04 pass |
| `01_BUSINESS_CONTEXT.md` | ICP / offer / proof / voice / claim policy | no ICP, offer, or claim policy |
| `02_RESEARCH_GATE.md` | gather + score real sources | everything rests on weak sources |
| `03_SOURCE_PACK_GATE.md` | the citable backbone | a fact with no source |
| `04_BRIEF_READINESS_GATE.md` | the brief | missing audience / goal / angle / CTA |
| `05_DRAFT_QUALITY_GATE.md` | write from sources, score it | claim not in source pack; score < 55 |
| `06_EDITORIAL_UPLIFT_GATE.md` | improve — no new facts | uplift invented a fact |
| `07_PUBLISH_READINESS_GATE.md` | go / no-go | score < 85 or any P0 |

Optional deterministic helpers:

```bash
python -m scripts.cli research --topic "payment stacks for founders"   # → source-pack draft
python -m scripts.cli score    --file content-agent/_work/draft.md     # → 0-100 + blockers
python -m scripts.cli check    --file content-agent/_work/draft.md     # → anti-slop + score
```

Research uses whichever free key you set: [Tavily](https://app.tavily.com) (search),
[Firecrawl](https://firecrawl.dev) (read a URL), [Serper](https://serper.dev) (SERP / People-Also-Ask,
free, no card). With no key, the agent does the research itself.

## How it's different from one-shot AI writers

| | **ContentOS Agent Lite** | One-shot AI writers (paste a prompt) |
|---|---|---|
| How text is produced | a 7-gate **process**: sources → brief → draft → checks | one prompt → one draft |
| Grounding | a fact without a source is a hard stop | will confidently make things up |
| Quality signal | transparent 0–100 score, 8 axes, you can read the code | a black box |
| Where it runs | your IDE (Claude Code / Cursor / Codex), local | a web app |
| Cost | free, open-source (MIT), bring-your-own keys | subscription |

This is an honest skeleton — it does the *process*, not a feature-complete writing suite. For the
managed pipeline (per-engine AEO, deep fact-check, best-of-N, team scale, hosting), see below.

## Free vs the hosted workspace

| | **ContentOS Agent Lite** (this repo, free) | **Humanswith.ai ContentOS** (hosted) |
|---|---|---|
| The gate process | ✅ | ✅ |
| Research | your key, one pass | managed, multi-tier |
| Quality score | transparent single heuristic | per-engine AEO (ChatGPT / Perplexity / Gemini / AI Overview) |
| Fact-check | source-presence discipline | KG + NLI + deep-verify |
| Best-of-N variants | — | LLM-judge tournament |
| Languages | EN / RU / AR content scoring | EN / RU / AR native pipelines |
| Team scale, hosting, learning loop | self-run | managed |

Outgrow the skeleton? → **[See ContentOS for your category](https://humanswith.ai/platform/contentos/)**.

## FAQ

### Is it free?
Yes — MIT-licensed and open-source. You bring your own (free-tier) keys if you want the deterministic
research/scoring helpers; otherwise it runs with no keys at all.

### Do I need an API key?
No. Inside Claude Code / Cursor / Codex the agent is the model. A free Tavily / Firecrawl / Serper key
only makes the `research` and `score` steps deterministic and repeatable.

### How is this different from the hosted Humanswith.ai ContentOS?
Lite is the open-source _skeleton_ of the process. The hosted [ContentOS](https://humanswith.ai/platform/contentos/)
adds per-engine AEO scoring, KG + NLI + deep fact-check, a best-of-N judge tournament, native EN/RU/AR
pipelines, team scale, and managed hosting.

### Does it guarantee SEO or AI search rankings?
No. It improves how grounded, structured, and citable your text is — it does not promise positions.
Anyone claiming a tool guarantees rankings is selling you something.

### Does it work for Russian or Arabic content?
Yes. The scorer and anti-slop scanner accept `--lang ru` (Russian) and `--lang ar` (Arabic) — the
repo docs themselves are English. Arabic detection covers MSA clichés, «حشو» filler, and dialect
markers, and reads the Arabic question mark (؟). Deep native EN/RU/AR pipelines are the hosted ContentOS.

### What is AEO / GEO?
Answer-Engine / Generative-Engine Optimization: writing so AI search (ChatGPT, Perplexity, Gemini,
Google AI Overviews) can cite you — clear answers, named entities, sourced numbers, structure.

## Contributing & license

Issues and PRs welcome. MIT — [LICENSE](LICENSE). Security: [SECURITY.md](SECURITY.md) ·
verify before install: [TRUST.md](TRUST.md).

## Built by

[**Gregory Shevchenko**](https://github.com/g-shevchenko), founder of [**Humanswith.ai**](https://humanswith.ai).
Born from the R-Founders "content agent for founders" workshop · MIT · © 2026 Humanswith.ai
