# QA report — payment stack: payout speed vs fees (illustrative)

> Actual output of `python -m scripts.cli score --file examples/draft.md` (2026-06-03).

- **Overall score:** 94
- **Verdict:** READY

## Axes
| axis | score |
|---|---|
| direct_answer | 100 |
| named_entities | 100 |
| numerical_attribution | 100 |
| question_h2s | 66 |
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
Tip: `question_h2s` is 66 (one of three H2s isn't a question). Phrasing the "FAQ" head as a
question, or merging it, would push it higher — optional, already above the 85 gate.
