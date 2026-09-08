"""Terminology and orthography corrections for the Arabic catalogs.

The catalogs were seeded from machine translation and carry three families of
defect that no placeholder check can catch:

* **Wrong sense chosen for a homograph.**  ``Stock`` was read as *equity* and
  rendered ``أسهم`` (shares) throughout the inventory module — ``Stock Entry``
  became ``دخول الأسهم`` ("entrance of the shares").  ``Leave`` became the verb
  ``غادر``, ``Draft`` became ``مشروع`` (project), ``Amount`` became ``كمية``
  (quantity — the word ERPNext already uses for *Qty*).
* **Word-by-word rendering of a compound doctype name.**  ``Delivery Note``
  became ``ملاحظة التسليم`` (a remark about delivery) rather than the shipping
  document ``إشعار التسليم``; ``Journal Entry`` became ``إدخال دفتر اليومية``
  (data *entry*) rather than the accounting record ``قيد اليومية``.
* **Pipeline artifacts.**  A literal ``\\n<br>\\n`` followed by the untranslated
  English, misplaced parentheses that break RTL rendering, and hamzat-wasl
  spellings (``إستلام`` for ``استلام``).

Register is Gulf/Saudi ERP standard, matching the glossary the README already
declares.  Rules are applied by ``scripts/apply_terminology.py``.
"""

# --------------------------------------------------------------------------
# 1. Guarded glossary substitutions.
#
# (guard, pattern, replacement) — `pattern` is rewritten in the msgstr only
# when `guard` matches the *msgid*.  The guard is what keeps these safe: it
# stops "سهم" (arrow) in "Ctrl + Up" from being rewritten as inventory, and
# stops "إجازة" appearing where "Leave" meant "leave blank".
# --------------------------------------------------------------------------
GLOSSARY = [
	# -- Stock read as equity ------------------------------------------------
	(r"\bStock\b",           r"سوق الأسهم",            "المخزون"),
	(r"\bStock\b",           r"الأسهم",                "المخزون"),
	(r"\bStock\b",           r"أسهم",                  "مخزون"),
	(r"\bStock\b",           r"السهم",                 "المخزون"),
	(r"\bStock\b",           r"اسهم",                  "مخزون"),

	# -- Entry: accounting/stock record is قيد, not data entry ---------------
	(r"\bJournal Entry\b",   r"إدخال دفتر اليومية",    "قيد اليومية"),
	(r"\bJournal Entry\b",   r"إدخال القيود اليومية",  "قيد اليومية"),
	(r"\bJournal Entry\b",   r"دخول دفتر اليومية",     "قيد اليومية"),
	(r"\bJournal Entr",      r"إدخالات دفتر اليومية",  "قيود اليومية"),
	(r"\bJournal Entr",      r"إدخالات قيد اليومية",   "قيود اليومية"),
	(r"\bJournal Entr",      r"القيود اليومية",        "قيد اليومية"),
	(r"\bJournal Entr",      r"دخول المجلة",           "قيد اليومية"),
	(r"\bJournal Entr",      r"إدخال المجلة",          "قيد اليومية"),
	(r"\bJournal Entr",      r"مدخل يومية",            "قيد يومية"),
	(r"\bPayment Entr",      r"تدوينات المدفوعات",     "قيد الدفع"),
	(r"\bPayment Entr",      r"تدوين المدفوعات",       "قيد الدفع"),
	(r"\bPayment Entr",      r"تدوين مدفوعات",         "قيد الدفع"),
	(r"\bPayment Entr",      r"إدخالات الدفع",         "قيود الدفع"),
	(r"\bPayment Entr",      r"مدخلات الدفع",          "قيود الدفع"),
	(r"\bPayment Entr",      r"إدخال الدفعة",          "قيد الدفع"),
	(r"\bPayment Entr",      r"إدخال الدفع",           "قيد الدفع"),
	(r"\bPayment Entr",      r"إدخال دفع",             "قيد دفع"),
	(r"\bPayment Entr",      r"ادخال دفعات",           "قيود الدفع"),
	(r"\bPayment Entr",      r"دفع الدخول",            "قيد الدفع"),
	(r"\bPayroll Entry\b",   r"دخول الرواتب",          "قيد الرواتب"),
	(r"\bPayroll Entry\b",   r"إدخال الرواتب",         "قيد الرواتب"),
	(r"\bStock Entr",        r"إدخال المخزون",         "قيد المخزون"),
	(r"\bStock Entr",        r"ادخال المخزون",         "قيد المخزون"),
	(r"\bStock Entr",        r"إدخالات المخزون",       "قيود المخزون"),
	(r"\bStock Entr",        r"تدوينات مخزون",         "قيود مخزون"),
	(r"\bStock Entr",        r"إدخال مخزون",           "قيد مخزون"),
	(r"\bLedger Entr",       r"إدخال دفتر أستاذ",      "قيد دفتر الأستاذ"),
	(r"\bLedger Entr",       r"إدخالات دفتر الأستاذ",  "قيود دفتر الأستاذ"),
	(r"\bOpening Entr",      r"إدخالات افتتاحية",      "قيود افتتاحية"),
	(r"\bOpening Entr",      r"إدخالات الافتتاح",      "القيود الافتتاحية"),
	(r"\bOpening Entry\b",   r"مدخل افتتاح",           "قيد افتتاحي"),
	(r"\bOpening Entry\b",   r"إدخال فتح",             "قيد افتتاحي"),

	# -- Note: the shipping/credit document is إشعار, not a remark -----------
	(r"\bDelivery Note",     r"ملاحظات التسليم",       "إشعارات التسليم"),
	(r"\bDelivery Note",     r"مذكرات التسليم",        "إشعارات التسليم"),
	(r"\bDelivery Note",     r"ملاحظة التسليم",        "إشعار التسليم"),
	(r"\bDelivery Note",     r"مذكرة التسليم",         "إشعار التسليم"),
	(r"\bDelivery Note",     r"ملاحظه التسليم",        "إشعار التسليم"),
	(r"\bDelivery Note",     r"مذكرة تسليم",           "إشعار تسليم"),
	(r"\bDelivery Note",     r"ملاحظة تسليم",          "إشعار تسليم"),
	(r"\bCredit Note\b",     r"ملاحظة الائتمان",       "الإشعار الدائن"),
	(r"\bCredit Note\b",     r"مذكرة ائتمان",          "إشعار دائن"),
	(r"\bDebit Note\b",      r"ملاحظة الخصم",          "الإشعار المدين"),
	(r"\bDebit Note\b",      r"مذكرة خصم",             "إشعار مدين"),

	# -- Voucher is سند; إيصال is a payment receipt -------------------------
	(r"\bVoucher\b",         r"الإيصال",               "السند"),
	(r"\bVoucher\b",         r"إيصال",                 "سند"),
	(r"\bVoucher\b",         r"القسيمة",               "السند"),
	(r"\bVoucher\b",         r"قسيمة",                 "سند"),

	# -- Leave (HR) is إجازة, never the verb "to depart" --------------------
	(r"\bLeave Ledger",      r"ترك دخول دفتر الأستاذ", "قيد دفتر أستاذ الإجازات"),
	(r"\bLeave Encashment",  r"إجازة مغادرة السيارات", "استبدال الإجازة نقدًا"),
]

# --------------------------------------------------------------------------
# 2. Exact msgid -> msgstr rewrites.
#
# Entries whose machine translation is word-salad and cannot be repaired by
# substitution.  Keyed by app so an identical msgid in two apps can differ.
# --------------------------------------------------------------------------
EXACT = {
	"frappe": {
		"Draft": "مسودة",
		"Ledger": "دفتر الأستاذ",
		"Warehouse": "المستودع",
		"Post": "نشر",
		"Create Entry": "إنشاء قيد",
	},
	"erpnext": {
		# Stock read as equity, beyond what substitution repairs
		"Stock In Hand": "المخزون المتاح",
		"In Stock Qty": "الكمية المتوفرة في المخزون",
		"Not in stock": "غير متوفر في المخزون",
		"Non stock items": "أصناف غير مخزنية",
		"Stock Entry {0} created": "تم إنشاء قيد المخزون {0}",
		"Stock Entry Child": "تفاصيل قيد المخزون",
		"Stock and Account Value Comparison": "مقارنة قيمة المخزون والحساب",
		"Show Stock Ageing Data": "عرض بيانات تقادم المخزون",
		"Qty as per Stock UOM": "الكمية حسب وحدة قياس المخزون",
		"Quick Stock Balance": "رصيد المخزون السريع",
		"Project wise Stock Tracking ": "تتبع المخزون حسب المشروع ",
		"Warehouse required for stock Item {0}": "المستودع مطلوب للصنف المخزني {0}",
		"Cannot change Attributes after stock transaction. Make a new Item and transfer stock to the new Item":
			"لا يمكن تغيير الخصائص بعد إجراء حركة مخزنية. أنشئ صنفًا جديدًا وحوّل المخزون إليه",
		"Stock Entry (Outward GIT)": "قيد المخزون (بضاعة بالطريق صادرة)",
		"Default Stock UOM": "وحدة قياس المخزون الافتراضية",
		"Please set default UOM in Stock Settings": "يرجى تعيين وحدة القياس الافتراضية في إعدادات المخزون",

		# Accounting entries rendered as "entrance"
		"Cash Entry": "قيد نقدي",
		"Contra Entry": "قيد مقابل",
		"Excise Entry": "قيد المكوس",
		"Entry Type": "نوع القيد",
		"GL Entry": "قيد دفتر الأستاذ العام",
		"Write Off Entry": "قيد الشطب",
		"Downtime Entry": "قيد وقت التوقف",
		"Opening Entry": "قيد افتتاحي",
		"Is Opening Entry": "قيد افتتاحي؟",
		"Invalid Opening Entry": "قيد افتتاحي غير صالح",
		"Make Difference Entry": "إنشاء قيد الفرق",
		"Credit Card Entry": "قيد بطاقة ائتمان",
		"Loyalty Point Entry": "قيد نقاط الولاء",
		"Loyalty Point Entry Redemption": "استبدال قيد نقاط الولاء",
		"Inter Company Journal Entry": "قيد يومية بين الشركات",
		"Inter Company Journal Entry Reference": "مرجع قيد اليومية بين الشركات",
		"Reverse Journal Entry": "عكس قيد اليومية",
		"Journal Entry Account": "حساب قيد اليومية",
		"Series for Asset Depreciation Entry (Journal Entry)": "التسلسل لقيد إهلاك الأصل (قيد اليومية)",
		"Book Asset Depreciation Entry Automatically": "تسجيل قيد إهلاك الأصل تلقائيًا",
		"Book Deferred Entries Via Journal Entry": "تسجيل القيود المؤجلة عبر قيد اليومية",
		"Book Deferred Entries Based On": "تسجيل القيود المؤجلة بناءً على",
		"POS Closing Entry": "قيد إقفال نقطة البيع",
		"POS Closing Entry Detail": "تفاصيل قيد إقفال نقطة البيع",
		"POS Closing Entry Taxes": "ضرائب قيد إقفال نقطة البيع",
		"POS Opening Entry": "قيد افتتاح نقطة البيع",
		"POS Opening Entry Detail": "تفاصيل قيد افتتاح نقطة البيع",
		"POS Opening Entry Exists": "قيد افتتاح نقطة البيع موجود بالفعل",
		"Multiple POS Opening Entry": "قيود افتتاح متعددة لنقطة البيع",
		"Outdated POS Opening Entry": "قيد افتتاح نقطة البيع منتهي الصلاحية",
		"Sample Retention Stock Entry": "قيد مخزون الاحتفاظ بالعينات",
		"Accounting Entry for Asset": "القيد المحاسبي للأصل",
		"Reconcile Entries": "تسوية القيود",
		"Get Unreconciled Entries": "جلب القيود غير المسوّاة",
		"Get Payment Entries": "جلب قيود الدفع",
		"Allocated Entries": "القيود المخصصة",
		"Failed Entries": "القيود الفاشلة",
		"Restart Failed Entries": "إعادة تشغيل القيود الفاشلة",
		"Show Cancelled Entries": "إظهار القيود الملغاة",
		"Show Return Entries": "إظهار قيود المرتجعات",
		"'Entries' cannot be empty": "لا يمكن أن تكون القيود فارغة",
		"Roles Allowed to Set and Edit Frozen Account Entries":
			"الأدوار المسموح لها بتعيين وتعديل قيود الحسابات المجمدة",
		"Please select Periodic Accounting Entry Difference Account":
			"يرجى تحديد حساب فرق القيد المحاسبي الدوري",
		"Automatically Process Deferred Accounting Entry": "معالجة القيد المحاسبي المؤجل تلقائيًا",
		"Incorrect number of General Ledger Entries found. You might have selected a wrong Account in the transaction.":
			"تم العثور على عدد غير صحيح من قيود دفتر الأستاذ العام. ربما حددت حسابًا خاطئًا في المعاملة.",

		# Misplaced parentheses / wrong string entirely
		"Age (Days)": "العمر (أيام)",
		"All Lead (Open)": "جميع العملاء المحتملين (مفتوح)",
		"Source of Funds (Liabilities)": "مصدر الأموال (الخصوم)",
		# msgstr carried the translation of "To Date cannot be before From Date"
		"Rates cannot be modified for quoted items": "لا يمكن تعديل الأسعار للأصناف المسعّرة",
		"From Date cannot be greater than To Date": 'لا يمكن أن يكون "من تاريخ" أكبر من "إلى تاريخ"',
		"From date cannot be greater than To date": 'لا يمكن أن يكون "من تاريخ" أكبر من "إلى تاريخ"',
		"To Date cannot be before From Date": 'لا يمكن أن يكون "إلى تاريخ" قبل "من تاريخ"',
		"From Currency and To Currency cannot be same": 'لا يمكن أن تكون "من عملة" و"إلى عملة" متطابقتين',
		"From Range has to be less than To Range": 'يجب أن يكون "من النطاق" أقل من "إلى النطاق"',
		"From value must be less than to value in row {0}": 'يجب أن تكون "من قيمة" أقل من "إلى قيمة" في الصف {0}',
		"From Date should be within the Fiscal Year. Assuming From Date = {0}":
			'يجب أن يكون "من تاريخ" ضمن السنة المالية. بافتراض "من تاريخ" = {0}',

		# Placeholder bugs the English tail used to mask: the msgstr dropped or
		# duplicated an index, which msgfmt rejects once the tail is stripped.
		"Accounting Entry for {0}: {1} can only be made in currency: {2}":
			"القيد المحاسبي لـ {0}: {1} لا يمكن إجراؤه إلا بالعملة: {2}",
		"Please set default Cash or Bank account in Mode of Payment {0}":
			"يرجى تعيين حساب النقد أو البنك الافتراضي في طريقة الدفع {0}",
		"Purchase Order number required for Item {0}": "رقم أمر الشراء مطلوب للصنف {0}",
		"Row #{0}: Journal Entry {1} does not have account {2} or already matched against another voucher":
			"الصف رقم {0}: قيد اليومية {1} لا يحتوي على الحساب {2} أو تمت مطابقته بالفعل مع سند آخر",

		"Against Stock Entry": "مقابل قيد المخزون",
		"Make Stock Entry": "إنشاء قيد مخزون",
		"Not allowed to update stock transactions older than {0}":
			"غير مسموح بتحديث الحركات المخزنية الأقدم من {0}",
		"You can not enter current voucher in 'Against Journal Entry' column":
			"لا يمكنك إدخال السند الحالي في عمود \"قيد اليومية المقابل\".",

		# Homograph / literalism
		"Amount": "مبلغ",
		"Order Amount": "مبلغ الطلب",
		"Quotation Amount": "مبلغ عرض السعر",
		"Selling Amount": "مبلغ البيع",
		"Return": "مرتجع",
		"Bin": "رصيد المخزون",
		"BIN Qty": "كمية رصيد المخزون",
		"Bin Qty Recalculated": "تمت إعادة حساب كمية رصيد المخزون",
		"Recalculate Bin Qty": "إعادة حساب كمية رصيد المخزون",
		"Get Balance": "عرض الرصيد",
		"Balance Serial No": "الرقم التسلسلي للرصيد",
		"Batch": "دفعة",
		"Batch Description": "وصف الدفعة",
		"Issue": "بلاغ",
		"Opportunity": "فرصة بيع",
		"Bill of Materials": "قائمة المواد",
		"Purchase Receipt": "إشعار استلام المشتريات",
		"Serial No": "الرقم التسلسلي",
		"Journal Entry": "قيد اليومية",
		"Payment Entry": "قيد الدفع",
		"Payroll Entry": "قيد الرواتب",
		"Voucher": "سند",
		"Rate": "السعر",
		"Expense Claim": "مطالبة المصاريف",
		"Timesheet": "سجل الدوام",
		"Item": "صنف",
		"Stock": "المخزون",
		"Lead": "عميل محتمل",
		"Quotation": "عرض سعر",
		"Create Quotation": "إنشاء عرض سعر",
		"Create Supplier Quotation": "إنشاء عرض سعر مورد",
		"Open Quotations": "عروض الأسعار المفتوحة",
		"Delivery Note Item": "صنف إشعار التسليم",
		"Supplier Delivery Note": "إشعار تسليم المورد",
		"Is Return (Credit Note)": "مرتجع (إشعار دائن)؟",
		"Is Return (Debit Note)": "مرتجع (إشعار مدين)؟",
		"Consolidated Credit Note": "إشعار دائن موحد",
		"Credit Note {0} has been created automatically": "تم إنشاء الإشعار الدائن {0} تلقائيًا",
	},
	"hrms": {
		"Draft": "مسودة",
		"Leave": "إجازة",
		"Return": "مرتجع",
		"Amount": "مبلغ",
		"Rate": "السعر",
		"Payment Entry": "قيد الدفع",
		"Payroll Entry": "قيد الرواتب",
		"Expense Claim": "مطالبة المصاريف",
		"Timesheet": "سجل الدوام",
		"Late Entry": "الدخول المتأخر",
		"Late Entries": "حالات الدخول المتأخر",
		"Total Late Entries": "إجمالي حالات الدخول المتأخر",
		"Leave Ledger Entry": "قيد دفتر أستاذ الإجازات",
		"Invalid Leave Ledger Entry": "قيد دفتر أستاذ الإجازات غير صالح",
		"Auto Leave Encashment": "استبدال الإجازة نقدًا تلقائيًا",
		"Shift": "وردية",
		"From Date cannot be greater than To Date": 'لا يمكن أن يكون "من تاريخ" أكبر من "إلى تاريخ"',
		"To Date cannot be before From Date": 'لا يمكن أن يكون "إلى تاريخ" قبل "من تاريخ"',
		"Leave Type {0} cannot be carry-forwarded": "لا يمكن ترحيل نوع الإجازة {0}",
		"This will submit Salary Slips and create accrual Journal Entry. Do you want to proceed?":
			"سيؤدي هذا إلى ترحيل قسائم الرواتب وإنشاء قيد اليومية للاستحقاق. هل تريد المتابعة؟",
	},
}

# --------------------------------------------------------------------------
# 3. Orthography — applied everywhere, no guard needed.
#
# Hamzat wasl: form VIII/X verbal nouns take a bare alif, not إ.  Only words
# that are unambiguously wrong are listed; form IV nouns that legitimately
# carry hamza (إضافة، إنشاء، إلغاء، إرسال، إجازة …) are deliberately absent.
# --------------------------------------------------------------------------
ORTHOGRAPHY = {
	"إستلام": "استلام", "إستخدام": "استخدام", "إستيراد": "استيراد",
	"إسترجاع": "استرجاع", "إستعلام": "استعلام", "إستعراض": "استعراض",
	"إسترداد": "استرداد", "إستبدال": "استبدال", "إستحقاق": "استحقاق",
	"إستهلاك": "استهلاك", "إستقبال": "استقبال", "إستئناف": "استئناف",
	"إستمارة": "استمارة", "إستطلاع": "استطلاع", "إستفسار": "استفسار",
	"إستنساخ": "استنساخ", "إستمرار": "استمرار", "إستئجار": "استئجار",
	"إختيار": "اختيار", "إختبار": "اختبار", "إجتماع": "اجتماع",
	"إحتساب": "احتساب", "إنتهاء": "انتهاء", "إنتظار": "انتظار",
	"إفتراضي": "افتراضي", "إحتياطي": "احتياطي", "إتصال": "اتصال",
	"إعتماد": "اعتماد", "إرتباط": "ارتباط", "إنخفاض": "انخفاض",
	"إرتفاع": "ارتفاع", "إشتراك": "اشتراك", "إنضمام": "انضمام",
	"إحتمال": "احتمال", "إسم": "اسم", "إبن": "ابن", "إثنين": "اثنين",
	# ta marbuta written as ha
	"ملاحظه": "ملاحظة", "مذكره": "مذكرة", "قسيمه": "قسيمة",
	"فاتوره": "فاتورة", "الشركه": "الشركة", "المده": "المدة",
	"السلعه": "السلعة", "الكميه": "الكمية", "القيمه": "القيمة",
	"موجوده": "موجودة",
	# "الي" as the preposition إلى (distinct from the relative pronoun الذي)
	"(الي تاريخ)": "(إلى تاريخ)", "(الي التاريخ)": "(إلى التاريخ)",
	"(الي القيمة)": "(إلى القيمة)",
}
