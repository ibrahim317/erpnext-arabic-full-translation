import click
import frappe


@click.command("install-arabic-translations")
@click.option("--site", help="Site name. Omit to apply for all apps in the environment (Docker builds).")
@click.option(
	"--mode",
	type=click.Choice(["overlay", "overwrite", "both"]),
	default=None,
	help="Delivery mode. Defaults to arabic_translations_mode from site config, else 'overlay'.",
)
def install_arabic_translations(site=None, mode=None):
	"""Apply the Arabic translations (compile overlay and/or copy bundles)."""
	from arabic_translations.utils import apply_translations, check_overlay_precedence, get_mode

	if site:
		click.echo(f"Applying Arabic translations for site: {site}")
		frappe.init(site=site)
		frappe.connect()
		try:
			apply_translations(mode=mode)
			shadowing = check_overlay_precedence()
			if shadowing and (mode or get_mode()) in ("overlay", "both"):
				click.secho(
					f"Warning: apps installed after arabic_translations may shadow the overlay: "
					f"{', '.join(shadowing)}",
					fg="yellow",
				)
		finally:
			frappe.destroy()
	else:
		click.echo("No site provided. Copying Arabic bundles for all apps in the environment.")
		frappe.init("")
		try:
			apps = frappe.get_all_apps(with_internal=True)
			click.echo(f"Found apps: {', '.join(apps)}")
			# Without a site there is no config and no compiled-assets target, so
			# only the overwrite copy makes sense here (bench build handles the rest).
			from arabic_translations.utils import copy_locale_files

			copy_locale_files(apps=apps)
		except Exception as e:
			click.echo(f"Error copying translations: {e}")
			raise


@click.command("restore-original-translations")
@click.option("--site", required=True, help="Site name")
def restore_original_translations(site=None):
	"""Undo overwrite mode: git-restore the ar.po/ar.csv files in other apps."""
	from arabic_translations.utils import restore_locale_files

	frappe.init(site=site)
	frappe.connect()
	try:
		restored = restore_locale_files()
		click.echo(f"Restored {len(restored)} file(s).")
	finally:
		frappe.destroy()


@click.command("audit-arabic-translations")
@click.option("--site", required=True, help="Site name")
@click.option("--as-po", is_flag=True, help="Emit paste-ready PO entries for what is missing.")
@click.option("--lang", default="ar", help="Language code to audit. Defaults to 'ar'.")
def audit_arabic_translations(site=None, as_po=False, lang="ar"):
	"""Report UI labels that render untranslated on a live site.

	Covers the class no POT can see: Workspaces, Dashboard Charts, Number Cards
	and Reports ship as database fixtures, so the gettext extractor never sees
	them even though Frappe resolves them by msgid at render time.
	"""
	from arabic_translations.audit import report

	frappe.init(site=site)
	frappe.connect()
	try:
		report(as_po=as_po, lang=lang)
	finally:
		frappe.destroy()


commands = [install_arabic_translations, restore_original_translations, audit_arabic_translations]
