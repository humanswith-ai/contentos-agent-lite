#!/usr/bin/env bash
# Pre-install verification for ContentOS Agent Lite.
# No sudo, no network. Exit 0 = safe to install. See TRUST.md for the full contract.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "ContentOS Agent Lite — pre-install check"
echo "Root: $ROOT"
echo

echo "[1] Expected write paths (this tool writes ONLY inside the project you point it at):"
echo "    init  ->  <your project>/content-agent/**           (the gate folder)"
echo "              <your project>/.env.example               (key template)"
echo "              <your project>/CLAUDE.md , AGENTS.md       (a managed block between markers; re-runnable, keeps your content)"
echo "    gates ->  <your project>/content-agent/_work/*.md   (working files the agent fills)"
echo "              <your project>/content-agent/_work/.cache/ (research cache, only if a key is set)"
echo

echo "[2] Network behavior:"
echo "    - NO network calls by default."
echo "    - Calls a provider ONLY if you set its key (TAVILY/FIRECRAWL/SERPER) in .env,"
echo "      and only during the 'research' step."
echo

echo "[3] Secret scan (tracked files must contain NO real keys):"
if grep -REn 'sk-[A-Za-z0-9]{20,}|tvly-[A-Za-z0-9]{20,}|fc-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}' \
     --include='*.py' --include='*.md' --include='*.txt' --include='*.toml' --include='*.sh' \
     --exclude-dir='.venv' --exclude-dir='.git' --exclude-dir='__pycache__' --exclude-dir='.pytest_cache' \
     "$ROOT" | grep -v '.env.example' ; then
  echo "    FAIL: potential secret found above — do NOT install until resolved."
  exit 1
else
  echo "    ok: no real-key patterns in tracked files"
fi
echo

echo "[4] Runtime (optional scripts only — the gates work without Python):"
if command -v python3 >/dev/null 2>&1 ; then
  echo "    ok: python3 present ($(python3 -V 2>&1))"
else
  echo "    note: python3 not found — the markdown gates still work; the helper scripts need it."
fi
echo

echo "PASS: pre-install check passed. Safe to install. Read TRUST.md for the full contract."
