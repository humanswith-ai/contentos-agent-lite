# Public release audit — contentos-agent-lite

Run this checklist before any push to `humanswith-ai/contentos-agent-lite` (per
`publication-visibility-gate` + `repo-release-packaging`). All boxes must be ticked.

## Visibility chain
- [ ] Audience = strangers/customers (public-org is correct for an HWAI-branded tool).
- [ ] **Zero secrets:** `bash scripts/agent-preinstall-check.sh` passes; no tokens/IPs/internal hostnames.
- [ ] Every referenced URL resolves and matches its declared visibility (`humanswith.ai/platform/contentos/`, the repo URL).
- [ ] Brand: prose says "Humanswith.ai"; `HWAI` only in technical identifiers (none here).
- [ ] Reciprocity: a stranger can actually run the 60-sec quickstart from a clean clone.

## Moat boundary (mcp-stack-moat-guard)
- [ ] No `gateway.py` / `COMPLEXITY_CHAINS` / tuned AEO weights / judge prompts / engine code.
- [ ] No `scraper-core` URL or key, no HWAI infra hostnames.
- [ ] The scorer is the transparent illustrative heuristic, not the private tuned model.
- [ ] Grep clean: `grep -REn 'scraper-core|COMPLEXITY_CHAINS|hwai-ops|gateway\.py' .` → none (outside docs/links).

## Self-contained (repo-release-packaging)
- [ ] No reference to `greg-personal-claude`, `hwai-internal`, private Notion, or local paths.
- [ ] No dangling internal-doc refs: `grep -REn '\.claude/rules|services/vhumanize|aeo_citability|spec section' . --exclude-dir=.venv` → none (they point at the private monorepo, unresolvable for a public reader).
- [ ] Examples use placeholders / public URLs only.
- [ ] `LICENSE` (MIT), `SECURITY.md`, `TRUST.md`, `trust/*.trust.json`, `scripts/agent-preinstall-check.sh` present.

## CI hardening
- [ ] `.github/workflows/ci.yml` third-party Actions **pinned to full commit SHA** (replace the `@vN` tags — fetch real SHAs at release).
- [ ] `pytest` green in CI.

## Final
- [ ] Rebase the source branch on `origin/main` (currently behind).
- [ ] Greg's explicit "go" recorded.
- [ ] After push: verify `/releases` / repo renders, README badges resolve, `/platform/contentos/` "Open source →" PR opened.
