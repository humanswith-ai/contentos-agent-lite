import pytest


@pytest.fixture(autouse=True)
def _isolated_cwd(tmp_path, monkeypatch):
    """Run every test in a fresh cwd so research's `_work/.cache` never pollutes
    the repo tree or leaks between runs."""
    monkeypatch.chdir(tmp_path)
