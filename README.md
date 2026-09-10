# Arabic Translations for Frappe / ERPNext / HRMS

Complete Arabic translations for **Frappe Framework**, **ERPNext**, and **HRMS**, packaged as an installable Frappe app supporting **v15 and v16**.

## Coverage

Measured against the current upstream `version-16` POT templates (not a stale snapshot):

| App | Translated | Untranslated | Fuzzy (excluded at runtime) |
|---|---|---|---|
| Frappe | 6,328 (100%) | 0 | 1 |
| ERPNext | 10,181 (100%) | 0 | 11 |
| HRMS | 2,228 (100%) | 0 | 1 |

Every string in the current upstream `version-16` templates is translated. The overlay catalog additionally carries strings that upstream removed after v16 but that remain live on v15 — 19,523 unique messages in total. Untranslated strings fall back to English; nothing breaks.

## How it works

Frappe merges translations app by app **in installed order — later apps win**. This app ships a single merged catalog (`arabic_translations/locale/ar.po`); installed after `frappe`/`erpnext`/`hrms`, its strings override theirs without touching their source trees.

Two delivery modes, selected via `arabic_translations_mode` in `site_config.json`:

| Mode | What it does | Use when |
|---|---|---|
| `overlay` *(default)* | Compiles this app's own catalog. Other repos stay clean; survives `bench update`; works on Frappe Cloud. | Almost always |
| `overwrite` | Copies version-matched `ar.po`/`ar.csv` bundles into the other apps' trees (legacy behaviour), then force-compiles. | Docker images where assets are built from the patched files |
| `both` | Both of the above. | Belt and suspenders |

Version detection picks the newest bundle `<=` the running Frappe major version, so a future v17 still receives the v16 bundle instead of silently doing nothing.

### Version layout facts (verified against upstream release tags)

The usual summary — "CSV until v15, gettext from v16" — is right for ERPNext and
HRMS but not for the framework, which got the gettext backport mid-v15:

- **Frappe v15.0–v15.32** reads `frappe/translations/ar.csv`. **v15.33.0** backported
  gettext, so **v15.33+ and v16** read `frappe/locale/ar.po`. Verifiable per tag: the
  `v15.32.0` tree ships the CSV and has no `locale/ar.po`; `v15.33.0` ships the PO and
  has no `translations/ar.csv`. From v15.33 the loader reads CSV first and then the
  compiled MO, so **the MO overrides the CSV key by key** — a CSV-only package's
  framework translations are silently dead on any bench at v15.33 or later.
- **ERPNext / HRMS v15** are CSV throughout (`<app>/translations/ar.csv`); their **v16**
  branches use `<app>/locale/ar.po`. Neither got the backport.
- **The v15 Frappe bundle therefore ships both**: the CSV serves benches pinned below
  15.33 (which have no PO machinery at all), the PO serves 15.33+ (where the CSV alone
  would lose to Frappe's own MO). Both are generated from the same source catalog, so
  they cannot drift.

The bundles in `arabic_translations/locale/other-apps/` follow exactly that layout.

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/ibrahim317/erpnext-arabic-full-translation
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
RUN bench get-app https://github.com/ibrahim317/erpnext-arabic-full-translation
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
    │   ├── frappe/frappe/locale/ar.po            # frappe >=15.33 (its own MO beats a CSV)
    │   ├── frappe/frappe/translations/ar.csv     # frappe <15.33 (no PO machinery yet)
    │   ├── erpnext/erpnext/translations/ar.csv   # erpnext v15 is CSV-only
    │   └── hrms/hrms/translations/ar.csv         # hrms v15 is CSV-only
    └── v16/<app>/<app>/locale/ar.po
scripts/
├── build.py            # repair + regenerate all bundles from source catalogs
├── build_overlay.py    # regenerate the merged overlay catalog
├── extract_todo.py     # regenerate the open-entries manifest for a translation pass
├── apply_trans.py      # apply a batch dict onto a source catalog (placeholder-guarded)
├── fill_from_upstream.py  # harvest safe entries from the upstream Crowdin exports
├── corrections.py      # hand-written fixes for placeholder-defective entries
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

## License

MIT
