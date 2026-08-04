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

## Merge back and regenerate

```bash
msgcat --use-first translated.po "$SRC" -o "$SRC.new" && mv "$SRC.new" "$SRC"

python scripts/build.py . /path/to/pots
python scripts/build_overlay.py arabic_translations/locale/source arabic_translations/locale/ar.po
python scripts/check_catalogs.py   # must pass
```

## Rules (CI-enforced)

1. `msgfmt --check` clean on every catalog.
2. Never introduce a `{placeholder}` in `msgstr` that isn't in `msgid` —
   Frappe runs `str.format()` on translated strings; extras raise `IndexError`.
3. No HTML entities (`&#39;`…) unless present in the `msgid`.
4. Keep leading/trailing whitespace identical to the `msgid` (gettext requires it).
