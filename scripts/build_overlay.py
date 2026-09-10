"""Build the overlay catalog: one merged `ar.po` shipped by this app itself.

Frappe merges translations app-by-app in installed order and later apps win
(`frappe.translate.get_translations_from_apps`).  So a single catalog shipped by
`arabic_translations` — installed last — overrides Frappe/ERPNext/HRMS strings
without ever touching their source trees.
"""

import sys
from pathlib import Path

from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po

# Later apps win on conflict; ERPNext/HRMS wording is more domain-correct.
ORDER = ("frappe", "erpnext", "hrms")


def main():
	src_root = Path(sys.argv[1])
	out = Path(sys.argv[2])

	merged = Catalog(
		locale="ar",
		domain="arabic_translations",
		project="arabic_translations",
		copyright_holder="Arabic Translations contributors",
		charset="UTF-8",
	)
	# Babel stamps a fresh `creation_date` (now()) on every new Catalog, which lands
	# in POT-Creation-Date and makes the overlay differ byte-for-byte between runs
	# even when nothing changed. Carry the date from the frappe source catalog
	# instead - read_po preserves it - so the build is genuinely reproducible and a
	# rebuild produces a diff only when the translations actually changed.
	with (src_root / "frappe/ar.po").open(encoding="utf-8") as fh:
		merged.creation_date = read_po(fh).creation_date

	seen: dict[tuple, str] = {}
	stats = {}
	for app in ORDER:
		with (src_root / app / "ar.po").open(encoding="utf-8") as fh:
			cat = read_po(fh)
		added = 0
		for msg in cat:
			if not msg.id or msg.fuzzy:
				continue
			sid = msg.id if isinstance(msg.id, str) else msg.id[0]
			st = msg.string if isinstance(msg.string, str) else (msg.string[0] if msg.string else "")
			if not st or not sid.strip():
				continue
			key = (sid, msg.context)
			if key in seen and seen[key] == st:
				continue
			seen[key] = st
			merged.delete(msg.id, msg.context)
			merged.add(sid, st, context=msg.context, auto_comments=[f"source: {app}"])
			added += 1
		stats[app] = added

	# Babel re-adds `python-format` whenever a msgid contains a `%`. Frappe formats
	# translated strings with str.format(), never %-formatting, so the flag is noise
	# that only makes msgfmt --check fail on legitimate Arabic percent signs.
	for msg in merged:
		msg.flags.discard("python-format")

	merged.last_translator = "Arabic Translations contributors"
	merged.language_team = "Arabic"

	out.parent.mkdir(parents=True, exist_ok=True)
	with out.open("wb") as fh:
		write_po(fh, merged, width=88, sort_output=True, omit_header=False)

	print("overlay entries per app (after dedup):", stats)
	print("total unique messages:", len(seen))


if __name__ == "__main__":
	main()
