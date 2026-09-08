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

## Terminology corrections

Wrong-sense translations are fixed as a *rule table*, not by editing PO entries
one at a time, so a reviewer can check the reasoning rather than 600 diff hunks:

```bash
python scripts/apply_terminology.py --dry-run   # report; sample diff to /tmp
python scripts/apply_terminology.py             # rewrite the source catalogs
```

`scripts/terminology_fixes.py` holds three tables:

* `GLOSSARY` — `(guard, pattern, replacement)`. The pattern is rewritten in the
  msgstr only when `guard` matches the **msgid**. The guard is what makes this
  safe: it stops `سهم` (arrow) in `Ctrl + Up` being rewritten as inventory.
* `EXACT` — full msgstr replacements, keyed by app then msgid, for entries whose
  machine translation is word-salad and cannot be repaired by substitution.
* `ORTHOGRAPHY` — unguarded spelling fixes (hamzat wasl, ta marbuta).

The script aborts before writing if any rewrite would give a msgstr a
`{placeholder}` its msgid lacks. It is idempotent: running it on already-corrected
catalogs reports zero changes.

## Rules (CI-enforced)

1. `msgfmt --check` clean on every catalog.
2. Never introduce a `{placeholder}` in `msgstr` that isn't in `msgid` —
   Frappe runs `str.format()` on translated strings; extras raise `IndexError`.
3. No HTML entities (`&#39;`…) unless present in the `msgid`.
4. Keep leading/trailing whitespace identical to the `msgid` (gettext requires it).
