# QA report — daily deploys founder post (illustrative)

> Actual output of `python -m scripts.cli score --file examples/founder-post/draft.md` (2026-06-03).

- **Overall score:** 95
- **Verdict:** READY

## Axes
| axis | score |
|---|---|
| direct_answer | 100 |
| named_entities | 100 |
| numerical_attribution | 80 |
| question_h2s | 100 |
| structured_elements | 80 |
| faq_block | 100 |
| anti_slop | 100 |
| citation_markers | 100 |

## Gates
- Source pack validates (all sections filled, every fact sourced): **ok**
- Brief validates (all fields present): **ok**

## Blockers
- none

## Next step
READY → publish (founder's call — the agent does not auto-publish).
Note: `numerical_attribution` is 80 — the "30-second rollback" figure is a team practice, not a
sourced external stat, so it isn't anchored to a citation. That's honest; the two DORA numbers that
*do* carry weight are both sourced. Already well above the 85 gate.
