# Security

## What this tool does on your machine

- It is **markdown gate files + a small Python layer** (`scripts/`).
- It makes **no network calls by default**. It only calls a provider (Tavily / Firecrawl / Serper)
  if **you** set that provider's key in `.env`, and only during the `research` step.
- It writes only inside the directory you run it in (the `content-agent/_work/` files and an
  optional `_work/.cache/`).
- It contains **no secrets**. `.env` is git-ignored; keys are read from your environment only.

## Reporting a vulnerability

Email **security@humanswith.ai** with details and steps to reproduce. Please do not open a public
issue for security reports. We aim to acknowledge within 72 hours.

## Your keys

Provider keys live only in your local `.env` (git-ignored) or your shell environment. Never commit
real keys. The example file ships with empty placeholders.
