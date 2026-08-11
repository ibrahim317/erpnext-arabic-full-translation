"""Apply a translations dict (index -> Arabic) onto the app's source catalog."""
import importlib.util
import json
import re
import sys
from pathlib import Path

from babel.messages.pofile import read_po, write_po

BRACE = re.compile(r"\{[^{}]*\}")

def load_T(pyfile):
    spec = importlib.util.spec_from_file_location("T", pyfile)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.T

def ws_align(sid, st):
    """Copy leading/trailing whitespace from msgid onto msgstr."""
    lead = sid[:len(sid)-len(sid.lstrip())]
    trail = sid[len(sid.rstrip()):]
    return lead + st.strip() + trail if st.strip() else st

def main(app, todo_json, trans_py, src_po):
    items = json.load(open(todo_json, encoding="utf-8"))
    T = load_T(trans_py)
    # coverage + placeholder pre-check
    errors = []
    for i, it in enumerate(items):
        if i not in T:
            continue  # partial batches allowed
        st = T[i]
        want = sorted(BRACE.findall(it["id"]))
        got = sorted(BRACE.findall(st))
        if want != got:
            errors.append(f"idx {i}: placeholders {want} != {got} :: {it['id'][:60]!r}")
    if errors:
        print(f"{app}: {len(errors)} problems")
        for e in errors[:20]:
            print("  ", e)
        sys.exit(1)

    with open(src_po, encoding="utf-8") as f:
        cat = read_po(f)
    by_key = {}
    for i, it in enumerate(items):
        if i in T:
            by_key[(it["id"], it["ctx"])] = ws_align(it["id"], T[i])

    applied = 0
    for m in cat:
        if not m.id:
            continue
        sid = m.id if isinstance(m.id, str) else m.id[0]
        key = (sid, m.context)
        if key in by_key:
            new = by_key.pop(key)
            m.string = new if isinstance(m.string, str) or m.string is None else tuple([new]+list(m.string[1:]))
            m.flags.discard("fuzzy")
            m.flags.discard("python-format")
            applied += 1

    # entries in todo not present in source (new strings from POT) -> append
    appended = 0
    for (sid, ctx), st in by_key.items():
        cat.add(sid, st, context=ctx)
        appended += 1

    with open(src_po, "wb") as f:
        write_po(f, cat, width=88, sort_output=False, sort_by_file=False)
    print(f"{app}: applied={applied} appended={appended}")

if __name__ == "__main__":
    main(*sys.argv[1:])
