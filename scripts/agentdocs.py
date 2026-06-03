"""Teach the target project: write a managed teaching block + trigger vocabulary
into the user's CLAUDE.md and AGENTS.md so a beginner can invoke the content agent
in natural language, without knowing the gate filenames or CLI.

Per repo-release-packaging "one-command install must teach the target workspace".
The block lives between stable markers so `init` can refresh it idempotently
without clobbering the user's own content.
"""
import pathlib

BEGIN_MARKER = "<!-- BEGIN contentos-agent-lite -->"
END_MARKER = "<!-- END contentos-agent-lite -->"

AGENT_DOC_NAMES = ("CLAUDE.md", "AGENTS.md")

# What a coding agent (Claude Code / Cursor / Codex) in the user's project reads.
# English-only by design (the repo is EN; the scorer still accepts RU/AR user
# content via --lang). Keep it tight — it is injected into the agent's context.
TEACHING_BLOCK = """\
## Content agent (ContentOS Agent Lite)

This project ships a **content agent** in `content-agent/`. When you (the AI
assistant) are asked to produce marketing or founder content, do **not** free-write
from one prompt. Act as the content agent and follow its gates: good text comes from
a *process* (context -> sources -> brief -> draft -> checks -> uplift), not a guess.

**When to run it — treat any of these (in any language) as "run the content agent":**
- "write a post about ..." / "draft a LinkedIn or Telegram post"
- "write a founder letter" / "warm-up email" / "sales email"
- "write a landing block" / "hero / offer section"
- "act as my content agent" / "run the content gates" / "use the content agent"

**How to run it:**
1. Read `content-agent/00_FOUNDER_CONTENT_AGENT.md` first — it is the operating contract.
2. Walk gates `01` -> `07` in order, writing working files into `content-agent/_work/`.
3. **Iron rule: no draft before gates `01`-`04` pass.** A fact without a source is a hard STOP;
   never invent facts to fill a draft.
4. Optional deterministic helpers (only if Python + a free key are set):
   - `python -m scripts.cli research --topic "<topic>"`  (source-pack draft)
   - `python -m scripts.cli score   --file content-agent/_work/draft.md`  (0-100 + blockers)
   - `python -m scripts.cli check   --file content-agent/_work/draft.md`  (anti-slop + score)

Honest scope: this is a *skeleton* of a content process, not a guarantee of rankings.
The managed version (per-engine AEO, deep fact-check, team scale) is at
https://humanswith.ai/platform/contentos/
"""


def upsert_block(existing, block_body):
    """Insert or refresh the managed teaching block in `existing`, idempotently.

    - Markers already present -> replace only the block, preserving text before/after.
    - File non-empty, no markers -> append the block (keeps the user's content).
    - Empty/new file -> the block becomes the content.
    """
    block = f"{BEGIN_MARKER}\n{block_body.strip()}\n{END_MARKER}"
    if BEGIN_MARKER in existing and END_MARKER in existing:
        pre, _, rest = existing.partition(BEGIN_MARKER)
        _, _, post = rest.partition(END_MARKER)
        return f"{pre}{block}{post}"
    if existing.strip():
        return f"{existing.rstrip()}\n\n{block}\n"
    return f"{block}\n"


def write_agent_docs(into):
    """Write/refresh the managed block in <into>/CLAUDE.md and <into>/AGENTS.md.

    Returns the list of file paths written (as strings)."""
    into = pathlib.Path(into)
    into.mkdir(parents=True, exist_ok=True)
    written = []
    for name in AGENT_DOC_NAMES:
        path = into / name
        existing = path.read_text() if path.exists() else ""
        path.write_text(upsert_block(existing, TEACHING_BLOCK))
        written.append(str(path))
    return written
