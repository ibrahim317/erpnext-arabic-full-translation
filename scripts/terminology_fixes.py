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

	# -- Driver is the person, not a device driver ---------------------------
	(r"\bDriver\b",          r"برنامج التشغيل",        "السائق"),

	# -- "-wise" phrasings unified on حسب ------------------------------------
	(r"wise",                 r"وفقاً للصنف",           "حسب الصنف"),
	(r"wise",                 r"من ناحية الزبائن",      "حسب العميل"),
	(r"wise",                 r"المعني بالزبائن",       "حسب العميل"),

	# -- Dashboard unified on لوحة المعلومات ---------------------------------
	(r"\bDashboard\b",       r"لوحة القيادة",          "لوحة المعلومات"),

	# -- Timesheet is سجل الدوام, not "a sheet of time" ----------------------
	(r"\bTimesheet",          r"ورقة الوقت",            "سجل الدوام"),
	(r"\bTimesheet",          r"جداول زمنية",           "سجلات الدوام"),
	(r"\bTimesheet",          r"الجدول الزمني",         "سجل الدوام"),

	# -- Sales Order is أمر البيع (matches the rest of the register) ---------
	(r"\bSales Order\b",     r"طلب مبيعات",            "أمر بيع"),

	# -- Sales Person is مندوب المبيعات, not "a sales human" -----------------
	(r"\bSales\s*Person\b",  r"شخص المبيعات",          "مندوب المبيعات"),
	(r"\bSales\s*Person\b",  r"رجل المبيعات",          "مندوب المبيعات"),

	# -- Leaves (HR) is إجازات, never أوراق (foliage / sheets of paper) -----
	(r"\bLeaves\b",          r"الأوراق",               "الإجازات"),
	(r"\bLeaves\b",          r"أوراق",                 "إجازات"),

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
		# "Field" was rendered الميدان — the battlefield/arena sense — across the
		# DocType and LDAP settings screens. The UI sense is الحقل.
		# the English tail carried the {0}; stripping it exposed the omission
		"Fieldname is limited to 64 characters ({0})": "اسم الحقل محدود بـ 64 حرفًا ({0})",
		"Jump to field": "الانتقال إلى الحقل",
		"5 Records": "5 سجلات",
		# Action is إجراء; حدث is an *event* and العمل is *work*
		"Action": "إجراء",
		"Action / Route": "الإجراء / المسار",
		"Action Failed": "فشل الإجراء",
		"Action Type": "نوع الإجراء",
		"DocType Action": "إجراء نوع المستند",
		"Server Action": "إجراء الخادم",
		"Success Action": "إجراء النجاح",
		"Trigger Primary Action": "تشغيل الإجراء الأساسي",
		"Next Action Email Template": "قالب البريد الإلكتروني للإجراء التالي",
		"Workflow Action Master": "سجل إجراء سير العمل الرئيسي",
		"Workflow Action Name": "اسم إجراء سير العمل",
		"Call To Action URL": "رابط الدعوة إلى الإجراء",
		# missing space between Arabic and a Latin token
		"API Endpoint": "نقطة نهاية API",
		"API Endpoint Args": "وسائط نقطة نهاية API",
		"API Secret": "المفتاح السري لـ API",
		"Access Key Secret": "المفتاح السري للوصول",
		"Custom CSS": "CSS مخصص",
		"Custom HTML": "HTML مخصص",
		"Custom HTML Help": "مساعدة HTML المخصص",
		"OAuth Provider Settings": "إعدادات موفر OAuth",
		"To and CC": "إلى ونسخة",
		# miscellaneous
		"Alert": "تنبيه",
		"Accounts User": "مستخدم الحسابات",       # role name; was reversed genitive
		"Allowed In Mentions": "مسموح به في الإشارات",   # @-mentions, not memos
		"Both DocType and Name required": "نوع المستند والاسم كلاهما مطلوبان",
		"Doctype": "نوع المستند",
		"Idx": "الترتيب",
		"&lt;head&gt; HTML": "HTML في &lt;head&gt;",
		# these are case-sensitive technical values - uppercasing them broke them
		"MyISAM": "MyISAM",
		"StartTLS": "StartTLS",
		# "Allow X" labels take the masdar, not a conjugated verb
		"Allow Google Drive Access": "السماح بالوصول إلى Google Drive",
		"Allow user to login only after this hour (0-24)":
			"السماح للمستخدم بتسجيل الدخول بعد هذه الساعة فقط (0-24)",
		"Allow user to login only before this hour (0-24)":
			"السماح للمستخدم بتسجيل الدخول قبل هذه الساعة فقط (0-24)",
		"Bypass Two Factor Auth for users who login from restricted IP Address":
			"تجاوز المصادقة الثنائية للمستخدمين الذين يسجلون الدخول من عنوان IP مقيد",
		"Bypass Restricted IP Address Check If Two Factor Auth Enabled":
			"تجاوز فحص تقييد عنوان IP إذا تم تفعيل المصادقة الثنائية",
		"About Us": "من نحن",
		"ALL": "الكل",
		"All Day": "طوال اليوم",
		"Add Child": "إضافة سجل فرعي",          # a child row, not a human child
		"Account Balance": "رصيد الحساب",
		"Aggregate Function Based On": "دالة التجميع بناءً على",
		"A featured post must have a cover image": "يجب أن يحتوي المنشور المميز على صورة غلاف",
		"A list of resources which the Client App will have access to after the user allows it.<br> e.g. project":
			"قائمة الموارد التي سيتمكن التطبيق العميل من الوصول إليها بعد سماح المستخدم بذلك.<br> مثال: مشروع",
		"Round Robin": "التوزيع بالتناوب",        # assignment rule, not "Robin's round"
		"New Kanban Board": "لوح كانبان جديد",     # Board was read as مجلس (council)
		"This Kanban Board will be private": "سيكون لوح كانبان هذا خاصًا",
		"Was this article helpful?": "هل كان هذا المقال مفيدًا؟",                  # tamyiz: 3-10 takes an indefinite plural
		"Assignment Update on {0}": "تحديث التكليف بتاريخ {0}",   # work task, not homework
		"Bounced": "مرتجع",                      # of a cheque/email, not 'leapt'
		"Soft-Bounced": "ارتداد مؤقت",
		"Reports & Masters": "التقارير والبيانات الرئيسية",   # master data, not a degree
		"Block Module": "حظر الوحدة",            # the verb, not the noun كتلة
		"Block Modules": "حظر الوحدات",
		"Is Child Table": "جدول فرعي",
		"Is Primary": "أساسي",                   # was 'الابتدائية' (elementary school)
		"Is Optional State": "حالة اختيارية",     # State was read as الدولة (country)
		"1 Currency = [?] Fraction\nFor e.g. 1 USD = 100 Cent":
			"1 عملة = [؟] وحدة فرعية\nعلى سبيل المثال 1 دولار أمريكي = 100 سنت",
		"Interests": "الاهتمامات",               # hedged both senses: 'الإهتمامات او الفوائد'
		"Based on Field": "بناءً على الحقل",
		"Image Field": "حقل الصورة",
		"Is Published Field": "حقل حالة النشر",
		"LDAP Email Field": "حقل البريد الإلكتروني في LDAP",
		"LDAP First Name Field": "حقل الاسم الأول في LDAP",
		"LDAP Username Field": "حقل اسم المستخدم في LDAP",
		"Remove Field": "إزالة الحقل",
		"Timeline Field": "حقل الجدول الزمني",
		"X Field": "حقل X",
		"Y Field": "حقل Y",
		"Options 'Dynamic Link' type of field must point to another Link Field with options as 'DocType'":
			"خيارات الحقل من نوع \"ارتباط ديناميكي\" يجب أن تشير إلى حقل ارتباط آخر خياراته \"DocType\"",
		# "User" was rendered المستعمل here but المستخدم in ~70 other entries
		"User": "المستخدم",
		"User ": "المستخدم ",
		# msgstr began with the full stop - an RTL artifact that renders wrong
		"Administrator accessed {0} on {1} via IP Address {2}.":
			"المسؤول ولج {0} بتاريخ {1} عبر العنوان {2}.",
		"Use a few words, avoid common phrases.": "استخدم كلمات قليلة، وتجنب العبارات الشائعة.",
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

		# cross-app disagreements, resolved toward the correct sense
		"No.": "الرقم",                        # was 'لا.' - the negation, not the number
		"N/A": "غير متوفر",                     # was left untranslated as 'N / A'
		"Employee Exit": "إنهاء خدمة الموظف",    # was just 'موظف'
		"Field Mapping": "ربط الحقول",           # was 'رسم الخرائط الميدانية' (field cartography)

		# -wise means "broken down by", not حكيم ("wise")
		"Batch-Wise Balance History": "سجل الرصيد حسب الدفعة",
		"Customer-wise Item Price": "سعر الصنف حسب العميل",
		"Project wise Stock Tracking": "تتبع المخزون حسب المشروع",
		"Show Warehouse-wise Stock": "عرض المخزون حسب المستودع",
		"Supplier-Wise Sales Analytics": "تحليلات المبيعات حسب المورد",
		"Territory-wise Sales": "المبيعات حسب الإقليم",
		"Warehouse wise Item Balance Age and Value": "عمر وقيمة رصيد الصنف حسب المستودع",
		"Set targets Item Group-wise for this Sales Person.":
			"تحديد الأهداف حسب مجموعة الأصناف لمندوب المبيعات هذا.",
		"Set Item Group-wise budgets on this Territory. You can also include seasonality by setting the Distribution.":
			"تعيين الميزانيات حسب مجموعة الأصناف على هذا الإقليم. يمكنك أيضًا تضمين الموسمية عن طريق تعيين التوزيع.",

		# Blanket Order is a standing/open order, not a بطانية (blanket)
		"Blanket Order": "أمر شامل",
		"Blanket Order Item": "صنف الأمر الشامل",
		"Blanket Order Rate": "سعر الأمر الشامل",
		"Blanket Order Allowance (%)": "نسبة السماح للأمر الشامل (٪)",
		"Against Blanket Order": "مقابل الأمر الشامل",
		"Invalid Blanket Order for the selected Customer and Item":
			"أمر شامل غير صالح للعميل والصنف المحدد",
		"Item {0} cannot be ordered more than {1} against Blanket Order {2}.":
			"لا يمكن طلب الصنف {0} بأكثر من {1} مقابل الأمر الشامل {2}.",
		"Percentage you are allowed to order beyond the Blanket Order quantity.":
			"النسبة المئوية المسموح لك بطلبها بما يتجاوز كمية الأمر الشامل.",
		"Percentage you are allowed to sell beyond the Blanket Order quantity.":
			"النسبة المئوية المسموح لك ببيعها بما يتجاوز كمية الأمر الشامل.",

		# banking / accounting terms of art
		# Term here is a contract condition (شرط), not a vocabulary term
		"Call Missed": "مكالمة فائتة",            # a phone call, not an invitation
		"Amount In Figure": "المبلغ بالأرقام",
		"Asset Owner Company": "الشركة المالكة للأصل",   # was transliterated 'أسيت أونر'
		"Available Batch Qty at From Warehouse": "كمية الدفعة المتاحة في مستودع المصدر",
		"Available Batch Qty at Warehouse": "كمية الدفعة المتاحة في المستودع",
		"Billed Qty": "الكمية المفوترة",
		"Billing Interval Count": "عدد فترات الفوترة",
		"Billing State": "ولاية الفوترة",
		"Campaign Naming By": "تسمية الحملة بواسطة",
		"Actual Qty is mandatory": "الكمية الفعلية إلزامية",
		"Allow Overtime": "السماح بالعمل الإضافي",
		"Academics User": "مستخدم الأكاديميات",
		"lft": "lft",
		"rgt": "rgt",
		"Cannot Calculate Arrival Time as Driver Address is Missing.":
			"لا يمكن حساب وقت الوصول لأن عنوان السائق مفقود.",
		"Cannot Optimize Route as Driver Address is Missing.":
			"لا يمكن تحسين المسار لأن عنوان السائق مفقود.",
		"Cannot ensure delivery by Serial No as Item {0} is added with and without Ensure Delivery by Serial No.":
			"لا يمكن ضمان التسليم بالرقم التسلسلي لأن الصنف {0} مضاف مع خيار ضمان التسليم بالرقم التسلسلي وبدونه.",
		# msgstr said "BOM creation" and dropped the second sentence
		"Opening stock creation has been queued and will be created in the background. Please check the stock entry after some time.":
			"تم وضع إنشاء المخزون الافتتاحي في قائمة الانتظار وسيُنشأ في الخلفية. يرجى التحقق من قيد المخزون بعد قليل.",
		# the final sentence was missing from the translation
		"Applying a Discount Amount? When this Sales Order is partially fulfilled through multiple Delivery Notes and Sales Invoices, the Discount Amount is allocated on a FIFO basis. The earlier transactions receive a larger share of the discount. To spread the discount proportionally across item prices, use Additional Discount Percentage instead.":
			"هل تطبّق مبلغ خصم؟ عندما يُنفَّذ أمر البيع هذا جزئيًا عبر عدة إشعارات تسليم وفواتير مبيعات، "
			"يُوزَّع مبلغ الخصم على أساس الوارد أولًا يُصرف أولًا. تحصل المعاملات الأسبق على حصة أكبر من "
			"الخصم. لتوزيع الخصم بالتناسب على أسعار الأصناف، استخدم \"نسبة الخصم الإضافي\" بدلًا من ذلك.",

		"Accepted Qty": "الكمية المقبولة",       # was 'المطلوبة' (requested)
		"Accepted Quantity": "الكمية المقبولة",
		"Accepted Warehouse": "مستودع القبول",
		"Set Accepted Warehouse": "تعيين مستودع القبول",
		"Account Manager": "مدير الحساب",        # was 'إدارة حساب المستخدم'
		"Account Head": "الحساب الرئيسي",         # Head of account, not a person
		"Accounting Ledger": "دفتر الأستاذ",      # was 'موازنة دفتر الأستاذ'
		"Accounts Payable Summary": "ملخص الحسابات الدائنة",
		"Active Leads": "العملاء المحتملون النشطون",   # Leads, not 'offers'
		"Acquisition Date": "تاريخ الاقتناء",      # was over-specific 'تاريخ شراء المركبة'
		"AMC Expiry Date": "تاريخ انتهاء عقد الصيانة السنوي",
		"Academics User": "المستخدم الأكاديمي",
		"Ageing Based On": "التقادم بناءً على",
		"Against Doctype": "مقابل نوع المستند",
		"Add to Transit": "إضافة إلى العبور",
		"Add Item": "إضافة صنف",
		"Add Items": "إضافة أصناف",
		"Add items in the Item Locations table": "أضف أصنافًا في جدول مواقع الأصناف",
		"Action Initialised": "تم بدء الإجراء",
		"Control Action": "إجراء التحكم",
		"Quality Action": "إجراء الجودة",
		"Quality Action Resolution": "حل إجراء الجودة",
		# Advance here is the noun (a cash advance), not the adverb "in advance"
		"Advance Amount": "مبلغ السلفة",
		"Advance amount": "مبلغ السلفة",
		"Advance Paid": "المبلغ المدفوع مقدمًا",
		"Number of days appointments can be booked in advance":
			"عدد الأيام التي يمكن حجز المواعيد خلالها مسبقًا",
		"A Lead requires either a person's name or an organization's name":
			"يتطلب العميل المحتمل اسم شخص أو اسم مؤسسة",
		"Customer/Lead Name": "اسم العميل / العميل المحتمل",
		"Quot/Lead %": "نسبة عرض السعر / العميل المحتمل %",
		"A Packing Slip can only be created for Draft Delivery Note.":
			"لا يمكن إنشاء قسيمة تعبئة إلا لمسودة إشعار التسليم.",

		"Payment Term": "شرط الدفع",
		"Payment Term Name": "اسم شرط الدفع",
		"Payment Terms Template Detail": "تفاصيل قالب شروط الدفع",
		"Round Off Account": "حساب التقريب",       # was 'جولة قبالة حساب'
		"Time Sheet": "سجل الدوام",
		"Time Sheet List": "قائمة سجلات الدوام",
		"Hold Invoice": "تعليق الفاتورة",          # was 'عقد الفاتورة' (contract)
		"Trial Period Start Date": "تاريخ بدء الفترة التجريبية",
		"Frequently Read Articles": "المقالات الأكثر قراءة",
		"See All Articles": "عرض جميع المقالات",
		"Closed Document": "مستند مغلق",
		"No of Shares": "عدد الأسهم",              # alef/lam were transposed
		"New Sales Person Name": "اسم مندوب المبيعات الجديد",
		"Sales Person Target Variance Based On Item Group":
			"تباين مستهدف مندوب المبيعات بناءً على مجموعة الأصناف",
		"Please enter Employee Id of this sales person":
			"يرجى إدخال معرّف الموظف الخاص بمندوب المبيعات هذا",

		"Bank Clearance Summary": "ملخص المقاصة البنكية",   # المقاصة, not التخليص (customs)
		"Bank Draft": "حوالة بنكية",                        # an instrument, not a text draft
		"Bank Overdraft Account": "حساب السحب على المكشوف",
		"Bank / Cash Account": "حساب البنك / النقدية",
		"Account Paid From": "مدفوع من حساب",
		"Accounting Masters": "البيانات المحاسبية الرئيسية",  # master data, not a degree
		"% Complete Method": "طريقة نسبة الإنجاز",
		"Billed Amt": "المبلغ المفوتر",
		"Total(Amt)": "الإجمالي (المبلغ)",
		"Address Desc": "وصف العنوان",                       # Address as noun, not "to address"
		"Actual Operating Cost": "تكاليف التشغيل الفعلية",    # adjective follows the noun
		"Actual Operation Time": "وقت التشغيل الفعلي",
		"BOM Detail No": "رقم تفاصيل قائمة المواد",
		"Block Supplier": "حظر المورد",
		" Is Child Table": " جدول فرعي",
		"A Customer Group exists with same name please change the Customer name or rename the Customer Group":
			"توجد مجموعة عملاء بنفس الاسم، يرجى تغيير اسم العميل أو إعادة تسمية مجموعة العملاء",
		"'Update Stock' can not be checked because items are not delivered via {0}":
			"لا يمكن تحديد خيار \"تحديث المخزون\" لأن الأصناف لا تُسلَّم عبر {0}",

		# "Finance Book" is a parallel set of books (tax vs accounting), not a
		# book you read; and "Book" as a verb is حجز/تسجيل, never الكتاب.
		"Finance Book": "الدفتر المالي",
		"Finance Book Detail": "تفاصيل الدفتر المالي",
		"Finance Book Id": "معرّف الدفتر المالي",
		"Default Finance Book": "الدفتر المالي الافتراضي",
		"Asset Finance Book": "الدفتر المالي للأصل",
		"Row #{}: Please use a different Finance Book.": "الصف رقم #{}: يرجى استخدام دفتر مالي مختلف.",
		"Book Appointment": "حجز موعد",          # was 'موعد الكتاب' (the book's appointment)

		# word-salad rewrites
		"Row {0}: Bill of Materials not found for the Item {1}":
			"الصف {0}: لم يتم العثور على قائمة المواد للصنف {1}",
		"Total Applicable Charges in Purchase Receipt Items table must be same as Total Taxes and Charges":
			"يجب أن يساوي إجمالي الرسوم المطبقة في جدول أصناف إشعار استلام المشتريات إجمالي الضرائب والرسوم",
		"POS Field": "حقل نقطة البيع",
		"This is a root account and cannot be edited.": "هذا حساب جذري ولا يمكن تعديله.",
		"You are not authorized to set Frozen value": "أنت غير مخول لتعيين القيمة المجمدة",
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
		" Unlink Payment on Cancellation of Employee Advance":
			" إلغاء ربط الدفعة عند إلغاء سلفة الموظف",   # Advance = سلفة, not تقدم
		"Actual Encashable Days": "الأيام الفعلية القابلة للصرف",
		"Appraisee": "المُقَيَّم",                    # the person appraised, not the appraisal
		"Appraisees: {0}": "المُقَيَّمون: {0}",
		"Set optional filters to fetch employees in the appraisee list":
			"تعيين عوامل تصفية اختيارية لجلب الموظفين في قائمة المُقَيَّمين",
		"Attach Proof": "إرفاق إثبات",               # masdar, not the verb 'we hang'
		"Attendance marked successfully": "تم تسجيل الحضور بنجاح",
		"Carry Forwarded Leaves": "الإجازات المرحّلة",
		"Expire Carry Forwarded Leaves (Days)": "انتهاء صلاحية الإجازات المرحّلة (بالأيام)",
		"Maximum Carry Forwarded Leaves": "الحد الأقصى للإجازات المرحّلة",
		"Total Leaves Encashed": "إجمالي الإجازات المستبدلة نقدًا",
		"Allocate leaves to {0} employee(s)?": "تخصيص إجازات لـ {0} موظف؟",
		"Apply / Approve Leaves": "طلب / اعتماد الإجازات",
		"Block Holidays on important days.": "حظر الإجازات في الأيام المهمة.",
		"Added tax components from the Salary Component master as the salary structure didn't have any tax component.":
			"تمت إضافة المكونات الضريبية من سجل مكوّن الراتب الرئيسي لأن هيكل الرواتب لم يكن يحتوي على أي مكوّن ضريبي.",
		"User": "المستخدم",
		"Action": "إجراء",
		"Action on Submission": "الإجراء عند الترحيل",
		"Add Day-wise Dates": "إضافة تواريخ حسب اليوم",   # day-wise, not "daytime"
		"Allow Over Allocation": "السماح بالتخصيص الزائد",
		"Allow User": "السماح للمستخدم",
		"AttendanceRequestListView": "قائمة عرض طلبات الحضور",
		"Avg Utilization": "متوسط الاستخدام",
		"Avg Utilization (Billed Only)": "متوسط الاستخدام (المفوتر فقط)",
		"Avg Feedback Score": "متوسط درجة التقييم",
		"The day(s) on which you are applying for leave are holidays. You need not apply for leave.":
			"الأيام التي تطلب فيها إجازة هي أيام عطلة. لا حاجة لتقديم طلب إجازة.",
		"Advance": "سلفة",
		"Advance Amount": "مبلغ السلفة",
		"Advance Paid": "المبلغ المدفوع مقدمًا",
		"Total Advance Amount": "إجمالي مبلغ السلفة",
		"Expense Claim Advance": "سلفة مطالبة المصاريف",
		"Actual Amount": "المبلغ الفعلي",        # Amount = مبلغ, not كمية
		"Employee Hours Utilization Based On Timesheet":
			"استخدام ساعات الموظف بناءً على سجل الدوام",
		"A Job Requisition for {0} requested by {1} already exists: {2}":
			"يوجد بالفعل طلب توظيف لـ {0} مقدَّم من {1}: {2}",
		"Service Item": "صنف الخدمة",       # Item = صنف; was 'بند الخدمة'
		"Added On": "تاريخ الإضافة",         # was 'تمت إضافة على' (broken grammar)
		"Apply": "تقديم طلب",                # job-application button; was 'يتقدم'
		"Utilization": "الاستخدام",          # was 'الاستغلال' (exploitation)
		"Assigning...": "جارٍ التعيين...",
		"Uploading...": "جارٍ الرفع...",
		"Archive": "أرشفة",
		"Confirm": "تأكيد",
		'<span class="h4"><b>Your Shortcuts</b></span>':
			'<span class="h4"><b>اختصاراتك</b></span>',
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
	# U+FEF9, an Arabic presentation-form ligature, sits inside words like اﻹجازة.
	# It is a rendering artifact, not a letter: it breaks search and comparison.
	"ﻹ": "لإ",
	# "الي" as the preposition إلى (distinct from the relative pronoun الذي)
	"(الي تاريخ)": "(إلى تاريخ)", "(الي التاريخ)": "(إلى التاريخ)",
	"(الي القيمة)": "(إلى القيمة)",
}

# --------------------------------------------------------------------------
# 4. Spelling, applied to whole Arabic words only.
#
# Almost every entry is backed by corpus evidence rather than judgement: the
# corrected form already outnumbers the defective one by at least 3:1 in these
# same catalogs, so these are typos against the catalogs' own established
# spelling. Both directions are tested — hamza missing from a form IV word
# (انشاء -> إنشاء) and hamza wrongly added to a form VIII/X word
# (الأفتراضي -> الافتراضي) — and chains are resolved, so الألكتروني lands on
# الإلكتروني rather than stopping at the equally-wrong الالكتروني.
#
# `بعدة` ("with several") and `دفعه` ("paying it") are excluded explicitly:
# both are correct words that the ta-marbuta test would otherwise flag.
# --------------------------------------------------------------------------
SPELLING = {
	# -- hamza restored on bare alif — the hamzated spelling dominates the corpus (89 forms) --
	"الالكتروني": "الإلكتروني",
	"اخرى": "أخرى",
	"الاجازة": "الإجازة",
	"الغاء": "إلغاء",
	"انشاء": "إنشاء",
	"اجازة": "إجازة",
	"ارسال": "إرسال",
	"اعادة": "إعادة",
	"ادخل": "أدخل",
	"اشعار": "إشعار",
	"اصناف": "أصناف",
	"الاجازات": "الإجازات",
	"الاهلاك": "الإهلاك",
	"اعدادات": "إعدادات",
	"الاصناف": "الأصناف",
	"ارقام": "أرقام",
	"اضافية": "إضافية",
	"اظهار": "إظهار",
	"الاجمالي": "الإجمالي",
	"الاساسي": "الأساسي",
	"الاسبوع": "الأسبوع",
	"الكتروني": "إلكتروني",
	"ايام": "أيام",
	"لانه": "لأنه",
	"اجازات": "إجازات",
	"اجمالي": "إجمالي",
	"ارجاع": "إرجاع",
	"اساس": "أساس",
	"اضافة": "إضافة",
	"الاغلاق": "الإغلاق",
	"الايام": "الأيام",
	"انشاؤه": "إنشاؤه",
	"ايرادات": "إيرادات",
	"للانتاج": "للإنتاج",
	"اجراء": "إجراء",
	"اخفاء": "إخفاء",
	"ادارة": "إدارة",
	"ادخال": "إدخال",
	"ادراج": "إدراج",
	"اذونات": "أذونات",
	"ازالة": "إزالة",
	"اساسي": "أساسي",
	"اسبوعين": "أسبوعين",
	"اسعار": "أسعار",
	"اصدار": "إصدار",
	"اصول": "أصول",
	"اعداد": "إعداد",
	"اعلى": "أعلى",
	"اعمدة": "أعمدة",
	"اغلاق": "إغلاق",
	"افضل": "أفضل",
	"اقصى": "أقصى",
	"اقفال": "إقفال",
	"اكبر": "أكبر",
	"الاجراء": "الإجراء",
	"الاخطاء": "الأخطاء",
	"الادارة": "الإدارة",
	"الادخال": "الإدخال",
	"الادنى": "الأدنى",
	"الارقام": "الأرقام",
	"الاستاذ": "الأستاذ",
	"الاسعار": "الأسعار",
	"الاشعار": "الإشعار",
	"الاصل": "الأصل",
	"الاصلي": "الأصلي",
	"الاصول": "الأصول",
	"الاضافي": "الإضافي",
	"الاعلى": "الأعلى",
	"الاقسام": "الأقسام",
	"الاقصى": "الأقصى",
	"الالزامية": "الإلزامية",
	"الالغاء": "الإلغاء",
	"الانتاج": "الإنتاج",
	"الانترنت": "الإنترنت",
	"الاوراق": "الأوراق",
	"الايرادات": "الإيرادات",
	"الايصال": "الإيصال",
	"الزامي": "إلزامي",
	"انتاج": "إنتاج",
	"انشئ": "أنشئ",
	"انها": "أنها",
	"اهداف": "أهداف",
	"اولا": "أولا",
	"اولاً": "أولاً",
	"ايصال": "إيصال",
	"بالايام": "بالأيام",
	"بامر": "بأمر",
	"لانشاء": "لإنشاء",
	"لانها": "لأنها",
	# -- hamzat wasl: hamza wrongly added to a form VIII/X word (17 forms) --
	"أكتمل": "اكتمل",
	"الإستجابة": "الاستجابة",
	"أتصال": "اتصال",
	"أجازة": "إجازة",
	"أختر": "اختر",
	"أستلام": "استلام",
	"أفتح": "افتح",
	"إنتهى": "انتهى",
	"الأتصال": "الاتصال",
	"الأجازات": "الإجازات",
	"الأجمالي": "الإجمالي",
	"الأحتياطية": "الاحتياطية",
	"الأستخدام": "الاستخدام",
	"الأفتراضي": "الافتراضي",
	"الألكتروني": "الإلكتروني",
	"الإصناف": "الأصناف",
	"للأسم": "للاسم",
	# -- ta marbuta / ha confusion (21 forms) --
	"السنه": "السنة",
	"قيمه": "قيمة",
	"مجموعه": "مجموعة",
	"الاجازه": "الإجازة",
	"الافتراضيه": "الافتراضية",
	"التاريخيه": "التاريخية",
	"المتداخله": "المتداخلة",
	"المجموعه": "المجموعة",
	"المرسله": "المرسلة",
	"بدايه": "بداية",
	"بواسطه": "بواسطة",
	"خريطه": "خريطة",
	"طريقه": "طريقة",
	"فارغه": "فارغة",
	"قاعده": "قاعدة",
	"كلمه": "كلمة",
	"لدية": "لديه",
	"مطالبه": "مطالبة",
	"مطلوبه": "مطلوبة",
	"مكرره": "مكررة",
	"نقطه": "نقطة",
	# -- doubled letters, missing spaces, prepositions, participle, typos (22 forms) --
	"جاري": "جارٍ",
	"الى": "إلى",
	"او": "أو",
	"علي": "على",
	"الايميل": "الإيميل",
	"الأيصال": "الإيصال",
	"الفلتره": "الفلترة",
	"ان": "أن", "الا": "إلا", "اي": "أي", "امر": "أمر", "اصل": "أصل",
	"ارباح": "أرباح", "اخر": "آخر", "األسهم": "الأسهم", "العمرعلى": "العمر على",
	"لايمكن": "لا يمكن",
	"أسم": "اسم",
	"الي": "إلى",
	"اذا": "إذا",
	"لان": "لأن",
	"االاستهالك": "الاستهلاك",
	"االمستخدم": "المستخدم",
	"اختيارالحساب": "اختيار الحساب",
	"الإهتمامات": "الاهتمامات",
	"الااسم": "الاسم",
	"التقريرالقياسي": "التقرير القياسي",
	"الذى": "الذي",
	"العثورعلى": "العثور على",
	"تحوبله": "تحويله",
	"سعرالمواد": "سعر المواد",
	"قواائم": "قوائم",
	"كتيرة": "كثيرة",
}
