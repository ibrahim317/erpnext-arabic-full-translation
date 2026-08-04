# CLAUDE CODE — arabic_translations: finish ERPNext translation pass, release v0.3.0

You are working in the `erpnext-arabic-full-translation` repo (to be hosted at
github.com/anos4444). Two commits exist: `v0.2.0` (repairs + overlay architecture)
and the translation-pass-1 commit (hrms 100%, frappe 100%, erpnext 8,952/10,047).
Your job: translate the remaining **1,095 ERPNext entries**, rebuild, validate,
release **v0.3.0**, push.

Work on `main`. Commit in the logical units below.

---

## Environment setup (once)

```bash
sudo apt-get install -y gettext        # msgfmt, msgmerge, msgattrib
pip install babel
```

Sanity check before touching anything:

```bash
python scripts/check_catalogs.py       # MUST print "All catalogs clean."
```

## Repo facts (do not rediscover)

- **Canonical catalogs**: `arabic_translations/locale/source/<app>/ar.po`. Edit ONLY these.
- **Generated** (never hand-edit): `locale/other-apps/**` bundles and `locale/ar.po` overlay.
- `scripts/build.py . /path/to/pots` regenerates bundles from sources. It only runs
  its bootstrap-repair when `locale/source` is absent — with sources present it is
  a pure source→bundle generator. NEVER delete `locale/source`.
- POT templates: download once to `/tmp/pots/` as `<app>-version-16.pot` and
  `frappe-version-15.pot` from
  `https://raw.githubusercontent.com/frappe/<app>/<branch>/<app>/locale/main.pot`.
- The upstream `version-16` `ar.po` files are the live Crowdin exports (project
  639578). `scripts/fill_from_upstream.py` already harvested everything safe from
  them — re-running it is idempotent and cheap; do it once at the start in case
  Crowdin has synced new strings since.
- Frappe feeds `_()` output straight into `str.format()`. A `{placeholder}` in a
  msgstr that is not in the msgid = IndexError = HTTP 500 in production.
  `scripts/apply_trans.py` and `scripts/check_catalogs.py` both enforce this.
- `python-format` flags are noise (Frappe never uses %-formatting); the pipeline
  strips them. Do not re-add.

## The translation task

`translations_workbench/erpnext-remaining.json` lists the 1,095 open entries as
`{"id": msgid, "ctx": context, "old": fuzzy-suggestion-or-null}`.

### Batch workflow (repeat until empty, ~150–200 entries per batch)

1. Read a slice of `erpnext-remaining.json`.
2. Write `translations_workbench/erpnext-ar-N.py` containing a dict `T = {index: "الترجمة", ...}`
   where index = position in `erpnext-remaining.json` (0-based). Partial dicts are
   fine — the applier tolerates gaps. Look at `erpnext-ar-1.py` for the format and
   at `hrms-ar.py` for register/terminology.
3. Apply + validate:

```bash
python scripts/apply_trans.py erpnext \
    translations_workbench/erpnext-remaining.json \
    translations_workbench/erpnext-ar-N.py \
    arabic_translations/locale/source/erpnext/ar.po
msgfmt --check --statistics -o /dev/null arabic_translations/locale/source/erpnext/ar.po
```

   `apply_trans.py` exits non-zero listing any placeholder mismatches — fix the
   batch file, never weaken the check.
4. Commit each batch: `git commit -am "erpnext translation batch N (indices X–Y)"`.

### Translation rules (Saudi ERP register — match the existing catalogs)

- Formal MSA, Saudi HR/accounting terminology. Consistency beats elegance.
- Glossary (already used throughout — do not deviate):
  - Item = صنف (never بند/عنصر) · Warehouse = مستودع · Batch = دفعة
  - Serial No = الرقم التسلسلي · Sales Order = أمر البيع · Purchase Order = أمر الشراء
  - Delivery Note = إشعار تسليم · Purchase Receipt = إيصال شراء · Stock Entry = قيد المخزون
  - submit/submitted = ترحيل/مُرحّل (docstatus sense, never إرسال) · cancel = إلغاء
  - Journal Entry = قيد اليومية · GL = دفتر الأستاذ العام · debit/credit = مدين/دائن
  - Payment Entry = قيد الدفع · voucher = سند · reconcile = تسوية
  - BOM = قائمة المواد · Work Order = أمر العمل · UOM = وحدة القياس
  - Subcontracting = التعاقد من الباطن · allocation = تخصيص · accrual = استحقاق
  - Leave = إجازة · benefit = ميزة · overtime = عمل إضافي · arrears = متأخرات
  - Row #{0} = الصف رقم {0} · mandatory = إلزامي · default = افتراضي
- Preserve EXACTLY: `{0}`-style placeholders (count and names), HTML tags and
  attributes, `\n`/`\t`, leading/trailing whitespace (the applier copies edge
  whitespace from the msgid automatically — still don't fight it), `<b>…</b>`
  emphasis positions.
- Literal `{{` `}}` in msgids are escaped braces — keep them literal.
- Empty-ish msgids (`"  "`, `"<hr>"`) → translate as themselves.
- The `old` field is the discarded fuzzy match — often WRONG (attached to a
  different English string). Use it only as vocabulary inspiration; translate the
  `id`, not the `old`.
- If a string is untranslatable-in-isolation (bare identifiers like
  `modify_half_day_status`), keep the English verbatim as the translation.

## Release v0.3.0 (after the last batch)

```bash
# 1. final harvest + rebuild + gate
python scripts/fill_from_upstream.py
python scripts/build.py . /tmp/pots
python scripts/build_overlay.py arabic_translations/locale/source arabic_translations/locale/ar.po
python scripts/check_catalogs.py          # must be clean
ruff check arabic_translations scripts    # must be clean

# 2. verify coverage — target: 0 untranslated on all three v16 bundles
for app in frappe erpnext hrms; do
  msgfmt --statistics -o /dev/null \
    arabic_translations/locale/other-apps/v16/$app/$app/locale/ar.po
done
```

3. Update `README.md`: coverage table to the real final numbers, add a `0.3.0`
   changelog section ("complete Arabic translation pass: X new strings translated,
   Crowdin fill layer, translation workbench").
4. Bump `arabic_translations/__init__.py` to `__version__ = "0.3.0"`.
5. Commit `v0.3.0: complete Arabic translation pass`, tag `v0.3.0`.

## Publish to anos4444

```bash
gh repo create anos4444/erpnext-arabic-full-translation --public \
  --description "Complete Arabic translations for Frappe, ERPNext & HRMS (v15/v16) — installable app with overlay mode" \
  --source . --push
git push origin v0.2.0 v0.3.0
git remote add upstream https://github.com/ibrahim317/erpnext-arabic-full-translation.git
```

Then open a PR from `anos4444:main` → `ibrahim317:develop`; the two release commit
messages are the PR body.

## Hard constraints

- NEVER edit files under `locale/other-apps/` or `locale/ar.po` by hand.
- NEVER delete `locale/source/` (build.py would re-bootstrap and lose everything).
- NEVER commit if `check_catalogs.py` fails.
- Do not "fix" Arabic text flagged by ruff RUF001 — it is whitelisted in
  pyproject; Arabic letters are not ambiguous unicode.
- The 85 remaining fuzzy entries in the erpnext source are excluded from runtime
  by design; the remaining-json includes them — your batch translations replace
  them and clear the flag automatically.
