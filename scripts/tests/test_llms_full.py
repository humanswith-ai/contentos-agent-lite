import pathlib
from scripts import build_llms_full

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_llms_full_contains_readme_and_all_gates():
    out = build_llms_full.build_llms_full(REPO_ROOT)
    assert "ContentOS Agent Lite" in out
    # Every gate 00-07 must be inlined for full LLM citation.
    for n in range(8):
        assert f"0{n}_" in out, f"missing gate 0{n} in llms-full"
    # The behavioral spine should survive into the full file.
    assert "no draft" in out.lower()
    assert "https://humanswith.ai/platform/contentos/" in out


def test_committed_llms_full_is_in_sync():
    """Drift guard: the committed file must equal the generator output, so the
    published llms-full.txt can never silently fall behind the gate sources."""
    committed = (REPO_ROOT / "llms-full.txt").read_text()
    generated = build_llms_full.build_llms_full(REPO_ROOT)
    assert committed == generated, (
        "llms-full.txt is stale — regenerate with `python -m scripts.build_llms_full`"
    )
