"""Rebuild the Arabic bundles from the raw upstream-derived catalogs.

Pipeline
--------
1. Load the raw ``ar.po`` for each app.
2. Repair: strip HTML-entity artifacts, drop bogus ``python-format`` flags,
   apply hand-written corrections for placeholder-defective entries.
3. Write the canonical catalog to ``locale/source/<app>/ar.po``.
4. Emit per-version bundles:
     * v16 -> ``<app>/locale/ar.po``     (frappe, erpnext, hrms)
     * v15 -> ``frappe/locale/ar.po`` *and* ``frappe/translations/ar.csv``
       (frappe backported gettext in v15.33.0: benches below that read only the
       CSV, benches at or above it compile their own MO which overrides the CSV
       key by key, so the PO is the only thing that wins there - ship both)
     * v15 -> ``<app>/translations/ar.csv`` (erpnext & hrms v15 are CSV-only)
"""

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

from babel.messages.pofile import read_po, write_po

sys.path.insert(0, str(Path(__file__).parent))
from corrections import CORRECTIONS, KEEP

BRACE = re.compile(r"\{[^{}]*\}")
PCT = re.compile(r"%(?:\([^)]*\))?[-+ #0]*[\d*]*(?:\.\d+)?[hlL]?[diouxXeEfFgGcrs%]")
ENTS = {"&#39;": "'", "&#x27;": "'", "&quot;": '"', "&amp;": "&", "&gt;": ">", "&lt;": "<"}
APPS = ("frappe", "erpnext", "hrms")

REPORT = {}


def _strings(msg):
	return list(msg.string) if not isinstance(msg.string, str) else [msg.string]


def _assign(msg, strs):
	msg.string = tuple(strs) if not isinstance(msg.string, str) else strs[0]


def repair(app: str, raw: Path) -> "object":
	with raw.open(encoding="utf-8") as fh:
		cat = read_po(fh)

	stats = dict(entities=0, dropped_pyformat=0, corrected=0, kept=0, blanked=0)
	defect_index = -1
	corrections = CORRECTIONS.get(app, {})

	for msg in cat:
		if not msg.id or not msg.string:
			continue
		sid = msg.id if isinstance(msg.id, str) else msg.id[0]
		strs = _strings(msg)

		# --- 1. HTML entity artifacts leaked in from the translation pipeline
		for i, st in enumerate(strs):
			if not st:
				continue
			new = st
			for ent, ch in ENTS.items():
				if ent in new and ent not in sid:
					new = new.replace(ent, ch)
			if new != st:
				strs[i] = new
				stats["entities"] += 1
		_assign(msg, strs)

		# --- 2. bogus `python-format` flags (Frappe uses str.format, not %-format)
		if "python-format" in msg.flags:
			mismatch = any(st and len(PCT.findall(st)) != len(PCT.findall(sid)) for st in strs)
			if mismatch:
				msg.flags.discard("python-format")
				stats["dropped_pyformat"] += 1

		# --- 3. placeholder defects -> apply hand-written corrections
		want = set(BRACE.findall(sid))
		if any(st and set(BRACE.findall(st)) != want for st in strs):
			defect_index += 1
			fix = corrections.get(defect_index)
			if fix is KEEP:
				stats["kept"] += 1
			elif fix:
				_assign(msg, [fix] + strs[1:] if len(strs) > 1 else [fix])
				msg.flags.discard("fuzzy")
				stats["corrected"] += 1
			else:
				# Unknown defect: fall back to English rather than crash .format()
				_assign(msg, ["" for _ in strs])
				stats["blanked"] += 1

	REPORT[app] = stats
	print(f"  {app}: {stats}")
	return cat


def write_catalog(cat, path: Path):
	path.parent.mkdir(parents=True, exist_ok=True)
	with path.open("wb") as fh:
		write_po(fh, cat, width=88, sort_output=False, sort_by_file=False)


def strip_pyformat(path: Path):
	"""Frappe formats translations with str.format(), never %-formatting; the
	auto-added `python-format` flags only make msgfmt fail on Arabic text."""
	with path.open(encoding="utf-8") as fh:
		cat = read_po(fh)
	for m in cat:
		m.flags.discard("python-format")
	with path.open("wb") as fh:
		write_po(fh, cat, width=88, sort_output=False, sort_by_file=False)


def msgmerge(po: Path, pot: Path, out: Path):
	out.parent.mkdir(parents=True, exist_ok=True)
	tmp = out.with_suffix(".merge.tmp")
	subprocess.run(
		["msgmerge", "--quiet", "--no-fuzzy-matching", "-o", str(tmp), str(po), str(pot)],
		check=True,
	)
	subprocess.run(["msgattrib", "--no-obsolete", "-o", str(out), str(tmp)], check=True)
	tmp.unlink()
	strip_pyformat(out)


def po_to_csv(po: Path, out: Path):
	"""v15 ERPNext/HRMS still read `translations/ar.csv` (no header row)."""
	with po.open(encoding="utf-8") as fh:
		cat = read_po(fh)
	out.parent.mkdir(parents=True, exist_ok=True)
	rows = 0
	with out.open("w", encoding="utf-8", newline="") as fh:
		w = csv.writer(fh)
		for msg in cat:
			if not msg.id or msg.fuzzy:
				continue
			sid = msg.id if isinstance(msg.id, str) else msg.id[0]
			st = msg.string if isinstance(msg.string, str) else (msg.string[0] if msg.string else "")
			if not st or not sid.strip():
				continue
			w.writerow([sid, st, msg.context or ""])
			rows += 1
	print(f"  csv {out.name}: {rows} rows")


def main():
	root = Path(sys.argv[1])          # repo root
	pots = Path(sys.argv[2])          # dir with <app>-version-1x.pot
	raw_root = root / "arabic_translations/locale/other-apps"
	src_root = root / "arabic_translations/locale/source"
	out_root = raw_root

	if all((src_root / app / "ar.po").is_file() for app in APPS):
		print("Source catalogs exist - using them as canonical input (no repair).")
		for app in APPS:
			strip_pyformat(src_root / app / "ar.po")
	else:
		print("Bootstrapping source catalogs from raw bundles (one-time repair)...")
		for app in APPS:
			cat = repair(app, raw_root / f"v16/{app}/{app}/locale/ar.po")
			write_catalog(cat, src_root / app / "ar.po")

	print("Building v16 bundles (PO)...")
	for app in APPS:
		msgmerge(
			src_root / app / "ar.po",
			pots / f"{app}-version-16.pot",
			out_root / f"v16/{app}/{app}/locale/ar.po",
		)

	print("Building v15 bundles...")
	# frappe v15 ships both: the PO for >=15.33 (where frappe's own compiled MO
	# would otherwise override a CSV), the CSV for <15.33 (no PO machinery yet).
	msgmerge(
		src_root / "frappe/ar.po",
		pots / "frappe-version-15.pot",
		out_root / "v15/frappe/frappe/locale/ar.po",
	)
	po_to_csv(src_root / "frappe/ar.po", out_root / "v15/frappe/frappe/translations/ar.csv")
	# erpnext + hrms v15 are still CSV-based
	for app in ("erpnext", "hrms"):
		po_to_csv(src_root / app / "ar.po", out_root / f"v15/{app}/{app}/translations/ar.csv")

	(root / "coverage.json").write_text(json.dumps(REPORT, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
	main()
