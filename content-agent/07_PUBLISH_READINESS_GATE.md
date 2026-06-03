# 07 · Publish Readiness Gate — the go / no-go

The final gate. Write the verdict into `_work/qa_report.md`. **Publish only if the piece scores
≥ 85 AND has zero P0 blockers.** Otherwise it is not ready — route it back.

## Decision

```
if score >= 85 and no P0:
    → READY TO PUBLISH
elif any P0:
    → STOP. Fix the root cause:
        - claim/fact not sourced      → back to 02/03 (get the source) then 05/06
        - score < 55                  → back to 05 (rewrite from sources)
else (55-84, no P0):
    → POLISH. Back to 06 for another uplift pass, then re-check here.
```

## What this gate does NOT promise
It does not guarantee rankings, it is not multi-source adult fact-checking, and there is no
learning loop yet. It promises: grounded, checked, on-voice text — and an honest go/no-go.

## Write the report

Fill `_work/qa_report.md`: overall score, per-axis, the blocker list, the verdict, and the next
step. That file is the artifact you keep as proof of the run.

---

```
GATE 07 — Publish Readiness
Score:   <0-100>
Status:  READY | REVISE | STOP
Blockers:
  - [P0] Score < 85, or any unresolved P0 from earlier gates.
Next step:
  - READY  → publish (founder's call — the agent never auto-publishes).
  - STOP   → back to the cited gate.
```

**The agent never publishes for you.** It hands you a `READY` piece + the `qa_report.md`. You press
the button. To grow this into the full pipeline (multi-engine scoring, deep fact-check, team scale,
hosted), see the repo README → https://humanswith.ai/platform/contentos/.
