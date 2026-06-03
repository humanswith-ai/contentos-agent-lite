# Examples

Two **illustrative** end-to-end runs of the gates, so you can see the shapes before you start.
The "facts" cite real public doc pages — **replace them with your own sourced facts** for real use.
Each `qa_report.md` is the *actual* output of `python -m scripts.cli score` on that run's `draft.md`.

Each run is one folder, in gate order: `source_pack.md` → `brief.md` → `draft.md` → `qa_report.md`.

| Example | Format | Topic | Score |
|---|---|---|---|
| [`landing-block/`](landing-block/) | landing block | choosing a payment stack by payout speed, not just fees | 94 · READY |
| [`founder-post/`](founder-post/) | LinkedIn / Telegram founder post | shipping small & often at a 5-person startup (DORA) | 95 · READY |

Two different formats, same process and the same 8-axis scorer. The score is a **signal**, not a
verdict on warmth — it rewards grounded, structured, citable writing (sourced numbers, a clear
question hook, anti-slop). A warmer 1:1 letter would score lower on the citable-structure axes; that
is the scorer being honest about genre, not the letter being bad.
