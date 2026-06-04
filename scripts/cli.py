"""ContentOS Agent Lite CLI: init / research / score / check / publish."""
import argparse
import json
import sys
import pathlib
import shutil
from scripts import score as score_mod, antislop, research, agentdocs, publish as publish_mod

_HERE = pathlib.Path(__file__).resolve().parent
_AGENT_SRC = _HERE.parent / "content-agent"


def _cmd_score(a):
    text = pathlib.Path(a.file).read_text()
    r = score_mod.score_draft(text, a.lang)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else _fmt_score(r))
    return 0


def _cmd_check(a):
    text = pathlib.Path(a.file).read_text()
    r = {"antislop": antislop.scan(text, a.lang), "score": score_mod.score_draft(text, a.lang)}
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else _fmt_score(r["score"]))
    return 0


def _cmd_research(a):
    r = research.gather(a.topic, a.url or [])
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(research.to_source_pack_md(r, a.topic))
    return 0


def _cmd_publish(a):
    text = pathlib.Path(a.file).read_text()
    out = {"lint": publish_mod.lint_publish(text, a.canonical)}
    if a.distribute:
        if not (a.canonical and a.title and a.summary):
            print("error: --distribute needs --canonical, --title and --summary", file=sys.stderr)
            return 2
        plats = [p.strip() for p in a.platforms.split(",")] if a.platforms else None
        out["distribution"] = publish_mod.distribution_drafts(a.canonical, a.title, a.summary, plats)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(_fmt_lint(out["lint"]))
        for plat, body in out.get("distribution", {}).items():
            print(f"\n--- {plat} ---\n{body}")
    return 0 if out["lint"]["passed"] else 1


def _fmt_lint(r):
    lines = [f"publish lint [{r['format']}]: {'PASS' if r['passed'] else 'FAIL'}"]
    for k, v in r["checks"].items():
        mark = "ok " if v is True else ("n/a" if v is None else "MISS")
        lines.append(f"  [{mark}] {k}")
    for b in r["blockers"]:
        lines.append(f"  [{b['severity']}] {b['check']}: {b['message']}")
    return "\n".join(lines)


def _cmd_init(a):
    into = pathlib.Path(a.into)
    dst = into / "content-agent"
    if _AGENT_SRC.is_dir():
        shutil.copytree(_AGENT_SRC, dst, dirs_exist_ok=True)
    else:
        dst.mkdir(parents=True, exist_ok=True)
        (dst / "README.md").write_text("# content-agent\n")
    env_src = _HERE.parent / ".env.example"
    if env_src.exists():
        shutil.copy(env_src, into / ".env.example")
    else:
        (into / ".env.example").write_text("TAVILY_API_KEY=\nFIRECRAWL_API_KEY=\nSERPER_API_KEY=\n")
    taught = agentdocs.write_agent_docs(into)
    print(f"Scaffolded content-agent/ into {into}")
    print(f"Taught the project agent: {', '.join(pathlib.Path(p).name for p in taught)} "
          "(managed block — safe to re-run)")
    return 0


def _fmt_score(r):
    lines = [f"overall: {r['overall']}  verdict: {r['verdict']}"]
    lines += [f"  {k}: {v}" for k, v in r["axes"].items()]
    lines += [f"  [{b['severity']}] {b['axis']}: {b['message']}" for b in r["blockers"]]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(prog="contentos-agent-lite")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score")
    s.add_argument("--file", required=True)
    s.add_argument("--lang", default="en")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=_cmd_score)
    c = sub.add_parser("check")
    c.add_argument("--file", required=True)
    c.add_argument("--lang", default="en")
    c.add_argument("--json", action="store_true")
    c.set_defaults(fn=_cmd_check)
    r = sub.add_parser("research")
    r.add_argument("--topic", required=True)
    r.add_argument("--url", action="append")
    r.add_argument("--json", action="store_true")
    r.set_defaults(fn=_cmd_research)
    i = sub.add_parser("init")
    i.add_argument("--into", default=".")
    i.set_defaults(fn=_cmd_init)
    pub = sub.add_parser("publish")
    pub.add_argument("--file", required=True)
    pub.add_argument("--canonical")
    pub.add_argument("--distribute", action="store_true")
    pub.add_argument("--title")
    pub.add_argument("--summary")
    pub.add_argument("--platforms")
    pub.add_argument("--json", action="store_true")
    pub.set_defaults(fn=_cmd_publish)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
