# content-agent/

A portable content agent you run inside **Claude Code, Cursor, or Codex**. It writes from a
**process, not a prompt**: context → sources → brief → draft → checks → uplift, with a gate after
each step.

## Use it

1. Open this folder in your agent.
2. Say: *"Act as my content agent. Follow gates `00`→`07`. My topic is: <topic>."*
3. Fill `01_BUSINESS_CONTEXT.md` once. The agent walks the gates and writes into `_work/`.

Start with `00_FOUNDER_CONTENT_AGENT.md` — it's the operating contract.

## Gates

| File | Step |
|---|---|
| `00_FOUNDER_CONTENT_AGENT.md` | operating contract (read first) |
| `01_BUSINESS_CONTEXT.md` | ICP / offer / proof / voice / claim policy (fill once) |
| `02_RESEARCH_GATE.md` | gather + score real sources |
| `03_SOURCE_PACK_GATE.md` | assemble the citable backbone |
| `04_BRIEF_READINESS_GATE.md` | the brief (no draft before this passes) |
| `05_DRAFT_QUALITY_GATE.md` | write from the source pack; score it |
| `06_EDITORIAL_UPLIFT_GATE.md` | improve clarity/structure/CTA — no new facts |
| `07_PUBLISH_READINESS_GATE.md` | publish only at 85+ and no P0 |

## Working files (`_work/`)

`source_pack.md` · `brief.md` · `draft.md` · `qa_report.md` — the agent fills these as it goes.

## Optional deterministic helpers

With the `scripts/` layer installed and a free key (`.env`), the agent can run
`research` / `score` / `check`. **None are required** — with zero keys the agent does every gate
itself. See the repo README for the full setup and the hosted version.
