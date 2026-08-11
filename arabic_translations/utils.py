"""Installation / activation logic for the Arabic Translations app.

Two delivery modes are supported, selected via ``arabic_translations_mode`` in
site config:

``overlay`` (default, recommended)
    Nothing outside this app is touched.  The app ships a single merged
    ``arabic_translations/locale/ar.po``.  Frappe merges translations app by app
    in installed order and later apps win, so - as long as this app is installed
    after ``frappe``/``erpnext``/``hrms`` - its strings override theirs.
    Survives ``bench update``, keeps other app repos clean, works on
    Frappe Cloud.

``overwrite``
    Legacy behaviour: copy version-matched ``ar.po`` / ``ar.csv`` bundles
    directly into the other apps' source trees.  Needed when assets must be
    built from the patched files (custom Docker images), but leaves the other
    app repos dirty and is undone by ``bench update``.

``both``
    Do both.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import frappe

_LOGGER = frappe.logger("arabic_translations")

APP_NAME = "arabic_translations"
LOCALE = "ar"
BUNDLE_FILENAMES = {"ar.po", "ar.csv"}
VALID_MODES = ("overlay", "overwrite", "both")
DEFAULT_MODE = "overlay"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _locale_root() -> Path:
	return Path(__file__).parent / "locale"


def get_mode() -> str:
	"""Resolve delivery mode from site config, falling back to the default."""
	mode = DEFAULT_MODE
	try:
		mode = (frappe.conf.get("arabic_translations_mode") or DEFAULT_MODE).strip().lower()
	except Exception:
		pass
	if mode not in VALID_MODES:
		_LOGGER.warning("Unknown arabic_translations_mode %r; using %r", mode, DEFAULT_MODE)
		mode = DEFAULT_MODE
	return mode


def get_frappe_major_version() -> int | None:
	raw = getattr(frappe, "__version__", "") or ""
	for sep in ("-", "+"):
		if sep in raw:
			raw = raw.split(sep, 1)[0]
			break
	try:
		return int(raw.split(".")[0])
	except Exception:
		return None


def available_bundle_versions() -> list[int]:
	root = _locale_root() / "other-apps"
	if not root.is_dir():
		return []
	versions = []
	for entry in root.iterdir():
		if entry.is_dir() and entry.name.startswith("v") and entry.name[1:].isdigit():
			versions.append(int(entry.name[1:]))
	return sorted(versions)


def resolve_bundle_version(major: int | None) -> int | None:
	"""Pick the newest bundle that is <= the running Frappe major version.

	A future Frappe v17 therefore still gets the v16 bundle instead of
	silently installing nothing.
	"""
	versions = available_bundle_versions()
	if not versions or major is None:
		return None
	candidates = [v for v in versions if v <= major]
	if not candidates:
		_LOGGER.warning("Frappe v%s is older than the oldest bundle (v%s)", major, versions[0])
		return None
	return candidates[-1]


def _installed_apps() -> list[str]:
	try:
		return list(frappe.get_installed_apps())
	except Exception:
		try:
			return list(frappe.get_all_apps(with_internal=True))
		except Exception:
			_LOGGER.warning("Could not determine installed apps; nothing to do")
			return []


def clear_translation_cache() -> None:
	try:
		from frappe.translate import clear_cache

		clear_cache()
		_LOGGER.info("Cleared translation cache")
	except Exception:
		_LOGGER.exception("Could not clear the translation cache")


def compile_locale(app: str) -> bool:
	"""Compile ``<app>/locale/ar.po`` into the bench-level assets MO file.

	Frappe skips compilation when the MO is newer than the PO, so this forces a
	rebuild - copied files could otherwise carry stale mtimes.
	"""
	try:
		from frappe.gettext.translate import compile_translations

		compile_translations(target_app=app, locale=LOCALE, force=True)
		return True
	except ImportError:
		# Pre-PO Frappe: nothing to compile.
		return False
	except Exception:
		_LOGGER.exception("Failed to compile translations for %s", app)
		return False


# --------------------------------------------------------------------------- #
# overlay mode
# --------------------------------------------------------------------------- #
def apply_overlay() -> None:
	"""Compile this app's own catalog so Frappe picks it up as an override."""
	po_path = _locale_root() / f"{LOCALE}.po"
	if not po_path.is_file():
		_LOGGER.warning("Overlay catalog missing at %s", po_path)
		return

	compile_locale(APP_NAME)
	clear_translation_cache()
	_LOGGER.info("Arabic overlay catalog activated")


def check_overlay_precedence() -> list[str]:
	"""Return apps installed *after* this one - those would shadow the overlay.

	Frappe merges translations in installed-app order with later apps winning.
	"""
	apps = _installed_apps()
	if APP_NAME not in apps:
		return []
	return apps[apps.index(APP_NAME) + 1 :]


# --------------------------------------------------------------------------- #
# overwrite mode
# --------------------------------------------------------------------------- #
def copy_locale_files(apps: list[str] | None = None, version: int | None = None) -> list[str]:
	"""Copy version-matched Arabic bundles into the other apps' source trees."""
	major = version or get_frappe_major_version()
	bundle_version = resolve_bundle_version(major)
	if bundle_version is None:
		_LOGGER.warning("No Arabic bundle available for Frappe v%s; skipping copy", major)
		return []

	source_root = _locale_root() / "other-apps" / f"v{bundle_version}"
	if not source_root.is_dir():
		_LOGGER.warning("Bundle path missing: %s", source_root)
		return []

	if apps is None:
		apps = _installed_apps()

	written: list[str] = []
	for app in apps or []:
		written.extend(_copy_for_app(app, source_root))

	touched_apps = sorted({a for a in (apps or []) if (source_root / a).is_dir()})
	for app in touched_apps:
		compile_locale(app)

	if written:
		clear_translation_cache()
	return written


def _copy_for_app(app: str, source_root: Path) -> list[str]:
	app_source_dir = source_root / app
	if not app_source_dir.is_dir():
		_LOGGER.debug("No Arabic bundle for app %s", app)
		return []

	try:
		app_dest_root = Path(frappe.get_app_path(app))
	except Exception:
		_LOGGER.warning("Could not resolve app path for %s; skipping", app)
		return []

	written: list[str] = []
	for dirpath, _dirs, files in os.walk(app_source_dir):
		for filename in files:
			if filename not in BUNDLE_FILENAMES:
				continue

			source_file = Path(dirpath) / filename
			rel_path = source_file.relative_to(app_source_dir)
			# Bundles are laid out as <app>/<app>/locale/ar.po - drop the extra
			# leading app folder so we land in the real app root.
			if rel_path.parts and rel_path.parts[0] == app:
				rel_path = Path(*rel_path.parts[1:])

			dest_path = app_dest_root / rel_path
			dest_path.parent.mkdir(parents=True, exist_ok=True)

			# NB: shutil.copy (not copy2). Preserving the source mtime would make
			# Frappe's compiler consider an existing .mo "up to date" and skip it.
			shutil.copy(source_file, dest_path)
			os.utime(dest_path, None)
			written.append(str(dest_path))
			_LOGGER.info("Copied %s -> %s", filename, dest_path)

	return written


def restore_locale_files(apps: list[str] | None = None) -> list[str]:
	"""Undo overwrite mode by checking bundle files back out of each app's git tree."""
	import subprocess

	restored: list[str] = []
	for app in apps or _installed_apps():
		if app == APP_NAME:
			continue
		try:
			app_root = Path(frappe.get_app_path(app)).parent
		except Exception:
			continue
		for rel in (f"{app}/locale/{LOCALE}.po", f"{app}/translations/{LOCALE}.csv"):
			target = app_root / rel
			if not target.exists():
				continue
			try:
				subprocess.run(
					["git", "checkout", "--", rel],
					cwd=app_root,
					check=True,
					capture_output=True,
				)
				restored.append(str(target))
			except Exception:
				_LOGGER.warning("Could not restore %s via git", target)
		compile_locale(app)

	clear_translation_cache()
	return restored


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #
def apply_translations(mode: str | None = None, apps: list[str] | None = None) -> None:
	mode = mode or get_mode()
	if mode in ("overlay", "both"):
		apply_overlay()
	if mode in ("overwrite", "both"):
		copy_locale_files(apps=apps)


# --------------------------------------------------------------------------- #
# hooks
# --------------------------------------------------------------------------- #
def after_install(*args, **kwargs) -> None:
	try:
		apply_translations()
	except Exception:
		_LOGGER.exception("Failed to apply Arabic translations during install")


def before_install(*args, **kwargs) -> None:
	# Kept for backwards compatibility with deployments pinning the old hook
	# name. Real work happens in after_install: the overlay catalog can only be
	# compiled once the app is registered on the bench.
	return None


def after_app_install(app_name: str | None = None, *args, **kwargs) -> None:
	"""Re-apply after another app installs (it may ship its own ar.po/ar.csv)."""
	if app_name == APP_NAME:
		return
	try:
		apply_translations()
		_LOGGER.info("Re-applied Arabic translations after install of %s", app_name or "app")
	except Exception:
		_LOGGER.exception("Failed to re-apply Arabic translations after app install")


def after_app_uninstall(app_name: str | None = None, *args, **kwargs) -> None:
	try:
		clear_translation_cache()
	except Exception:
		_LOGGER.exception("Failed to clear translation cache after app uninstall")


def after_migrate() -> None:
	try:
		apply_translations()
		_LOGGER.info("Re-applied Arabic translations after migrate")
	except Exception:
		_LOGGER.exception("Failed to re-apply Arabic translations after migrate")


def before_uninstall(*args, **kwargs) -> None:
	try:
		if get_mode() in ("overwrite", "both"):
			restore_locale_files()
		clear_translation_cache()
	except Exception:
		_LOGGER.exception("Failed to clean up Arabic translations during uninstall")
