"""Generate llms-full.txt: the whole tool inlined into one LLM-ingestable file
(README + content-agent overview + all gates 00-07), per the llms.txt convention
(https://llmstxt.org). Committed to the repo and drift-guarded by a test, so the
published file can never silently fall out of sync with the gate sources.

Regenerate:  python -m scripts.build_llms_full
"""
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

_HEADER = (
    "# ContentOS Agent Lite — llms-full.txt\n"
    "\n"
    "> Full machine-readable content for LLM ingestion and citation: the README plus\n"
    "> every gate of the open-source content agent, inlined into one file.\n"
    "> Source: https://github.com/humanswith-ai/contentos-agent-lite (MIT, by Humanswith.ai).\n"
    "> Hosted product: https://humanswith.ai/platform/contentos/\n"
)


def build_llms_full(root):
    """Assemble the full-content file deterministically from the canonical sources."""
    root = pathlib.Path(root)
    sections = [
        ("README", root / "README.md"),
        ("content-agent (overview)", root / "content-agent" / "README.md"),
    ]
    gate_files = sorted((root / "content-agent").glob("0[0-9]_*.md"))
    sections += [(f"content-agent/{p.name}", p) for p in gate_files]

    parts = [_HEADER.rstrip()]
    for title, path in sections:
        body = path.read_text().strip()
        parts.append(f"\n\n---\n\n# === {title} ===\n\n{body}")
    return "".join(parts).rstrip() + "\n"


if __name__ == "__main__":  # pragma: no cover
    (REPO_ROOT / "llms-full.txt").write_text(build_llms_full(REPO_ROOT))
    print(f"Wrote {REPO_ROOT / 'llms-full.txt'}")
