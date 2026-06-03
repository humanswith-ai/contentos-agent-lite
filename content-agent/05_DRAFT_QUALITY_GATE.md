# 05 · Draft Quality Gate — write from sources, then score

Now — and only now — write `_work/draft.md`, following `brief.md`, using facts **only** from
`source_pack.md`. Then score it. Do not polish yet (that's `06`).

## Writing rules
- Every factual claim must trace to a `source_pack.md` fact. If you reach for a fact that isn't
  there, STOP and go back to `02`/`03` — do not invent it.
- Answer first: lead with the point, not a throat-clearing intro.
- Use the source pack's numbers and name real entities — that's what makes text citable.
- Match the brand voice from `01`.

## Score it

**Deterministic (optional):**
```
python -m scripts.cli score --file _work/draft.md --lang en
```
Returns a 0-100 overall + 8 axes (direct answer, named entities, numerical attribution,
question-style H2s, structured elements, FAQ, anti-slop, citation markers) + blockers + verdict.

**By judgment (always):** score the same axes yourself: does it answer fast, name real things,
cite numbers, use structure, avoid AI-slop, stay in voice, and is it actually useful?

## Verdict thresholds
- **< 55 → STOP** (P0): too weak — usually missing sources/numbers/structure or heavy slop.
- **55–71 → REVISE**: proceed to `06` to uplift.
- **≥ 72 and no P0 → READY**.

---

```
GATE 05 — Draft Quality
Score:   <0-100>
Status:  READY | REVISE | STOP
Blockers:
  - [P0] A claim/fact in the draft does not trace to source_pack.md.
  - [P0] Score < 55.
Next step: if REVISE/READY → 06_EDITORIAL_UPLIFT_GATE.md
```
