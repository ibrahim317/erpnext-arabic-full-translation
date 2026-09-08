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
from terminology_fixes import EXACT, GLOSSARY, ORTHOGRAPHY, SPELLING

ROOT = Path(__file__).resolve().parent.parent / "arabic_translations" / "locale" / "source"
APPS = ("frappe", "erpnext", "hrms")

BRACE = re.compile(r"\{[^{}]*\}")
ARABIC = re.compile(r"[؀-ۿ]")
LATIN = re.compile(r"[A-Za-z]")
# the pipeline appended the English original after a <br>; the separator shows up
# as a real tag, sometimes wrapped in literal backslash-n rather than newlines
BILINGUAL = re.compile(r"(?:\\n)?\s*<br\s*/?>\s*(?:\\n)?")

# guards are case-insensitive: msgids mix "Stock Entry" and "stock transactions"
GUARDS = [(re.compile(g, re.I), re.compile(p), r) for g, p, r in GLOSSARY]
# whole-word only: "علي" is the preposition to fix, but it must not be touched
# inside a longer word, and Arabic has no \b that respects its script.
AR = "؀-ۿ"
SPELL = [(re.compile(f"(?<![{AR}]){re.escape(w)}(?![{AR}])"), c) for w, c in SPELLING.items()]


def strip_bilingual(sid: str, st: str) -> str:
	"""Drop the "<br> + untranslated English" tail the pipeline appended.

	Verified across all three catalogs: whenever the msgid carries no <br> but
	the msgstr does, the tail is always a leftover - the English original, or a
	duplicate Arabic rendering - and never content the translation added. So the
	presence of an unmatched <br> is itself the signal.
	"""
	if "<br" not in st or "<br" in sid:
		return st
	head = BILINGUAL.split(st, 1)[0]
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

	# Spelling first. A glossary pattern like "إيصال" cannot match text that
	# still reads "ايصال", so normalising the spelling before the terminology
	# pass is what makes a single run a fixpoint rather than needing a second.
	for wrong, right in ORTHOGRAPHY.items():
		if wrong in new:
			new = new.replace(wrong, right)

	for pat, right in SPELL:
		new = pat.sub(right, new)

	for guard, pat, repl in GUARDS:
		if guard.search(sid):
			new = pat.sub(repl, new)

	# EXACT has the last word: these are hand-written, already correct, and must
	# not be re-mangled by a later rule.
	exact = EXACT.get(app, {}).get(sid)
	if exact is not None:
		new = exact

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
