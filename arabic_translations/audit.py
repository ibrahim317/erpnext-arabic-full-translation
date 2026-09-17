"""Audit a live site for UI strings that render untranslated.

Why this exists
---------------
`scripts/extract_todo.py` answers "what is untranslated *in the POT*". It cannot
answer "what is untranslated *on screen*", because a large class of UI labels
never reaches a POT at all: Workspaces, Workspace Links and Shortcuts, Dashboard
Charts, Number Cards and Reports ship as JSON fixtures installed as database
records, so the gettext extractor never sees them. Frappe still resolves them by
msgid at render time, so defining them in our catalog is all that is needed --
but nothing upstream tells us they exist. This reads them back off a real site.

It is read-only: it queries the database and the translation dict, and writes
nothing.

Usage
-----
    bench --site <site> execute arabic_translations.audit.report
    bench --site <site> execute arabic_translations.audit.report --kwargs "{'as_po': True}"

`as_po=True` emits paste-ready PO entries for everything still missing.
"""

import json

import frappe

# (doctype, field) pairs whose values Frappe renders through __() in the desk UI.
SOURCES = [
	("Workspace", "label"),
	("Workspace", "title"),
	("Workspace Link", "label"),
	("Workspace Shortcut", "label"),
	("Workspace Chart", "label"),
	("Workspace Number Card", "label"),
	("Dashboard Chart", "chart_name"),
	("Dashboard Chart Link", "chart_name"),
	("Number Card", "label"),
	("Dashboard", "dashboard_name"),
	("Report", "report_name"),
	("Module Def", "module_name"),
	("Onboarding Step", "title"),
	("Form Tour", "title"),
	("Custom HTML Block", "name"),
]


def _harvest():
	"""Every distinct label a desk screen may render, with where it came from."""
	seen = {}
	for doctype, field in SOURCES:
		if not frappe.db.table_exists(doctype):
			continue
		try:
			rows = frappe.get_all(doctype, pluck=field)
		except Exception:
			continue  # field absent on this version
		for value in rows:
			if not value or not isinstance(value, str):
				continue
			value = value.strip()
			# skip machine-ish names: no letters, or clearly an id
			if not value or not any(c.isalpha() for c in value):
				continue
			seen.setdefault(value, set()).add(f"{doctype}.{field}")
	return seen


def report(as_po=False, lang="ar"):
	"""Print every harvested label that has no translation in `lang`."""
	translations = frappe.translate.get_all_translations(lang) or {}
	harvested = _harvest()

	missing, identical = [], []
	for label, origins in sorted(harvested.items()):
		translated = translations.get(label)
		if not translated:
			missing.append((label, origins))
		elif translated == label:
			identical.append((label, origins))

	print(f"harvested {len(harvested)} distinct fixture labels from this site")
	print(f"  missing a translation : {len(missing)}")
	print(f"  translated to itself  : {len(identical)}")

	if as_po:
		print("\n# --- paste into arabic_translations/locale/source/<app>/ar.po ---")
		for label, origins in missing:
			print(f"\n#. {', '.join(sorted(origins))}")
			print(f"msgid {json.dumps(label, ensure_ascii=False)}")
			print('msgstr ""')
		return

	if missing:
		print("\nMISSING:")
		for label, origins in missing:
			print(f"  {label!r}   [{', '.join(sorted(origins))}]")
	if identical:
		print("\nTRANSLATED TO ITSELF (check these are meant to stay English):")
		for label, origins in identical:
			print(f"  {label!r}   [{', '.join(sorted(origins))}]")

	return {"missing": [m[0] for m in missing], "identical": [i[0] for i in identical]}
