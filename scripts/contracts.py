"""Validate ContentOS Agent Lite working-file shapes. Pure, no I/O."""
import re

# "Competitor gaps" is OPTIONAL — the founder's own knowledge base + content sources
# (5-10 links on the topic) are the requirement; competitor analysis is a bonus angle.
_PACK_SECTIONS = ["Facts", "Numbers", "Audience questions", "Founder angle"]
_BRIEF_FIELDS = ["Audience", "Goal", "Format", "Angle", "Structure", "Must-mention", "Forbidden", "CTA", "Success criteria"]


def _sections(md: str) -> dict[str, list[str]]:
    out, cur = {}, None
    for line in md.splitlines():
        h = re.match(r"^##\s+(.*\S)\s*$", line)
        if h:
            cur = h.group(1).strip()
            out[cur] = []
        elif cur is not None and line.strip().startswith("-"):
            out[cur].append(line.strip()[1:].strip())
    return out


def _has_source(fact_line: str) -> bool:
    # require a URL or a "(YYYY" date token; a bare em-dash alone is not enough
    return bool(re.search(r"https?://|\(\d{4}", fact_line))


def validate_source_pack(md: str) -> dict:
    secs = _sections(md)
    missing = [s for s in _PACK_SECTIONS if s not in secs or not secs.get(s)]
    facts = secs.get("Facts", [])
    facts_without_source = [f for f in facts if not _has_source(f)]
    ok = not missing and bool(facts) and not facts_without_source
    return {"ok": ok, "missing": missing, "facts_without_source": facts_without_source}


def validate_brief(md: str) -> dict:
    present = {m.group(1).strip().lower(): m.group(2).strip()
               for m in re.finditer(r"^([A-Za-z][\w \-]*?):\s*(.*)$", md, re.M)}
    missing = [f for f in _BRIEF_FIELDS if not present.get(f.lower())]
    return {"ok": not missing, "missing": missing}
