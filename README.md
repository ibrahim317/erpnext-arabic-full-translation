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
├── terminology_fixes.py   # glossary + orthography rule table (reviewable)
├── apply_terminology.py   # applies terminology_fixes.py to the source catalogs
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

### 0.3.3

Corrects translations that were wrong rather than missing: the catalogs were
seeded from machine translation, so coverage reached 100% while the *sense* was
often wrong. **1,360 entries corrected and 225 newly translated.**

- **Wrong-sense terminology across every module** — `Stock` was read as *equity*
  (`Stock Entry` rendered as "entrance of the shares"), `Journal`/`Payment`/`Payroll
  Entry` as data entry, `Delivery Note`/`Credit Note` as remarks, `Leaves` as
  foliage, `-wise` as "wise", `Blanket Order` as a blanket, `Draft` as "project",
  `Leave` as "he departed", and `Amount` as the word already used for *Qty*.
  `Voucher`, `Dashboard`, `Timesheet` and `Sales Order` unified on one form each.
- **189 bilingual artifacts removed** — msgstrs carrying the Arabic followed by the
  untranslated English, which displayed both in the UI. Stripping the English tail
  exposed 4 latent placeholder bugs that failed `msgfmt --check`; those are fixed.
- **99 `Is X` checkbox labels** read as questions (`هل مجموعة؟`) or as a copula;
  Arabic field labels are noun phrases. Also adjective/noun order, number
  agreement, and reversed genitives (`Billed Qty` read "the invoices' quantity").
- **Orthography** — 149 spelling forms normalised against the catalogs' own usage
  (hamzat wasl, ta marbuta, `جاري` → `جارٍ`), doubled letters, missing spaces,
  13 misplaced-parenthesis renderings, Arabic presentation-form ligatures, and
  machine-translation stutter (`Finished Good` read `جيد جيد`).
- **Case-sensitive identifiers restored** — `MyISAM`, `StartTLS`, `lft`/`rgt` and
  `DocType` had been uppercased or transliterated, which breaks them as values.
- **225 new upstream strings translated** (101 Frappe, 124 ERPNext), keeping the
  v16 bundles at 0 untranslated against the current templates.
- **Two CI guards added**, both of which caught real defects when switched on:
  duplicate keys in the rule tables (Python silently keeps the last of a repeated
  dict key, so an earlier rule never runs), and cross-app divergence (the overlay
  merges frappe → erpnext → hrms with the later app winning, so a msgid corrected
  in an earlier app can still be overridden by an uncorrected copy in a later one).
- **Deterministic overlay build** — `POT-Creation-Date` is carried from the source
  catalog instead of being stamped with `now()`, so a rebuild produces a diff only
  when the translations actually changed.

### 0.3.2

- **Accounting register terminology** — the `Total` / `Credit` / `Debit` cluster corrected against live GL and Journal Entry screens: `Total` no longer reads "الاجمالي غير شامل الضريبة" (excluding tax) on every screen, GL columns use دائن/مدين, `Total Amount` no longer reads "الاعتماد الأساسي", and `Balance` no longer reads "الموازنة".
- **41 new upstream ERPNext strings translated** (reposting and stock-expense-accounting clusters added to `version-16` after the 0.3.0 pass), keeping the v16 bundle at 0 untranslated.
- **Review cleanup**: remove working files from the app source (translation workbench, internal instructions, stray git bundle); batch manifests are now generated by `scripts/extract_todo.py`; README version-layout section corrected to the v15.33 dual-ship reality.
- **v15 Frappe bundle now ships the CSV alongside the PO**, so benches pinned below 15.33 — which have no gettext support at all — get framework translations again. `build.py` generates both from the one source catalog.

### 0.3.1

- **Fix install failure**: `pyproject.toml` was missing `[tool.bench.frappe-dependencies]`, so `bench get-app` and Frappe Cloud both rejected the app with *"Could not find compatible Frappe version in pyproject.toml"*. Declared `frappe = ">=15.0.0-dev,<17.0.0"`, matching the v15 and v16 bundles the app ships.

### 0.3.0

- **Complete Arabic translation pass** — the 1,095 open ERPNext entries plus 9 Frappe strings added upstream since the last pass. The ERPNext `version-16` bundle goes from **8,952 translated / 1,010 untranslated** to **10,039 translated / 0 untranslated**; Frappe and HRMS were already complete and stay at 0 untranslated.
- **Crowdin fill layer** (`scripts/fill_from_upstream.py`): harvests everything safe from the live upstream `version-16` Crowdin exports, rejecting any entry whose placeholders do not match the msgid.
- Consistent Saudi ERP register throughout — Item = صنف, submit = ترحيل (docstatus sense, never إرسال), Journal Entry = قيد اليومية, Row #{0} = الصف رقم {0}, and the rest of the glossary applied uniformly.
- ERPNext fuzzy entries reduced from 85 to 8 in the v16 bundle (104 to 23 in the source catalog); the remainder stay flagged and are excluded from runtime by design.
- `scripts/` is now `ruff` clean.

### 0.2.0

- **Overlay mode** (new default): overrides translations without modifying other apps — Frappe Cloud safe, `bench update` safe.
- **Fixed 86 defective entries** (46 crash-risk: `msgstr` with placeholders missing from `msgid` → `IndexError` on `.format()`; 40 mistranslations from bad fuzzy matches).
- **Fixed corrupt PO header** in the Frappe catalog (duplicate `msgid ""` — `msgfmt` rejected the file; Arabic's 6 plural forms could be lost).
- **Added `v15/frappe` PO bundle** — the CSV alone was not being loaded on maintained v15 benches (from v15.33 Frappe compiles its own `ar.po`, and the resulting MO overrides the CSV key by key). 5,723 framework translations were silently dead. Since 0.3.2 both files ship.
- **v15 CSVs regenerated** from repaired catalogs; header row removed (Frappe ingested `msgid,msgstr` as a real translation).
- Removed 85 HTML entity artifacts; dropped 8 bogus `python-format` flags.
- Force-compile after copy (`copy2` preserved mtimes, making Frappe's compiler skip "up to date" MO files) and clear translation caches — translations now appear immediately.
- `after_install` replaces `before_install` (the catalog can only compile once the app is registered).
- `before_uninstall` cleanup; `restore-original-translations` command.
- Version-fallback bundle resolution (future v17 → v16 bundle).
- Reproducible build pipeline + CI validation gate.

## License

MIT
