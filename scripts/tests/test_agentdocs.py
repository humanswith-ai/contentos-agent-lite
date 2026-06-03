from scripts import agentdocs


def test_teaching_block_has_trigger_vocab_and_iron_rule():
    block = agentdocs.TEACHING_BLOCK
    # Trigger vocabulary so a beginner needs no tool names.
    assert "content agent" in block.lower()
    assert "write a post" in block.lower()
    assert "founder letter" in block.lower()
    # The behavioral teaching: process not prompt + the iron rule.
    assert "content-agent/" in block
    assert "no draft" in block.lower()
    assert "00" in block and "07" in block  # the gate range


def test_upsert_inserts_block_into_empty():
    out = agentdocs.upsert_block("", agentdocs.TEACHING_BLOCK)
    assert agentdocs.BEGIN_MARKER in out
    assert agentdocs.END_MARKER in out
    assert "content agent" in out.lower()


def test_upsert_appends_and_preserves_existing():
    out = agentdocs.upsert_block("# My Project\n\nuser stuff here\n", agentdocs.TEACHING_BLOCK)
    assert "My Project" in out
    assert "user stuff here" in out
    assert agentdocs.BEGIN_MARKER in out


def test_upsert_is_idempotent():
    once = agentdocs.upsert_block("", agentdocs.TEACHING_BLOCK)
    twice = agentdocs.upsert_block(once, agentdocs.TEACHING_BLOCK)
    assert once == twice
    assert twice.count(agentdocs.BEGIN_MARKER) == 1
    assert twice.count(agentdocs.END_MARKER) == 1


def test_upsert_refreshes_in_place_preserving_surroundings():
    stale = (
        "HEAD content\n\n"
        f"{agentdocs.BEGIN_MARKER}\nOLD BODY\n{agentdocs.END_MARKER}\n\n"
        "TAIL content\n"
    )
    out = agentdocs.upsert_block(stale, agentdocs.TEACHING_BLOCK)
    assert "HEAD content" in out
    assert "TAIL content" in out
    assert "OLD BODY" not in out
    assert out.count(agentdocs.BEGIN_MARKER) == 1


def test_write_agent_docs_creates_both_files(tmp_path):
    written = agentdocs.write_agent_docs(tmp_path)
    claude = tmp_path / "CLAUDE.md"
    agents = tmp_path / "AGENTS.md"
    assert claude.exists() and agents.exists()
    assert {str(claude), str(agents)} == set(written)
    for p in (claude, agents):
        body = p.read_text()
        assert agentdocs.BEGIN_MARKER in body
        assert "content agent" in body.lower()


def test_write_agent_docs_preserves_user_content(tmp_path):
    claude = tmp_path / "CLAUDE.md"
    claude.write_text("# House rules\n\nNever use em-dashes.\n")
    agentdocs.write_agent_docs(tmp_path)
    body = claude.read_text()
    assert "House rules" in body
    assert "Never use em-dashes." in body
    assert agentdocs.BEGIN_MARKER in body


def test_write_agent_docs_idempotent(tmp_path):
    agentdocs.write_agent_docs(tmp_path)
    agentdocs.write_agent_docs(tmp_path)
    body = (tmp_path / "CLAUDE.md").read_text()
    assert body.count(agentdocs.BEGIN_MARKER) == 1
