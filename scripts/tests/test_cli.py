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
