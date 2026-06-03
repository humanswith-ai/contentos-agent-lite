import json
from scripts import cli


def test_score_subcommand(tmp_path, capsys):
    draft = tmp_path / "draft.md"
    draft.write_text("## Why? \nStripe did $1.4T in 2024 [1].\n[1] https://stripe.com\n")
    rc = cli.main(["score", "--file", str(draft), "--lang", "en", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert "overall" in out and "verdict" in out


def test_check_subcommand_runs_antislop_and_score(tmp_path, capsys):
    draft = tmp_path / "d.md"
    draft.write_text("Let's delve into our robust seamless game-changing solution.\n")
    rc = cli.main(["check", "--file", str(draft), "--lang", "en", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert "antislop" in out and "score" in out
    assert out["antislop"]["count"] >= 1


def test_init_scaffolds(tmp_path):
    rc = cli.main(["init", "--into", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / "content-agent").is_dir()
    assert (tmp_path / ".env.example").exists()


def test_init_teaches_project_agent_docs(tmp_path):
    rc = cli.main(["init", "--into", str(tmp_path)])
    assert rc == 0
    for name in ("CLAUDE.md", "AGENTS.md"):
        body = (tmp_path / name).read_text()
        assert "content agent" in body.lower()
        assert "<!-- BEGIN contentos-agent-lite -->" in body


def test_init_agent_docs_idempotent(tmp_path):
    cli.main(["init", "--into", str(tmp_path)])
    cli.main(["init", "--into", str(tmp_path)])
    body = (tmp_path / "CLAUDE.md").read_text()
    assert body.count("<!-- BEGIN contentos-agent-lite -->") == 1


def test_init_preserves_existing_claude_md(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# My Project\n\nhouse rule: be terse.\n")
    cli.main(["init", "--into", str(tmp_path)])
    body = (tmp_path / "CLAUDE.md").read_text()
    assert "My Project" in body
    assert "house rule: be terse." in body
    assert "<!-- BEGIN contentos-agent-lite -->" in body
