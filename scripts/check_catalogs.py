"""CI gate: validate every shipped catalog.

Checks
------
1. msgfmt --check passes (syntax, plural forms, format-string consistency).
2. No msgstr introduces a {placeholder} absent from its msgid (crash risk:
   frappe._() output goes straight into str.format()).
3. No HTML-entity artifacts (&#39; etc.) in msgstr that aren't in msgid.
4. CSV bundles have no header row and no empty msgid/msgstr.
5. Every catalog still matches scripts/terminology_fixes.py, so a hand-edit or a
   fresh upstream import cannot quietly reintroduce a defect the rules cover.
6. No rule table has a duplicate key. Python keeps the last of a repeated dict
   key silently, so a duplicate means an earlier rule never runs - and check 5
   cannot see it, because the catalogs agree with whichever rule won.
7. A msgid corrected in one app is not left uncorrected in another. The overlay
   merges frappe -> erpnext -> hrms with the later app winning, so fixing only
   the earlier app leaves the wrong value as the one actually shipped.
"""

import ast
import collections

import csv
import re
import subprocess
import sys
from pathlib import Path

from babel.messages.pofile import read_po

BRACE = re.compile(r"\{[^{}]*\}")
ENT = re.compile(r"&(#39|quot|amp|lt|gt|#x27);")
ROOT = Path(__file__).resolve().parent.parent / "arabic_translations" / "locale"

# Entries whose msgstr legitimately differs in braces (code samples etc.)
PLACEHOLDER_WHITELIST = {
	"<h3>Print Format Help</h3>",  # prefix match, see below
	"Set the filters here. For example:",
	"Only values between [0,1) are allowed.",
	"Special Characters except",  # literal {{ }} escapes, Arabic conjunction differs
}

failures = 0


def fail(msg):
	global failures
	failures += 1
	print(f"FAIL: {msg}")


def whitelisted(sid: str) -> bool:
	return any(sid.startswith(w) for w in PLACEHOLDER_WHITELIST)


def check_po(path: Path):
	r = subprocess.run(["msgfmt", "--check", "-o", "/dev/null", str(path)], capture_output=True, text=True)
	if r.returncode != 0:
		fail(f"{path}: msgfmt --check\n{r.stderr.strip()}")

	with path.open(encoding="utf-8") as fh:
		cat = read_po(fh)
	for m in cat:
		if not m.id or not m.string:
			continue
		sid = m.id if isinstance(m.id, str) else m.id[0]
		strs = [m.string] if isinstance(m.string, str) else list(m.string)
		want = set(BRACE.findall(sid))
		for st in strs:
			if not st:
				continue
			extra = set(BRACE.findall(st)) - want
			if extra and not whitelisted(sid):
				fail(f"{path}: extra placeholder(s) {extra} in msgstr for: {sid[:80]!r}")
			if ENT.search(st) and not ENT.search(sid):
				fail(f"{path}: HTML entity artifact in msgstr for: {sid[:80]!r}")


def check_csv(path: Path):
	with path.open(encoding="utf-8", newline="") as fh:
		rows = list(csv.reader(fh))
	if rows and rows[0][:2] == ["msgid", "msgstr"]:
		fail(f"{path}: header row present (Frappe would load it as a translation)")
	for i, row in enumerate(rows, 1):
		if len(row) < 2 or not row[0].strip() or not row[1].strip():
			fail(f"{path}:{i}: empty msgid/msgstr")
			break
		want = set(BRACE.findall(row[0]))
		extra = set(BRACE.findall(row[1])) - want
		if extra and not whitelisted(row[0]):
			fail(f"{path}:{i}: extra placeholder(s) {extra} for: {row[0][:80]!r}")


def check_rule_table_keys():
	"""A repeated dict key silently shadows the earlier one; nothing else catches it."""
	path = Path(__file__).parent / "terminology_fixes.py"
	tree = ast.parse(path.read_text(encoding="utf-8"))

	def dupes(node, label):
		counts = collections.Counter()
		lines = collections.defaultdict(list)
		for k in node.keys:
			if isinstance(k, ast.Constant) and isinstance(k.value, str):
				counts[k.value] += 1
				lines[k.value].append(k.lineno)
		for key, n in counts.items():
			if n > 1:
				fail(f"{label}: duplicate key {key[:60]!r} at lines {lines[key]}")

	for node in ast.walk(tree):
		if not isinstance(node, ast.Assign):
			continue
		name = getattr(node.targets[0], "id", None)
		if name == "EXACT" and isinstance(node.value, ast.Dict):
			for app, sub in zip(node.value.keys, node.value.values):
				if isinstance(sub, ast.Dict):
					dupes(sub, f"EXACT[{getattr(app, 'value', '?')!r}]")
		elif name in ("SPELLING", "ORTHOGRAPHY") and isinstance(node.value, ast.Dict):
			dupes(node.value, name)


def check_cross_app_agreement():
	"""A fix in an earlier app is useless if a later app still overrides it."""
	sys.path.insert(0, str(Path(__file__).parent))
	from terminology_fixes import EXACT

	order = ("frappe", "erpnext", "hrms")
	src = ROOT / "source"
	per_app = {}
	for app in order:
		path = src / app / "ar.po"
		if not path.is_file():
			continue
		with path.open(encoding="utf-8") as fh:
			cat = read_po(fh)
		per_app[app] = {
			(m.id if isinstance(m.id, str) else m.id[0]): (
				m.string if isinstance(m.string, str) else (m.string[0] if m.string else "")
			)
			for m in cat
			if m.id
		}

	for app, fixes in EXACT.items():
		for msgid in fixes:
			# only meaningful when this app actually carries the msgid; a rule can
			# name a msgid that only exists in a later app
			if msgid not in per_app.get(app, {}):
				continue
			later = [a for a in order[order.index(app) + 1 :] if msgid in per_app.get(a, {})]
			for other in later:
				if per_app[other][msgid] != per_app[app][msgid]:
					fail(
						f"{msgid[:60]!r} is corrected in {app} but {other} still has "
						f"{per_app[other][msgid][:40]!r}, and {other} wins in the overlay"
					)


def check_terminology():
	"""Re-run the terminology rules in check mode; they must be a no-op."""
	script = Path(__file__).parent / "apply_terminology.py"
	r = subprocess.run(
		[sys.executable, str(script), "--check"], capture_output=True, text=True
	)
	if r.returncode != 0:
		fail(f"terminology rules not applied\n{r.stdout.strip()}")


def main():
	pos = sorted(ROOT.rglob("*.po"))
	csvs = sorted(ROOT.rglob("*.csv"))
	print(f"Checking {len(pos)} PO and {len(csvs)} CSV catalog(s)...")
	for p in pos:
		check_po(p)
	for c in csvs:
		check_csv(c)
	check_rule_table_keys()
	check_cross_app_agreement()
	check_terminology()
	if failures:
		print(f"\n{failures} failure(s).")
		sys.exit(1)
	print("All catalogs clean.")


if __name__ == "__main__":
	main()
