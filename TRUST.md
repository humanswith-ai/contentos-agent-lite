# Verify before you install

ContentOS Agent Lite is designed to be **inspected before it's trusted**. You should not have to
take our word for it. Here's exactly what it does — and how to prove it.

## What it is
- A folder of **markdown gate files** (`content-agent/`) your coding agent reads and follows.
- An optional **~5-file Python layer** (`scripts/`) with one runtime dependency (`requests`).
- No binaries, no install scripts that touch your system, no `sudo`, no telemetry.

## The contract

| Property | Guarantee |
|---|---|
| **Network** | None by default. A provider (Tavily/Firecrawl/Serper) is called **only** if you set its key in `.env`, and **only** during `research`. |
| **Writes** | Only inside the project you point it at. `init` scaffolds `content-agent/`, writes a `.env.example`, and adds a **managed teaching block** (between `<!-- BEGIN/END contentos-agent-lite -->` markers, re-runnable, your own content preserved) to `CLAUDE.md` + `AGENTS.md`. The gates write working files into `content-agent/_work/*.md` (+ optional `_work/.cache/`). Nothing outside that folder. |
| **Secrets** | Read from your local `.env` / environment only. None are committed. `.env` is git-ignored. |
| **Privilege** | No `sudo`, no system changes. |
| **Publishing** | The agent **never** publishes your content — it hands you a `READY` piece + a QA report; you press the button. |

## Prove it (60 seconds, no install side effects)

```bash
git clone https://github.com/humanswith-ai/contentos-agent-lite
cd contentos-agent-lite
bash scripts/agent-preinstall-check.sh      # lists write paths + scans for secrets, exits 0 if clean
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q                # the test suite that proves the behavior
```

Machine-readable contract: [`trust/contentos-agent-lite.trust.json`](trust/contentos-agent-lite.trust.json).

## Forbidden patterns (we will never ship these)
- `curl … | bash` from an untrusted host
- anything requiring `sudo`
- writing outside your project directory
- bundling or transmitting your keys/content anywhere

If you ever see one of these, it is not us — stop and report to security@humanswith.ai.
