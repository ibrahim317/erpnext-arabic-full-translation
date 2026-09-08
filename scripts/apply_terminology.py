"""Apply scripts/terminology_fixes.py to the canonical source catalogs.

Order matters: pipeline artifacts are stripped first, then the guarded glossary
rewrites the bulk, then EXACT overrides have the final word on entries that
needed a full rewrite, then orthography and whitespace normalisation run over
the result.

Every change is placeholder-checked before anything is written: a msgstr may
never gain a ``{placeholder}`` its msgid lacks, because Frappe feeds ``_()``
output straight into ``str.format()`` and an invented placeholder is an
``IndexError`` in production.

Usage:
    python scripts/apply_terminology.py --dry-run     # report only
    python scripts/apply_terminology.py               # write catalogs
"""

import re
import sys
from pathlib import Path

from babel.messages.pofile import read_po, write_po

sys.path.insert(0, str(Path(__file__).parent))
from terminology_fixes import EXACT, GLOSSARY, ORTHOGRAPHY

ROOT = Path(__file__).resolve().parent.parent / "arabic_translations" / "locale" / "source"
APPS = ("frappe", "erpnext", "hrms")

BRACE = re.compile(r"\{[^{}]*\}")
ARABIC = re.compile(r"[؀-ۿ]")
LATIN = re.compile(r"[A-Za-z]")
# the pipeline emitted a literal backslash-n, not a newline
BILINGUAL = re.compile(r"\\n<br>\\n")

# guards are case-insensitive: msgids mix "Stock Entry" and "stock transactions"
GUARDS = [(re.compile(g, re.I), re.compile(p), r) for g, p, r in GLOSSARY]


def strip_bilingual(sid: str, st: str) -> str:
	"""Drop a trailing '\\n<br>\\n<english original>' tail left by the pipeline."""
	if not BILINGUAL.search(st):
		return st
	if BILINGUAL.search(sid):
		return st  # the msgid genuinely carries the separator
	head, _tail = BILINGUAL.split(st, 1)
	# the tail is always a leftover: either the untranslated English or a
	# duplicate Arabic rendering. The msgid has no <br>, so neither belongs.
	return head.rstrip() if head.strip() else st


def normalise_ws(sid: str, st: str) -> str:
	"""Collapse defects the msgid does not itself contain."""
	# leave preformatted / multi-line help text alone, and never touch spacing in
	# strings carrying {placeholders} or JSON samples - collapsing a space inside
	# `{"a" : 1}` rewrites the brace token itself.
	if "\n" in sid or "<pre" in sid or "  " in sid or "{" in sid:
		return st
	st = re.sub(r"  +", " ", st)
	st = re.sub(r"\s+([،؛:.!؟])", r"\1", st)
	return st


def align_ws(sid: str, st: str) -> str:
	"""gettext requires msgstr to keep the msgid's leading/trailing whitespace."""
	if not st.strip():
		return st
	lead = sid[: len(sid) - len(sid.lstrip())]
	trail = sid[len(sid.rstrip()) :]
	return lead + st.strip() + trail


def fix(app: str, sid: str, st: str) -> str:
	new = strip_bilingual(sid, st)

	for guard, pat, repl in GUARDS:
		if guard.search(sid):
			new = pat.sub(repl, new)

	exact = EXACT.get(app, {}).get(sid)
	if exact is not None:
		new = exact

	for wrong, right in ORTHOGRAPHY.items():
		if wrong in new:
			new = new.replace(wrong, right)

	new = normalise_ws(sid, new)
	return align_ws(sid, new)


def main() -> None:
	dry = "--dry-run" in sys.argv
	total = 0
	errors = []
	report = []

	for app in APPS:
		path = ROOT / app / "ar.po"
		with path.open(encoding="utf-8") as fh:
			cat = read_po(fh)

		changed = 0
		for msg in cat:
			if not msg.id or not msg.string:
				continue
			sid = msg.id if isinstance(msg.id, str) else msg.id[0]
			strs = [msg.string] if isinstance(msg.string, str) else list(msg.string)

			out = []
			for st in strs:
				out.append(fix(app, sid, st) if st else st)

			if out == strs:
				continue

			# placeholder parity: never introduce one the msgid lacks
			want = set(BRACE.findall(sid))
			for st in out:
				extra = set(BRACE.findall(st)) - want if st else set()
				if extra:
					errors.append(f"{app}: {sid[:60]!r} would gain {extra}")

			msg.string = out[0] if isinstance(msg.string, str) else tuple(out)
			changed += 1
			if len(report) < 3000:
				report.append((app, sid, strs[0], out[0]))

		total += changed
		print(f"  {app}: {changed} entries changed")

		if not dry and not errors:
			with path.open("wb") as fh:
				write_po(fh, cat, width=88, sort_output=False, sort_by_file=False)

	if errors:
		print(f"\nABORTED - {len(errors)} placeholder violation(s):")
		for e in errors[:20]:
			print("  ", e)
		sys.exit(1)

	print(f"\ntotal: {total} entries {'would change' if dry else 'changed'}")
	if dry:
		Path("/tmp/terminology_report.txt").write_text(
			"\n".join(f"[{a}] {i!r}\n   -  {o!r}\n   +  {n!r}" for a, i, o, n in report),
			encoding="utf-8",
		)
		print("sample diff written to /tmp/terminology_report.txt")


if __name__ == "__main__":
	main()
