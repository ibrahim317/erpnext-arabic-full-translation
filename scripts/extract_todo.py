"""Regenerate the open-entries manifest for a translation batch.

Syncs the canonical source catalog against the current upstream POT and dumps
everything still open — untranslated *and* fuzzy — as JSON on stdout. Feed the
result to scripts/apply_trans.py, which addresses entries by list position.

This replaces committing a static snapshot of the open entries: the manifest is
cheap to rebuild and never goes stale against upstream.

Usage:
    python scripts/extract_todo.py erpnext /tmp/pots/erpnext-version-16.pot > todo.json
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from babel.messages.pofile import read_po

ROOT = Path(__file__).resolve().parent.parent / "arabic_translations" / "locale" / "source"


def sync(src: Path, pot: Path, out: Path) -> None:
	"""msgmerge against the POT, then drop entries upstream no longer defines."""
	merged = out.with_suffix(".merged.po")
	subprocess.run(
		["msgmerge", "-q", "--no-fuzzy-matching", "-o", str(merged), str(src), str(pot)], check=True
	)
	subprocess.run(["msgattrib", "--no-obsolete", "-o", str(out), str(merged)], check=True)


def main() -> None:
	if len(sys.argv) != 3:
		sys.exit(__doc__.strip().splitlines()[-1].strip())
	app, pot = sys.argv[1], Path(sys.argv[2])
	src = ROOT / app / "ar.po"
	if not src.exists():
		sys.exit(f"no source catalog for {app!r}: {src}")

	with tempfile.TemporaryDirectory() as tmp:
		synced = Path(tmp) / f"{app}-synced.po"
		sync(src, pot, synced)
		with synced.open(encoding="utf-8") as fh:
			cat = read_po(fh)

	todo = []
	for m in cat:
		if not m.id:
			continue  # PO header
		sid = m.id if isinstance(m.id, str) else m.id[0]
		st = m.string if isinstance(m.string, str) else (m.string[0] if m.string else "")
		if st and not m.fuzzy:
			continue
		todo.append({"id": sid, "ctx": m.context, "old": st if m.fuzzy and st else None})

	json.dump(todo, sys.stdout, ensure_ascii=False, indent=1)
	sys.stdout.write("\n")
	print(f"{app}: {len(todo)} open entries", file=sys.stderr)


if __name__ == "__main__":
	main()
