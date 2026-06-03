import pathlib
from scripts import contracts


def test_missing_source_pack_is_stop():
    md = (pathlib.Path(__file__).parent / "fixtures" / "missing_source_pack.md").read_text()
    r = contracts.validate_source_pack(md)
    assert r["ok"] is False
    assert "Our product is the best on the market." in r["facts_without_source"]
    # every section but Facts is empty -> also reported missing
    assert "Numbers" in r["missing"]
