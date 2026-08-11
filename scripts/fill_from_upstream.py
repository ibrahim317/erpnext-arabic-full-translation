"""Fill untranslated/fuzzy entries in the source catalogs from upstream ar.po.

Upstream `frappe/<app>` version-16 branches carry the live Crowdin exports
(project 639578 and siblings). This closes part of the gap for free, but every
fill is validated first — the same Crowdin pipeline produced the placeholder
defects fixed in v0.2.0, so nothing is accepted blind:

  * msgstr must not introduce a {placeholder} absent from msgid
  * no HTML-entity artifacts absent from msgid
  * existing non-fuzzy translations are NEVER overwritten (local wins)

Usage:
    python scripts/fill_from_upstream.py [--branch version-16]
"""

import argparse
import re
import sys
import urllib.request
from pathlib import Path

from babel.messages.pofile import read_po, write_po

BRACE = re.compile(r"\{[^{}]*\}")
ENT = re.compile(r"&(#39|quot|amp|lt|gt|#x27);")
APPS = ("frappe", "erpnext", "hrms")
ROOT = Path(__file__).resolve().parent.parent / "arabic_translations" / "locale" / "source"
RAW = "https://raw.githubusercontent.com/frappe/{app}/{branch}/{app}/locale/ar.po"


def fetch(app: str, branch: str) -> Path:
	dest = Path(f"/tmp/upstream-{app}-{branch}-ar.po")
	if not dest.exists():
		print(f"  fetching {app}@{branch} ...")
		urllib.request.urlretrieve(RAW.format(app=app, branch=branch), dest)
	return dest


def index(path: Path) -> dict:
	with path.open(encoding="utf-8") as fh:
		cat = read_po(fh)
	out = {}
	for m in cat:
		if not m.id or m.fuzzy:
			continue
		sid = m.id if isinstance(m.id, str) else m.id[0]
		st = m.string if isinstance(m.string, str) else (m.string[0] if m.string else "")
		if st:
			out[(sid, m.context)] = st
	return out


def safe(sid: str, st: str) -> bool:
	if set(BRACE.findall(st)) - set(BRACE.findall(sid)):
		return False
	if ENT.search(st) and not ENT.search(sid):
		return False
	return True


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("--branch", default="version-16")
	args = ap.parse_args()

	total = 0
	for app in APPS:
		up = index(fetch(app, args.branch))
		src = ROOT / app / "ar.po"
		with src.open(encoding="utf-8") as fh:
			cat = read_po(fh)
		filled = rejected = 0
		for m in cat:
			if not m.id:
				continue
			sid = m.id if isinstance(m.id, str) else m.id[0]
			st = m.string if isinstance(m.string, str) else (m.string[0] if m.string else "")
			if st and not m.fuzzy:
				continue  # local translation wins
			cand = up.get((sid, m.context))
			if not cand:
				continue
			if not safe(sid, cand):
				rejected += 1
				continue
			m.string = cand if isinstance(m.string, str) or m.string is None else tuple([cand] + list(m.string[1:]))
			m.flags.discard("fuzzy")
			m.flags.discard("python-format")
			filled += 1
		with src.open("wb") as fh:
			write_po(fh, cat, width=88, sort_output=False, sort_by_file=False)
		print(f"{app}: filled={filled} rejected(unsafe)={rejected}")
		total += filled
	print(f"total filled from upstream: {total}")
	if total == 0:
		sys.exit(0)


if __name__ == "__main__":
	main()
