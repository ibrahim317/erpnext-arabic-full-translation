# Arabic Translations for Frappe / ERPNext / HRMS

Complete Arabic translations for **Frappe Framework**, **ERPNext**, and **HRMS**, packaged as an installable Frappe app supporting **v15 and v16**.

## Coverage

Measured against the current upstream `version-16` POT templates (not a stale snapshot):

| App | Translated | Untranslated | Fuzzy (excluded at runtime) |
|---|---|---|---|
| Frappe | 6,239 (100%) | 0 | 1 |
| ERPNext | 10,039 (100%) | 0 | 8 |
| HRMS | 2,228 (100%) | 0 | 1 |

Every string in the current upstream `version-16` templates is translated. The overlay catalog additionally carries strings that upstream removed after v16 but that remain live on v15 — 19,259 unique messages in total. Untranslated strings fall back to English; nothing breaks.

## How it works

Frappe merges translations app by app **in installed order — later apps win**. This app ships a single merged catalog (`arabic_translations/locale/ar.po`); installed after `frappe`/`erpnext`/`hrms`, its strings override theirs without touching their source trees.

Two delivery modes, selected via `arabic_translations_mode` in `site_config.json`:

| Mode | What it does | Use when |
|---|---|---|
| `overlay` *(default)* | Compiles this app's own catalog. Other repos stay clean; survives `bench update`; works on Frappe Cloud. | Almost always |
| `overwrite` | Copies version-matched `ar.po`/`ar.csv` bundles into the other apps' trees (legacy behaviour), then force-compiles. | Docker images where assets are built from the patched files |
| `both` | Both of the above. | Belt and suspenders |

Version detection picks the newest bundle `<=` the running Frappe major version, so a future v17 still receives the v16 bundle instead of silently doing nothing.

### Version layout facts (verified against upstream)

- **Frappe v15 and v16** both use `frappe/locale/ar.po` (PO/gettext).
- **ERPNext / HRMS v15** still use `<app>/translations/ar.csv`; their **v16** branches use `<app>/locale/ar.po`.

The bundles in `arabic_translations/locale/other-apps/` follow exactly that layout.

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/anos4444/erpnext-arabic-full-translation
bench --site yoursite install-app arabic_translations
bench --site yoursite clear-cache
```

That's it for the default overlay mode. Translations are re-applied automatically:

- `after_install` — initial activation
- `after_app_install` — another app's install could ship its own `ar` catalog
- `after_migrate` — so `bench update` can't drop them
- `before_uninstall` — overwrite-mode files are git-restored; caches cleared

### Manual / CI application

```bash
# Apply for one site (respects arabic_translations_mode)
bench install-arabic-translations --site yoursite

# Force a mode for this run
bench install-arabic-translations --site yoursite --mode both

# Docker build (no site yet): copies bundles for every app in the environment
bench install-arabic-translations

# Undo overwrite mode (git-restores the touched files)
bench restore-original-translations --site yoursite
```

### Docker

```dockerfile
RUN bench get-app https://github.com/anos4444/erpnext-arabic-full-translation
RUN bench install-arabic-translations
RUN bench build
```

## Repository layout

```
arabic_translations/locale/
├── ar.po                      # merged overlay catalog (what overlay mode ships)
├── source/<app>/ar.po         # canonical per-app catalogs — edit these
└── other-apps/
    ├── v15/
    │   ├── frappe/frappe/locale/ar.po           # frappe v15 is PO-based
    │   ├── erpnext/erpnext/translations/ar.csv  # erpnext v15 is CSV-based
    │   └── hrms/hrms/translations/ar.csv
    └── v16/<app>/<app>/locale/ar.po
scripts/
├── build.py            # repair + regenerate all bundles from source catalogs
├── build_overlay.py    # regenerate the merged overlay catalog
├── corrections.py      # hand-written fixes for defective entries
└── check_catalogs.py   # CI gate: msgfmt, placeholder & artifact checks
```

## Contributing translations

Edit only `arabic_translations/locale/source/<app>/ar.po`, then regenerate:

```bash
pip install babel && sudo apt install gettext
python scripts/build.py . /path/to/pots       # rebuild v15+v16 bundles
python scripts/build_overlay.py arabic_translations/locale/source arabic_translations/locale/ar.po
python scripts/check_catalogs.py              # must pass before committing
```

Hard rules enforced by CI:

1. `msgfmt --check` must pass on every catalog.
2. A `msgstr` must never introduce a `{placeholder}` absent from its `msgid` — Frappe feeds `_()` output straight into `str.format()`, so extra placeholders raise `IndexError` → HTTP 500.
3. No HTML entity artifacts (`&#39;`, `&quot;`, …) in `msgstr`.
4. CSV bundles: no header row, no empty cells.

## Changelog

### 0.3.1

- **Fix install failure**: `pyproject.toml` was missing `[tool.bench.frappe-dependencies]`, so `bench get-app` and Frappe Cloud both rejected the app with *"Could not find compatible Frappe version in pyproject.toml"*. Declared `frappe = ">=15.0.0-dev,<17.0.0"`, matching the v15 and v16 bundles the app ships.

### 0.3.0

- **Complete Arabic translation pass** — the 1,095 open ERPNext entries plus 9 Frappe strings added upstream since the last pass. The ERPNext `version-16` bundle goes from **8,952 translated / 1,010 untranslated** to **10,039 translated / 0 untranslated**; Frappe and HRMS were already complete and stay at 0 untranslated.
- **Crowdin fill layer** (`scripts/fill_from_upstream.py`): harvests everything safe from the live upstream `version-16` Crowdin exports, rejecting any entry whose placeholders do not match the msgid.
- **Translation workbench** (`translations_workbench/`): the open-entry manifests and the per-batch Arabic dictionaries, so a future pass is a diff rather than a rewrite.
- Consistent Saudi ERP register throughout — Item = صنف, submit = ترحيل (docstatus sense, never إرسال), Journal Entry = قيد اليومية, Row #{0} = الصف رقم {0}, and the rest of the glossary applied uniformly.
- ERPNext fuzzy entries reduced from 85 to 8 in the v16 bundle (104 to 23 in the source catalog); the remainder stay flagged and are excluded from runtime by design.
- `scripts/` is now `ruff` clean.

### 0.2.0

- **Overlay mode** (new default): overrides translations without modifying other apps — Frappe Cloud safe, `bench update` safe.
- **Fixed 86 defective entries** (46 crash-risk: `msgstr` with placeholders missing from `msgid` → `IndexError` on `.format()`; 40 mistranslations from bad fuzzy matches).
- **Fixed corrupt PO header** in the Frappe catalog (duplicate `msgid ""` — `msgfmt` rejected the file; Arabic's 6 plural forms could be lost).
- **Added `v15/frappe` PO bundle** — the previous CSV was never loaded on v15 (Frappe v15 is PO-based; its own compiled MO overrode the CSV). 5,723 framework translations were silently dead.
- **v15 CSVs regenerated** from repaired catalogs; header row removed (Frappe ingested `msgid,msgstr` as a real translation).
- Removed 85 HTML entity artifacts; dropped 8 bogus `python-format` flags.
- Force-compile after copy (`copy2` preserved mtimes, making Frappe's compiler skip "up to date" MO files) and clear translation caches — translations now appear immediately.
- `after_install` replaces `before_install` (the catalog can only compile once the app is registered).
- `before_uninstall` cleanup; `restore-original-translations` command.
- Version-fallback bundle resolution (future v17 → v16 bundle).
- Reproducible build pipeline + CI validation gate.

## License

MIT
