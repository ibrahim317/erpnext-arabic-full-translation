# Translation workflow

Canonical catalogs live in `arabic_translations/locale/source/<app>/ar.po`.
Everything else (v15/v16 bundles, the merged overlay) is generated.

## Prerequisites

```bash
sudo apt install gettext          # msgmerge, msgattrib, msgcat, msgfmt
pip install babel
```

## Find what needs translating

```bash
APP=erpnext   # or frappe / hrms
SRC=arabic_translations/locale/source/$APP/ar.po

# Sync against the current upstream POT first (download from
# https://raw.githubusercontent.com/frappe/$APP/version-16/$APP/locale/main.pot)
msgmerge -U --no-fuzzy-matching "$SRC" main.pot

# Extract untranslated entries
msgattrib --no-obsolete --untranslated "$SRC" -o to_translate.po
```

Translate the `msgstr` fields in `to_translate.po`, save as `translated.po`.

### Strings no POT contains

The steps above only find what is untranslated **in the POT**. They cannot find
what is untranslated **on screen**, because a whole class of UI labels never
reaches a POT: Workspaces and their Links and Shortcuts, Dashboard Charts,
Number Cards, Dashboards and Reports ship as JSON fixtures installed as database
records, so the gettext extractor never sees them. Frappe still resolves these
by msgid at render time, so defining them in our catalog is all that is needed --
but nothing upstream tells us they exist.

Read them back off a real site:

```bash
bench audit-arabic-translations --site <site>
bench audit-arabic-translations --site <site> --as-po   # paste-ready stubs

# or without the command, straight through execute:
bench --site <site> execute arabic_translations.audit.report
```

It is read-only. Add what it reports to `locale/source/<app>/ar.po` and rebuild.

Two consequences worth knowing:

* These msgids survive only where a catalog is **copied** rather than merged.
  `build.py` runs `msgmerge` against the POT and then `msgattrib --no-obsolete`
  on every PO bundle, which drops any entry the POT does not define, so all four
  PO bundles lose them: `v16/{frappe,erpnext,hrms}` and `v15/frappe`. The three
  v15 **CSV** bundles are written by `po_to_csv` straight from `locale/source/`
  and are never msgmerged, so they carry every one of them -- as do
  `locale/source/` itself and the merged `locale/ar.po`.

  In `overwrite` mode that makes this a **v16-only** gap. A v15 site is served
  the CSVs and does get these labels (on frappe >= 15.33 the compiled PO wins
  key by key, but it has no entry for them, so the CSV row stands). A **v16**
  site running `overwrite` alone will not get them; it needs `overlay` or
  `both`.
* A label that renders in English on a site whose other strings are Arabic is
  usually one of these, or a stale cache -- not a missing translation. Check the
  catalog before translating anything:

  ```bash
  msggrep -K -e "Incoming Leads" arabic_translations/locale/ar.po
  ```

## Merge back and regenerate

```bash
msgcat --use-first translated.po "$SRC" -o "$SRC.new" && mv "$SRC.new" "$SRC"

python scripts/build.py . /path/to/pots
python scripts/build_overlay.py arabic_translations/locale/source arabic_translations/locale/ar.po
python scripts/check_catalogs.py   # must pass
```

## Batch translation workflow

For a large pass it is easier to work from a JSON manifest than to edit PO files
by hand:

```bash
APP=erpnext
# 1. regenerate the list of open entries (untranslated + fuzzy)
python scripts/extract_todo.py $APP /tmp/pots/$APP-version-16.pot > todo.json

# 2. write batch.py containing  T = {index: "الترجمة", ...}
#    index = position in todo.json (0-based); partial dicts are fine

# 3. apply, then regenerate everything
python scripts/apply_trans.py $APP todo.json batch.py \
    arabic_translations/locale/source/$APP/ar.po
python scripts/build.py . /tmp/pots
python scripts/build_overlay.py arabic_translations/locale/source arabic_translations/locale/ar.po
python scripts/check_catalogs.py   # must pass
```

`apply_trans.py` refuses the whole batch and exits non-zero if any translation's
`{placeholder}` set differs from its `msgid` — Frappe passes `_()` output through
`str.format()`, so an invented placeholder is an `IndexError` in production. Fix
the batch file rather than weakening the check.

`todo.json` and the `batch.py` dicts are local working files, not part of the
app — regenerate the manifest whenever you need it and keep both out of commits.
Putting them under `translations_workbench/` keeps them gitignored for you.

## Rules (CI-enforced)

1. `msgfmt --check` clean on every catalog.
2. Never introduce a `{placeholder}` in `msgstr` that isn't in `msgid` —
   Frappe runs `str.format()` on translated strings; extras raise `IndexError`.
3. No HTML entities (`&#39;`…) unless present in the `msgid`.
4. Keep leading/trailing whitespace identical to the `msgid` (gettext requires it).
