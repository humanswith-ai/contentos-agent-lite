# Architecture Gate — ContentOS Agent Lite

> Contracts first, prompts last. This is the transparent, public record of what the
> LLM (the founder's coding agent) owns versus what code owns in this tool — so the
> gates are *enforced*, not eyeballed. Every file named here is in this repo.

## Task class
`side_effecting_workflow` + `agent_workflow` with an LLM-backed surface: the founder's
coding agent walks the markdown gates (`content-agent/00`–`07`), while a thin Python
layer does deterministic scoring, anti-slop, research, and project scaffolding. The
full architecture gate was applied at design time; this document is its materialized,
public record.

## LLM-owned (judgment, constrained by the gate prose)
Reading sources, assembling the source pack, writing the brief, writing the draft, and
editorial uplift. These are inherently model tasks. The gates constrain them (no draft
before gates `01`–`04` pass; a fact without a source is a hard stop) — they do not
replace the model's judgment.

## Code-owned (deterministic, so the numbers aren't the model's mood)
- **Scoring** — `scripts/score.py`: the transparent 0–100, per-axis (8 axes), P0/P1
  blockers, and verdict, as a stable JSON contract. The numbers and the STOP/GO
  arithmetic are code, not LLM opinion.
- **Anti-slop** — `scripts/antislop.py`: deterministic regex rules (EN, plus RU/AR for
  user content), hit count + verdict.
- **Working-file shapes** — `scripts/contracts.py`: a gate refuses to advance if the
  prior artifact is incomplete (e.g. a `source_pack` fact with no source token).
- **Side effects** — `scripts/research.py` (network, with explicit timeout, graceful
  no-key fallback, on-disk cache, never crash) and `scripts/cli.py init` (scaffolds the
  folder + teaches the project; writes only inside the target project — see `TRUST.md`).

## Required schemas
- Working files in `content-agent/_work/`: `source_pack.md`, `brief.md`, `draft.md`,
  `qa_report.md`, each with required sections enforced by `contracts.py`.
- `score.py` JSON: `{ "overall": 0-100, "axes": {<axis>: 0-100}, "blockers":
  [{ "severity": "P0|P1", "axis", "message", "fix_hint" }], "verdict": "READY|REVISE|STOP" }`.
- The managed teaching block written by `init` (between
  `<!-- BEGIN/END contentos-agent-lite -->` markers) — idempotent and content-preserving.

## Required validators
- `contracts.validate_source_pack` / `validate_brief` — presence + every fact sourced.
- `score.score_draft` (pure, deterministic) and `antislop.scan` (deterministic).
- `scripts/agent-preinstall-check.sh` — declared write-paths + secret scan (no network).
- `scripts/build_llms_full.py` is drift-guarded by a sync test.

## Required golden cases
- A **negative golden**: a source pack whose fact lacks a source MUST validate as a hard
  STOP / P0 — proving the gate enforces rather than suggests (`scripts/tests/`).
- Scorer, anti-slop, research-fallback, CLI, agent-docs, and llms-full tests run under
  `pytest`, written tests-first (TDD, verify-red).

## Proof gate ("accepted")
1. Fresh clone (zero keys agent-only, or one free key) → topic → `draft.md`, and
   `score.py` returns a deterministic 0–100 + verdict.
2. The negative golden returns STOP / P0.
3. `pytest` green; `agent-preinstall-check.sh` passes; no secrets / private references.

## Human gate
The agent **never auto-publishes** — it hands the founder a `READY` piece + a QA report;
the founder presses the button.
