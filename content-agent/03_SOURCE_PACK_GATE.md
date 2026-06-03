# 03 · Source Pack Gate — the citable backbone

Assemble `_work/source_pack.md`. This is the **only** material the draft may draw facts from.

## Required shape (required sections filled; Intent + Competitor gaps are optional)

```markdown
## Facts
- <fact> — <source URL> (<date>)        # EVERY fact line needs a source token (URL or (YYYY)
- ...                                     # aim for ~10

## Numbers
- <number + what it measures>             # aim for ~3, each traceable to a fact above

## Audience questions
- <question>                              # aim for ~5

## Intent / queries                       # optional — auto-filled from Serper PAA + related searches
- <what your audience actually searches>  # shape the angle + audience questions around these

## Competitor gaps                        # optional — a bonus angle, not required
- <what competitors miss>

## Founder angle
- <your unique POV from 01>
```

## Validate (deterministic, optional)

If the scripts are installed, the agent can check the shape:
```
python -m scripts.cli  # (the source-pack validator is also exposed in scripts/contracts.py)
```
Or validate by eye against the rules below.

## The hard rule

**A fact without a source is a P0.** "Our product is the best" with no source is not a fact —
it's a claim, and it stops the process. Either source it or cut it.

---

```
GATE 03 — Source Pack
Score:   <0-100>   (completeness + every fact sourced)
Status:  READY | REVISE | STOP
Blockers:
  - [P0] A fact has no source.
  - [P0] A required section (Facts/Numbers/Audience questions/Founder angle) is empty.
Next step: if READY → build 04_BRIEF_READINESS_GATE.md
```
