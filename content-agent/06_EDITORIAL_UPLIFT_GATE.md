# 06 · Editorial Uplift Gate — improve without inventing

Raise the draft's quality. You may improve **clarity, structure, flow, and the CTA**. You may
**NOT add a fact that isn't in `source_pack.md`** and you may **NOT strengthen a claim beyond its
source**. Uplift is editing, not embellishing.

## Do
- Tighten the opening so it answers first.
- Fix structure: question-style H2s, short paragraphs, a list/table where it helps, a clear CTA.
- Run an anti-slop pass — cut filler, hype adjectives, and AI tells.

## Anti-slop check

**Deterministic (optional):**
```
python -m scripts.cli check --file _work/draft.md --lang en
```
`check` runs the anti-slop scanner (flags "delve", "in today's fast-paced world", "robust seamless",
"game-changing", sycophantic openings, etc.) **and** re-scores. ≥3 slop hits = block.

**By judgment (always):** would a sharp reader smell AI? Remove it.

## Hard rule
If the uplift introduced any fact not in the source pack, that's a **P0** — revert it or source it.

---

```
GATE 06 — Editorial Uplift
Score:   <0-100>   (should be >= the gate-05 score)
Status:  READY | REVISE | STOP
Blockers:
  - [P0] Uplift introduced an unsourced fact or over-strengthened a claim.
  - [P1] Anti-slop hits remain.
Next step: → 07_PUBLISH_READINESS_GATE.md
```
